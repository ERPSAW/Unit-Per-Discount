app_name = "unit_discount"
app_title = "Unit Discount"
app_publisher = "eactive"
app_description = "Unit Discount"
app_email = "laxman@eactive.in"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/unit_discount/css/unit_discount.css"
# app_include_js = "/assets/unit_discount/js/unit_discount.js"
app_include_js = "/unit_discount/public/js/sales_order.js"

# include js, css files in header of web template
# web_include_css = "/assets/unit_discount/css/unit_discount.css"
# web_include_js = "/assets/unit_discount/js/unit_discount.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "unit_discount/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Customer" : "public/js/customer.js",
               "Sales Invoice": "public/js/sales_invoice.js",
               "Sales Order": "public/js/sales_order.js",
               "Pricing Rule": "public/js/pricing_rule.js",
            }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "unit_discount/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "unit_discount.utils.jinja_methods",
# 	"filters": "unit_discount.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "unit_discount.install.before_install"
# after_install = "unit_discount.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "unit_discount.uninstall.before_uninstall"
# after_uninstall = "unit_discount.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "unit_discount.utils.before_app_install"
# after_app_install = "unit_discount.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "unit_discount.utils.before_app_uninstall"
# after_app_uninstall = "unit_discount.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "unit_discount.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# },
    "Sales Order": {
		# "on_update": "method",
		# "on_cancel": "method",
		# "on_trash": "method",
	"validate": "unit_discount.overrides.custom_price_list.custom_before_submit",
        "before_submit": "unit_discount.overrides.custom_price_list.custom_before_submit",
	}
}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"unit_discount.tasks.all"
# 	],
# 	"daily": [
# 		"unit_discount.tasks.daily"
# 	],
# 	"hourly": [
# 		"unit_discount.tasks.hourly"
# 	],
# 	"weekly": [
# 		"unit_discount.tasks.weekly"
# 	],
# 	"monthly": [
# 		"unit_discount.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "unit_discount.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "unit_discount.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "unit_discount.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["unit_discount.utils.before_request"]
# after_request = ["unit_discount.utils.after_request"]

# Job Events
# ----------
# before_job = ["unit_discount.utils.before_job"]
# after_job = ["unit_discount.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"unit_discount.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

from unit_discount.overrides.custom_price_list import apply_price_discount_rule
from erpnext.accounts.doctype.pricing_rule import pricing_rule
pricing_rule.apply_price_discount_rule = apply_price_discount_rule


from erpnext.accounts.doctype.promotional_scheme import promotional_scheme
from unit_discount.overrides.custom_promotional_scheme import price_discount_fields
promotional_scheme.price_discount_fields = price_discount_fields


fixtures = [
    { "dt": "Custom Field", "filters": [["module", "=", "Unit Discount"]]},
    { "dt": "Property Setter", "filters": [["module", "=", "Unit Discount"]]},
    { "dt": "Server Script", "filters": [["module", "=", "Unit Discount"]]},
    { "dt": "Client Script", "filters": [["module", "=", "Unit Discount"]]}
]
