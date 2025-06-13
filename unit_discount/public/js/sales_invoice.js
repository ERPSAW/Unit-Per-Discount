frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		frm.set_query("custom_scheme", function() {
            return {
                query: "unit_discount.unit_discount.scheme_utils.get_active_schemes",
                filters: {
                    "customer": frm.doc.customer,
                    "customer_group": frm.doc.customer_group,
                    "posting_date": frm.doc.posting_date
                }
            }
        })
	}
})