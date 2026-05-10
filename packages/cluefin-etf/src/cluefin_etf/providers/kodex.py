from __future__ import annotations

import json
import re
from datetime import date
from decimal import Decimal
from math import ceil
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, TypeAdapter, field_validator

from cluefin_etf._errors import FetchError
from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._parsing import (
    compact_raw,
    json_ld_objects,
    meta_content,
    normalize_space,
    parse_compact_date,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
)


class KodexEtfListItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    fNm: str
    stkTicker: str
    fId: str | None = None
    typeLnm: str | None = None
    typeNm: str | None = None
    listD: str | None = None
    gijunYMD: str | None = None
    basp: Decimal | None = None
    nav: Decimal | None = None
    curp: Decimal | None = None
    risep: Decimal | None = None
    risepRt: Decimal | None = None
    basrp: Decimal | None = None
    basrpRt: Decimal | None = None
    yieldWeek: Decimal | None = None
    yieldMon1: Decimal | None = None
    yieldMon3: Decimal | None = None
    yieldMon6: Decimal | None = None
    yieldYear1: Decimal | None = None
    yieldYear3: Decimal | None = None
    yieldYear: Decimal | None = None
    yieldList: Decimal | None = None
    dcYn: str | None = None
    irpYn: str | None = None
    totalCnt: int | None = None

    @field_validator(
        "basp",
        "nav",
        "curp",
        "risep",
        "risepRt",
        "basrp",
        "basrpRt",
        "yieldWeek",
        "yieldMon1",
        "yieldMon3",
        "yieldMon6",
        "yieldYear1",
        "yieldYear3",
        "yieldYear",
        "yieldList",
        mode="before",
    )
    @classmethod
    def _empty_decimal_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value


_KODEX_LIST_ADAPTER = TypeAdapter(list[KodexEtfListItem])


