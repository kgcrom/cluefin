from __future__ import annotations

import json
from typing import Any

from bs4 import BeautifulSoup

from cluefin_etf.providers._parsing import normalize_space


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
