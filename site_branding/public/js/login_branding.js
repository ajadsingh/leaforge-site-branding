(() => {
	"use strict";

	whenDocumentReady(loadBranding);

	function whenDocumentReady(callback) {
		if (document.readyState === "loading") {
			document.addEventListener("DOMContentLoaded", callback, { once: true });
			return;
		}
		callback();
	}

	async function loadBranding() {
		try {
			const response = await fetch(
				"/api/method/site_branding.api.get_branding",
				{ credentials: "same-origin" }
			);
			if (!response.ok) return;

			const { message: settings } = await response.json();
			if (!settings) return;

			if (window.location.pathname === "/login" && settings.enabled) {
				applyLoginBranding(settings);
			} else if (settings.website_enabled) {
				applyWebsiteBranding(settings);
			}
		} catch (error) {
			console.warn("Login branding could not be loaded.", error);
		}
	}

	function applyLoginBranding(settings) {
		const body = document.body;
		body.classList.add("site-branding-login");
		body.classList.toggle("branding-hide-footer", settings.hide_footer);
		body.classList.toggle("branding-layout-minimal", settings.layout_style === "Minimal");
		body.classList.toggle("branding-spacing-compact", settings.card_spacing === "Compact");

		setThemeVariables(settings);
		setBrandName(settings.brand_name);
		setBrandTagline(settings.brand_tagline);
		setLogo(settings.logo, settings.brand_name);
		setSupportDetails(settings);
		setFavicon(settings.favicon || settings.logo);
		document.title = settings.brand_name;
	}

	function setBrandTagline(tagline) {
		document.querySelectorAll(getLoginHeadingSelector()).forEach((heading) => {
			let element = heading.querySelector(".site-branding-tagline");
			if (!element) {
				element = document.createElement("p");
				element.className = "site-branding-tagline";
				heading.append(element);
			}
			element.textContent = tagline || "";
		});
	}

	function setSupportDetails(settings) {
		document.querySelectorAll("section.for-login .page-card, section.for-email-login .page-card").forEach((card) => {
			let support = card.querySelector(".site-branding-support");
			if (!support) {
				support = document.createElement("div");
				support.className = "site-branding-support";
				card.append(support);
			}

			support.replaceChildren();
			appendSupportLink(support, settings.website_url, "Leaforge365.com", true);
			appendSupportLink(support, `mailto:${settings.support_email}`, settings.support_email);
			appendSupportLink(
				support,
				`tel:${settings.support_phone.replace(/[^+\d]/g, "")}`,
				settings.support_phone
			);
		});
	}

	function appendSupportLink(wrapper, href, label, external = false) {
		if (!href || !label) return;
		if (wrapper.childElementCount) wrapper.append(document.createTextNode("•"));

		const link = document.createElement("a");
		link.href = href;
		link.textContent = label;
		if (external) {
			link.target = "_blank";
			link.rel = "noopener noreferrer";
		}
		wrapper.append(link);
	}

	function applyWebsiteBranding(settings) {
		const title = settings.website_title || settings.brand_name;
		setFavicon(settings.favicon || settings.logo);
		setWebsiteLogo(settings.logo, title);
		setWebsiteTitle(title);
		document.body.style.setProperty("--primary", settings.primary_color);
	}

	function setThemeVariables(settings) {
		const style = document.body.style;
		style.setProperty("--branding-bg", settings.page_background);
		style.setProperty("--branding-card", settings.card_background);
		style.setProperty("--branding-text", settings.text_color);
		style.setProperty("--branding-primary", settings.primary_color);
	}

	function setBrandName(brandName) {
		document.querySelectorAll(getLoginHeadingSelector()).forEach((heading) => {
			heading.querySelectorAll(".site-branding-name:not(h4)").forEach((element) => element.remove());
			const name = heading.querySelector("h4") || createBrandHeading(heading);
			name.classList.add("site-branding-name");
			name.textContent = brandName;
		});
	}

	function setLogo(logo, brandName) {
		if (!logo) return;
		document.querySelectorAll(getLoginLogoSelector()).forEach((image) => {
			image.src = logo;
			image.alt = brandName;
		});
	}

	function setWebsiteLogo(logo, brandName) {
		if (!logo) return;
		document.querySelectorAll(".navbar-brand img, .web-header .app-logo").forEach((image) => {
			image.src = logo;
			image.alt = brandName;
		});
	}

	function setFavicon(iconUrl) {
		if (!iconUrl) return;
		let links = document.querySelectorAll("link[rel~='icon']");
		if (!links.length) {
			const link = document.createElement("link");
			link.rel = "icon";
			document.head.append(link);
			links = [link];
		}
		links.forEach((link) => (link.href = iconUrl));
	}

	function setWebsiteTitle(brandName) {
		const currentTitle = document.title.trim();
		if (!currentTitle || currentTitle.toLowerCase().includes(brandName.toLowerCase())) return;
		const replacedTitle = currentTitle.replace(/\b(?:ERPNext|Frappe)\b/gi, brandName);
		document.title =
			replacedTitle === currentTitle ? `${currentTitle} | ${brandName}` : replacedTitle;
	}

	function getLoginHeadingSelector() {
		return [
			"section.for-login .page-card-head",
			"section.for-email-login .page-card-head",
		].join(",");
	}

	function getLoginLogoSelector() {
		return [
			"section.for-login .page-card-head .app-logo",
			"section.for-email-login .page-card-head .app-logo",
		].join(",");
	}

	function createBrandHeading(heading) {
		const name = document.createElement("h4");
		heading.append(name);
		return name;
	}
})();