class KodexProvider(EtfProvider):
    list_url = "https://www.samsungfund.com/api/v1/kodex/product.do"
    detail_url_template = "https://www.samsungfund.com/etf/product/view.do?id={code}"
    detail_url_base = "https://www.samsungfund.com/etf/product/view.do"
    product_url_base = "https://www.samsungfund.com/api/v1/kodex/product"
    holdings_url_base = "https://www.samsungfund.com/api/v1/kodex/product-pdf"
    list_headers = {
        "Accept": "application/json",
    }

    info = ProviderInfo(
        name=ProviderName.KODEX,
        display_name="KODEX",
        homepage_url="https://www.samsungfund.com/etf/main.do",
    )

    def fetch_list(self) -> list[EtfSummary]:
        page_no = 1
        total_pages: int | None = None
        summaries: list[EtfSummary] = []

        while total_pages is None or page_no <= total_pages:
            result = self.fetcher.fetch(
                self._list_url(page_no),
                provider=self.name,
                validator=self.validate_list_result,
                headers=self.list_headers,
            )
            items = self._parse_list_response(result.html)
            if not items:
                break

            if total_pages is None:
                total_pages = self._total_pages(items)

            summaries.extend(self._to_summary(item) for item in items)
            page_no += 1

        return summaries

    def fetch_detail(self, code: str) -> EtfDetail:
        fund_id = self._resolve_detail_fund_id(code)
        url = f"{self.detail_url_base}?id={fund_id}"
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        detail = self.parse_detail_html(code, result.html)
        try:
            holdings_url, holdings = self._fetch_pdf_holdings(fund_id, referrer=url)
        except FetchError:
            rendered_result = self.fetcher.fetch(
                url, provider=self.name, validator=self.validate_rendered_holdings_result
            )
            holdings_url = f"{url}#pdf"
            holdings = self.parse_holdings_html(rendered_result.html)
        return detail.model_copy(
            update={
                "holdings_url": holdings_url,
                "holdings": holdings,
            }
        )

    def validate_list_result(self, result: FetchResult) -> bool:
        try:
            items = self._parse_list_response(result.html)
        except (json.JSONDecodeError, ValueError):
            return False
        return all(item.stkTicker and item.fNm for item in items)

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return [self._to_summary(item) for item in self._parse_list_response(html)]

    def validate_detail_result(self, result: FetchResult) -> bool:
        detail = self.parse_detail_html("", result.html)
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        soup = BeautifulSoup(html, "html.parser")
        investment_fund = _find_investment_fund_json_ld(html)
        description = meta_content(soup, name="description") or meta_content(soup, property_="og:description")
        title = meta_content(soup, property_="og:title")
        name = _strip_kodex_title(investment_fund.get("name") or title)
        benchmark = _benchmark_from_description(description)
        fees = investment_fund.get("feesAndCommissionsSpecification")

        return EtfDetail(
            provider=self.name,
            code=str(investment_fund.get("tickerSymbol") or investment_fund.get("identifier") or code),
            name=name,
            category=_category_from_description(description),
            benchmark=benchmark,
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

    def validate_product_result(self, result: FetchResult) -> bool:
        try:
            return bool(self._parse_product_pdf_gijun_ymd(result.html))
        except (json.JSONDecodeError, ValueError):
            return False

    def validate_holdings_result(self, result: FetchResult) -> bool:
        try:
            payload = json.loads(result.html)
        except json.JSONDecodeError:
            return False
        pdf = payload.get("pdf")
        return isinstance(pdf, dict) and isinstance(pdf.get("list"), list)

    def validate_rendered_holdings_result(self, result: FetchResult) -> bool:
        return bool(_rendered_holdings_table(BeautifulSoup(result.html, "html.parser")))

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        payload = json.loads(html)
        pdf = payload.get("pdf") if isinstance(payload.get("pdf"), dict) else {}
        items = pdf.get("list") if isinstance(pdf, dict) else None
        if not isinstance(items, list):
            return []
        as_of_date = parse_compact_date(pdf.get("gijunYMD")) if isinstance(pdf, dict) else None
        return [
            _holding_from_pdf_item(index, item, as_of_date=as_of_date)
            for index, item in enumerate(items, start=1)
            if isinstance(item, dict)
        ]

    def parse_holdings_html(self, html: str) -> list[EtfHolding]:
        soup = BeautifulSoup(html, "html.parser")
        table = _rendered_holdings_table(soup)
        if table is None:
            return []

        as_of_date = _rendered_pdf_date(soup)
        holdings: list[EtfHolding] = []
        for index, row in enumerate(table.select("tbody tr"), start=1):
            cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
            if len(cells) < 5:
                continue
            holdings.append(
                EtfHolding(
                    rank=index,
                    name=cells[0] or None,
                    code=cells[1] or None,
                    weight=parse_decimal_text(cells[2]),
                    quantity=parse_decimal_text(cells[3]),
                    valuation_amount=parse_decimal_text(cells[4]),
                    as_of_date=as_of_date,
                    raw=compact_raw(
                        {
                            "secNm": cells[0],
                            "itmNo": cells[1],
                            "ratio": cells[2],
                            "applyQ": cells[3],
                            "evalA": cells[4],
                        },
                        ("itmNo", "secNm", "applyQ", "evalA", "ratio"),
                    ),
                )
            )
        return holdings

    def _fetch_pdf_holdings(self, fund_id: str, *, referrer: str) -> tuple[str, list[EtfHolding]]:
        product_result = self.fetcher.fetch(
            f"{self.product_url_base}/{fund_id}.do",
            provider=self.name,
            validator=self.validate_product_result,
            headers=self.list_headers,
            referrer=referrer,
        )
        gijun_ymd = self._parse_product_pdf_gijun_ymd(product_result.html)
        holdings_url = f"{self.holdings_url_base}/{fund_id}.do?gijunYMD={gijun_ymd}"
        holdings_result = self.fetcher.fetch(
            holdings_url,
            provider=self.name,
            validator=self.validate_holdings_result,
            headers=self.list_headers,
            referrer=referrer,
        )
        actual_gijun_ymd = self._parse_holdings_pdf_gijun_ymd(holdings_result.html)
        actual_holdings_url = f"{self.holdings_url_base}/{fund_id}.do?gijunYMD={actual_gijun_ymd}"
        return actual_holdings_url, self.parse_holdings_json(holdings_result.html)

    def _parse_list_response(self, html: str) -> list[KodexEtfListItem]:
        return _KODEX_LIST_ADAPTER.validate_json(html)

    def _parse_product_pdf_gijun_ymd(self, html: str) -> str:
        payload = json.loads(html)
        pdf = payload.get("pdf")
        if not isinstance(pdf, dict):
            raise ValueError("KODEX PDF 정보가 없습니다")
        value = pdf.get("gijunYMD")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("KODEX PDF 기준일이 없습니다")
        return value.strip().replace(".", "")

    def _parse_holdings_pdf_gijun_ymd(self, html: str) -> str:
        payload = json.loads(html)
        pdf = payload.get("pdf")
        if not isinstance(pdf, dict):
            raise ValueError("KODEX 구성종목 PDF 정보가 없습니다")
        value = pdf.get("gijunYMD")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("KODEX 구성종목 PDF 기준일이 없습니다")
        return value.strip().replace(".", "")

    def _to_summary(self, item: KodexEtfListItem) -> EtfSummary:
        return EtfSummary(
            provider=self.name,
            code=item.stkTicker,
            name=item.fNm,
            category=item.typeLnm or item.typeNm,
            listing_date=_parse_kodex_date(item.listD),
            nav=item.basp,
            aum=item.nav,
            as_of_date=_parse_kodex_date(item.gijunYMD),
            detail_url=f"{self.detail_url_base}?id={item.fId}" if item.fId else None,
            raw=item.model_dump(mode="json"),
        )

    def _list_url(self, page_no: int) -> str:
        query = urlencode(
            {
                "srchTerm": "w",
                "ordrSort": "DESC",
                "ordrColm": "YIELD_WEEK",
                "pageNo": str(page_no),
            }
        )
        return f"{self.list_url}?{query}"

    def _total_pages(self, items: list[KodexEtfListItem]) -> int:
        total_count = items[0].totalCnt
        if total_count is None:
            return 1
        return ceil(total_count / len(items))

    def _resolve_detail_fund_id(self, code: str) -> str:
        if code.upper().startswith("2ETF"):
            return code

        for summary in self.fetch_list():
            if summary.code == code and summary.raw.get("fId"):
                return str(summary.raw["fId"])

        return code


def _parse_kodex_date(value: str | None) -> date | None:
    if not value:
        return None
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))


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


