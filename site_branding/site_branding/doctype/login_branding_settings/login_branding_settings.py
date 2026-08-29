import frappe
from frappe import _
from frappe.model.document import Document


BRAND_ASSET_PREFIX = "/assets/site_branding/images/"


class LoginBrandingSettings(Document):
	def validate(self):
		self.logo = make_brand_asset_public(self.logo, "logo")
		self.favicon = make_brand_asset_public(self.favicon, "favicon")


def make_brand_asset_public(file_url: str | None, fieldname: str) -> str:
	if not file_url:
		return ""
	if file_url.startswith("/files/"):
		return file_url
	if file_url.startswith(BRAND_ASSET_PREFIX) and ".." not in file_url:
		return file_url
	if not file_url.startswith("/private/files/"):
		frappe.throw(_("Brand assets must be uploaded image files."), frappe.ValidationError)

	file_name = frappe.db.get_value(
		"File",
		{
			"file_url": file_url,
			"attached_to_doctype": "Login Branding Settings",
			"attached_to_field": fieldname,
		},
		"name",
	)
	if not file_name:
		frappe.throw(_("The uploaded brand asset could not be found."), frappe.DoesNotExistError)

	file_doc = frappe.get_doc("File", file_name)
	file_doc.is_private = 0
	file_doc.save(ignore_permissions=True)
	return file_doc.file_url
