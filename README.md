# Buildiful 365 — Homepage

The public hub for [Buildiful 365](https://buildiful.github.io/), a collection of free, open-source tools built by Buildiful®.

## Contents

- `index.html` — generated, fully readable static homepage; cards work without JavaScript.
- `template.html` — homepage layout used by the generator.
- `tools.json` — single source of truth for the catalog. **Edit this to add daily releases.**
- `build.py` — standard Python only; generates `index.html`, `feed.xml`, and `sitemap.xml`.
- `styles.css`, `app.js` — responsive styling and optional search/category/sort enhancements.
- `analytics-consent.js`, `privacy.html` — consent-based analytics; no GA4 before opt-in.
- `fetch-brand-assets.sh` — optional one-time download of the official Buildiful logo and favicon into `assets/`.
- `.nojekyll`, `.gitignore`, `LICENSE`, `TRADEMARKS.md`, `QA_CHECKLIST.md` — public repository basics.

## First launch at buildiful.github.io

1. From the **Buildiful GitHub organization**, create a **public** repository named `buildiful.github.io` (exact name). Its URL should be `https://github.com/Buildiful/buildiful.github.io`. A user/organization Pages repository with this name serves the root address `https://buildiful.github.io/`.
2. Extract this ZIP. Optionally run `bash fetch-brand-assets.sh` once to put official brand files into `assets/`, avoiding remote logo loading. The homepage already has a fallback to the official logo in the public `music-player` repository if the local logo is not copied. The favicon and Apple touch icon currently link to that public repository regardless of whether you copy them; you can change the two `<link>` tags in `template.html` and `privacy.html` to local paths if desired, then rerun `build.py`.
3. Commit all project contents to `main` (including hidden `.nojekyll` and `.gitignore`). **Do not put files inside an extra enclosing folder.**
4. In repository **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
5. When the deployment finishes, visit `https://buildiful.github.io/` and click through the five tools. Check mobile layout, search, privacy, and analytics consent.

There is no npm, backend, database, or API key to deploy the site. The repository source is public; do not commit passwords or secrets.

## Add a new daily tool

1. Add one object at the end of `tools.json` and set `day`, `date`, `name`, `slug`, `category`, `kind`, `desc`, `tags`.
2. Run `python3 build.py`.
3. Commit `tools.json`, `index.html`, `feed.xml`, and `sitemap.xml`; GitHub Pages refreshes after your push. No site redesign or hand-editing card HTML needed.

**Notes:**

- The repository name and GitHub Pages URL are derived from `slug`: `https://buildiful.github.io/<slug>/` and `https://github.com/Buildiful/<slug>`.
- `category` currently allows `Create`, `Publish`, or `Enjoy`. Update the category buttons in `template.html` and the validation in `build.py` if you add categories.
- `kind` currently allows `book`, `card`, `gif`, `font`, or `music` for the decorative card image. Choose a close existing kind or add a new original SVG to the `ART` dictionary in `build.py`.
- The featured tool is the one with the highest `day`; counts update automatically.
- RSS and sitemap also update automatically.
- GA4 link-click events automatically accept only the validated tool slugs rendered in the static catalog. No manually maintained slug list is needed, and arbitrary search terms are excluded.
- Public tool repositories remain independent and should **not** contain Buildiful 365 day numbering or campaign promotional copy.

Example new entry:

```json
{
  "day": 6,
  "date": "2026-11-18",
  "name": "Example Tool",
  "slug": "example-tool",
  "category": "Create",
  "kind": "card",
  "desc": "A short, accurate description of what the tool does.",
  "tags": ["example", "creative"]
}
```

## Optional analytics

GA4 measurement ID is `G-TG14RBXLTF`, matching the existing Buildiful tools. Google Analytics only loads after acceptance; declines persist, and the choice can be changed from the footer. Two optional link click events are allowed: `tool_open` and `source_open`. Search terms are never sent. For this static site, disable analytics in a downloaded local copy. The consent key is shared with other Buildiful tools hosted at the same origin, per existing implementation.

## Public-facing brand/license

Code is licensed under MIT. The Buildiful® name, wordmark, logo, favicon, and brand assets are reserved, and are not licensed for unrelated use. See `LICENSE` and `TRADEMARKS.md`.
