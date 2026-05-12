from __future__ import annotations

import json
import re
from urllib.parse import urljoin

from pydantic import ValidationError

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._ace_models import AceDetailPayload, AceEtfListItem, AceHoldingsPayload, AcePdfHoldingItem
from cluefin_etf.providers._parsing import compact_raw


class AceProvider(EtfProvider):
    list_url = "https://www.aceetf.co.kr/modal/allfund"
    detail_url_template = "https://www.aceetf.co.kr/fund/{code}"
    detail_url_base = "https://www.aceetf.co.kr/fund"
    detail_api_url_base = "https://papi.aceetf.co.kr/api/funds"
    detail_headers = {
        "Accept": "application/json",
    }

    info = ProviderInfo(
        name=ProviderName.ACE,
        display_name="ACE",
        homepage_url="https://www.aceetf.co.kr/",
    )

    def fetch_list(self) -> list[EtfSummary]:
        page_result = self.fetcher.fetch(self.list_url, provider=self.name, validator=self.validate_list_result)
        chunk_url = self._find_allfund_chunk_url(page_result.html)
        chunk_result = self.fetcher.fetch(chunk_url, provider=self.name, validator=self._validate_chunk_result)
        return self.parse_list_html(chunk_result.html)

    def fetch_detail(self, code: str) -> EtfDetail:
        page_url = f"{self.detail_url_base}/{code}"
        self.fetcher.fetch(page_url, provider=self.name, validator=self._validate_detail_page_result)
        api_result = self.fetcher.fetch(
            f"{self.detail_api_url_base}/{code}",
            provider=self.name,
            validator=self.validate_detail_result,
            headers=self.detail_headers,
            referrer=page_url,
        )
        holdings_url = f"{self.detail_api_url_base}/{code}/pdf"
        holdings_result = self.fetcher.fetch(
            holdings_url,
            provider=self.name,
            validator=self.validate_holdings_result,
            headers=self.detail_headers,
            referrer=page_url,
        )
        detail = self.parse_detail_html(code, api_result.html)
        return detail.model_copy(
            update={
                "holdings_url": holdings_url,
                "holdings": self.parse_holdings_json(holdings_result.html),
            }
        )

    def validate_list_result(self, result: FetchResult) -> bool:
        try:
            self._find_allfund_chunk_url(result.html)
        except ValueError:
            return False
        return True

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return [self._to_summary(item) for item in self._parse_chunk_items(html)]

    def validate_detail_result(self, result: FetchResult) -> bool:
        try:
            payload = json.loads(result.html)
            AceDetailPayload.model_validate(payload)
        except (json.JSONDecodeError, ValidationError):
            return False
        return True

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        raw_payload = json.loads(html)
        payload = AceDetailPayload.model_validate(raw_payload)
        badge = payload.badge
        category = _join_badges(
            badge.get("regionTypeNames"),
            badge.get("assetTypeNames"),
            badge.get("themeTypeNames"),
        )

        return EtfDetail(
            provider=self.name,
            code=payload.fundCd or code,
            name=payload.fundNm,
            isin=payload.fundCd,
            category=category,
            listing_date=payload.lstdDt,
            nav=payload.stpr,
            aum=payload.nastAmt,
            as_of_date=payload.stdDt,
            detail_url=f"{self.detail_url_base}/{payload.fundCd or code}",
            raw=_ace_detail_raw(raw_payload),
        )

    def validate_holdings_result(self, result: FetchResult) -> bool:
        try:
            payload = json.loads(result.html)
            AceHoldingsPayload.model_validate(payload)
        except (json.JSONDecodeError, ValidationError):
            return False
        return True

    def parse_holdings_json(self, html: str) -> list[EtfHolding]:
        try:
            raw_payload = json.loads(html)
            payload = AceHoldingsPayload.model_validate(raw_payload)
        except (json.JSONDecodeError, ValidationError):
            return []
        raw_items = raw_payload.get("pdfList")
        if not isinstance(raw_items, list):
            raw_items = [{} for _ in payload.pdfList]
        return [
            _holding_from_pdf_item(item, raw_item) for item, raw_item in zip(payload.pdfList, raw_items, strict=False)
        ]

    def _validate_chunk_result(self, result: FetchResult) -> bool:
        return bool(self._parse_chunk_items(result.html))

    def _validate_detail_page_result(self, result: FetchResult) -> bool:
        return result.html.find('"page":"/fund/[fundCode]"') >= 0

    def _find_allfund_chunk_url(self, html: str) -> str:
        match = re.search(r'src="(?P<src>/_next/static/chunks/pages/modal/allfund-[^"]+\.js)"', html)
        if match is None:
            raise ValueError("ACE allfund chunk URL was not found")
        return urljoin(self.list_url, match.group("src"))

    def _parse_chunk_items(self, chunk: str) -> list[AceEtfListItem]:
        current_category: str | None = None
        items: list[AceEtfListItem] = []
        events = sorted(_iter_category_events(chunk) + _iter_item_events(chunk), key=lambda event: event["start"])

        for index, event in enumerate(events):
            if event["type"] == "category":
                current_category = event["category"]
                continue

            next_start = events[index + 1]["start"] if index + 1 < len(events) else len(chunk)
            context = chunk[event["start"] : next_start]
            pension_flags = [flag for flag in ("개인연금", "퇴직연금") if f'children:"{flag}"' in context]
            raw = {
                "fundCode": event["fund_code"],
                "category": current_category,
                "pensionFlags": pension_flags,
            }
            items.append(
                AceEtfListItem(
                    fund_code=event["fund_code"],
                    name=event["name"],
                    category=current_category,
                    pension_flags=pension_flags,
                    raw=raw,
                )
            )

        return items

    def _to_summary(self, item: AceEtfListItem) -> EtfSummary:
        return EtfSummary(
            provider=self.name,
            code=item.fund_code,
            isin=item.fund_code,
            name=item.name,
            category=item.category,
            detail_url=f"{self.detail_url_base}/{item.fund_code}",
            raw=item.raw,
        )


