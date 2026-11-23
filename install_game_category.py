#!/usr/bin/env python3
"""Local, backup-first Buildiful 365 Game category + Day 010 homepage update.

Usage: python3 install_game_category.py /path/to/buildiful.github.io
No network connection, commits, or pushes are performed.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RELEASE = {
    "day": 10,
    "date": "2026-11-22",
    "name": "Pair Where?",
    "slug": "pair-where",
    "category": "Game",
    "kind": "music",  # Homepage tint: Day 010 is mint, independent of category.
    "image": "assets/tools/010_pair-where.png",
    "desc": "Match the pairs, then sort the cards into numerical order.",
    "tags": ["memory game", "matching", "pairs", "card game", "puzzle", "sorting", "numbers", "logic", "brain teaser", "Beebbots"],
}


def add_category(source: str, label: str) -> str:
    """Extend only the existing category set in a known Python code location."""
    if label == 'builder':
        pattern = r"(assert\s+tool\[['\"]category['\"]\]\s+in\s+)(\{[^\n}]*\})"
    else:
        pattern = r"(\bCATEGORIES\s*=\s*)(\{[^\n}]*\})"
    m = re.search(pattern, source)
    if m is None:
        raise ValueError(f"Could not locate category whitelist in {label}; file not changed")
    inside = m.group(2)[1:-1]
    existing = set(re.findall(r"['\"]([^'\"]+)['\"]", inside))
    if not {'Create', 'Publish', 'Enjoy'} <= existing:
        raise ValueError(f"Unexpected {label} categories {sorted(existing)}; review manually")
    if 'Game' in existing:
        return source
    new_set = '{' + inside.strip() + ", 'Game'}"
    return source[:m.start(2)] + new_set + source[m.end(2):]


def update_template(source: str) -> str:
    if re.search(r'data-category=["\']Game["\']', source):
        return source
    pattern = r'(<button\s+class="tab"\s+data-category="Enjoy"[^>]*>Enjoy</button>)'
    m = re.search(pattern, source)
    if not m:
        raise ValueError('Cannot locate Enjoy filter in template.html; no files changed')
    addition = '\n            <button class="tab" data-category="Game" type="button" aria-pressed="false">Game</button>'
    return source[:m.end()] + addition + source[m.end():]


def update_catalog(source: str) -> tuple[str, bool]:
    items = json.loads(source)
    if not isinstance(items, list):
        raise ValueError('tools.json must be a list')
    by_day = {int(t['day']): t for t in items}
    slugs = {t.get('slug') for t in items}
    if 9 not in by_day or by_day[9].get('slug') != 'stepcells':
        raise ValueError('Day 009 Stepcells is missing or unexpected')
    by_day[9]['category'] = 'Game'
    added = False
    if 10 in by_day:
        if by_day[10].get('slug') != 'pair-where':
            raise ValueError('Day 010 already exists under a different slug')
        by_day[10]['category'] = 'Game'
    else:
        if 'pair-where' in slugs:
            raise ValueError('pair-where slug exists under a different day')
        items.append(dict(RELEASE))
        added = True
    return json.dumps(items, ensure_ascii=False, indent=2) + '\n', added


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('repository', type=Path, help='Existing local buildiful.github.io repository')
    args = p.parse_args()
    root = args.repository.expanduser().resolve()
    bundle = Path(__file__).resolve().parent
    required = ['tools.json', 'template.html', 'build.py', 'import_release.py']
    for name in required:
        if not (root / name).is_file():
            p.error(f'Missing {name} in {root}. Point to the existing homepage repository, not the tool repository.')
    if not (bundle / RELEASE['image']).is_file():
        p.error('Day 010 artwork missing from the update pack.')
    target_icon = root / RELEASE['image']
    originals = {name: (root / name).read_text('utf-8') for name in required}
    new_catalog, added = update_catalog(originals['tools.json'])
    updated = {
        'tools.json': new_catalog,
        'template.html': update_template(originals['template.html']),
        'build.py': add_category(originals['build.py'], 'builder'),
        'import_release.py': add_category(originals['import_release.py'], 'importer'),
    }
    changed = [name for name in required if updated[name] != originals[name]]
    generated = ['index.html', 'feed.xml', 'sitemap.xml']
    original_bytes = {name: (root / name).read_bytes() if (root / name).exists() else None for name in generated}
    existing_icon = target_icon.read_bytes() if target_icon.exists() else None
    paths_to_backup = changed + generated + ([RELEASE['image']] if existing_icon else [])
    backup_root = root.parent / f'{root.name}-backup-before-game-{datetime.now():%Y%m%d-%H%M%S}'
    backup_root.mkdir(parents=True, exist_ok=False)
    for name in paths_to_backup:
        src = root / name
        if src.exists():
            dest = backup_root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    if changed or added or existing_icon is None:
        try:
            for name in changed:
                (root / name).write_text(updated[name], encoding='utf-8')
            if existing_icon is None:
                target_icon.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(bundle / RELEASE['image'], target_icon)
            subprocess.run([sys.executable, str(root / 'build.py')], cwd=root, check=True)
        except Exception:
            for name in changed:
                (root / name).write_text(originals[name], encoding='utf-8')
            for name in generated:
                path = root / name
                data = original_bytes[name]
                if data is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(data)
            if existing_icon is None:
                target_icon.unlink(missing_ok=True)
            else:
                target_icon.write_bytes(existing_icon)
            print('Update failed; original files restored. Check the error above.', file=sys.stderr)
            raise
    else:
        print('Day 010 and Game category already configured; no changes needed.')
    print('Updated:', ', '.join(changed) if changed else 'no source edits needed')
    print('Generated: index.html, feed.xml, sitemap.xml')
    print('Day 009: Stepcells → Game; Day 010: Pair Where? → Game')
    print('Backup (outside repo):', backup_root)
    print('Review git diff, test locally, then commit and push when ready.')


if __name__ == '__main__':
    main()
