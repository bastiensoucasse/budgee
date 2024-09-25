"""Utilities module."""

import re

from unidecode import unidecode


def slugify(text: str) -> str:
    """Slugifies (normalizes) the characters of a text string (useful for building identifiers).

    The original text is converted to a lowercased ASCII string.
    Then, all non-alpha-numerical characters are replaced by hyphens.
    Finally, the string is stripped to remove starting or trailing hyphens.

    Args:
        text: Text to slugify.

    Returns:
        slugified_text: Slugified version of the original text.
    """
    return re.sub(r"[^a-z0-9]+", "-", unidecode(text).lower()).strip("-")
