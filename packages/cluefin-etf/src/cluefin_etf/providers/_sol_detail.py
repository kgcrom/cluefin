from __future__ import annotations

import re

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, ProviderName
from cluefin_etf.providers._parsing import (
    definition_value,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
    parse_korean_eok_amount,
)
from cluefin_etf.providers._sol_list import parse_sol_name_and_code


def parse_sol_detail_html(code: str, html: str, provider: ProviderName, detail_url_base: str) -> EtfDetail:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one(".fv-name") or soup.find("h1")
    name, etf_code = parse_sol_name_and_code(normalize_space(title.get_text(" ", strip=True)) if title else "")
    badges = [normalize_space(node.get_text(" ", strip=True)) for node in soup.select(".i-bdg-g .i-bdg")]
    pension_flags = [badge for badge in badges if badge in {"개인연금", "퇴직연금"}]
    category_badges = [badge for badge in badges if badge not in pension_flags]

    return EtfDetail(
        provider=provider,
        code=etf_code or code,
        name=name,
        category=" / ".join(category_badges) if category_badges else None,
        benchmark=sol_base_index_name(soup),
        listing_date=parse_date_text(definition_value(soup, "상장일")),
        nav=sol_fund_head_decimal(soup, "기준가격"),
        aum=parse_korean_eok_amount(definition_value(soup, "순자산 총액")),
        expense_ratio=parse_decimal_text(definition_value(soup, "총보수")),
        detail_url=f"{detail_url_base}/{sol_fund_code_from_html(html) or code}",
        raw={
            "inputCode": code,
            "fundCode": sol_fund_code_from_html(html),
            "badges": badges,
            "pensionFlags": pension_flags,
        },
    )


def sol_fund_head_decimal(soup: BeautifulSoup, label: str):
    for node in soup.select(".fv-exp dl"):
        title = node.find("dt")
        if title is None or label not in normalize_space(title.get_text(" ", strip=True)):
            continue
        value = node.select_one(".fd-pri")
        if value is not None:
            return parse_decimal_text(value.get_text(" ", strip=True))
    return None


def sol_base_index_name(soup: BeautifulSoup) -> str | None:
    for container in soup.select(".cont-col"):
        title = container.select_one(".g-title, h3")
        if title is None or "기초지수정보" not in normalize_space(title.get_text(" ", strip=True)):
            continue
        node = container.select_one("dl.g-conts dt")
        return normalize_space(node.get_text(" ", strip=True)) if node else None
    return None


def sol_fund_code_from_html(html: str) -> str | None:
    for match in re.finditer(r"/ko/fund/etf/(?P<fund_code>[^/?#'\"]+)", html):
        fund_code = match.group("fund_code")
        if fund_code not in {"pds", "summary"}:
            return fund_code
    return None
