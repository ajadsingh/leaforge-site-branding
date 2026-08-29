import frappe


def execute():
	# This field is new, so no earlier user preference can be overwritten.
	frappe.db.set_single_value(
		"Login Branding Settings", "show_logo_on_loading_screen", 1
	)
