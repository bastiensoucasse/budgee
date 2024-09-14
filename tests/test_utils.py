"""Tests for the utility functions."""

import pytest

from budgee.utils import slugify


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("This is a test ---", "this-is-a-test"),
        ("影師嗎", "ying-shi-ma"),
        ("C'est déjà l'été.", "c-est-deja-l-ete"),
        ("Nín hǎo. Wǒ shì zhōng guó rén", "nin-hao-wo-shi-zhong-guo-ren"),
        ("---", ""),
        ("   ", ""),
        ("", ""),
    ],
)
def test_slugify_handles_various_inputs(text: str, expected: str) -> None:
    assert slugify(text) == expected
