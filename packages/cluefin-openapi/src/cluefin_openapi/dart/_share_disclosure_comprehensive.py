"""지분공시 종합정보 (Disclosure Comprehensive Information) API client."""

from typing import Mapping, Optional

from ._client import Client
from ._share_disclosure_comprehensive_types import (
    ExecutiveMajorShareholderOwnershipReport,
    ExecutiveMajorShareholderOwnershipReportItem,
    LargeHoldingReport,
    LargeHoldingReportItem,
)


class ShareDisclosureComprehensive:
    def __init__(self, client: Client):
        self.client = client

    def large_holding_report(
        self,
        corp_code: str,
    ) -> LargeHoldingReport:
        """주식등의 대량보유 상황보고 정보를 조회합니다.

        Args:
            corp_code: 공시대상회사의 고유번호(8자리)

        Returns:
            LargeHoldingReport: 주식등의 대량보유 상황보고 목록과 페이지 정보
        """

        normalized_code = corp_code.strip()
        if not normalized_code:
            raise ValueError("대량보유 상황보고를 조회하려면 corp_code를 지정해야 합니다.")

        params = {
            "corp_code": normalized_code,
        }
        query_params = {key: value for key, value in params.items() if value is not None}

        payload = self.client._get("/api/majorstock.json", params=query_params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"주식등의 대량보유 상황보고 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        parsed = LargeHoldingReport.parse(payload, list_model=LargeHoldingReportItem)
        return parsed

    def executive_major_shareholder_ownership_report(
        self,
        corp_code: str,
    ) -> ExecutiveMajorShareholderOwnershipReport:
        """임원·주요주주 소유보고 정보를 조회합니다.

        임원·주요주주특정증권등 소유상황보고서 내에 임원·주요주주 소유보고
        정보를 제공합니다.

        Args:
            corp_code: 공시대상회사의 고유번호(8자리)

        Returns:
            ExecutiveMajorShareholderOwnershipReport: 임원·주요주주 소유보고 목록과 페이지 정보
        """

        normalized_code = corp_code.strip()
        if not normalized_code:
            raise ValueError("임원·주요주주 소유보고를 조회하려면 corp_code를 지정해야 합니다.")

        params = {
            "corp_code": normalized_code,
        }
        query_params = {key: value for key, value in params.items() if value is not None}

        payload = self.client._get("/api/elestock.json", params=query_params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"임원·주요주주 소유보고 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        parsed = ExecutiveMajorShareholderOwnershipReport.parse(
            payload, list_model=ExecutiveMajorShareholderOwnershipReportItem
        )
        return parsed
