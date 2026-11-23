"""Shared homepage category validation and display order.

A category is a user-defined, human-readable label rather than a fixed enum.
This module is used by both the importer and the static-site generator.
"""

BASE_CATEGORIES = ('Create', 'Publish', 'Enjoy', 'Game')
MAX_CATEGORY_LENGTH = 40
_ALLOWED_PUNCTUATION = " &/+-'().,"
_BASE_BY_CASE = {c.casefold(): c for c in BASE_CATEGORIES}


def normalize_category(value):
    """Validate a short category label; canonicalize the established names."""
    if not isinstance(value, str):
        raise ValueError('Category must be a text label.')
    label = value.strip()
    if (not label or len(label) > MAX_CATEGORY_LENGTH or
            not label[0].isalnum() or not label.isprintable() or
            label.casefold() == 'all' or
            '  ' in label or
            not any(character.isalpha() for character in label) or
            not all(character.isalnum() or character in _ALLOWED_PUNCTUATION for character in label)):
        raise ValueError('Invalid category: use a short name (up to 40 characters), such as Game or Explore.')
    return _BASE_BY_CASE.get(label.casefold(), label)


def ordered_categories(categories):
    """Known categories first, followed by any custom categories alphabetically."""
    found = {}
    for category in categories:
        label = normalize_category(category)
        found.setdefault(label.casefold(), label)
    known = [label for label in BASE_CATEGORIES if label.casefold() in found]
    custom = sorted((name for key, name in found.items() if key not in _BASE_BY_CASE), key=str.casefold)
    return known + custom