def _rendered_holdings_table(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        headers = [normalize_space(node.get_text(" ", strip=True)) for node in table.find_all(["th", "td"])]
        if {"종목명", "종목코드", "비중(%)", "수량", "평가금액(원)"}.issubset(headers):
            return table
    return None


def _rendered_pdf_date(soup: BeautifulSoup) -> date | None:
    for node in soup.find_all("input"):
        value = node.get("value")
        if isinstance(value, str):
            parsed = parse_date_text(value)
            if parsed is not None:
                return parsed

    return parse_date_text(soup.get_text(" ", strip=True))


def _holding_from_pdf_item(index: int, item: dict[str, object], *, as_of_date: date | None) -> EtfHolding:
    return EtfHolding(
        rank=parse_int_text(item.get("rank")) or index,
        code=str(item.get("itmNo")) if item.get("itmNo") is not None else None,
        name=str(item.get("secNm")) if item.get("secNm") is not None else None,
        quantity=parse_decimal_text(str(item.get("applyQ"))) if item.get("applyQ") is not None else None,
        valuation_amount=parse_decimal_text(str(item.get("evalA"))) if item.get("evalA") is not None else None,
        weight=parse_decimal_text(str(item.get("ratio"))) if item.get("ratio") is not None else None,
        as_of_date=as_of_date,
        raw=compact_raw(item, ("rank", "itmNo", "secNm", "applyQ", "evalA", "ratio")),
    )
