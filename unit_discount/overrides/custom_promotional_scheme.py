import frappe
from frappe import _
from frappe.model.document import Document

price_discount_fields = [
	"rate_or_discount",
	"apply_discount_on",
	"apply_discount_on_rate",
	"rate",
	"discount_amount",
	"discount_percentage",
	"validate_applied_rule",
	"apply_multiple_pricing_rules",
	"for_price_list",
	"custom_discount_per_unit_rate",
	"custom_discount_unit",
	"custom_is_slab_discount",
	"custom_discount_slab_text"
]