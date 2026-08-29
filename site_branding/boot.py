from site_branding.api import get_public_branding


def boot_session(bootinfo):
	bootinfo.site_branding = get_public_branding()
