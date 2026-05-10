from __future__ import annotations

import re
from datetime import date
from decimal import Decimal
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._parsing import (
    compact_raw,
    definition_value,
    meta_content,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
)


class TigerEtfListItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    name: str
    ksd_fund: str | None = None
    category: str | None = None
    categories: list[str] = Field(default_factory=list)
    pension_flags: list[str] = Field(default_factory=list)
    listing_date: date | None = None
    nav: Decimal | None = None
    aum: Decimal | None = None
    returns: dict[str, str | None] = Field(default_factory=dict)
    total_count: int | None = None

    @field_validator("code", "name", mode="before")
    @classmethod
    def _required_text(cls, value: object) -> object:
        value = _blank_to_none(value)
        if isinstance(value, str):
            return normalize_space(value)
        return value

    @field_validator("ksd_fund", "category", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return _blank_to_none(value)

    @field_validator("listing_date", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, date):
            return value
        return parse_date_text(value)

    @field_validator("nav", "aum", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return _parse_display_decimal(value)

    @field_validator("total_count", mode="before")
    @classmethod
    def _parse_int(cls, value: object) -> object:
        return parse_int_text(_blank_to_none(value))

    @field_validator("returns", mode="before")
    @classmethod
    def _normalize_returns(cls, value: object) -> object:
        if not isinstance(value, dict):
            return value
        return {str(key): _return_text(item) for key, item in value.items()}


class TigerEtfDetailData(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    name: str
    category: str | None = None
    benchmark: str | None = None
    listing_date: date | None = None
    nav: Decimal | None = None
    aum: Decimal | None = None
    expense_ratio: Decimal | None = None
    as_of_date: date | None = None
    detail_url: str | None = None
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("code", "name", mode="before")
    @classmethod
    def _required_text(cls, value: object) -> object:
        value = _blank_to_none(value)
        if isinstance(value, str):
            return normalize_space(value)
        return value

    @field_validator("category", "benchmark", "detail_url", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return _blank_to_none(value)

    @field_validator("listing_date", "as_of_date", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, date):
            return value
        return parse_date_text(value)

    @field_validator("nav", "aum", "expense_ratio", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return _parse_display_decimal(value)


class TigerHoldingItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    rank: int | None = None
    code: str | None = None
    name: str | None = None
    quantity: Decimal | None = None
    valuation_amount: Decimal | None = None
    weight: Decimal | None = None
    as_of_date: date | None = None
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("rank", mode="before")
    @classmethod
    def _parse_int(cls, value: object) -> object:
        return parse_int_text(_blank_to_none(value))

    @field_validator("code", "name", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return _blank_to_none(value)

    @field_validator("quantity", "valuation_amount", "weight", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return _parse_display_decimal(value)


class TigerProvider(EtfProvider):
    detail_url_template = "https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund={code}"
    detail_url_base = "https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do"
    holdings_url_base = "https://investments.miraeasset.com/tigeretf/ko/product/search/detail"
    search_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/list.ajax"
    search_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }

    info = ProviderInfo(
        name=ProviderName.TIGER,
        display_name="TIGER",
        homepage_url="https://investments.miraeasset.com/magi/index.do",
    )

    def fetch_list(self) -> list[EtfSummary]:
        result = self.fetcher.fetch(
            self.search_url,
            provider=self.name,
            validator=self.validate_list_result,
            method="POST",
            headers=self.search_headers,
            data=self._list_request_data(),
        )
        return self.parse_list_html(result.html)

    def fetch_detail(self, code: str) -> EtfDetail:
        ksd_fund = code if code.startswith("KR") else self._resolve_ksd_fund(code)
        url = f"{self.detail_url_base}?{urlencode({'ksdFund': ksd_fund})}"
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        pdf_page_url = f"{self.holdings_url_base}/pdf.ajax"
        pdf_page = self.fetcher.fetch(
            pdf_page_url,
            provider=self.name,
            validator=self.validate_holdings_page_result,
            method="POST",
            headers=self.search_headers,
            data={"ksdFund": ksd_fund},
            referrer=url,
        )
        holdings_url = f"{self.holdings_url_base}/pdfListAjax.ajax"
        holdings_result = self.fetcher.fetch(
            holdings_url,
            provider=self.name,
            validator=self.validate_holdings_result,
            method="POST",
            headers=self.search_headers,
            data={
                "ksdFund": ksd_fund,
                "fixDate": "",
                "prfPrd": "",
                "order": "",
                "pageIndex": "1",
                "firstIndex": "0",
                "listCnt": "999",
            },
            referrer=url,
        )
        detail = self.parse_detail_html(code, result.html)
        return detail.model_copy(
            update={
                "holdings_url": holdings_url,
                "holdings": self.parse_holdings_html(holdings_result.html, as_of_date=_pdf_date(pdf_page.html)),
            }
        )

    def validate_list_result(self, result: FetchResult) -> bool:
        return bool(self.parse_list_html(result.html))

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        soup = BeautifulSoup(html, "html.parser")
        items: list[EtfSummary] = []
        for row in soup.select(".c-data-row[data-ksd-fund]"):
            summary = self._to_summary(row)
            if summary is not None:
                items.append(summary)
        return items

    def validate_detail_result(self, result: FetchResult) -> bool:
        try:
            detail = self.parse_detail_html("", result.html)
        except ValidationError:
            return False
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        soup = BeautifulSoup(html, "html.parser")
        title_node = soup.select_one("#thisLead h1") or _first_product_title(soup)
        title_text = normalize_space(title_node.get_text(" ", strip=True) if title_node else "")
        name, ticker = _parse_title_and_code(title_text)
        categories = [
            normalize_space(node.get_text(" ", strip=True))
            for node in soup.select(".category span")
            if normalize_space(node.get_text(" ", strip=True))
        ]
        category = " / ".join(
            item for item in categories if not item.startswith("개인연금") and not item.startswith("퇴직연금")
        )
        item = TigerEtfDetailData(
            code=ticker or code,
            name=name,
            category=category,
            benchmark=definition_value(soup, "벤치마크") or definition_value(soup, "기초지수"),
            listing_date=definition_value(soup, "상장일"),
            nav=_summary_decimal(soup, "기준가격"),
            aum=_summary_decimal(soup, "순자산 규모") or definition_value(soup, "순자산총액"),
            expense_ratio=definition_value(soup, "총보수"),
            as_of_date=_as_of_date(soup),
            detail_url=meta_content(soup, property_="og:url") or meta_content(soup, name="canonical"),
            raw={
                "inputCode": code,
                "ksdFund": _ksd_fund_from_html(html),
                "categories": categories,
            },
        )

        return EtfDetail(
            provider=self.name,
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

    def validate_holdings_page_result(self, result: FetchResult) -> bool:
        soup = BeautifulSoup(result.html, "html.parser")
        return soup.select_one("#formPdfList") is not None or soup.select_one("input[name='fixDate']") is not None

    def validate_holdings_result(self, result: FetchResult) -> bool:
        soup = BeautifulSoup(result.html, "html.parser")
        return soup.select_one("tr[data-tot-cnt]") is not None

    def parse_holdings_html(self, html: str, *, as_of_date=None) -> list[EtfHolding]:
        soup = BeautifulSoup(html, "html.parser")
        holdings: list[EtfHolding] = []
        for index, row in enumerate(soup.select("tr[data-tot-cnt]"), start=1):
            cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
            if len(cells) < 5:
                continue
            item = TigerHoldingItem(
                rank=index,
                code=cells[0],
                name=cells[1],
                quantity=cells[2],
                valuation_amount=cells[3],
                weight=cells[4],
                as_of_date=as_of_date,
                raw=compact_raw(
                    {
                        "code": cells[0],
                        "name": cells[1],
                        "quantity": cells[2],
                        "valuationAmount": cells[3],
                        "weight": cells[4],
                        "return": cells[5] if len(cells) > 5 else None,
                    },
                    ("code", "name", "quantity", "valuationAmount", "weight", "return"),
                ),
            )
            holdings.append(
                EtfHolding(
                    rank=item.rank,
                    code=item.code,
                    name=item.name,
                    quantity=item.quantity,
                    valuation_amount=item.valuation_amount,
                    weight=item.weight,
                    as_of_date=item.as_of_date,
                    raw=item.raw,
                )
            )
        return holdings

    def _resolve_ksd_fund(self, code: str) -> str:
        result = self.fetcher.fetch(
            self.search_url,
            provider=self.name,
            validator=self._validate_search_result,
            method="POST",
            headers=self.search_headers,
            data=self._search_request_data(code),
        )
        soup = BeautifulSoup(result.html, "html.parser")
        row = soup.select_one(".c-data-row[data-ksd-fund]")
        item = self._list_item_from_row(row) if row is not None else None
        if item is None:
            return code
        return item.ksd_fund or code

    def _validate_search_result(self, result: FetchResult) -> bool:
        soup = BeautifulSoup(result.html, "html.parser")
        row = soup.select_one(".c-data-row[data-ksd-fund]")
        return row is not None and self._list_item_from_row(row) is not None

    def _search_request_data(self, code: str) -> dict[str, str]:
        return {
            "pdfNameYn": "N",
            "pageIndex": "1",
            "firstIndex": "0",
            "listCnt": "10",
            "periodType": "short",
            "listType": "table",
            "etfTemaCode": "",
            "cateNameYn": "N",
            "inCateNationNot": "",
            "inCateFundNot": "",
            "q": code,
            "prfPrd": "1w",
            "orderA": "Month03",
            "orderB": "descending",
        }

    def _list_request_data(self) -> dict[str, str]:
        data = self._search_request_data("")
        data["listCnt"] = "500"
        return data

    def _to_summary(self, row) -> EtfSummary | None:
        item = self._list_item_from_row(row)
        if item is None:
            return None

        return EtfSummary(
            provider=self.name,
            code=item.code,
            isin=item.ksd_fund,
            name=item.name,
            category=item.category,
            listing_date=item.listing_date,
            nav=item.nav,
            aum=item.aum,
            detail_url=f"{self.detail_url_base}?{urlencode({'ksdFund': item.ksd_fund})}" if item.ksd_fund else None,
            raw={
                "ksdFund": item.ksd_fund,
                "categories": item.categories,
                "pensionFlags": item.pension_flags,
                "returns": item.returns,
                "totalCount": item.total_count,
            },
        )

    def _list_item_from_row(self, row) -> TigerEtfListItem | None:
        name = normalize_space(
            row.select_one(".title a").get_text(" ", strip=True) if row.select_one(".title a") else ""
        )
        code = _code_from_text(row.select_one(".code").get_text(" ", strip=True) if row.select_one(".code") else "")
        if not name or not code:
            return None

        categories = [
            normalize_space(node.get_text(" ", strip=True))
            for node in row.select(".category .each")
            if normalize_space(node.get_text(" ", strip=True))
        ]
        pension_flags = [item for item in categories if item.startswith("개인연금") or item.startswith("퇴직연금")]
        category = " / ".join(item for item in categories if item not in pension_flags)
        ksd_fund = str(row.get("data-ksd-fund") or "")

        try:
            return TigerEtfListItem(
                code=code,
                name=name,
                ksd_fund=ksd_fund,
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


def _parse_title_and_code(value: str) -> tuple[str | None, str | None]:
    match = re.search(r"^(?P<name>.+?)\s*\((?P<code>[^)]+)\)", value)
    if match is None:
        return (value or None), None
    return match.group("name").strip(), match.group("code").strip()


def _code_from_text(value: str) -> str | None:
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


def _blank_to_none(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, str):
        normalized = normalize_space(value)
        return None if normalized in {"", "-"} else normalized
    return value


def _parse_display_decimal(value: object) -> Decimal | None:
    value = _blank_to_none(value)
    if value is None or isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        value = value.replace(" 상승", "").replace(" 하락", "").removeprefix("연 ")
    return parse_decimal_text(value)


def _return_text(value: object) -> str | None:
    value = _blank_to_none(value)
    if value is None:
        return None
    return normalize_space(str(value)).replace(" 상승", "").replace(" 하락", "")


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


def _ksd_fund_from_html(html: str) -> str | None:
    match = re.search(r"ksdFund=([A-Z0-9]+)", html)
    return match.group(1) if match else None


def _as_of_date(soup: BeautifulSoup):
    text = soup.get_text(" ", strip=True)
    match = re.search(r"기준일\s*(?P<date>\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})", text)
    if match is not None:
        return parse_date_text(match.group("date"))
    match = re.search(r"(?P<date>\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})\s*기준", text)
    return parse_date_text(match.group("date")) if match else None


def _pdf_date(html: str):
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("input[name='fixDate']")
    value = node.get("value") if node is not None else None
    return parse_date_text(value) if isinstance(value, str) else None
