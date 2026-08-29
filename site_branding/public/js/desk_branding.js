(() => {
	"use strict";

	whenDocumentReady(initializeDeskBranding);

	function whenDocumentReady(callback) {
		if (document.readyState === "loading") {
			document.addEventListener("DOMContentLoaded", callback, { once: true });
			return;
		}
		callback();
	}

	async function initializeDeskBranding() {
		const settings = window.frappe?.boot?.site_branding || (await fetchBranding());
		if (!settings?.desk_enabled) return;

		document.body.classList.add("site-branding-desk");
		document.body.style.setProperty("--site-brand-primary", settings.primary_color);
		customizeRuntimeAppData(settings);
		applyDeskBranding(settings);
		watchDeskChanges(settings);
	}

	function customizeRuntimeAppData(settings) {
		const brandName = settings.desk_brand_name || settings.brand_name;
		const appData = window.frappe?.boot?.app_data || [];
		appData.forEach((app) => {
			if (!["erpnext", "frappe"].includes(app.app_name)) return;
			app.app_title = brandName;
			if (settings.show_logo_in_desk_header && settings.logo) {
				app.app_logo_url = settings.logo;
			}
		});
	}

	async function fetchBranding() {
		try {
			const response = await fetch("/api/method/site_branding.api.get_branding", {
				credentials: "same-origin",
			});
			if (!response.ok) return null;
			return (await response.json()).message;
		} catch (error) {
			console.warn("Desk branding could not be loaded.", error);
			return null;
		}
	}

	function applyDeskBranding(settings) {
		const brandName = settings.desk_brand_name || settings.brand_name;
		if (!brandName) return;

		if (window.frappe?.app?.sidebar) {
			frappe.app.sidebar.header_subtitle = brandName;
		}

		setText(".sidebar-header .header-subtitle", brandName);
		setHeaderLogo(settings.logo, brandName, settings.show_logo_in_desk_header);
		applyAppsPageBranding(settings, brandName);
		setFavicon(settings.favicon || settings.logo);
		if (settings.show_brand_in_page_title) setPageTitle(brandName);
	}

	function applyAppsPageBranding(settings, brandName) {
		if (!settings.apps_page_enabled) return;

		const appsPageName = settings.apps_page_brand_name || brandName;
		const settingsLabel = settings.settings_tile_label || "System Settings";
		if (settings.show_brand_logo_on_apps_page) {
			setAppsLauncherLogo(settings.favicon || settings.logo, appsPageName);
			brandDesktopTile("Framework", appsPageName, settings.favicon || settings.logo);
		} else {
			brandDesktopTile("Framework", appsPageName);
		}
		renameDesktopTile("ERPNext Settings", settingsLabel);
	}

	function setAppsLauncherLogo(logoUrl, brandName) {
		if (!logoUrl) return;
		const image = document.querySelector(".navbar-home #brand-logo");
		if (!image) return;

		if (image.getAttribute("src") !== logoUrl) image.src = logoUrl;
		if (image.alt !== brandName) image.alt = brandName;
		image.dataset.siteBrandingLogo = "1";
	}

	function brandDesktopTile(originalLabel, brandName, logoUrl) {
		const tile = findDesktopTile(originalLabel);
		if (!tile) return;

		tile.dataset.siteBrandingTile = "brand";
		setDesktopTileLabel(tile, brandName);
		if (!logoUrl) return;

		const image = tile.querySelector(".app-icon");
		if (!image) return;
		if (image.getAttribute("src") !== logoUrl) image.src = logoUrl;
		if (image.alt !== brandName) image.alt = brandName;
	}

	function renameDesktopTile(originalLabel, label) {
		const tile = findDesktopTile(originalLabel);
		if (!tile) return;
		tile.dataset.siteBrandingTile = "settings";
		setDesktopTileLabel(tile, label);
	}

	function findDesktopTile(originalLabel) {
		return document.querySelector(`.desktop-icon[data-id="${originalLabel}"]`);
	}

	function setDesktopTileLabel(tile, label) {
		const title = tile.querySelector(".icon-title");
		if (!title) return;
		if (title.textContent.trim() !== label) title.textContent = label;
		if (title.dataset.originalTitle !== label) title.dataset.originalTitle = label;
	}

	function setText(selector, value) {
		document.querySelectorAll(selector).forEach((element) => {
			if (element.textContent.trim() !== value) element.textContent = value;
		});
	}

	function setHeaderLogo(logoUrl, brandName, enabled) {
		if (!enabled || !logoUrl) return;
		document.querySelectorAll(".sidebar-header .header-logo").forEach((wrapper) => {
			const currentImage = wrapper.querySelector("img[data-site-branding-logo]");
			if (currentImage?.getAttribute("src") === logoUrl) return;

			const image = document.createElement("img");
			image.src = logoUrl;
			image.alt = brandName;
			image.dataset.siteBrandingLogo = "1";
			wrapper.replaceChildren(image);
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
		links.forEach((link) => {
			if (link.getAttribute("href") !== iconUrl) link.href = iconUrl;
		});
	}

	function setPageTitle(brandName) {
		const currentTitle = document.title.trim();
		if (!currentTitle || containsBrand(currentTitle, brandName)) return;

		const replacedTitle = currentTitle.replace(/\b(?:ERPNext|Frappe)\b/gi, brandName);
		document.title =
			replacedTitle === currentTitle ? `${currentTitle} | ${brandName}` : replacedTitle;
	}

	function containsBrand(title, brandName) {
		return title.toLocaleLowerCase().includes(brandName.toLocaleLowerCase());
	}

	function watchDeskChanges(settings) {
		let scheduled = false;
		const scheduleApply = () => {
			if (scheduled) return;
			scheduled = true;
			window.requestAnimationFrame(() => {
				scheduled = false;
				applyDeskBranding(settings);
			});
		};

		const desk = document.querySelector("#body") || document.body;
		if (desk) {
			new MutationObserver(scheduleApply).observe(desk, {
				childList: true,
				subtree: true,
			});
		}
		const title = document.querySelector("title");
		if (title) new MutationObserver(scheduleApply).observe(title, { childList: true });
		window.addEventListener("hashchange", scheduleApply);
	}
})();
