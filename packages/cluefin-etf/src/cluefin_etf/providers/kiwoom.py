from __future__ import annotations

import json
import re
from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field

from cluefin_etf._errors import FetchError
from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._parsing import (
    compact_raw,
    definition_value,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
)


class KiwoomSearchVO(BaseModel):
    model_config = ConfigDict(extra="allow")

    pageNo: int = 1
    endPage: int | None = None


class KiwoomEtfListItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    gcode: str
    goodsNm: str
    goodsTypeNm: str | None = None
    bsisIdex: str | None = None
    idexNm: str | None = None
    setdate: str | None = None
    standardprice: Decimal | None = None
    fundtotalamount: Decimal | None = None


class KiwoomEtfListResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    totalCnt: int = 0
    searchVO: KiwoomSearchVO = Field(default_factory=KiwoomSearchVO)
    etfList: list[KiwoomEtfListItem] = Field(default_factory=list)


class KiwoomProvider(EtfProvider):
    list_url = "https://www.kiwoometf.com/service/etf/KO02010100MAjax"
    detail_url_template = "https://www.kiwoometf.com/service/etf/KO02010200M?gcode={code}"
    detail_url_base = "https://www.kiwoometf.com/service/etf/KO02010200M"
    holdings_url = "https://www.kiwoometf.com/service/etf/KO02010200MAjax4"
    list_referrer = "https://www.kiwoometf.com/service/etf/KO02010100M"
    list_headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }

    info = ProviderInfo(
        name=ProviderName.KIWOOM,
        display_name="Kiwoom",
        homepage_url="https://www.kiwoometf.com/",
    )

    def fetch_detail(self, code: str) -> EtfDetail:
        url = self.detail_url_template.format(code=code)
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        detail = self.parse_detail_html(code, result.html)
        pdf_date = _pdf_date_from_html(result.html) or _compact_date(detail.as_of_date)
        holdings_url = self.holdings_url
        try:
            holdings_result = self.fetcher.fetch(
                self.holdings_url,
                provider=self.name,
                validator=self.validate_holdings_result,
                method="POST",
                headers=self.list_headers,
                data={"schGubun1": detail.code, "startDate": pdf_date or ""},
                referrer=url,
            )
            holdings = self.parse_holdings_json(holdings_result.html)
            if not holdings:
                raise FetchError(f"Kiwoom holdings API returned no rows for {detail.code}")
        except FetchError:
            holdings = self.parse_holdings_html(result.html, as_of_date=detail.as_of_date)
            if not holdings:
                rendered_result = self.fetcher.fetch(
                    url, provider=self.name, validator=self.validate_rendered_holdings_result
                )
                holdings = self.parse_holdings_html(rendered_result.html, as_of_date=detail.as_of_date)
            holdings_url = f"{url}#pdf"
        return detail.model_copy(
            update={
                "holdings_url": holdings_url,
                "holdings": holdings,
            }
        )

    def fetch_list(self) -> list[EtfSummary]:
        page_no = 1
        end_page = 1
        summaries: list[EtfSummary] = []

        while page_no <= end_page:
            result = self.fetcher.fetch(
                self.list_url,
                provider=self.name,
                validator=self.validate_list_result,
                method="POST",
                headers=self.list_headers,
                data=self._list_request_data(page_no),
                referrer=self.list_referrer,
            )
            response = self._parse_list_response(result.html)
            end_page = response.searchVO.endPage or page_no
            summaries.extend(self._to_summary(item) for item in response.etfList)
            page_no += 1

        return summaries

    def validate_list_result(self, result: FetchResult) -> bool:
        try:
            response = self._parse_list_response(result.html)
        except (json.JSONDecodeError, ValueError):
            return False
        if not response.etfList:
            return False
        if response.totalCnt > 0 and response.searchVO.endPage is None:
            return False
        return all(bool(item.gcode.strip() and item.goodsNm.strip()) for item in response.etfList)

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        response = self._parse_list_response(html)
        return [self._to_summary(item) for item in response.etfList]

    def validate_detail_result(self, result: FetchResult) -> bool:
        detail = self.parse_detail_html("", result.html)
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select_one(".head-group h2, .fund-title h2, h2")
        code_text = (
            normalize_space(soup.select_one(".fund-code").get_text(" ", strip=True))
            if soup.select_one(".fund-code")
            else ""
        )
        parsed_code = _code_from_text(code_text) or code

        return EtfDetail(
            provider=self.name,
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
            detail_url=f"{self.detail_url_base}?gcode={parsed_code}" if parsed_code else None,
            raw={
                "fundCodeText": code_text,
                "basicInfo": _basic_info(soup),
            },
        )

    def validate_holdings_result(self, result: FetchResult) -> bool:
        try:
            payload = json.loads(result.html)
        except json.JSONDecodeError:
            return False
        return isinstance(payload.get("pdfList"), list)

    def validate_rendered_holdings_result(self, result: FetchResult) -> bool:
        return bool(_rendered_holdings_table(BeautifulSoup(result.html, "html.parser")))

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        payload = json.loads(html)
        items = payload.get("pdfList")
        if not isinstance(items, list):
            return []
        return [
            _holding_from_pdf_item(index, item) for index, item in enumerate(items, start=1) if isinstance(item, dict)
        ]

    def parse_holdings_html(self, html: str, *, as_of_date: date | None = None) -> list[EtfHolding]:
        table = _rendered_holdings_table(BeautifulSoup(html, "html.parser"))
        if table is None:
            return []

        holdings: list[EtfHolding] = []
        for row in table.select("tbody tr"):
            cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
            if len(cells) < 4:
                continue
            rank = parse_int_text(cells[0])
            name = cells[1] or None
            code = cells[2] or None
            weight = parse_decimal_text(cells[3])
            holdings.append(
                EtfHolding(
                    rank=rank,
                    code=code,
                    name=name,
                    weight=weight,
                    as_of_date=as_of_date,
                    raw=compact_raw(
                        {
                            "rank": cells[0],
                            "itemTitle": cells[1],
                            "itemCode": cells[2],
                            "ratio": cells[3],
                        },
                        ("rank", "itemCode", "itemTitle", "ratio"),
                    ),
                )
            )
        return holdings

    def _parse_list_response(self, html: str) -> KiwoomEtfListResponse:
        return KiwoomEtfListResponse.model_validate_json(html)

    def _to_summary(self, item: KiwoomEtfListItem) -> EtfSummary:
        return EtfSummary(
            provider=self.name,
            code=item.gcode,
            name=item.goodsNm,
            category=item.goodsTypeNm,
            benchmark=item.bsisIdex or item.idexNm,
            listing_date=_parse_kiwoom_date(item.setdate),
            nav=item.standardprice,
            aum=item.fundtotalamount,
            detail_url=f"{self.detail_url_base}?gcode={item.gcode}",
            raw=item.model_dump(mode="json"),
        )

    def _list_request_data(self, page_no: int) -> dict[str, str]:
        return {
            "pageNo": str(page_no),
            "schContent": "",
            "schGubun1": "",
            "pension": "false",
            "schOrder": "03",
        }


