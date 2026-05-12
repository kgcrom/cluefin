from __future__ import annotations

from urllib.parse import urlencode

from bs4 import BeautifulSoup
from pydantic import ValidationError

from cluefin_etf._models import EtfSummary, ProviderName
from cluefin_etf.providers._parsing import normalize_space
from cluefin_etf.providers._tiger_models import TigerEtfListItem


def parse_tiger_list_html(html: str, provider: ProviderName, detail_url_base: str) -> list[EtfSummary]:
    soup = BeautifulSoup(html, "html.parser")
    items: list[EtfSummary] = []
    for row in soup.select(".c-data-row[data-ksd-fund]"):
        summary = tiger_to_summary(row, provider, detail_url_base)
        if summary is not None:
            items.append(summary)
    return items


def tiger_search_item(html: str) -> TigerEtfListItem | None:
    soup = BeautifulSoup(html, "html.parser")
    row = soup.select_one(".c-data-row[data-ksd-fund]")
    return tiger_list_item_from_row(row) if row is not None else None


def tiger_to_summary(row, provider: ProviderName, detail_url_base: str) -> EtfSummary | None:
    item = tiger_list_item_from_row(row)
    if item is None:
        return None

    return EtfSummary(
        provider=provider,
        code=item.code,
        isin=item.ksd_fund,
        name=item.name,
        category=item.category,
        listing_date=item.listing_date,
        nav=item.nav,
        aum=item.aum,
        detail_url=f"{detail_url_base}?{urlencode({'ksdFund': item.ksd_fund})}" if item.ksd_fund else None,
        raw={
            "ksdFund": item.ksd_fund,
            "categories": item.categories,
            "pensionFlags": item.pension_flags,
            "returns": item.returns,
            "totalCount": item.total_count,
        },
    )


def tiger_list_item_from_row(row) -> TigerEtfListItem | None:
    title = row.select_one(".title a")
    code_node = row.select_one(".code")
    name = normalize_space(title.get_text(" ", strip=True) if title else "")
    code = _code_from_text(code_node.get_text(" ", strip=True) if code_node else "")
    if not name or not code:
        return None

    categories = [
        normalize_space(node.get_text(" ", strip=True))
        for node in row.select(".category .each")
        if normalize_space(node.get_text(" ", strip=True))
    ]
    pension_flags = [item for item in categories if item.startswith("개인연금") or item.startswith("퇴직연금")]
    category = " / ".join(item for item in categories if item not in pension_flags)
    try:
        return TigerEtfListItem(
            code=code,
            name=name,
            ksd_fund=str(row.get("data-ksd-fund") or ""),
            category=category,
            categories=categories,
            pension_flags=pension_flags,
            listing_date=_pair_value(row, "상장일"),
            nav=_pair_value(row, "기준가"),
            aum=_pair_value(row, "순자산"),
            returns=_returns(row),
            total_count=row.get("data-tot-cnt"),
        )
    except ValidationError:
        return None


def _code_from_text(value: str) -> str | None:
    import re

    match = re.search(r"\((?P<code>[^)]+)\)", value)
    if match is None:
        return normalize_space(value) or None
    return match.group("code").strip()


def _pair_value(row, label: str) -> str | None:
    for pair in row.select(".c-pair"):
        key = pair.select_one(".key")
        value = pair.select_one(".value")
        if key is None or value is None:
            continue
        if label in normalize_space(key.get_text(" ", strip=True)):
            return normalize_space(value.get_text(" ", strip=True))
    return None


def _returns(row) -> dict[str, str | None]:
    returns: dict[str, str | None] = {}
    for item in row.select(".variations .each"):
        label_node = item.select_one(".lead")
        if label_node is None:
            continue
        label = normalize_space(label_node.get_text(" ", strip=True))
        returns[label] = _return_value(item)
    return returns


def _return_value(item) -> str | None:
    value_node = item.select_one(".val")
    if value_node is None:
        return None
    value = normalize_space(value_node.get_text(" ", strip=True))
    return None if value == "-" else value
