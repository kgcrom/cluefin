from typing import Mapping

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._periodic_report_key_information_types import (
    CapitalChangeStatus,
    CapitalChangeStatusItem,
    DividendInformation,
    DividendInformationItem,
)


class PeriodicReportKeyInformation:
    """DART 정기보고서 주요정보 조회 API"""

    def __init__(self, client: Client):
        self.client = client

    def get_capital_change_status(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> CapitalChangeStatus:
        """
        정기보고서에서 증자(감자) 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            CapitalChangeStatus: 증자(감자) 현황 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/irdsSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"증자(감자) 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return CapitalChangeStatus.parse(payload, list_model=CapitalChangeStatusItem)

    def get_dividend_information(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> DividendInformation:
        """
        정기보고서에서 배당 관련 사항을 조회합니다.

        Args:
            corp_code (str) : 공시대상회사의 고유번호(8자리)
            bsns_year (str) : 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str) : 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            DividendInformation: 배당 관련 사항 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        query_params = {key: value for key, value in params.items() if value is not None}

        payload = self.client._get("/api/alotMatter.json", params=query_params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"배당 관련 사항 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return DividendInformation.parse(payload, list_model=DividendInformationItem)

    def get_treasury_stock_activity(self) -> None:
        """정기보고서에서 자기주식 취득 및 처분 현황을 조회합니다."""
        # TODO implement

    def get_major_shareholder_status(self) -> None:
        """정기보고서에서 최대주주 현황을 조회합니다."""
        # TODO implement

    def get_major_shareholder_changes(self) -> None:
        """정기보고서에서 최대주주 변동현황을 조회합니다."""
        # TODO implement

    def get_minority_shareholder_status(self) -> None:
        """정기보고서에서 소액주주 현황을 조회합니다."""
        # TODO implement

    def get_executive_status(self) -> None:
        """정기보고서에서 임원 현황을 조회합니다."""
        # TODO implement

    def get_employee_status(self) -> None:
        """정기보고서에서 직원 현황을 조회합니다."""
        # TODO implement

    def get_board_and_audit_compensation_above_500m(self) -> None:
        """정기보고서에서 이사·감사 개별 보수현황(5억 이상)을 조회합니다."""
        # TODO implement

    def get_board_and_audit_total_compensation(self) -> None:
        """정기보고서에서 이사·감사 전체 보수지급금액을 조회합니다."""
        # TODO implement

    def get_top_five_individual_compensation(self) -> None:
        """정기보고서에서 개인별 보수지급 금액(5억 이상 상위 5인)을 조회합니다."""
        # TODO implement

    def get_other_corporation_investments(self) -> None:
        """정기보고서에서 타법인 출자현황을 조회합니다."""
        # TODO implement

    def get_total_number_of_shares(self) -> None:
        """정기보고서에서 주식의 총수 현황을 조회합니다."""
        # TODO implement

    def get_debt_securities_issuance_performance(self) -> None:
        """정기보고서에서 채무증권 발행실적을 조회합니다."""
        # TODO implement

    def get_outstanding_commercial_paper_balance(self) -> None:
        """정기보고서에서 기업어음증권 미상환 잔액을 조회합니다."""
        # TODO implement

    def get_outstanding_short_term_bonds(self) -> None:
        """정기보고서에서 단기사채 미상환 잔액을 조회합니다."""
        # TODO implement

    def get_outstanding_corporate_bonds(self) -> None:
        """정기보고서에서 회사채 미상환 잔액을 조회합니다."""
        # TODO implement

    def get_outstanding_hybrid_capital_securities(self) -> None:
        """정기보고서에서 신종자본증권 미상환 잔액을 조회합니다."""
        # TODO implement

    def get_outstanding_contingent_capital_securities(self) -> None:
        """정기보고서에서 조건부 자본증권 미상환 잔액을 조회합니다."""
        # TODO implement

    def get_auditor_name_and_opinion(self) -> None:
        """정기보고서에서 회계감사인 명칭과 감사의견을 조회합니다."""
        # TODO implement

    def get_audit_service_contracts(self) -> None:
        """정기보고서에서 감사용역 계약현황을 조회합니다."""
        # TODO implement

    def get_non_audit_service_contracts(self) -> None:
        """정기보고서에서 회계감사인과의 비감사용역 계약체결 현황을 조회합니다."""
        # TODO implement

    def get_outside_director_status(self) -> None:
        """정기보고서에서 사외이사 및 변동현황을 조회합니다."""
        # TODO implement

    def get_unregistered_executive_compensation(self) -> None:
        """정기보고서에서 미등기임원 보수현황을 조회합니다."""
        # TODO implement

    def get_board_and_audit_compensation_shareholder_approved(self) -> None:
        """정기보고서에서 이사·감사 전체 보수현황(주주총회 승인금액)을 조회합니다."""
        # TODO implement

    def get_board_and_audit_compensation_by_type(self) -> None:
        """정기보고서에서 이사·감사 전체 보수현황(보수지급금액 유형별)을 조회합니다."""
        # TODO implement

    def get_public_offering_fund_usage(self) -> None:
        """정기보고서에서 공모자금 사용내역을 조회합니다."""
        # TODO implement

    def get_private_placement_fund_usage(self) -> None:
        """정기보고서에서 사모자금 사용내역을 조회합니다."""
        # TODO implement
