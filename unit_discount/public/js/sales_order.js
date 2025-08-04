frappe.ui.form.on('Sales Order', {
    before_save: function(frm) {
        frm.doc.items.forEach(row => {
            row.custom_set_rate_ = row.rate;
            row.custom_set_amount = row.amount;
        });
        frm.refresh_field("items");
    },
    // after_save: function(frm) {
    //     frappe.call({
    //         method: "unit_discount.overrides.custom_price_list.rate_amount_update",
    //         args: {
    //             items: frm.doc.items
    //         },
    //         callback: function(r) {
    //             if (r.message) {
    //                 // frappe.msgprint(r.message);
    //                 frm.reload_doc(); 
    //             }
    //         }
           
    //     });
    // }
});

frappe.ui.form.on('Sales Order Item', {
    qty: async function(frm, cdt, cdn) {
        await handle_item_discount_logic(frm, cdt, cdn);
    },

    item_code: function(frm, cdt, cdn) {
        setTimeout(async () => {
            await handle_item_discount_logic(frm, cdt, cdn);
        }, 1000);
    },

    items_remove: function(frm) {
        setTimeout(async () => {
            frappe.dom.freeze("Recalculating Discount Rules...");

            try {
                const item_group_totals = {};
                frm.doc.items.forEach(row => {
                    if (!row.item_group) return;
                    if (!item_group_totals[row.item_group]) {
                        item_group_totals[row.item_group] = 0;
                    }
                    item_group_totals[row.item_group] += row.qty * row.custom_additional_quantity;
                });

                const promises = [];

                frm.doc.items.forEach(row => {
                    if (!row.item_group) return;
                    row.custom_item_group_total_qty = item_group_totals[row.item_group];
                    promises.push(apply_pricing_rule(frm, row, true));
                });

                await Promise.all(promises);
            } finally {
                frappe.dom.unfreeze();
            }
        }, 300);
    }    
});

async function handle_item_discount_logic(frm, cdt, cdn) {
	const table = frappe.ui.form.get_open_grid_form();
	if (table) {
		table.toggle_view(false);
	}
	frappe.dom.freeze("Fetching Discount Rules...");

	try {
		let custom_item_group_total_qty = 0;
		const row = locals[cdt][cdn];

		for (let tablerow of frm.doc.items) {
			if (tablerow.item_group === row.item_group) {
				if (!tablerow.custom_additional_quantity || tablerow.custom_additional_quantity == 0) {
					const res = await frappe.call({
						method: "unit_discount.overrides.custom_price_list.calculate_uom_qty",
						args: {
							item_code: tablerow.item_code,
							uom: "Litre"
						}
					});
					const uom_qty = flt(res.message || 0);
					tablerow.custom_additional_quantity = uom_qty;
					custom_item_group_total_qty += flt(tablerow.qty) * uom_qty;
				} else {
					custom_item_group_total_qty += flt(tablerow.qty) * flt(tablerow.custom_additional_quantity);
				}
			}
		}
		const promises = [];

		for (let tablerow of frm.doc.items) {
			if (tablerow.item_group !== row.item_group) continue;
			tablerow.custom_item_group_total_qty = custom_item_group_total_qty;
			promises.push(apply_pricing_rule(frm, tablerow, true));
		}

		await Promise.all(promises);
		frm.refresh_field("items");
	} finally {
		frappe.dom.unfreeze();
	}
}



function apply_pricing_rule(frm, item, calculate_taxes_and_totals) {
    var args = erpnext.TransactionController.prototype._get_args.call(frm.cscript, item);
    args['custom_item_group_total_qty'] = item.custom_item_group_total_qty;

    if (!(args.items && args.items.length)) {
        if (calculate_taxes_and_totals) erpnext.TransactionController.prototype.calculate_taxes_and_totals.call(frm.cscript);
        return;
    }

    // Target doc created from a mapped doc
    if (frm.doc.__onload?.load_after_mapping) {
        // Calculate totals even though pricing rule is not applied.
        // `apply_pricing_rule` is triggered due to change in data which most likely contributes to Total.
        if (calculate_taxes_and_totals) erpnext.TransactionController.prototype.calculate_taxes_and_totals.call(frm.cscript);
        return;
    }

    return frm.call({
        method: "erpnext.accounts.doctype.pricing_rule.pricing_rule.apply_pricing_rule",
        args: {	args: args, doc: frm.doc },
        callback: function(r) {
            if (!r.exc && r.message) {
                erpnext.TransactionController.prototype._set_values_for_item_list.call(frm.cscript, r.message);
                if(item) erpnext.TransactionController.prototype.set_gross_profit.call(frm.cscript, item);
                if (frm.doc.apply_discount_on) frm.trigger("apply_discount_on")
            }
        }
    });
}
