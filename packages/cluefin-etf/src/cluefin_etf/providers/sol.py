from __future__ import annotations

import json
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._sol_detail import parse_sol_detail_html
from cluefin_etf.providers._sol_holdings import (
    parse_sol_holdings_html,
    parse_sol_holdings_json_items,
    sol_holdings_work_date,
)
from cluefin_etf.providers._sol_list import parse_sol_list_items, sol_to_summary
from cluefin_etf.providers._sol_models import SolEtfListItem


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
        return bool(parse_sol_list_items(result.html))

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
        work_date = sol_holdings_work_date(holdings_page.html)
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
        return [sol_to_summary(item, self.name) for item in parse_sol_list_items(html)]

    def validate_detail_result(self, result: FetchResult) -> bool:
        detail = self.parse_detail_html("", result.html)
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        return parse_sol_detail_html(code, html, self.name, self.detail_url_base)

    def validate_holdings_page_result(self, result: FetchResult) -> bool:
        soup = BeautifulSoup(result.html, "html.parser")
        return soup.select_one("#pdf-table") is not None or sol_holdings_work_date(result.html) is not None

    def validate_holdings_result(self, result: FetchResult) -> bool:
        try:
            payload = json.loads(result.html)
        except json.JSONDecodeError:
            return False
        return isinstance(payload, list)

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        payload = json.loads(html)
        return parse_sol_holdings_json_items(payload)

    def parse_holdings_html(self, html: str) -> list[EtfHolding]:
        return parse_sol_holdings_html(html)

    def _resolve_detail_fund_code(self, code: str) -> str:
        for summary in self.fetch_list():
            if summary.code == code and summary.raw.get("fundCode"):
                return str(summary.raw["fundCode"])
        return code
