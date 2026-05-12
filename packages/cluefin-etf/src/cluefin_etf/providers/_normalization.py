from __future__ import annotations

from decimal import Decimal

from cluefin_etf.providers._parsing import normalize_space, parse_decimal_text


def blank_to_none(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, str):
        normalized = normalize_space(value)
        return None if normalized in {"", "-"} else normalized
    return value


def parse_display_decimal(value: object) -> Decimal | None:
    value = blank_to_none(value)
    if value is None or isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        value = value.replace(" 상승", "").replace(" 하락", "").removeprefix("연 ")
    return parse_decimal_text(value)


def return_text(value: object) -> str | None:
    value = blank_to_none(value)
    if value is None:
        return None
    return normalize_space(str(value)).replace(" 상승", "").replace(" 하락", "")
