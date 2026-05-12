from __future__ import annotations

import re

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, ProviderName
from cluefin_etf.providers._parsing import compact_raw, json_ld_objects, meta_content, parse_decimal_text


def parse_kodex_detail_html(code: str, html: str, provider: ProviderName) -> EtfDetail:
    soup = BeautifulSoup(html, "html.parser")
    investment_fund = _find_investment_fund_json_ld(html)
    description = meta_content(soup, name="description") or meta_content(soup, property_="og:description")
    title = meta_content(soup, property_="og:title")
    fees = investment_fund.get("feesAndCommissionsSpecification")

    return EtfDetail(
        provider=provider,
        code=str(investment_fund.get("tickerSymbol") or investment_fund.get("identifier") or code),
        name=_strip_kodex_title(investment_fund.get("name") or title),
        category=_category_from_description(description),
        benchmark=_benchmark_from_description(description),
        expense_ratio=parse_decimal_text(fees if isinstance(fees, str) else None),
        detail_url=str(investment_fund.get("url") or meta_content(soup, property_="og:url") or ""),
        raw={
            "inputCode": code,
            "jsonLd": compact_raw(
                investment_fund,
                ("@type", "name", "tickerSymbol", "identifier", "url", "feesAndCommissionsSpecification"),
            ),
        },
    )


def _find_investment_fund_json_ld(html: str) -> dict[str, object]:
    for item in json_ld_objects(html):
        if item.get("@type") == "InvestmentFund":
            return item
    return {}


def _strip_kodex_title(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    return value.removesuffix(" ETF | Kodex").removesuffix(" ETF").strip() or None


def _category_from_description(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"는\s+(?P<category>[^이며]+형 ETF)", value)
    return match.group("category") if match else None


def _benchmark_from_description(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"기초지수는\s+(?P<benchmark>.+?)입니다", value)
    return match.group("benchmark") if match else None
