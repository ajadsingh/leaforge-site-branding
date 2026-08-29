import frappe


NEW_SURFACE_DEFAULTS = {
	"enable_desk_branding": 1,
	"show_logo_in_desk_header": 1,
	"show_brand_in_page_title": 1,
	"enable_website_branding": 1,
}


def execute():
	# These fields are new in this release, so no earlier user preference can be overwritten.
	for fieldname, default in NEW_SURFACE_DEFAULTS.items():
		frappe.db.set_single_value("Login Branding Settings", fieldname, default)
