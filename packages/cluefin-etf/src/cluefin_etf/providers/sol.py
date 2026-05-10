from __future__ import annotations

import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, field_validator

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._parsing import (
    compact_raw,
    definition_value,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
    parse_korean_eok_amount,
)


class SolEtfListItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    fund_code: str
    etf_code: str
    name: str
    badges: list[str] = Field(default_factory=list)
    pension_flags: list[str] = Field(default_factory=list)
    nav: Decimal | None = None
    aum: Decimal | None = None
    detail_url: str
    returns: dict[str, str | None] = Field(default_factory=dict)
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("nav", "aum", mode="before")
    @classmethod
    def _empty_decimal_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value


class SolProvider(EtfProvider):
    list_url = "https://www.soletf.com/ko/fund"
    detail_url_template = "https://www.soletf.com/ko/fund/etf/{code}"
    detail_url_base = "https://www.soletf.com/ko/fund/etf"
    holdings_api_url = "https://www.soletf.com/api/fund/pdfList"
    holdings_headers = {
        "Accept": "application/json",
    }

    info = ProviderInfo(
        name=ProviderName.SOL,
        display_name="SOL",
        homepage_url="https://www.soletf.com/ko/main",
    )

    def validate_list_result(self, result: FetchResult) -> bool:
        return bool(self._parse_list_items(result.html))

    def fetch_detail(self, code: str) -> EtfDetail:
        fund_code = self._resolve_detail_fund_code(code)
        url = f"{self.detail_url_base}/{fund_code}"
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        holdings_page_url = f"{url}?tabIndex=3"
        holdings_page = self.fetcher.fetch(
            holdings_page_url,
            provider=self.name,
            validator=self.validate_holdings_page_result,
        )
        detail = self.parse_detail_html(code, result.html)
        work_date = _holdings_work_date(holdings_page.html)
        if work_date is None:
            return detail.model_copy(
                update={
                    "holdings_url": holdings_page_url,
                    "holdings": self.parse_holdings_html(holdings_page.html),
                }
            )

        holdings_url = f"{self.holdings_api_url}?{urlencode({'fund_cd': fund_code, 'work_dt': work_date})}"
        holdings_result = self.fetcher.fetch(
            holdings_url,
            provider=self.name,
            validator=self.validate_holdings_result,
            headers=self.holdings_headers,
            referrer=holdings_page_url,
        )
        return detail.model_copy(
            update={
                "holdings_url": holdings_url,
                "holdings": self.parse_holdings_json(holdings_result.html),
            }
        )

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return [self._to_summary(item) for item in self._parse_list_items(html)]

    def validate_detail_result(self, result: FetchResult) -> bool:
        detail = self.parse_detail_html("", result.html)
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select_one(".fv-name") or soup.find("h1")
        name, etf_code = _parse_name_and_code(normalize_space(title.get_text(" ", strip=True)) if title else "")
        badges = [normalize_space(node.get_text(" ", strip=True)) for node in soup.select(".i-bdg-g .i-bdg")]
        pension_flags = [badge for badge in badges if badge in {"개인연금", "퇴직연금"}]
        category_badges = [badge for badge in badges if badge not in pension_flags]

        return EtfDetail(
            provider=self.name,
            code=etf_code or code,
            name=name,
            category=" / ".join(category_badges) if category_badges else None,
            benchmark=_base_index_name(soup),
            listing_date=parse_date_text(definition_value(soup, "상장일")),
            nav=_fund_head_decimal(soup, "기준가격"),
            aum=parse_korean_eok_amount(definition_value(soup, "순자산 총액")),
            expense_ratio=parse_decimal_text(definition_value(soup, "총보수")),
            detail_url=f"{self.detail_url_base}/{_fund_code_from_html(html) or code}",
            raw={
                "inputCode": code,
                "fundCode": _fund_code_from_html(html),
                "badges": badges,
                "pensionFlags": pension_flags,
            },
        )

    def validate_holdings_page_result(self, result: FetchResult) -> bool:
        soup = BeautifulSoup(result.html, "html.parser")
        return soup.select_one("#pdf-table") is not None or _holdings_work_date(result.html) is not None

    def validate_holdings_result(self, result: FetchResult) -> bool:
        try:
            payload = json.loads(result.html)
        except json.JSONDecodeError:
            return False
        return isinstance(payload, list)

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        payload = json.loads(html)
        if not isinstance(payload, list):
            return []
        return [
            _holding_from_pdf_item(index, item) for index, item in enumerate(payload, start=1) if isinstance(item, dict)
        ]

    def parse_holdings_html(self, html: str) -> list[EtfHolding]:
        soup = BeautifulSoup(html, "html.parser")
        holdings: list[EtfHolding] = []
        for row in soup.select("#pdf-table tbody tr"):
            cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
            if len(cells) < 5:
                continue
            holdings.append(
                EtfHolding(
                    rank=parse_int_text(cells[0]),
                    name=cells[1] or None,
                    quantity=parse_decimal_text(cells[2]),
                    valuation_amount=parse_decimal_text(cells[3]),
                    weight=parse_decimal_text(cells[4]),
                    as_of_date=parse_date_text(_holdings_work_date(html)),
                    raw=compact_raw(
                        {
                            "rank": cells[0],
                            "name": cells[1],
                            "quantity": cells[2],
                            "valuationAmount": cells[3],
                            "weight": cells[4],
                        },
                        ("rank", "name", "quantity", "valuationAmount", "weight"),
                    ),
                )
            )
        return holdings

    def _parse_list_items(self, html: str) -> list[SolEtfListItem]:
        soup = BeautifulSoup(html, "html.parser")
        items: list[SolEtfListItem] = []

        for row in soup.select("table.fd-list tbody tr[id^='tr_']"):
            item = _parse_sol_row(row)
            if item is not None:
                items.append(item)

        return items

    def _to_summary(self, item: SolEtfListItem) -> EtfSummary:
        category_badges = [badge for badge in item.badges if badge not in item.pension_flags]
        return EtfSummary(
            provider=self.name,
            code=item.etf_code,
            name=item.name,
            category=" / ".join(category_badges) if category_badges else None,
            nav=item.nav,
            aum=item.aum,
            detail_url=item.detail_url,
            raw=item.raw,
        )

    def _resolve_detail_fund_code(self, code: str) -> str:
        for summary in self.fetch_list():
            if summary.code == code and summary.raw.get("fundCode"):
                return str(summary.raw["fundCode"])
        return code


