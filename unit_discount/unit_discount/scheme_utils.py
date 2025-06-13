import frappe

from frappe.desk.reportview import get_filters_cond, get_match_cond

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_active_schemes(doctype, txt, searchfield, start, page_len, filters):

    customer = filters.get("customer")
    customer_group = filters.get("customer_group")
    posting_date = filters.get("posting_date")

    sql = f"""
        SELECT
            s.scheme_name scheme_name
        FROM
            `tabScheme` s
        LEFT JOIN `tabCustomer Item` ci on ci.parent = s.name and ci.parenttype = 'Scheme'
        WHERE 
            '{posting_date}' BETWEEN s.from_date AND s.to_date
            AND (s.customer_group = '{customer_group}' OR ci.customer = '{customer}')
            AND s.scheme_name like '%{txt}%'
        LIMIT {start}, {page_len}
    """
    return frappe.db.sql(sql)