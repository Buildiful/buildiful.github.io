# Buildiful 365 — Homepage

The public hub for [Buildiful 365](https://buildiful.github.io/): a growing collection of free, open-source tools from Buildiful®.

## What is included

- `tools.json` — source of truth for the release catalog.
- `build.py` — Python standard library only; builds the static homepage, RSS feed and sitemap.
- `template.html` — homepage layout for the generator.
- `index.html`, `feed.xml`, `sitemap.xml` — generated, committed output for GitHub Pages.
- `styles.css`, `app.js` — responsive styling, accessible filters, search and sorting.
- `assets/tools/` — optional unique tool artwork files referenced from `tools.json`.
- `assets/` — official Buildiful® logo and favicon set.
- `analytics-consent.js`, `privacy.html` — consent-based optional GA4.
- `LICENSE`, `TRADEMARKS.md`, `QA_CHECKLIST.md`, `.gitignore`, `.nojekyll` — public repository support files.

The site is static. There is no npm, backend, database, or API key to deploy. All release cards appear in generated HTML even with JavaScript disabled.

## Preview locally

From the extracted folder, run:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Press Ctrl+C in Terminal to stop. Analytics runs only after opt-in on hosted HTTP pages; test consent on a local server or decline it while previewing. Directly opening `index.html` as a file also works; analytics is disabled for `file://`.

## Publishing to GitHub Pages

The live homepage repository is [`Buildiful/buildiful.github.io`](https://github.com/Buildiful/buildiful.github.io). As checked for this update, its default branch is **`master`**. Extract this package at the repository root, commit the updated files, and push to the branch already configured for GitHub Pages in **Settings → Pages**. Do not add an extra enclosing directory.

To avoid overwriting newer work, compare the ZIP with the repository before replacing it. The pack represents the inspected homepage plus the Volume Normalizer catalog/artwork update. **This local package has not been pushed to GitHub.**

## Add the next release

1. Append one JSON object to `tools.json`. Keep the `day`, `date`, `name`, `slug`, `category`, `kind`, `desc`, and `tags` fields.
2. Optionally save a unique PNG (or WebP/JPEG) into `assets/tools/` and set `"image": "assets/tools/your-tool.png"`. No edits to the generator's illustration dictionary are needed when you provide a custom image. Choose any currently supported `kind` as the fallback illustration.
3. Run `python3 build.py`.
4. Check the homepage locally, then commit `tools.json`, the added image, `index.html`, `feed.xml`, and `sitemap.xml`. No hand-editing cards or site redesign needed.

Here is the Volume Normalizer catalog record:

```json
{
  "day": 6,
  "date": "2026-11-18",
  "name": "Volume Normalizer",
  "slug": "volume-normalizer",
  "category": "Enjoy",
  "kind": "music",
  "image": "assets/tools/volume-normalizer.png",
  "desc": "Normalize audio files for consistent playback volume",
  "tags": ["audio", "music", "loudness", "LUFS", "normalization", "sound"]
}
```

**Catalog conventions:** `slug` determines the live URL `https://buildiful.github.io/<slug>/` and source repository `https://github.com/Buildiful/<slug>`. `day` determines newest-first order, the featured release and the padded day label. `category` is currently `Create`, `Publish`, or `Enjoy`; extend the buttons in `template.html` and validation in `build.py` to add categories. `kind` is used only for the legacy fallback SVG and default background color. Tool images are optional for backwards compatibility.

Custom images must be stored locally under `assets/tools/` and named using lowercase letters, digits and hyphens, with a `.png`, `.jpg`, `.jpeg` or `.webp` extension. The build fails when the referenced image is missing. Give individual tools distinctive images and keep files reasonably small.

## Analytics and privacy

The existing GA4 measurement ID is `G-TG14RBXLTF`. The consent module does not load the Google Analytics tag before opt-in. Only `tool_open` and `source_open` link events are allowed with catalog-validated slugs; search terms and private content are never included. Analytics is off for `file://` previews. See `privacy.html`.

## License and brand

Code is MIT licensed. Buildiful® name, logo, icons, and other official brand assets are reserved; see `LICENSE` and `TRADEMARKS.md`.

Each standalone tool remains an independent repository. The homepage may refer to Buildiful 365 and campaign day numbers; those references do not belong inside the standalone tools' repositories.
