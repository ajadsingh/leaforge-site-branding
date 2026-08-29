import frappe


APPS_PAGE_DEFAULTS = {
	"enable_apps_page_branding": 1,
	"apps_page_brand_name": "Leaforge 365",
	"settings_tile_label": "System Settings",
	"show_brand_logo_on_apps_page": 1,
}


def execute():
	# These fields are new, so no existing user preference can be overwritten.
	for fieldname, default in APPS_PAGE_DEFAULTS.items():
		frappe.db.set_single_value("Login Branding Settings", fieldname, default)
