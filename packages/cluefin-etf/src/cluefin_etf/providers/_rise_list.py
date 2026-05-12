from __future__ import annotations

import json
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pydantic import ValidationError

from cluefin_etf._models import EtfSummary, ProviderName
from cluefin_etf.providers._parsing import compact_raw, normalize_space, parse_int_text
from cluefin_etf.providers._rise_models import RiseEtfListItem


def parse_rise_list_html(html: str, provider: ProviderName) -> list[EtfSummary]:
    soup = BeautifulSoup(html, "html.parser")
    return [summary for row in soup.select('[data-class="dataList"]') if (summary := rise_to_summary(row, provider))]


def rise_list_total_count(html: str) -> int | None:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one('[data-class="more"]')
    return _total_count_from_node(node)


def rise_to_summary(row, provider: ProviderName) -> EtfSummary | None:
    link = row.select_one('a[href*="/prod/finderDetail/"]')
    name = normalize_space(link.get_text(" ", strip=True) if link else "")
    code = _code_from_row(row)
    if link is None or not name or not code:
        return None

    href = str(link.get("href") or "")
    try:
        item = RiseEtfListItem(
            code=code,
            name=name,
            category=_row_category(row),
            listing_date=_cell_text(row.find_all("td", recursive=False), 8),
            nav=_cell_text(row.find_all("td", recursive=False), 0),
            expense_ratio=_cell_text(row.find_all("td", recursive=False), 1),
            detail_url=urljoin("https://www.riseetf.co.kr", href),
            raw=compact_raw(
                {
                    "productId": _product_id_from_href(href),
                    "tags": _row_tags(row),
                    "returns": _row_returns(row),
                },
                ("productId", "tags", "returns"),
            ),
        )
    except ValidationError:
        return None

    return EtfSummary(
        provider=provider,
        code=item.code,
        name=item.name,
        category=item.category,
        listing_date=item.listing_date,
        nav=item.nav,
        expense_ratio=item.expense_ratio,
        detail_url=item.detail_url,
        raw=item.raw,
    )


def _cell_text(cells, index: int) -> str | None:
    if index >= len(cells):
        return None
    return normalize_space(cells[index].get_text(" ", strip=True))


def _row_tags(row) -> list[str]:
    return [
        normalize_space(node.get_text(" ", strip=True))
        for node in row.select('[class^="tag_type"]')
        if normalize_space(node.get_text(" ", strip=True))
    ]


def _row_category(row) -> str | None:
    tags = [
        normalize_space(node.get_text(" ", strip=True))
        for node in row.select(".tag_type01, .tag_type02")
        if normalize_space(node.get_text(" ", strip=True))
    ]
    return " / ".join(tags) if tags else None


def _row_returns(row) -> dict[str, str | None]:
    labels = ("1개월", "3개월", "6개월", "1년", "3년", "상장이후")
    cells = row.find_all("td", recursive=False)
    returns: dict[str, str | None] = {}
    for label, cell in zip(labels, cells[2:8], strict=False):
        value = normalize_space(cell.get_text(" ", strip=True))
        value = value.replace(" 상승", "").replace(" 하락", "")
        returns[label] = None if value == "-" else value
    return returns


def _total_count_from_node(node) -> int | None:
    if node is None:
        return None
    value = node.get("data-value")
    if not isinstance(value, str):
        return None
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return parse_int_text(payload.get("totalCount"))


def _code_from_row(row) -> str | None:
    node = row.select_one(".code")
    match = re.search(r"\((?P<code>[^)]+)\)", normalize_space(node.get_text(" ", strip=True) if node else ""))
    return match.group("code").strip() if match else None


def _product_id_from_href(href: str) -> str | None:
    match = re.search(r"/prod/finderDetail/(?P<product_id>[^/?#]+)", href)
    return match.group("product_id") if match else None
