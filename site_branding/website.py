from site_branding.api import get_public_branding


LOGIN_ROUTE = "login"
DESK_ROUTE = "desk"
BRANDING_BASE_TEMPLATE = "site_branding/templates/site_branding_base.html"


def update_website_context(context):
	settings = get_public_branding()
	route = context.get("route")

	if route == LOGIN_ROUTE and settings["enabled"]:
		apply_login_context(context, settings)
	elif route == DESK_ROUTE and settings["desk_enabled"]:
		apply_desk_context(context, settings)


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


def apply_desk_context(context, settings):
	context["app_name"] = settings["desk_brand_name"] or settings["brand_name"]
	context["favicon"] = settings["favicon"] or settings["logo"]

	if settings["show_logo_on_loading_screen"] and settings["logo"]:
		context["splash_image"] = settings["logo"]


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
