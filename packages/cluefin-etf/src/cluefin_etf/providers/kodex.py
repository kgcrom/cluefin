from __future__ import annotations

import json

from bs4 import BeautifulSoup

from cluefin_etf._errors import FetchError
from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._kodex_detail import parse_kodex_detail_html
from cluefin_etf.providers._kodex_holdings import (
    kodex_pdf_gijun_ymd,
    parse_kodex_holdings_html,
    parse_kodex_holdings_json,
    rendered_kodex_holdings_table,
    validate_kodex_holdings_json,
)
from cluefin_etf.providers._kodex_list import (
    kodex_list_url,
    kodex_to_summary,
    kodex_total_pages,
    parse_kodex_list_response,
    resolve_kodex_detail_fund_id,
)
from cluefin_etf.providers._kodex_models import KodexEtfListItem


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
                kodex_list_url(self.list_url, page_no),
                provider=self.name,
                validator=self.validate_list_result,
                headers=self.list_headers,
            )
            items = self._parse_list_response(result.html)
            if not items:
                break

            if total_pages is None:
                total_pages = kodex_total_pages(items)

            summaries.extend(kodex_to_summary(item, self.name, self.detail_url_base) for item in items)
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
        return [kodex_to_summary(item, self.name, self.detail_url_base) for item in self._parse_list_response(html)]

    def validate_detail_result(self, result: FetchResult) -> bool:
        detail = self.parse_detail_html("", result.html)
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        return parse_kodex_detail_html(code, html, self.name)

    def validate_product_result(self, result: FetchResult) -> bool:
        try:
            return bool(kodex_pdf_gijun_ymd(result.html))
        except (json.JSONDecodeError, ValueError):
            return False

    def validate_holdings_result(self, result: FetchResult) -> bool:
        return validate_kodex_holdings_json(result.html)

    def validate_rendered_holdings_result(self, result: FetchResult) -> bool:
        return bool(rendered_kodex_holdings_table(BeautifulSoup(result.html, "html.parser")))

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        return parse_kodex_holdings_json(html)

    def parse_holdings_html(self, html: str) -> list[EtfHolding]:
        return parse_kodex_holdings_html(html)

    def _fetch_pdf_holdings(self, fund_id: str, *, referrer: str) -> tuple[str, list[EtfHolding]]:
        product_result = self.fetcher.fetch(
            f"{self.product_url_base}/{fund_id}.do",
            provider=self.name,
            validator=self.validate_product_result,
            headers=self.list_headers,
            referrer=referrer,
        )
        gijun_ymd = kodex_pdf_gijun_ymd(product_result.html)
        holdings_url = f"{self.holdings_url_base}/{fund_id}.do?gijunYMD={gijun_ymd}"
        holdings_result = self.fetcher.fetch(
            holdings_url,
            provider=self.name,
            validator=self.validate_holdings_result,
            headers=self.list_headers,
            referrer=referrer,
        )
        actual_gijun_ymd = kodex_pdf_gijun_ymd(holdings_result.html, label="KODEX 구성종목 PDF")
        actual_holdings_url = f"{self.holdings_url_base}/{fund_id}.do?gijunYMD={actual_gijun_ymd}"
        return actual_holdings_url, self.parse_holdings_json(holdings_result.html)

    def _parse_list_response(self, html: str) -> list[KodexEtfListItem]:
        return parse_kodex_list_response(html)

    def _resolve_detail_fund_id(self, code: str) -> str:
        if code.upper().startswith("2ETF"):
            return code
        return resolve_kodex_detail_fund_id(code, self.fetch_list())
