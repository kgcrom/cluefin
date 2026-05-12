from __future__ import annotations

from datetime import date

from cluefin_etf._models import EtfSummary, ProviderName
from cluefin_etf.providers._kiwoom_models import KiwoomEtfListItem, KiwoomEtfListResponse


def parse_kiwoom_list_response(html: str) -> KiwoomEtfListResponse:
    return KiwoomEtfListResponse.model_validate_json(html)


def kiwoom_to_summary(item: KiwoomEtfListItem, provider: ProviderName, detail_url_base: str) -> EtfSummary:
    return EtfSummary(
        provider=provider,
        code=item.gcode,
        name=item.goodsNm,
        category=item.goodsTypeNm,
        benchmark=item.bsisIdex or item.idexNm,
        listing_date=_parse_kiwoom_date(item.setdate),
        nav=item.standardprice,
        aum=item.fundtotalamount,
        detail_url=f"{detail_url_base}?gcode={item.gcode}",
        raw=item.model_dump(mode="json"),
    )


def kiwoom_list_request_data(page_no: int) -> dict[str, str]:
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