def _iter_category_events(chunk: str) -> list[dict[str, str | int]]:
    pattern = re.compile(
        r'children:\["(?P<category>[^"]+)",\(0,[A-Za-z_$][\w$]*\.jsx\)'
        r'\("span",\{className:"cnt",children:"(?P<count>\d+)건"\}\)\]'
    )
    return [
        {"type": "category", "category": match.group("category"), "start": match.start()}
        for match in pattern.finditer(chunk)
    ]


def _iter_item_events(chunk: str) -> list[dict[str, str | int]]:
    pattern = re.compile(
        r'onClick:\(\)=>goPage\([^)]*?\.G\.FundDetail,"(?P<fund_code>[^"]+)"\)'
        r'.{0,500}?className:"txt",children:(?P<name>"(?:\\.|[^"\\])*")',
        re.DOTALL,
    )
    return [
        {
            "type": "item",
            "fund_code": match.group("fund_code"),
            "name": json.loads(match.group("name")),
            "start": match.start(),
        }
        for match in pattern.finditer(chunk)
    ]


def _join_badges(*groups: object) -> str | None:
    values: list[str] = []
    for group in groups:
        if not isinstance(group, list):
            continue
        values.extend(str(item) for item in group if item)
    return " / ".join(values) if values else None


def _ace_detail_raw(payload: dict[str, object]) -> dict[str, object]:
    return compact_raw(
        payload,
        (
            "fundCd",
            "stockCd",
            "fundNm",
            "fundWhlNm",
            "stdDt",
            "stpr",
            "nastAmt",
            "lstdDt",
            "badge",
            "summaryContent",
        ),
    )


def _holding_from_pdf_item(item: AcePdfHoldingItem, raw_item: object | None = None) -> EtfHolding:
    raw = raw_item if isinstance(raw_item, dict) else item.model_dump(mode="python")
    return EtfHolding(
        rank=item.rank,
        code=item.jm_KSC_CD,
        name=item.sec_NM,
        quantity=item.cu_ITEM_CNT,
        valuation_amount=item.val_AM,
        weight=item.wg,
        as_of_date=item.std_DT,
        raw=compact_raw(raw, ("rank", "jm_KSC_CD", "sec_NM", "cu_ITEM_CNT", "val_AM", "wg", "std_DT")),
    )
