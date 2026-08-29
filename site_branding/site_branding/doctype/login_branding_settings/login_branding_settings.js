frappe.ui.form.on("Login Branding Settings", {
	refresh(frm) {
		renderPreview(frm);
	},

	enabled: renderPreview,
	brand_name: renderPreview,
	brand_tagline: renderPreview,
	logo: renderPreview,
	page_background: renderPreview,
	card_background: renderPreview,
	text_color: renderPreview,
	primary_color: renderPreview,
	layout_style: renderPreview,
	card_spacing: renderPreview,
	enable_desk_branding: renderPreview,
	desk_brand_name: renderPreview,
	show_logo_in_desk_header: renderPreview,
});

function renderPreview(frm) {
	const field = frm.get_field("preview");
	if (!field?.$wrapper) return;

	const values = previewValues(frm.doc);
	field.$wrapper.html(`
		<div class="branding-preview-dock" style="${previewVariables(values)}">
			<div class="branding-preview-toolbar">
				<strong>Login preview</strong>
				<span>${values.enabled ? "Enabled" : "Disabled"}</span>
			</div>
			<div class="branding-preview-page">
				<div class="branding-preview-card ${values.layoutClass} ${values.spacingClass}">
					${previewLogo(values)}
					<div class="branding-preview-name">${frappe.utils.escape_html(values.brandName)}</div>
					<div class="branding-preview-tagline">${frappe.utils.escape_html(values.brandTagline)}</div>
					<div class="branding-preview-input">piyush.silvassa@gmail.com</div>
					<div class="branding-preview-input">••••••••</div>
					<div class="branding-preview-button">Login</div>
				</div>
			</div>
		</div>
	`);
}

function previewValues(doc) {
	return {
		enabled: Boolean(doc.enabled),
		brandName: doc.brand_name || "Your Company",
		brandTagline: doc.brand_tagline || "",
		logo: doc.logo || "",
		pageBackground: doc.page_background || "#F8FAFC",
		cardBackground: doc.card_background || "#FFFFFF",
		textColor: doc.text_color || "#111827",
		primaryColor: doc.primary_color || "#2563EB",
		layoutClass: doc.layout_style === "Minimal" ? "is-minimal" : "",
		spacingClass: doc.card_spacing === "Compact" ? "is-compact" : "",
	};
}

function previewVariables(values) {
	return [
		`--preview-page:${safeColor(values.pageBackground, "#F8FAFC")}`,
		`--preview-card:${safeColor(values.cardBackground, "#FFFFFF")}`,
		`--preview-text:${safeColor(values.textColor, "#111827")}`,
		`--preview-primary:${safeColor(values.primaryColor, "#2563EB")}`,
	].join(";");
}

function safeColor(value, fallback) {
	return /^#[0-9a-f]{6}$/i.test(value) ? value : fallback;
}

function previewLogo(values) {
	if (
		!values.logo.startsWith("/files/") &&
		!values.logo.startsWith("/assets/site_branding/images/")
	) {
		return "";
	}
	const logo = frappe.utils.escape_html(values.logo);
	return `<img class="branding-preview-logo" src="${logo}" alt="">`;
}
