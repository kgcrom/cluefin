from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from math import ceil
from urllib.parse import urlencode

from pydantic import BaseModel, ConfigDict, TypeAdapter

from cluefin_etf._models import EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


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


_KODEX_LIST_ADAPTER = TypeAdapter(list[KodexEtfListItem])


class KodexProvider(EtfProvider):
    list_url = "https://www.samsungfund.com/api/v1/kodex/product.do"
    detail_url_template = None
    detail_url_base = "https://www.samsungfund.com/etf/product/view.do"
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

    def validate_list_result(self, result: FetchResult) -> bool:
        try:
            items = self._parse_list_response(result.html)
        except (json.JSONDecodeError, ValueError):
            return False
        return all(item.stkTicker and item.fNm for item in items)

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return [self._to_summary(item) for item in self._parse_list_response(html)]

    def _parse_list_response(self, html: str) -> list[KodexEtfListItem]:
        return _KODEX_LIST_ADAPTER.validate_json(html)

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


def _parse_kodex_date(value: str | None) -> date | None:
    if not value:
        return None
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))
