import frappe


LEAFORGE_DEFAULTS = {
	"enabled": 1,
	"brand_name": "Leaforge 365",
	"brand_tagline": "Business Central, Implemented Around Your Business",
	"logo": "/assets/site_branding/images/leaforge-logo.png",
	"favicon": "/assets/site_branding/images/leaforge-favicon.png",
	"website_url": "https://www.leaforge365.com/",
	"support_email": "Info@leaforge365.com",
	"support_phone": "+91 89558 61060",
	"page_background": "#F3F8F7",
	"card_background": "#FFFFFF",
	"text_color": "#0B2530",
	"primary_color": "#04414B",
	"enable_desk_branding": 1,
	"desk_brand_name": "Leaforge 365",
	"show_logo_in_desk_header": 1,
	"show_brand_in_page_title": 1,
	"enable_website_branding": 1,
	"website_title": "Leaforge Technologies",
}


def execute():
	settings = frappe.get_single("Login Branding Settings")
	settings.update(LEAFORGE_DEFAULTS)
	settings.save(ignore_permissions=True)
