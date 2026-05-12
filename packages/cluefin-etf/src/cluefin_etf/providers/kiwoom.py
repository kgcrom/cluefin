from __future__ import annotations

import json

from bs4 import BeautifulSoup

from cluefin_etf._errors import FetchError
from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._kiwoom_detail import compact_date, parse_kiwoom_detail_html, pdf_date_from_html
from cluefin_etf.providers._kiwoom_holdings import (
    parse_kiwoom_holdings_html,
    parse_kiwoom_holdings_json,
    rendered_kiwoom_holdings_table,
    validate_kiwoom_holdings_json,
)
from cluefin_etf.providers._kiwoom_list import kiwoom_list_request_data, kiwoom_to_summary, parse_kiwoom_list_response
from cluefin_etf.providers._kiwoom_models import KiwoomEtfListItem, KiwoomEtfListResponse


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
        pdf_date = pdf_date_from_html(result.html) or compact_date(detail.as_of_date)
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
        return parse_kiwoom_detail_html(code, html, self.name, self.detail_url_base)

    def validate_holdings_result(self, result: FetchResult) -> bool:
        return validate_kiwoom_holdings_json(result.html)

    def validate_rendered_holdings_result(self, result: FetchResult) -> bool:
        return bool(rendered_kiwoom_holdings_table(BeautifulSoup(result.html, "html.parser")))

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        return parse_kiwoom_holdings_json(html)

    def parse_holdings_html(self, html: str, *, as_of_date=None) -> list[EtfHolding]:
        return parse_kiwoom_holdings_html(html, as_of_date=as_of_date)

    def _parse_list_response(self, html: str) -> KiwoomEtfListResponse:
        return parse_kiwoom_list_response(html)

    def _to_summary(self, item: KiwoomEtfListItem) -> EtfSummary:
        return kiwoom_to_summary(item, self.name, self.detail_url_base)

    def _list_request_data(self, page_no: int) -> dict[str, str]:
        return kiwoom_list_request_data(page_no)
