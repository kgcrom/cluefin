from __future__ import annotations

from pydantic import ValidationError

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._rise_detail import looks_like_rise_ticker, parse_rise_detail_html
from cluefin_etf.providers._rise_holdings import parse_rise_holdings_html
from cluefin_etf.providers._rise_list import parse_rise_list_html, rise_list_total_count
from cluefin_etf.providers._rise_models import RiseEtfListItem, RiseHoldingItem  # noqa: F401


class RiseProvider(EtfProvider):
    list_url = "https://www.riseetf.co.kr/prod/finder/listJquery"
    detail_url_base = "https://www.riseetf.co.kr/prod/finderDetail"
    detail_url_template = f"{detail_url_base}/{{code}}"
    list_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    max_list_pages = 50

    info = ProviderInfo(
        name=ProviderName.RISE,
        display_name="RISE",
        homepage_url="https://www.riseetf.co.kr/",
    )

    def fetch_list(self) -> list[EtfSummary]:
        page = 1
        items: list[EtfSummary] = []
        total_count: int | None = None

        while page <= self.max_list_pages:
            result = self.fetcher.fetch(
                self.list_url,
                provider=self.name,
                validator=self.validate_list_result,
                method="POST",
                headers=self.list_headers,
                data=self._list_request_data(page),
                referrer="https://www.riseetf.co.kr/prod/finder",
            )
            page_items = self.parse_list_html(result.html)
            if not page_items:
                break

            if len(page_items) <= len(items):
                break

            items = page_items
            total_count = rise_list_total_count(result.html) or total_count
            if total_count is not None and len(items) >= total_count:
                break

            page += 1

        return items[:total_count] if total_count is not None else items

    def fetch_detail(self, code: str) -> EtfDetail:
        product_id = self._resolve_product_id(code) if looks_like_rise_ticker(code) else code
        url = f"{self.detail_url_base}/{product_id}"
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        detail = self.parse_detail_html(code, result.html)
        holdings = self.parse_holdings_html(result.html, as_of_date=detail.as_of_date)
        return detail.model_copy(update={"holdings_url": f"{url}#pdf", "holdings": holdings})

    def validate_list_result(self, result: FetchResult) -> bool:
        return bool(self.parse_list_html(result.html))

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return parse_rise_list_html(html, self.name)

    def validate_detail_result(self, result: FetchResult) -> bool:
        try:
            detail = self.parse_detail_html("", result.html)
        except ValidationError:
            return False
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        return parse_rise_detail_html(code, html, self.name)

    def validate_holdings_result(self, result: FetchResult) -> bool:
        return bool(self.parse_holdings_html(result.html))

    def parse_holdings_html(self, html: str, *, as_of_date=None) -> list[EtfHolding]:
        return parse_rise_holdings_html(html, as_of_date=as_of_date)

    def _list_request_data(self, page: int) -> dict[str, str]:
        return {
            "searchType1": "",
            "searchType2": "",
            "page": str(page),
            "searchOrder": "",
            "searchBoardType": "",
            "searchText": "",
            "searchFieldType": "list",
        }

    def _resolve_product_id(self, code: str) -> str:
        for summary in self.fetch_list():
            if summary.code == code and summary.raw.get("productId"):
                return str(summary.raw["productId"])
        return code
