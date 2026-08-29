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
