### Site Branding

Settings-driven login, Desk, website, title, favicon, logo, and color branding for Frappe and ERPNext.

All changes stay inside the custom app. Framework and ERPNext core files are not modified.

### Configuration

Open **Login Branding Settings** as a System Manager. The same form controls:

- Login page logo, brand name, colors, layout, and footer
- Desk workspace brand, header logo, page title, favicon, and primary color
- Website logo, title, favicon, and primary color

The live preview updates while you edit. Save the form and reload the target page to see the published branding.

New installations start with the official Leaforge 365 logo, favicon, company details, tagline, and `#04414B` brand color. All bundled brand assets are served locally by this app.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app site_branding
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/site_branding
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
