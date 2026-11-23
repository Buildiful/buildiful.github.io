# Buildiful 365 — Daily release workflow

Public contributor documentation for updating the [Buildiful 365 homepage](https://buildiful.github.io/). This importer is designed to work with the **internal** Buildiful 365 Card Builder's Daily Release Pack ZIP. It does **not** require access to that private application.

## First-time installation

Copy `import_release.py` into the root of the existing `Buildiful/buildiful.github.io` checkout, next to `tools.json` and `build.py`. Do **not** replace or remove the current homepage files. The script uses only Python 3.7+ standard-library modules, no API keys, no GitHub write access, and no dependencies.

## Every daily release

1. Publish and test the standalone tool at `https://buildiful.github.io/<slug>/`.
2. In your **private** Card Builder, enter the release day, name, short description, date, category, URL slug, homepage description, and search tags.
3. Upload a *transparent illustration without a yellow badge*, and use **Icon Studio** to apply the canonical solid-yellow circle and white ring. Alternatively, import a previously completed badge as-is.
4. Click **Download Daily Release Pack (.zip)**. It contains the icon, two social cards (square and landscape), and `release.json`.
5. From your existing local homepage checkout, import and publish in one command (after a confirmation prompt):

   ```sh
   python3 import_release.py /path/to/Buildiful-365-Release-008-example-tool.zip --publish
   ```

6. The importer checks for unrelated local edits, validates the ZIP, regenerates HTML/RSS/sitemap, and asks **Commit and push this homepage update now?** Confirm only when ready. You can run `python3 import_release.py /path/to/pack.zip --dry-run` first, or use the original command without `--publish` and inspect with `python3 -m http.server 8000`.
7. Check the live page after pushing. Publish the two social cards separately; the importer never copies them into the public repo.

The homepage is independent of the Card Builder. It is also possible to add an entry manually to `tools.json`, copy its PNG into `assets/tools/`, and run `python3 build.py` as before.

## Categories and homepage tint

Category names are not limited to Create, Publish, Enjoy and Game. Use any short descriptive label, such as **Explore**, **Education** or **Productivity**, in the internal Release Pack Builder. The homepage importer and static generator validate the name and automatically add a filter tab the first time a category appears. A repeat of the same label with different capitalization reuses the existing category. The built-in categories appear first in the order Create, Publish, Enjoy, Game; new categories follow alphabetically. No manual changes to `template.html` or `app.js` are needed.

**Category is not homepage tint.** The release pack's `category` is a freely typed label, whereas the `kind` field is the existing tint/fallback-artwork selector and remains limited to `book`, `card`, `gif`, `font`, and `music`. For example, Day 011 can use category `Explore` and kind `book`. Keep both fields as exported by the Builder.

If you replace scripts in an existing Git checkout, commit the script/template changes before using `--publish`, because that option intentionally refuses unrelated uncommitted changes. The `--dry-run` and plain import options work before committing.

## Icon Standard v1.0 (from Day 007 onward)

The icon generator runs entirely locally in Card Builder:

| Element | Specification |
|---|---|
| Export | 1024×1024 transparent PNG |
| Outer white circle | Center (512,512), radius 485px |
| Inner solid yellow circle | Center (512,512), radius 457px, fill `#F9E8A7` |
| White ring | 28px radial thickness |
| Illustration | Aspect-preserving and centered; default maximum dimension 72% of canvas |
| Suggested medium-blue outline | `#27577C` (art-direction guidance, not auto-recolored) |
| Shadow | None baked into the exported icon; let the homepage apply its existing CSS shadow |
| Transparency | Outside the outer white ring |

The first six released icons remain unchanged. Homepage background tints are separate from the badge; Days 006 and 007 can have their `kind` fields changed independently without replacing icons. Their current names and badge appearance are grandfathered in. The importer uses `NNN_slug.png` naming and checks for duplicates rather than overwriting existing releases. It **does not** copy internal project files or export the user's social card artwork to the public website. The `--publish` option also checks that `origin` is the official Buildiful homepage repository, is on `main`/`master`, and has no unrelated changes. Pushes are never silent. If Git authentication fails after a successful local commit, run `git push origin <branch>` to retry.

## Format and safety

`release.json` uses `"schema": "buildiful365-release-pack/v1"` and contains `release` data plus `assets.icon`. The importer validates day, slug, a custom category label, the existing homepage tint, tags, and a 1024×1024 PNG before writing. New entries are appended to `tools.json`, then the existing generator updates HTML, RSS, and sitemap. Existing day numbers, slugs, and images cannot be overwritten. If the generator fails, the importer attempts to restore original catalog and generated files.

Do not put the private Card Builder application, its working projects, internal release readiness notes, or the complete daily ZIP into the public homepage repository. You may include this document and the public-facing QA checklist.

## Recommended automatic tint cycle

The Card Builder now defaults the homepage tint by release day rather than type of tool: blue → pink → yellow → lavender → mint, repeated. To adopt this on existing homepage entries, set `kind` to `book` for Day 006 and `card` for Day 007 in `tools.json`, then run `python3 build.py`. Day 008 defaults to `gif` (Soft yellow) when exported from the revised Card Builder. The `kind` field currently doubles as a legacy fallback illustration key, but releases with custom `image` files still display their own artwork.
