from site_branding.api import get_public_branding


LOGIN_ROUTE = "login"
BRANDING_BASE_TEMPLATE = "site_branding/templates/site_branding_base.html"


def update_website_context(context):
	if context.get("route") != LOGIN_ROUTE:
		return

	settings = get_public_branding()
	if not settings["enabled"]:
		return

	apply_login_context(context, settings)


def apply_login_context(context, settings):
	context.update(
		{
			"app_name": settings["brand_name"],
			"title": settings["brand_name"],
			"body_class": _login_body_class(context.get("body_class"), settings),
			"base_template_path": BRANDING_BASE_TEMPLATE,
			"site_branding_config": settings,
		}
	)

	if settings["logo"]:
		context["logo"] = settings["logo"]
	context["favicon"] = settings["favicon"] or settings["logo"]


def _login_body_class(existing_classes, settings):
	classes = set((existing_classes or "").split())
	classes.add("site-branding-login")

	if settings["hide_footer"]:
		classes.add("branding-hide-footer")
	if settings["layout_style"] == "Minimal":
		classes.add("branding-layout-minimal")
	if settings["card_spacing"] == "Compact":
		classes.add("branding-spacing-compact")

	return " ".join(sorted(classes))
