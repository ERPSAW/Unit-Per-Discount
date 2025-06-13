# Copyright (c) 2024, eactive and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []

	columns = [
		{
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"label": "Customer"
		},
		{
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"label": "Item"
		},
		{
			"fieldname": "qty",
			"fieldtype": "Float",
			"label": "Quantity"
		},
		{
			"fieldname": "rate",
			"fieldtype": "Float",
			"label": "Rate"
		},
		{
			"fieldname": "amount",
			"fieldtype": "Float",
			"label": "Amount"
		},
		{
			"fieldname": "based_on",
			"fieldtype": "Data",
			"label": "Based on"
		},
		{
			"fieldname": "discount_type",
			"fieldtype": "Data",
			"label": "Discount Type"
		},
		{
			"fieldname": "qty_scheme",
			"fieldtype": "Float",
			"label": "Qty Scheme"
		},
		{
			"fieldname": "value_scheme",
			"fieldtype": "Float",
			"label": "Value Scheme"
		},
	]

	sql = f"""
		SELECT 
			si.customer,
			sii.item_code, SUM(sii.qty) qty, AVG(sii.rate) rate, SUM(sii.amount) amount,
			s.based_on, s.discount_type,
			(SELECT applicable_rate from `tabScheme Slab` ss WHERE qty BETWEEN ss.from_value and ss.to_value) qty_scheme,
			(SELECT applicable_rate from `tabScheme Slab` ss WHERE amount BETWEEN ss.from_value and ss.to_value) value_scheme
		FROM
			`tabSales Invoice` si
		LEFT JOIN
			`tabSales Invoice Item` sii ON sii.parent = si.name
		LEFT JOIN
			`tabScheme` s on s.name = si.custom_scheme
		LEFT JOIN
			`tabCustomer Item` ci on ci.customer = si.customer and ci.parenttype ='Scheme'
		WHERE 
			si.docstatus = 1
			AND si.posting_date BETWEEN s.from_date AND s.to_date
			AND si.custom_scheme = '{filters.get("scheme")}'
		GROUP BY si.customer
	"""

	data = frappe.db.sql(sql, as_dict=True)



	return columns, data
