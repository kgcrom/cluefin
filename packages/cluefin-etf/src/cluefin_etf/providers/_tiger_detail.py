from __future__ import annotations

import re

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, ProviderName
from cluefin_etf.providers._parsing import (
    definition_value,
    meta_content,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
)
from cluefin_etf.providers._tiger_models import TigerEtfDetailData


def parse_tiger_detail_html(code: str, html: str, provider: ProviderName) -> EtfDetail:
    soup = BeautifulSoup(html, "html.parser")
    title_node = soup.select_one("#thisLead h1") or _first_product_title(soup)
    title_text = normalize_space(title_node.get_text(" ", strip=True) if title_node else "")
    name, ticker = _parse_title_and_code(title_text)
    categories = [
        normalize_space(node.get_text(" ", strip=True))
        for node in soup.select(".category span")
        if normalize_space(node.get_text(" ", strip=True))
    ]
    item = TigerEtfDetailData(
        code=ticker or code,
        name=name,
        category=_detail_category(categories),
        benchmark=definition_value(soup, "벤치마크") or definition_value(soup, "기초지수"),
        listing_date=definition_value(soup, "상장일"),
        nav=_summary_decimal(soup, "기준가격"),
        aum=_summary_decimal(soup, "순자산 규모") or definition_value(soup, "순자산총액"),
        expense_ratio=definition_value(soup, "총보수"),
        as_of_date=tiger_as_of_date(soup),
        detail_url=meta_content(soup, property_="og:url") or meta_content(soup, name="canonical"),
        raw={"inputCode": code, "ksdFund": ksd_fund_from_html(html), "categories": categories},
    )

    return EtfDetail(
        provider=provider,
        code=item.code,
        name=item.name,
        category=item.category,
        benchmark=item.benchmark,
        listing_date=item.listing_date,
        nav=item.nav,
        aum=item.aum,
        expense_ratio=item.expense_ratio,
        as_of_date=item.as_of_date,
        detail_url=item.detail_url,
        raw=item.raw,
    )


def _detail_category(categories: list[str]) -> str:
    return " / ".join(
        item for item in categories if not item.startswith("개인연금") and not item.startswith("퇴직연금")
    )


def _parse_title_and_code(value: str) -> tuple[str | None, str | None]:
    match = re.search(r"^(?P<name>.+?)\s*\((?P<code>[^)]+)\)", value)
    if match is None:
        return (value or None), None
    return match.group("name").strip(), match.group("code").strip()


def _first_product_title(soup: BeautifulSoup):
    for node in soup.find_all("h1"):
        if re.search(r"\([A-Z0-9]{6}\)", node.get_text(" ", strip=True)):
            return node
    return soup.find("h1")


def _summary_decimal(soup: BeautifulSoup, label: str):
    for node in soup.select(".lead-main .each, .summary .each, .summary > div"):
        title = node.select_one(".title, dt")
        if title is None or label not in normalize_space(title.get_text(" ", strip=True)):
            continue
        value = node.select_one(".amount, .desc, dd")
        if value is not None:
            return parse_decimal_text(value.get_text(" ", strip=True))
    return None


def ksd_fund_from_html(html: str) -> str | None:
    match = re.search(r"ksdFund=([A-Z0-9]+)", html)
    return match.group(1) if match else None


def tiger_as_of_date(soup: BeautifulSoup):
    text = soup.get_text(" ", strip=True)
    match = re.search(r"기준일\s*(?P<date>\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})", text)
    if match is not None:
        return parse_date_text(match.group("date"))
    match = re.search(r"(?P<date>\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})\s*기준", text)
    return parse_date_text(match.group("date")) if match else None


def tiger_pdf_date(html: str):
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("input[name='fixDate']")
    value = node.get("value") if node is not None else None
    return parse_date_text(value) if isinstance(value, str) else None
