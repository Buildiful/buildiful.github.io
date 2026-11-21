# Buildiful 365

**One free tool a day.** Buildiful 365 is a growing collection of free tools for creating, publishing, learning, and playing. We want to make the web more open and creativity more accessible.

**Explore:** https://buildiful.github.io/

## About the project

Buildiful® creates and shares one free tool each day. Most tools are open source and live in their own independent GitHub repositories. The homepage is a searchable public catalog, with links to each tool and its source code.

The site is built with static HTML, CSS, and JavaScript and is hosted on GitHub Pages. Visitors do not need to sign in or subscribe. The catalog is available without JavaScript; search, sorting, and category filters are optional browser enhancements.

## Project files

- `index.html` — generated homepage, including the published catalog.
- `template.html` — homepage layout source.
- `tools.json` — public catalog data.
- `build.py` — standard-library Python generator for the homepage, RSS feed, and sitemap.
- `styles.css` and `homepage.css` — base styling and homepage typography.
- `app.js` — browser-side search, filters, sorting, and link event handling.
- `assets/` — Buildiful® branding and tool artwork.
- `privacy.html` and `analytics-consent.js` — privacy information and privacy-aware website analytics.
- `feed.xml` and `sitemap.xml` — release feed and sitemap.

## Run locally

No installation, backend, or build dependencies are required to view the existing site. Open `index.html` in a browser, or serve the directory with Python:

```sh
python3 -m http.server 8000
```

Then visit http://localhost:8000/.

Website analytics is restricted to the official Buildiful GitHub Pages host and is inactive on local previews and forks.

## Privacy

The homepage does not require an account or upload visitors' files. Catalog searches and filters run in the browser. Basic website analytics may measure page visits and tool/source-link openings, subject to regional privacy choices. Search terms and personal files are not analytics event parameters. See [Privacy](https://buildiful.github.io/privacy.html) for details.

## Source, licenses, and trademarks

Homepage source code is available under the MIT License; see [LICENSE](LICENSE). Each linked tool has its own repository and applicable license. Buildiful® and its official brand assets are reserved; see [TRADEMARKS.md](TRADEMARKS.md).

Built by [Buildiful®](https://buildiful.com/).
