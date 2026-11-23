#!/usr/bin/env python3
"""Import a Buildiful 365 Card Builder release ZIP into this homepage repository.

Python 3.7+; no Python dependencies. Imports locally by default.
The explicit --publish option can commit and push to GitHub after confirmation.
    python3 import_release.py /path/to/Buildiful-365-Release-007-your-tool.zip --dry-run
    python3 import_release.py /path/to/Buildiful-365-Release-007-your-tool.zip
    python3 import_release.py /path/to/Buildiful-365-Release-007-your-tool.zip --publish
"""
import argparse
import datetime
import json
import re
import struct
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile, BadZipFile

from category_utils import normalize_category

ROOT = Path(__file__).resolve().parent
SCHEMA = 'buildiful365-release-pack/v1'
KINDS = {'book', 'card', 'gif', 'font', 'music'}
MAX_PACKAGE = 75 * 1024 * 1024
MAX_ICON = 12 * 1024 * 1024


class ReleaseError(ValueError):
    """An invalid or conflicting release pack."""


def validate_release(obj):
    if not isinstance(obj, dict) or obj.get('schema') != SCHEMA:
        raise ReleaseError('Not a supported Buildiful 365 release pack (schema v1 required).')
    release = obj.get('release')
    if not isinstance(release, dict):
        raise ReleaseError('Missing release metadata.')
    day = release.get('day')
    if type(day) is not int or not (1 <= day <= 365):
        raise ReleaseError('Release day must be between 1 and 365.')
    slug = release.get('slug')
    if not isinstance(slug, str) or len(slug) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ReleaseError('Invalid release URL slug.')
    image = 'assets/tools/{:03d}_{}.png'.format(day, slug)
    if release.get('image') != image or not isinstance(obj.get('assets'), dict) or obj['assets'].get('icon') != image:
        raise ReleaseError('Expected canonical icon path {}.'.format(image))
    for key, size in (('name', 85), ('desc', 320), ('cardDescription', 180)):
        value = release.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > size or any(ord(c) < 32 for c in value):
            raise ReleaseError('Missing, invalid, or oversized {}.'.format(key))
    date = release.get('date')
    if not isinstance(date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        raise ReleaseError('Date must be YYYY-MM-DD.')
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ReleaseError('Release date is not a real calendar date.')
    try:
        category = normalize_category(release.get('category'))
    except ValueError as exc:
        raise ReleaseError(str(exc))
    if release.get('kind') not in KINDS:
        raise ReleaseError('Invalid homepage card tint (kind).')
    tags = release.get('tags')
    if not isinstance(tags, list) or len(tags) > 20 or any(not isinstance(t, str) or not t.strip() or len(t) > 40 for t in tags):
        raise ReleaseError('Invalid search tags.')
    return {
        'day': day,
        'date': date,
        'name': release['name'].strip(),
        'slug': slug,
        'category': category,
        'kind': release['kind'],
        'image': image,
        'desc': release['desc'].strip(),
        'tags': tags,
    }


def read_package(path):
    if not path.is_file() or path.stat().st_size > MAX_PACKAGE:
        raise ReleaseError('ZIP missing or exceeds 75 MB.')
    try:
        with ZipFile(str(path)) as package:
            names = package.namelist()
            if len(names) != len(set(names)):
                raise ReleaseError('Archive has duplicate entry names.')
            if 'release.json' not in names:
                raise ReleaseError('Archive does not contain release.json.')
            if package.getinfo('release.json').file_size > 65536:
                raise ReleaseError('Release metadata is too large.')
            try:
                manifest = json.loads(package.read('release.json').decode('utf-8'))
            except (UnicodeError, ValueError):
                raise ReleaseError('Invalid release.json.')
            release = validate_release(manifest)
            icon_path = release['image']
            if icon_path not in names or package.getinfo(icon_path).file_size > MAX_ICON:
                raise ReleaseError('Required PNG icon is missing or too large.')
            icon = package.read(icon_path)
    except (BadZipFile, EOFError) as exc:
        raise ReleaseError('Invalid ZIP archive: {}'.format(exc))
    if len(icon) < 33 or not icon.startswith(b'\x89PNG\r\n\x1a\n') or icon[12:16] != b'IHDR':
        raise ReleaseError('Icon is not a valid PNG image.')
    width, height = struct.unpack('>II', icon[16:24])
    if (width, height) != (1024, 1024):
        raise ReleaseError('Icon must be 1024 x 1024 pixels; got {} x {}.'.format(width, height))
    return release, icon


def import_release(package_path, dry_run=False):
    release, icon = read_package(package_path)
    catalog_path = ROOT / 'tools.json'
    generator = ROOT / 'build.py'
    if not catalog_path.exists() or not generator.exists():
        raise ReleaseError('Run the importer from the actual homepage repository (requires tools.json and build.py).')
    original_catalog = catalog_path.read_bytes()
    try:
        catalog = json.loads(original_catalog.decode('utf-8'))
    except (UnicodeError, ValueError):
        raise ReleaseError('Existing tools.json is invalid.')
    if not isinstance(catalog, list):
        raise ReleaseError('Existing tools.json must be a list.')
    # Reuse a previously published spelling when a category is typed with
    # different capitalization in the Builder (e.g. "explore" vs "Explore").
    existing_categories = {
        normalize_category(tool.get('category')).casefold(): normalize_category(tool.get('category'))
        for tool in catalog
    }
    release['category'] = existing_categories.get(release['category'].casefold(), release['category'])
    if any(tool.get('day') == release['day'] for tool in catalog):
        raise ReleaseError('Day {:03d} is already present; no existing release will be changed.'.format(release['day']))
    if any(tool.get('slug') == release['slug'] for tool in catalog):
        raise ReleaseError('Slug {} is already present.'.format(release['slug']))
    target = ROOT / release['image']
    if target.exists():
        raise ReleaseError('Icon {} already exists; will not overwrite it.'.format(release['image']))
    if target.parent.resolve() != (ROOT / 'assets' / 'tools').resolve():
        raise ReleaseError('Unsafe icon location.')
    print('Release: Day {:03d} | {} | {}'.format(release['day'], release['name'], release['date']))
    print('Icon: {} ({} bytes)'.format(release['image'], len(icon)))
    print('Homepage: https://buildiful.github.io/{}/'.format(release['slug']))
    if dry_run:
        print('Dry run complete. No files changed.')
        return release
    catalog.append(release)
    output = (json.dumps(catalog, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    generated = ['index.html', 'feed.xml', 'sitemap.xml']
    prior_generated = {name: (ROOT / name).read_bytes() if (ROOT / name).exists() else None for name in generated}
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(icon)
        catalog_path.write_bytes(output)
        subprocess.run([sys.executable, str(generator)], cwd=str(ROOT), check=True)
    except Exception:
        catalog_path.write_bytes(original_catalog)
        if target.exists():
            target.unlink()
        for name, data in prior_generated.items():
            path = ROOT / name
            if data is None:
                if path.exists():
                    path.unlink()
            else:
                path.write_bytes(data)
        raise
    print('Imported successfully. Updated tools.json, index.html, feed.xml, sitemap.xml.')
    print('No public social images copied. Review locally before committing and pushing.')
    return release




def git_output(*args):
    result = subprocess.run(['git', *args], cwd=str(ROOT), check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
    return result.stdout.strip()


def check_publish_repo(package_path):
    """Require a clean, recognized homepage checkout before an optional Git push."""
    remote = git_output('remote', 'get-url', 'origin')
    if not re.search(r'(?:[:/])Buildiful/buildiful\.github\.io(?:\.git)?$', remote, re.I):
        raise ReleaseError('Refusing to publish: origin is not Buildiful/buildiful.github.io.')
    branch = git_output('rev-parse', '--abbrev-ref', 'HEAD')
    if branch not in ('master', 'main'):
        raise ReleaseError('Refusing to publish from branch {} (expected master or main).'.format(branch))
    dirty = git_output('status', '--porcelain', '--untracked-files=all')
    # A user may copy the ZIP into the checkout; it will not be added to Git.
    if dirty:
        allowed = set()
        try:
            rel = package_path.resolve().relative_to(ROOT.resolve())
            allowed.add(str(rel))
        except ValueError:
            pass
        others = []
        for line in dirty.splitlines():
            path = line[3:].strip().strip('"')
            if path not in allowed:
                others.append(line)
        if others:
            raise ReleaseError('The homepage checkout contains other changes. Commit or stash these first:\n  ' + '\n  '.join(others[:10]))
    return branch


def publish_release(release, branch):
    """Stage only importer-owned outputs and request approval before committing/pushing."""
    print('\nReady to publish Day {:03d}: {}.'.format(release['day'], release['name']))
    print('This will commit and push the generated homepage files to origin/{}.'.format(branch))
    if not sys.stdin.isatty():
        print('Non-interactive shell: changes imported locally, but no push attempted.')
        return
    answer = input('Commit and push this homepage update now? [y/N] ').strip().lower()
    if answer not in ('y', 'yes'):
        print('No push performed. Files remain changed locally for review.')
        return
    owned = ['tools.json', 'index.html', 'feed.xml', 'sitemap.xml', release['image']]
    subprocess.run(['git', 'add', '--', *owned], cwd=str(ROOT), check=True)
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=str(ROOT), check=True)
    message = 'Add Buildiful 365 Day {:03d}: {}'.format(release['day'], release['name'])
    subprocess.run(['git', 'commit', '-m', message], cwd=str(ROOT), check=True)
    subprocess.run(['git', 'push', 'origin', branch], cwd=str(ROOT), check=True)
    print('Published Day {:03d} to origin/{}.'.format(release['day'], branch))

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('release_zip', type=Path, help='ZIP exported from the internal Card Builder')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='Validate and preview without modifying files')
    mode.add_argument('--publish', action='store_true', help='Import, rebuild, and ask before committing/pushing to GitHub')
    args = parser.parse_args()
    try:
        package = args.release_zip.expanduser()
        branch = check_publish_repo(package) if args.publish else None
        release = import_release(package, args.dry_run)
        if args.publish:
            publish_release(release, branch)
    except (ReleaseError, OSError, subprocess.CalledProcessError) as exc:
        print('Error: {}'.format(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
