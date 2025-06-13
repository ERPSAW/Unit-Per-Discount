frappe.ui.form.on('Customer',  {
    refresh: function(frm) {
        frm.add_custom_button("View Price List", function() {
            frappe.set_route('List', 'Pricing Rule', {
                "customer_group": frm.doc.customer_group,
            });
        }, "View")
    }
})