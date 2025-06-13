frappe.ui.form.on('Sales Order', {
    before_save: function(frm) {
        frm.doc.items.forEach(row => {
            row.custom_set_rate_ = row.rate;
            row.custom_set_amount = row.amount;
        });
        frm.refresh_field("items");
    },
    after_save: function(frm) {
        frappe.call({
            method: "unit_discount.overrides.custom_price_list.rate_amount_update",
            args: {
                items: frm.doc.items
            },
            callback: function(r) {
                if (r.message) {
                    // frappe.msgprint(r.message);
                    frm.reload_doc(); 
                }
            }
           
        });
    }
});

frappe.ui.form.on('Sales Order Item', {
    qty: function(frm, cdt, cdn) {
        let custom_item_group_total_qty = 0;
        let row = locals[cdt][cdn];

        frm.doc.items.forEach(tablerow => {
            if (tablerow.item_group !== row.item_group) return;
            custom_item_group_total_qty += tablerow.qty;
        });

        frm.doc.items.forEach(tablerow => {
            if (tablerow.item_group !== row.item_group) return;
            tablerow.custom_item_group_total_qty = custom_item_group_total_qty;
            apply_pricing_rule(frm, tablerow, true);
        })
    },
})

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