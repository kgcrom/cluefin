from __future__ import annotations

import re
from datetime import date

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, ProviderName
from cluefin_etf.providers._parsing import definition_value, normalize_space, parse_date_text, parse_decimal_text


def parse_kiwoom_detail_html(code: str, html: str, provider: ProviderName, detail_url_base: str) -> EtfDetail:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one(".head-group h2, .fund-title h2, h2")
    code_text = (
        normalize_space(soup.select_one(".fund-code").get_text(" ", strip=True))
        if soup.select_one(".fund-code")
        else ""
    )
    parsed_code = _code_from_text(code_text) or code

    return EtfDetail(
        provider=provider,
        code=parsed_code,
        name=_direct_text(title) if title else None,
        category=_category_from_title_area(soup),
        benchmark=definition_value(soup, "기초지수"),
        listing_date=parse_date_text(definition_value(soup, "설정일(상장일)")),
        nav=_summary_decimal(soup, "기준가"),
        aum=_summary_decimal(soup, "순자산 규모"),
        expense_ratio=parse_decimal_text(definition_value(soup, "보수(연)")),
        as_of_date=parse_date_text(soup.select_one(".fund-info-wrap .note").get_text(" ", strip=True))
        if soup.select_one(".fund-info-wrap .note")
        else None,
        detail_url=f"{detail_url_base}?gcode={parsed_code}" if parsed_code else None,
        raw={"fundCodeText": code_text, "basicInfo": _basic_info(soup)},
    )


def compact_date(value: date | None) -> str | None:
    return value.strftime("%Y%m%d") if value else None


def pdf_date_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("#pdfDt, input[name='pdfDt']")
    value = node.get("value") if node is not None else None
    if not isinstance(value, str):
        return None
    return value.replace("-", "").replace(".", "") or None


def _summary_decimal(soup: BeautifulSoup, label: str):
    for node in soup.select("dl.summary > div"):
        title = node.find("dt")
        if title is None or label not in normalize_space(title.get_text(" ", strip=True)):
            continue
        value = node.find("dd")
        if value is not None:
            return parse_decimal_text(value.get_text(" ", strip=True))
    return None


def _code_from_text(value: str) -> str | None:
    match = re.search(r"종목코드\s*:\s*(?P<code>[A-Z0-9]+)", value)
    return match.group("code") if match else None


def _category_from_title_area(soup: BeautifulSoup) -> str | None:
    tags = [normalize_space(node.get_text(" ", strip=True)) for node in soup.select(".tag-wrap em")]
    if tags:
        return " / ".join(tags)

    fund_title = soup.select_one(".fund-title")
    if fund_title is None:
        return None
    title = fund_title.select_one("h2")
    if title is not None:
        title.extract()
    text = normalize_space(fund_title.get_text(" ", strip=True))
    return text or None


def _direct_text(node) -> str:
    return normalize_space(" ".join(str(child).strip() for child in node.children if isinstance(child, str)))


def _basic_info(soup: BeautifulSoup) -> dict[str, str]:
    values: dict[str, str] = {}
    for node in soup.select(".fund-detail-info dl > div"):
        key = node.find("dt")
        value = node.find("dd")
        if key is not None and value is not None:
            values[normalize_space(key.get_text(" ", strip=True))] = normalize_space(value.get_text(" ", strip=True))
    return values
