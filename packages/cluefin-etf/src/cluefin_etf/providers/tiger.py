from __future__ import annotations

from urllib.parse import urlencode

from pydantic import ValidationError

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._tiger_detail import parse_tiger_detail_html, tiger_pdf_date
from cluefin_etf.providers._tiger_holdings import (
    parse_tiger_holdings_html,
    validate_tiger_holdings,
    validate_tiger_holdings_page,
)
from cluefin_etf.providers._tiger_list import parse_tiger_list_html, tiger_search_item
from cluefin_etf.providers._tiger_models import TigerEtfListItem, TigerHoldingItem


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
                "holdings": self.parse_holdings_html(holdings_result.html, as_of_date=tiger_pdf_date(pdf_page.html)),
            }
        )

    def validate_list_result(self, result: FetchResult) -> bool:
        return bool(self.parse_list_html(result.html))

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return parse_tiger_list_html(html, self.name, self.detail_url_base)

    def validate_detail_result(self, result: FetchResult) -> bool:
        try:
            detail = self.parse_detail_html("", result.html)
        except ValidationError:
            return False
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        return parse_tiger_detail_html(code, html, self.name)

    def validate_holdings_page_result(self, result: FetchResult) -> bool:
        return validate_tiger_holdings_page(result.html)

    def validate_holdings_result(self, result: FetchResult) -> bool:
        return validate_tiger_holdings(result.html)

    def parse_holdings_html(self, html: str, *, as_of_date=None) -> list[EtfHolding]:
        return parse_tiger_holdings_html(html, as_of_date=as_of_date)

    def _resolve_ksd_fund(self, code: str) -> str:
        result = self.fetcher.fetch(
            self.search_url,
            provider=self.name,
            validator=self._validate_search_result,
            method="POST",
            headers=self.search_headers,
            data=self._search_request_data(code),
        )
        item = tiger_search_item(result.html)
        if item is None:
            return code
        return item.ksd_fund or code

    def _validate_search_result(self, result: FetchResult) -> bool:
        return tiger_search_item(result.html) is not None

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
