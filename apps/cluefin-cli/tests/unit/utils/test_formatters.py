from __future__ import annotations

import pytest

from cluefin_cli.utils.formatters import format_currency, format_number


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1000, "1,000"),
        (1000000, "1,000,000"),
        ("1000000", "1,000,000"),
        ("1,234,567", "1,234,567"),
        (1234.56, "1,234.56"),
        (1234.0, "1,234"),
        ("1234.50", "1,234.50"),
        ("", "0"),
        ("  5000  ", "5,000"),
    ],
)
def test_format_number(value, expected) -> None:
    assert format_number(value) == expected


def test_format_number_returns_string_on_invalid() -> None:
    assert format_number("not-a-number") == "not-a-number"
    assert format_number(None) == "None"


def test_format_currency_with_and_without_unit() -> None:
    assert format_currency(1000000) == "₩ 1,000,000"
    assert format_currency(1000000, "천원") == "₩ 1,000,000천원"


def test_format_currency_falls_back_on_unformattable() -> None:
    assert format_currency("xyz") == "₩ xyz"
    assert format_currency("xyz", "원") == "₩ xyz원"
