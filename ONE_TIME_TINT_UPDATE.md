# One-time homepage tint update (Days 006–007)

The homepage's `kind` field currently determines the background tint and serves as a fallback illustration type. Since all the published tools have explicit `image` paths, changing `kind` changes the background color **without replacing the artwork**.

In the public homepage repository's `tools.json`, make these two one-time edits:

- Day 006 — Volume Normalizer: change `"kind": "music"` to `"kind": "book"` (Light blue).
- Day 007 — Boxophone: change `"kind": "music"` to `"kind": "card"` (Soft pink).

Days 001–005 already follow the desired five-color rotation. Day 008 from the updated Card Builder will default to `"kind": "gif"` (Soft yellow). Future tints automatically cycle: blue, pink, yellow, lavender, mint.

After editing the two existing catalog entries, run `python3 build.py` in the homepage repository, then commit and push `tools.json`, `index.html`, `feed.xml`, and `sitemap.xml` as usual. **Do this in a separate clean commit before running the new importer with `--publish`,** because that option intentionally refuses to bundle unrelated edits. Alternatively, import Day 008 without `--publish` and manually commit all the changes together.

The Day 008 ZIP attached in the previous conversation used the old default Light blue tint and a Book Builder description. Update both the social-card description and homepage description in Card Builder, and export a **fresh ZIP** before importing. If Day 008 has already been imported, the importer will refuse to overwrite it; in that case, edit the existing catalog record and regenerate the homepage instead.
