import re
from urllib.parse import urlsplit

import frappe


DEFAULTS = {
	"brand_name": "Leaforge 365",
	"brand_tagline": "Business Central, Implemented Around Your Business",
	"website_url": "https://www.leaforge365.com/",
	"support_email": "Info@leaforge365.com",
	"support_phone": "+91 89558 61060",
	"page_background": "#F3F8F7",
	"card_background": "#FFFFFF",
	"text_color": "#0B2530",
	"primary_color": "#04414B",
	"layout_style": "Card",
	"card_spacing": "Comfortable",
}

COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9 ()-]{7,20}$")
BRAND_ASSET_PREFIX = "/assets/site_branding/images/"


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_login_branding():
	return get_public_branding()


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_branding():
	return get_public_branding()


def get_public_branding():
	settings = frappe.get_cached_doc("Login Branding Settings")
	brand_name = settings.brand_name or DEFAULTS["brand_name"]
	desk_brand_name = getattr(settings, "desk_brand_name", None) or brand_name
	website_title = getattr(settings, "website_title", None) or brand_name
	return {
		"enabled": bool(settings.enabled),
		"brand_name": brand_name,
		"brand_tagline": getattr(settings, "brand_tagline", None)
		or DEFAULTS["brand_tagline"],
		"logo": _public_file_url(settings.logo),
		"favicon": _public_file_url(getattr(settings, "favicon", None)),
		"website_url": _safe_website_url(getattr(settings, "website_url", None)),
		"support_email": _safe_email(getattr(settings, "support_email", None)),
		"support_phone": _safe_phone(getattr(settings, "support_phone", None)),
		"page_background": _safe_color(settings.page_background, "page_background"),
		"card_background": _safe_color(settings.card_background, "card_background"),
		"text_color": _safe_color(settings.text_color, "text_color"),
		"primary_color": _safe_color(settings.primary_color, "primary_color"),
		"layout_style": _allowed_value(settings.layout_style, {"Card", "Minimal"}, "layout_style"),
		"card_spacing": _allowed_value(
			settings.card_spacing, {"Comfortable", "Compact"}, "card_spacing"
		),
		"hide_footer": bool(settings.hide_footer),
		"desk_enabled": _enabled_setting(settings, "enable_desk_branding"),
		"desk_brand_name": desk_brand_name,
		"show_logo_in_desk_header": _enabled_setting(
			settings, "show_logo_in_desk_header"
		),
		"show_logo_on_loading_screen": _enabled_setting(
			settings, "show_logo_on_loading_screen"
		),
		"show_brand_in_page_title": _enabled_setting(
			settings, "show_brand_in_page_title"
		),
		"website_enabled": _enabled_setting(settings, "enable_website_branding"),
		"website_title": website_title,
	}


def _enabled_setting(settings, fieldname):
	value = getattr(settings, fieldname, None)
	return True if value is None else bool(value)


def _safe_color(value, default_key):
	return value if value and COLOR_PATTERN.fullmatch(value) else DEFAULTS[default_key]


def _allowed_value(value, allowed, default_key):
	return value if value in allowed else DEFAULTS[default_key]


def _public_file_url(value):
	if not isinstance(value, str):
		return ""
	if value.startswith("/files/"):
		return value
	if value.startswith(BRAND_ASSET_PREFIX) and ".." not in value:
		return value
	return ""


def _safe_website_url(value):
	if not isinstance(value, str):
		return DEFAULTS["website_url"]
	parsed = urlsplit(value)
	if parsed.scheme not in {"http", "https"} or not parsed.netloc:
		return DEFAULTS["website_url"]
	return value


def _safe_email(value):
	if isinstance(value, str) and EMAIL_PATTERN.fullmatch(value):
		return value
	return DEFAULTS["support_email"]


def _safe_phone(value):
	if isinstance(value, str) and PHONE_PATTERN.fullmatch(value):
		return value
	return DEFAULTS["support_phone"]
