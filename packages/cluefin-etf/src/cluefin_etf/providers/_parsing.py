from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from bs4 import BeautifulSoup


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


def definition_value(soup: BeautifulSoup, label: str) -> str | None:
    for node in soup.find_all(["dt", "div"]):
        if label not in normalize_space(node.get_text(" ", strip=True)):
            continue

        if node.name == "dt":
            dd = node.find_next_sibling("dd")
            if dd is not None:
                return normalize_space(dd.get_text(" ", strip=True))

        classes = node.get("class", [])
        if "title" in classes or "c-card-header" in classes:
            sibling = node.find_next_sibling(["div", "p", "span"])
            if sibling is not None:
                return normalize_space(sibling.get_text(" ", strip=True))

            parent = node.parent
            if parent is not None:
                value = parent.select_one(".desc, .value, .c-card-content")
                if value is not None:
                    return normalize_space(value.get_text(" ", strip=True))

    return None


def json_ld_objects(html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    objects: list[dict[str, Any]] = []

    for script in soup.find_all("script", type="application/ld+json"):
        text = script.get_text(strip=True)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            objects.append(payload)
            graph = payload.get("@graph")
            if isinstance(graph, list):
                objects.extend(item for item in graph if isinstance(item, dict))

    return objects


def meta_content(soup: BeautifulSoup, *, name: str | None = None, property_: str | None = None) -> str | None:
    attrs: dict[str, str] = {}
    if name is not None:
        attrs["name"] = name
    if property_ is not None:
        attrs["property"] = property_
    node = soup.find("meta", attrs=attrs)
    if node is None:
        return None
    content = node.get("content")
    return normalize_space(content) if isinstance(content, str) else None
