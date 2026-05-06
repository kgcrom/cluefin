from __future__ import annotations

import re
from urllib.parse import urlencode

from bs4 import BeautifulSoup

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
        detail = self.parse_detail_html("", result.html)
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

        return EtfDetail(
            provider=self.name,
            code=ticker or code,
            name=name,
            category=category or None,
            benchmark=definition_value(soup, "벤치마크") or definition_value(soup, "기초지수"),
            listing_date=parse_date_text(definition_value(soup, "상장일")),
            nav=_summary_decimal(soup, "기준가격"),
            aum=_summary_decimal(soup, "순자산 규모") or parse_decimal_text(definition_value(soup, "순자산총액")),
            expense_ratio=parse_decimal_text(definition_value(soup, "총보수")),
            as_of_date=_as_of_date(soup),
            detail_url=meta_content(soup, property_="og:url") or meta_content(soup, name="canonical"),
            raw={
                "inputCode": code,
                "ksdFund": _ksd_fund_from_html(html),
                "categories": categories,
            },
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
            holdings.append(
                EtfHolding(
                    rank=index,
                    code=cells[0] or None,
                    name=cells[1] or None,
                    quantity=parse_decimal_text(cells[2]),
                    valuation_amount=parse_decimal_text(cells[3]),
                    weight=parse_decimal_text(cells[4]),
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
        if row is None:
            return code
        return str(row.get("data-ksd-fund") or code)

    def _validate_search_result(self, result: FetchResult) -> bool:
        soup = BeautifulSoup(result.html, "html.parser")
        return soup.select_one(".c-data-row[data-ksd-fund]") is not None

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

        return EtfSummary(
            provider=self.name,
            code=code,
            isin=ksd_fund or None,
            name=name,
            category=category or None,
            listing_date=parse_date_text(_pair_value(row, "상장일")),
            nav=parse_decimal_text(_pair_value(row, "기준가")),
            aum=parse_decimal_text(_pair_value(row, "순자산")),
            detail_url=f"{self.detail_url_base}?{urlencode({'ksdFund': ksd_fund})}" if ksd_fund else None,
            raw={
                "ksdFund": ksd_fund or None,
                "categories": categories,
                "pensionFlags": pension_flags,
                "returns": _returns(row),
                "totalCount": parse_int_text(row.get("data-tot-cnt")),
            },
        )


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
