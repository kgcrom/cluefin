from __future__ import annotations

import json
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from cluefin_etf._models import EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


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
    detail_url_template = None
    detail_url_base = "https://www.kiwoometf.com/service/etf/KO02010200M"
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
