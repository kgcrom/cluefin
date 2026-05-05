from __future__ import annotations

import json
import re
from urllib.parse import urljoin

from pydantic import BaseModel, ConfigDict, Field

from cluefin_etf._models import EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class AceEtfListItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    fund_code: str
    name: str
    category: str | None = None
    pension_flags: list[str] = Field(default_factory=list)
    raw: dict[str, object] = Field(default_factory=dict)


class AceProvider(EtfProvider):
    list_url = "https://www.aceetf.co.kr/modal/allfund"
    detail_url_template = None
    detail_url_base = "https://www.aceetf.co.kr/fund"

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

    def validate_list_result(self, result: FetchResult) -> bool:
        try:
            self._find_allfund_chunk_url(result.html)
        except ValueError:
            return False
        return True

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return [self._to_summary(item) for item in self._parse_chunk_items(html)]

    def _validate_chunk_result(self, result: FetchResult) -> bool:
        return bool(self._parse_chunk_items(result.html))

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