def _parse_sol_row(row) -> SolEtfListItem | None:
    link = row.select_one("a.fd-link[href]")
    name_node = row.select_one(".fd-name")
    if link is None or name_node is None:
        return None

    href = link.get("href", "")
    fund_code = _fund_code_from_href(href) or _fund_code_from_row_id(row.get("id", ""))
    name_text = name_node.get_text(" ", strip=True)
    name, etf_code = _parse_name_and_code(name_text)
    if not fund_code or not name or not etf_code:
        return None

    cells = row.find_all("td", recursive=False)
    badges = [badge.get_text(" ", strip=True) for badge in row.select(".i-bdg-g .i-bdg")]
    pension_flags = [badge for badge in badges if badge in {"개인연금", "퇴직연금"}]
    returns = _parse_return_cells(cells)
    raw = {
        "fundCode": fund_code,
        "etfCode": etf_code,
        "badges": badges,
        "pensionFlags": pension_flags,
        "returns": returns,
    }

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
        raw=raw,
    )


def _fund_code_from_href(href: str) -> str | None:
    match = re.search(r"/ko/fund/etf/(?P<fund_code>[^/?#]+)", href)
    return match.group("fund_code") if match else None


def _fund_code_from_row_id(row_id: str) -> str | None:
    if row_id.startswith("tr_"):
        return row_id.removeprefix("tr_")
    return None


def _parse_name_and_code(value: str) -> tuple[str | None, str | None]:
    match = re.search(r"^(?P<name>.+?)\s*\((?P<code>[^)]+)\)\s*$", " ".join(value.split()))
    if match is None:
        return None, None
    return match.group("name").strip(), match.group("code").strip()


def _parse_decimal_cell(cells: list, index: int) -> Decimal | None:
    if index >= len(cells):
        return None
    return _parse_decimal_text(cells[index].get_text(" ", strip=True))


def _parse_decimal_text(value: str) -> Decimal | None:
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


def _fund_head_decimal(soup: BeautifulSoup, label: str) -> Decimal | None:
    for node in soup.select(".fv-exp dl"):
        title = node.find("dt")
        if title is None or label not in normalize_space(title.get_text(" ", strip=True)):
            continue
        value = node.select_one(".fd-pri")
        if value is not None:
            return parse_decimal_text(value.get_text(" ", strip=True))
    return None


def _base_index_name(soup: BeautifulSoup) -> str | None:
    for container in soup.select(".cont-col"):
        title = container.select_one(".g-title, h3")
        if title is None or "기초지수정보" not in normalize_space(title.get_text(" ", strip=True)):
            continue
        node = container.select_one("dl.g-conts dt")
        return normalize_space(node.get_text(" ", strip=True)) if node else None
    return None


def _fund_code_from_html(html: str) -> str | None:
    for match in re.finditer(r"/ko/fund/etf/(?P<fund_code>[^/?#'\"]+)", html):
        fund_code = match.group("fund_code")
        if fund_code not in {"pds", "summary"}:
            return fund_code
    return None


def _holdings_work_date(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("#f-pdf-calendar")
    value = node.get("value") if node is not None else None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.replace("-", "").replace(".", "")


def _holding_from_pdf_item(index: int, item: dict[str, object]) -> EtfHolding:
    return EtfHolding(
        rank=index,
        code=str(item.get("STOCK_CODE")) if item.get("STOCK_CODE") is not None else None,
        name=str(item.get("SEC_NM")) if item.get("SEC_NM") is not None else None,
        quantity=parse_decimal_text(str(item.get("QTY"))) if item.get("QTY") is not None else None,
        valuation_amount=parse_decimal_text(str(item.get("PRICE"))) if item.get("PRICE") is not None else None,
        weight=parse_decimal_text(str(item.get("WT_DISP"))) if item.get("WT_DISP") is not None else None,
        as_of_date=_parse_compact_sol_date(item.get("WORK_DT")),
        raw=compact_raw(item, ("WORK_DT", "SEQ_NO", "STOCK_CODE", "SEC_NM", "QTY", "PRICE", "WT_DISP")),
    )


def _parse_compact_sol_date(value: object) -> date | None:
    if value is None:
        return None
    text = str(value)
    if re.fullmatch(r"\d{8}", text):
        return parse_date_text(f"{text[:4]}.{text[4:6]}.{text[6:8]}")
    return parse_date_text(text)
