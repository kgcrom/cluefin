"""XBRL JSON API (data.sec.gov/api/xbrl) — SEC가 공시 XBRL에서 미리 뽑아 둔 값."""

from __future__ import annotations

import re

from ._client import DATA_BASE_URL, Client
from ._ids import cik10, path_segment
from ._xbrl_api_types import CompanyConcept, CompanyFacts, Frame

_PERIOD_PATTERN = re.compile(r"^CY\d{4}(Q[1-4]I?)?$")


class XbrlApi:
    """SEC XBRL JSON API"""

    def __init__(self, client: Client):
        self.client = client

    def company_facts(self, cik: int | str) -> CompanyFacts:
        """회사의 모든 XBRL 값 (companyfacts). 대형사는 수 MB다.

        Args:
            cik (int | str): CIK

        Raises:
            SecNotFoundError: XBRL을 낸 적이 없는 회사
        """
        payload = self.client._get_json(f"{DATA_BASE_URL}/api/xbrl/companyfacts/CIK{cik10(cik)}.json")
        return CompanyFacts.model_validate(payload)

    def company_concept(self, cik: int | str, taxonomy: str, tag: str) -> CompanyConcept:
        """회사 하나의 개념 하나 시계열 (companyconcept).

        Args:
            cik (int | str): CIK
            taxonomy (str): 택소노미 (us-gaap, dei, ifrs-full, srt)
            tag (str): 개념 이름, 대소문자 구분 (예: AccountsPayableCurrent)

        Raises:
            SecNotFoundError: 회사가 그 개념을 보고한 적이 없을 때
        """
        taxonomy = path_segment(taxonomy, what="택소노미")
        tag = path_segment(tag, what="개념 이름")
        url = f"{DATA_BASE_URL}/api/xbrl/companyconcept/CIK{cik10(cik)}/{taxonomy}/{tag}.json"
        return CompanyConcept.model_validate(self.client._get_json(url))

    def frames(self, taxonomy: str, tag: str, unit: str, period: str) -> Frame:
        """개념 하나·기간 하나의 모든 회사 값 (frames). 회사마다 그 기간에 가장 잘 맞는 값 하나씩.

        Args:
            taxonomy (str): 택소노미 (us-gaap ...)
            tag (str): 개념 이름 (예: Revenues)
            unit (str): 단위 (USD, shares, USD/shares). `/`는 SEC 경로 표기 `-per-`로 바꿔 보낸다.
            period (str): 달력 기간. 연간 `CY2023`, 분기 `CY2023Q1`, 분기말 시점 `CY2023Q1I`.

        Raises:
            SecNotFoundError: 해당 조합의 frame이 없을 때
        """
        taxonomy = path_segment(taxonomy, what="택소노미")
        tag = path_segment(tag, what="개념 이름")
        unit = path_segment(unit.replace("/", "-per-"), what="단위")
        if not _PERIOD_PATTERN.match(period):
            raise ValueError(f"기간은 CY2023, CY2023Q1, CY2023Q1I 형식이어야 합니다: {period!r}")
        url = f"{DATA_BASE_URL}/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json"
        return Frame.model_validate(self.client._get_json(url))
