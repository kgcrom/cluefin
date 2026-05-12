from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_space(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def parse_decimal_text(value: str | None) -> Decimal | None:
    if not value:
        return None

    normalized = normalize_space(value)
    if not normalized or normalized == "-":
        return None

    match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?", normalized)
    if match is None:
        return None

    try:
        return Decimal(match.group(0).replace(",", ""))
    except InvalidOperation:
        return None


def parse_int_text(value: object) -> int | None:
    if value is None:
        return None

    decimal = parse_decimal_text(str(value))
    return int(decimal) if decimal is not None else None


def compact_raw(mapping: Mapping[str, Any], allowed_keys: Iterable[str]) -> dict[str, Any]:
    return {key: mapping[key] for key in allowed_keys if key in mapping and mapping[key] is not None}


def parse_korean_eok_amount(value: str | None) -> Decimal | None:
    if not value:
        return None

    normalized = normalize_space(value).replace(",", "")
    if "조" not in normalized:
        return parse_decimal_text(normalized)

    total = Decimal("0")
    jo_match = re.search(r"(?P<amount>\d+(?:\.\d+)?)\s*조", normalized)
    eok_match = re.search(r"(?P<amount>\d+(?:\.\d+)?)\s*억", normalized)
    if jo_match is not None:
        total += Decimal(jo_match.group("amount")) * Decimal("10000")
    if eok_match is not None:
        total += Decimal(eok_match.group("amount"))
    return total or None


def parse_date_text(value: str | None) -> date | None:
    if not value:
        return None

    match = re.search(r"(?P<year>\d{4})[.\-/년]\s*(?P<month>\d{1,2})[.\-/월]\s*(?P<day>\d{1,2})", value)
    if match is None:
        return None

    return date(int(match.group("year")), int(match.group("month")), int(match.group("day")))


def parse_compact_date(value: str | int | None) -> date | None:
    if value is None:
        return None
    text = str(value)
    if not re.fullmatch(r"\d{8}", text):
        return parse_date_text(text)
    return date(int(text[:4]), int(text[4:6]), int(text[6:8]))


from cluefin_etf.providers._html import definition_value, json_ld_objects, meta_content  # noqa: E402

__all__ = [
    "compact_raw",
    "definition_value",
    "json_ld_objects",
    "meta_content",
    "normalize_space",
    "parse_compact_date",
    "parse_date_text",
    "parse_decimal_text",
    "parse_int_text",
    "parse_korean_eok_amount",
]
