from frappe.tests import UnitTestCase

from types import SimpleNamespace

from site_branding.api import (
	_allowed_value,
	_enabled_setting,
	_public_file_url,
	_safe_color,
	_safe_email,
	_safe_phone,
	_safe_website_url,
)
from site_branding.website import (
	BRANDING_BASE_TEMPLATE,
	apply_desk_context,
	apply_login_context,
)


class TestLoginBrandingSanitizers(UnitTestCase):
	def test_accepts_hex_color(self):
		self.assertEqual(_safe_color("#12AbEF", "primary_color"), "#12AbEF")

	def test_rejects_css_injection(self):
		self.assertEqual(_safe_color("red; display:none", "primary_color"), "#04414B")

	def test_rejects_unknown_layout(self):
		self.assertEqual(_allowed_value("Wide", {"Card", "Minimal"}, "layout_style"), "Card")

	def test_only_returns_public_file_urls(self):
		self.assertEqual(_public_file_url("/files/logo.svg"), "/files/logo.svg")
		self.assertEqual(_public_file_url("/private/files/logo.svg"), "")
		self.assertEqual(_public_file_url("https://example.com/logo.svg"), "")
		self.assertEqual(
			_public_file_url("/assets/site_branding/images/leaforge-logo.png"),
			"/assets/site_branding/images/leaforge-logo.png",
		)
		self.assertEqual(_public_file_url("/assets/site_branding/images/../secret"), "")

	def test_contact_details_are_sanitized(self):
		self.assertEqual(_safe_email("hello@example.com"), "hello@example.com")
		self.assertEqual(_safe_email("javascript:alert(1)"), "Info@leaforge365.com")
		self.assertEqual(_safe_phone("+91 89558 61060"), "+91 89558 61060")
		self.assertEqual(_safe_phone("<script>"), "+91 89558 61060")
		self.assertEqual(_safe_website_url("https://example.com/help"), "https://example.com/help")
		self.assertEqual(_safe_website_url("javascript:alert(1)"), "https://www.leaforge365.com/")

	def test_new_toggle_defaults_to_enabled(self):
		self.assertTrue(_enabled_setting(SimpleNamespace(), "new_toggle"))

	def test_explicit_toggle_value_is_respected(self):
		self.assertFalse(_enabled_setting(SimpleNamespace(toggle=0), "toggle"))


class TestLoginWebsiteContext(UnitTestCase):
	def test_branding_is_present_in_initial_login_context(self):
		context = {"body_class": "existing-class", "logo": "/default-logo.svg"}
		settings = {
			"brand_name": "Leaforge 365",
			"logo": "/files/leaforge-logo.png",
			"favicon": "/files/leaforge-favicon.png",
			"hide_footer": True,
			"layout_style": "Minimal",
			"card_spacing": "Compact",
		}

		apply_login_context(context, settings)

		self.assertEqual(context["app_name"], "Leaforge 365")
		self.assertEqual(context["title"], "Leaforge 365")
		self.assertEqual(context["logo"], settings["logo"])
		self.assertEqual(context["favicon"], settings["favicon"])
		self.assertEqual(context["base_template_path"], BRANDING_BASE_TEMPLATE)
		self.assertIs(context["site_branding_config"], settings)
		self.assertEqual(
			set(context["body_class"].split()),
			{
				"existing-class",
				"site-branding-login",
				"branding-hide-footer",
				"branding-layout-minimal",
				"branding-spacing-compact",
			},
		)

	def test_branding_is_present_in_initial_desk_context(self):
		context = {
			"app_name": "ERPNext",
			"favicon": "/assets/erpnext/images/erpnext-favicon.svg",
			"splash_image": "/assets/erpnext/images/erpnext-logo.svg",
		}
		settings = {
			"brand_name": "Leaforge 365",
			"desk_brand_name": "Leaforge 365",
			"logo": "/files/leaforge-logo.png",
			"favicon": "/files/leaforge-favicon.png",
			"show_logo_on_loading_screen": True,
		}

		apply_desk_context(context, settings)

		self.assertEqual(context["app_name"], "Leaforge 365")
		self.assertEqual(context["favicon"], settings["favicon"])
		self.assertEqual(context["splash_image"], settings["logo"])
