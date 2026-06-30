from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfSummary, ProviderName
from cluefin_etf.providers._sol_models import SolEtfListItem


def parse_sol_list_items(html: str) -> list[SolEtfListItem]:
    soup = BeautifulSoup(html, "html.parser")
    items: list[SolEtfListItem] = []
    for row in soup.select("table.fd-list tbody tr[id^='tr_']"):
        item = _parse_sol_row(row)
        if item is not None:
            items.append(item)
    return items


def sol_to_summary(item: SolEtfListItem, provider: ProviderName) -> EtfSummary:
    category_badges = [badge for badge in item.badges if badge not in item.pension_flags]
    return EtfSummary(
        provider=provider,
        code=item.etf_code,
        name=item.name,
        category=" / ".join(category_badges) if category_badges else None,
        nav=item.nav,
        aum=item.aum,
        detail_url=item.detail_url,
        raw=item.raw,
    )


def _parse_sol_row(row) -> SolEtfListItem | None:
    link = row.select_one("a.fd-link[href]")
    name_node = row.select_one(".fd-name")
    if link is None or name_node is None:
        return None

    href = link.get("href", "")
    fund_code = _fund_code_from_href(href) or _fund_code_from_row_id(row.get("id", ""))
    name, etf_code = parse_sol_name_and_code(name_node.get_text(" ", strip=True))
    if not fund_code or not name or not etf_code:
        return None

    cells = row.find_all("td", recursive=False)
    badges = [badge.get_text(" ", strip=True) for badge in row.select(".i-bdg-g .i-bdg")]
    pension_flags = [badge for badge in badges if badge in {"개인연금", "퇴직연금"}]
    returns = _parse_return_cells(cells)
    return SolEtfListItem(
        fund_code=fund_code,
        etf_code=etf_code,
        name=name,
        badges=badges,
        pension_flags=pension_flags,
        nav=_parse_decimal_cell(cells, 1),
        aum=_parse_decimal_cell(cells, 2),
        detail_url=urljoin("https://www.soletf.com", href),
        returns=returns,
        raw={
            "fundCode": fund_code,
            "etfCode": etf_code,
            "badges": badges,
            "pensionFlags": pension_flags,
            "returns": returns,
        },
    )


def parse_sol_name_and_code(value: str) -> tuple[str | None, str | None]:
    match = re.search(r"^(?P<name>.+?)\s*\((?P<code>[^)]+)\)\s*$", " ".join(value.split()))
    if match is None:
        return None, None
    return match.group("name").strip(), match.group("code").strip()


def _fund_code_from_href(href: str) -> str | None:
    match = re.search(r"/ko/fund/etf/(?P<fund_code>[^/?#]+)", href)
    return match.group("fund_code") if match else None


def _fund_code_from_row_id(row_id: str) -> str | None:
    if row_id.startswith("tr_"):
        return row_id.removeprefix("tr_")
    return None


def _parse_decimal_cell(cells: list, index: int) -> Decimal | None:
    if index >= len(cells):
        return None
    return parse_sol_decimal_text(cells[index].get_text(" ", strip=True))


def parse_sol_decimal_text(value: str) -> Decimal | None:
    normalized = value.replace(",", "").strip()
    if not normalized or normalized == "-":
        return None
    try:
        return Decimal(normalized)
    except InvalidOperation:
        return None


def _parse_return_cells(cells: list) -> dict[str, str | None]:
    labels = ["week_1", "month_1", "month_3", "month_6", "ytd", "year_1", "year_3", "year_5", "since_listing"]
    values: dict[str, str | None] = {}
    for offset, label in enumerate(labels, start=3):
        if offset >= len(cells):
            values[label] = None
            continue
        text = cells[offset].get_text(" ", strip=True)
        values[label] = text or None
    return values
