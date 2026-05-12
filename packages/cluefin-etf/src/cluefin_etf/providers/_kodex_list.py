from __future__ import annotations

from datetime import date
from math import ceil
from urllib.parse import urlencode

from cluefin_etf._models import EtfSummary, ProviderName
from cluefin_etf.providers._kodex_models import KODEX_LIST_ADAPTER, KodexEtfListItem


def parse_kodex_list_response(html: str) -> list[KodexEtfListItem]:
    return KODEX_LIST_ADAPTER.validate_json(html)


def kodex_to_summary(item: KodexEtfListItem, provider: ProviderName, detail_url_base: str) -> EtfSummary:
    return EtfSummary(
        provider=provider,
        code=item.stkTicker,
        name=item.fNm,
        category=item.typeLnm or item.typeNm,
        listing_date=parse_kodex_date(item.listD),
        nav=item.basp,
        aum=item.nav,
        as_of_date=parse_kodex_date(item.gijunYMD),
        detail_url=f"{detail_url_base}?id={item.fId}" if item.fId else None,
        raw=item.model_dump(mode="json"),
    )


def kodex_list_url(list_url: str, page_no: int) -> str:
    query = urlencode(
        {
            "srchTerm": "w",
            "ordrSort": "DESC",
            "ordrColm": "YIELD_WEEK",
            "pageNo": str(page_no),
        }
    )
    return f"{list_url}?{query}"


def kodex_total_pages(items: list[KodexEtfListItem]) -> int:
    total_count = items[0].totalCnt
    if total_count is None:
        return 1
    return ceil(total_count / len(items))


def resolve_kodex_detail_fund_id(code: str, summaries: list[EtfSummary]) -> str:
    if code.upper().startswith("2ETF"):
        return code
    for summary in summaries:
        if summary.code == code and summary.raw.get("fId"):
            return str(summary.raw["fId"])
    return code


def parse_kodex_date(value: str | None) -> date | None:
    if not value:
        return None
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))
