import copy
import json
import re

import frappe
from frappe import _, throw
from frappe.model.document import Document
from frappe.utils import cint, flt

@frappe.whitelist()
def apply_price_discount_rule(pricing_rule, item_details, args):
	
	item_details.pricing_rule_for = pricing_rule.rate_or_discount

	if (pricing_rule.margin_type in ["Amount", "Percentage", "Per Unit"] and pricing_rule.currency == args.currency) or (
		pricing_rule.margin_type == "Percentage"
	):
		item_details.margin_type = pricing_rule.margin_type
		item_details.has_margin = True

		if pricing_rule.margin_type == "Per Unit":
			item_details.margin_type = 'Amount'
			conversion = get_item_conversion(args.get('item_code'), pricing_rule.custom_margin_unit)
			item_details.margin_rate_or_amount = pricing_rule.custom_margin_rate_per_unit * conversion

		else:
			if pricing_rule.apply_multiple_pricing_rules and item_details.margin_rate_or_amount is not None:
				item_details.margin_rate_or_amount += pricing_rule.margin_rate_or_amount
			else:
				item_details.margin_rate_or_amount = pricing_rule.margin_rate_or_amount

	elif pricing_rule.rate_or_discount == "Rate":
		pricing_rule_rate = 0.0
		if pricing_rule.currency == args.currency:
			pricing_rule_rate = pricing_rule.rate

		# TODO https://github.com/frappe/erpnext/pull/23636 solve this in some other way.
		if pricing_rule_rate:
			is_blank_uom = pricing_rule.get("uom") != args.get("uom")
			# Override already set price list rate (from item price)
			# if pricing_rule_rate > 0
			item_details.update(
				{
					"price_list_rate": pricing_rule_rate
					* (args.get("conversion_factor", 1) if is_blank_uom else 1),
				}
			)
		item_details.update({"discount_percentage": 0.0})

	for apply_on in ["Discount Amount", "Discount Percentage", "Discount Per Unit"]:

		if pricing_rule.rate_or_discount != apply_on:
			continue

		if apply_on == 'Discount Per Unit':
			# field = 'custom_discount_per_unit_rate'
			# value = pricing_rule.get(field, 0)


			conversion = get_item_conversion(args.get('item_code'), pricing_rule.custom_discount_unit)

			discount_rate = get_discount_rate(pricing_rule, item_details, args, conversion)

			if (pricing_rule.apply_on == 'Item Group' and args.custom_item_group_total_qty) or (pricing_rule.apply_on != "Item Group"):
				item_details['custom_discount_per_unit'] = discount_rate
				item_details['custom_discount_unit'] = pricing_rule.custom_discount_unit
				item_details['custom_additional_quantity'] = conversion 
				item_details['custom_unit_discount_amount'] = conversion * discount_rate
				# item_details['discount_amount'] = discount_rate * conversion
				item_details['discount_amount'] = discount_rate * conversion

			# item_details['custom_discount_per_unit'] = pricing_rule.custom_discount_per_unit_rate
			# item_details['custom_discount_unit'] = pricing_rule.custom_discount_unit
			# item_details['custom_additional_quantity'] = conversion * args.qty
			# item_details['custom_unit_discount_amount'] = conversion * args.qty * pricing_rule.custom_discount_per_unit_rate
			# item_details['discount_amount'] = pricing_rule.custom_discount_per_unit_rate * conversion
		
		else:
			field = frappe.scrub(apply_on)
			if pricing_rule.apply_discount_on_rate and item_details.get("discount_percentage"):
				# Apply discount on discounted rate
				item_details[field] += (100 - item_details[field]) * (pricing_rule.get(field, 0) / 100)
			
			elif args.price_list_rate:
				value = pricing_rule.get(field, 0)
				calculate_discount_percentage = False
				if field == "discount_percentage":
					field = "discount_amount"
					value = args.price_list_rate * (value / 100)
					calculate_discount_percentage = True 

				if field not in item_details:
					item_details.setdefault(field, 0)

				item_details[field] += value if pricing_rule else args.get(field, 0)
				if calculate_discount_percentage and args.price_list_rate and item_details.discount_amount:
					item_details.discount_percentage = flt(
						(flt(item_details.discount_amount) / flt(args.price_list_rate)) * 100
					)
			else:
				if field not in item_details:
					item_details.setdefault(field, 0)

				item_details[field] += pricing_rule.get(field, 0) if pricing_rule else args.get(field, 0)


def get_item_conversion(item_code, uom):
	item = frappe.get_doc("Item", item_code)

	for u in item.uoms:
		if u.uom == uom:
			return u.conversion_factor
	
	return 1

def get_discount_rate(pricing_rule, item_details, args, conversion):

	if pricing_rule.custom_is_slab_discount == 1:
		if pricing_rule.apply_on == 'Item Group' and args.custom_item_group_total_qty:
			qty = args.custom_item_group_total_qty
		else:
			qty = conversion * args.qty

		discount = 0
		query = frappe.db.sql("""
			SELECT
				discount_per_unit
			FROM
				`tabPricing Rule Slab`
			WHERE 
				((%s between from_qty and to_qty and to_qty !=0)
				OR (%s >= from_qty and to_qty = 0))
				and parent = %s
			LIMIT 1
		""", (qty, qty, pricing_rule.name), as_dict=True)
		
		if len(query) == 1:
			discount = query[0].get("discount_per_unit")
			return discount
		else: 
			return 0
	else:
		return pricing_rule.custom_discount_per_unit_rate




@frappe.whitelist()
def rate_amount_update():
	items = frappe.form_dict.get('items')
	if not items:
		frappe.response["message"] = "No items received"
		return

	item_detail = json.loads(items)

	if not item_detail:
		frappe.response["message"] = "No valid items found"

	total = 0
	sales_order_name = None
	
	for i in item_detail:
		total += i["custom_set_amount"]
		if not sales_order_name:
			sales_order_name = i.get("parent")
		frappe.db.set_value("Sales Order Item", i["name"], "rate", i["custom_set_rate_"])
		frappe.db.set_value("Sales Order Item", i["name"], "amount", i["custom_set_amount"])

		frappe.db.commit()
	# if sales_order_name:
	# 	frappe.log_error(message=total, title='total')
	# 	frappe.db.set_value("Sales Order", sales_order_name, "total", total)
	# 	frappe.db.set_value("Sales Order", sales_order_name, "grand_total", total)
	# 	frappe.db.set_value("Sales Order", sales_order_name, "rounded_total", total)
	# 	frappe.db.commit()

	frappe.response["message"] = "Saved Sucessfully"


@frappe.whitelist()
def custom_before_submit(doc, method):
    for i in doc.items:
        i.rate = i.custom_set_rate_
        i.amount = i.custom_set_amount


@frappe.whitelist()
def calculate_uom_qty(item_code, uom):
	return frappe.db.get_value("UOM Conversion Detail", { "parent": item_code, "uom": uom }, "conversion_factor")
