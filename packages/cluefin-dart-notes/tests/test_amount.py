from decimal import Decimal

import pytest

from cluefin_dart_notes import parse_amount


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("23,593,369", Decimal("23593369")),
        ("(23,593,369)", Decimal("-23593369")),
        ("△1,234", Decimal("-1234")),
        ("▲ 1,234", Decimal("-1234")),
        ("-1,234", Decimal("-1234")),
        ("−7", Decimal("-7")),
        ("0", Decimal("0")),
        (" 12.50 ", Decimal("12.50")),
        ("( 1,000 )", Decimal("-1000")),
    ],
)
def test_amounts(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize(
    "text", ["", "-", " - ", "(1,234", "1,234)", "12.5%", "1,23", "보통주", "2026.06.30", "1,234 (*1)"]
)
def test_non_amounts(text):
    assert parse_amount(text) is None
