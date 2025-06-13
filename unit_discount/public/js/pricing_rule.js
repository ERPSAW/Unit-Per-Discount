frappe.ui.form.on('Pricing Rule', {
    validate: function(frm) {
        if (frm.doc.rate_or_discount == 'Discount Per Unit'){
            if(frm.doc.custom_discount_per_unit_rate != 0 && frm.doc.custom_is_slab_discount == 1 && frm.doc.custom_discount_slab.length > 0){
                frappe.throw(__("Discount Per Unit cannot be applied on Discount Per Unit Rate and Slab Discount"));
            }
        }
    }
});