def _parse_kiwoom_date(value: str | None) -> date | None:
    if not value:
        return None
    year, month, day = (int(part) for part in value.split("."))
    return date(year, month, day)


def _compact_date(value: date | None) -> str | None:
    return value.strftime("%Y%m%d") if value else None


def _pdf_date_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("#pdfDt, input[name='pdfDt']")
    value = node.get("value") if node is not None else None
    if not isinstance(value, str):
        return None
    return value.replace("-", "").replace(".", "") or None


def _summary_decimal(soup: BeautifulSoup, label: str) -> Decimal | None:
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


def _rendered_holdings_table(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        headers = [normalize_space(node.get_text(" ", strip=True)) for node in table.find_all(["th", "td"])]
        if {"NO.", "종목명", "종목코드", "비중"}.issubset(headers):
            return table
    return None


def _holding_from_pdf_item(index: int, item: dict[str, object]) -> EtfHolding:
    code = item.get("itemCode") or item.get("gcode") or item.get("fundcode")
    return EtfHolding(
        rank=index,
        code=str(code) if code is not None else None,
        name=str(item.get("itemTitle")) if item.get("itemTitle") is not None else None,
        quantity=parse_decimal_text(str(item.get("volume"))) if item.get("volume") is not None else None,
        valuation_amount=parse_decimal_text(str(item.get("assessment")))
        if item.get("assessment") is not None
        else None,
        weight=parse_decimal_text(str(item.get("ratio"))) if item.get("ratio") is not None else None,
        as_of_date=parse_date_text(str(item.get("businessDate"))) if item.get("businessDate") is not None else None,
        raw=compact_raw(
            item,
            ("businessDate", "itemCode", "gcode", "fundcode", "itemTitle", "volume", "assessment", "ratio"),
        ),
    )
