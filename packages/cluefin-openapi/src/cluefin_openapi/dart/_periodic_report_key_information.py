from typing import Mapping

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._periodic_report_key_information_types import (
    AuditorNameAndOpinion,
    AuditorNameAndOpinionItem,
    AuditServiceContracts,
    AuditServiceContractsItem,
    BoardAndAuditCompensationAbove500m,
    BoardAndAuditCompensationAbove500mItem,
    BoardAndAuditCompensationByType,
    BoardAndAuditCompensationByTypeItem,
    BoardAndAuditCompensationShareholderApproved,
    BoardAndAuditCompensationShareholderApprovedItem,
    BoardAndAuditTotalCompensation,
    BoardAndAuditTotalCompensationItem,
    CapitalChangeStatus,
    CapitalChangeStatusItem,
    DebtSecuritiesIssuancePerformance,
    DebtSecuritiesIssuancePerformanceItem,
    DividendInformation,
    DividendInformationItem,
    EmployeeStatus,
    EmployeeStatusItem,
    ExecutiveStatus,
    ExecutiveStatusItem,
    MajorShareholderChanges,
    MajorShareholderChangesItem,
    MajorShareholderStatus,
    MajorShareholderStatusItem,
    MinorityShareholderStatus,
    MinorityShareholderStatusItem,
    NonAuditServiceContracts,
    NonAuditServiceContractsItem,
    OtherCorporationInvestments,
    OtherCorporationInvestmentsItem,
    OutsideDirectorStatus,
    OutsideDirectorStatusItem,
    OutstandingCommercialPaperBalance,
    OutstandingCommercialPaperBalanceItem,
    OutstandingContingentCapitalSecurities,
    OutstandingContingentCapitalSecuritiesItem,
    OutstandingCorporateBonds,
    OutstandingCorporateBondsItem,
    OutstandingHybridCapitalSecurities,
    OutstandingHybridCapitalSecuritiesItem,
    OutstandingShortTermBonds,
    OutstandingShortTermBondsItem,
    PrivatePlacementFundUsage,
    PrivatePlacementFundUsageItem,
    PublicOfferingFundUsage,
    PublicOfferingFundUsageItem,
    TopFiveIndividualCompensation,
    TopFiveIndividualCompensationItem,
    TotalNumberOfShares,
    TotalNumberOfSharesItem,
    TreasuryStockActivity,
    TreasuryStockActivityItem,
    UnregisteredExecutiveCompensation,
    UnregisteredExecutiveCompensationItem,
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

    def get_treasury_stock_activity(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> TreasuryStockActivity:
        """
        정기보고서에서 자기주식 취득 및 처분 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            TreasuryStockActivity: 자기주식 취득 및 처분 현황 응답 객체
        """

        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/tesstkAcqsDspsSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자기주식 취득 및 처분 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return TreasuryStockActivity.parse(payload, list_model=TreasuryStockActivityItem)

    def get_major_shareholder_status(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> MajorShareholderStatus:
        """
        정기보고서에서 최대주주 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            MajorShareholderStatus: 최대주주 현황 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/hyslrSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"최대주주 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return MajorShareholderStatus.parse(payload, list_model=MajorShareholderStatusItem)

    def get_major_shareholder_changes(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> MajorShareholderChanges:
        """
        정기보고서에서 최대주주 변동현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            MajorShareholderChanges: 최대주주 변동현황 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/hyslrChgSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"최대주주 변동현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return MajorShareholderChanges.parse(payload, list_model=MajorShareholderChangesItem)

    def get_minority_shareholder_status(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> MinorityShareholderStatus:
        """
        정기보고서에서 소액주주 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            MinorityShareholderStatus: 소액주주 현황 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/mrhlSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"소액주주 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return MinorityShareholderStatus.parse(payload, list_model=MinorityShareholderStatusItem)

    def get_executive_status(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> ExecutiveStatus:
        """
        정기보고서에서 임원 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            ExecutiveStatus: 임원 현황 응답 객체
        """

        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/exctvSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"임원 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return ExecutiveStatus.parse(payload, list_model=ExecutiveStatusItem)

    def get_employee_status(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> EmployeeStatus:
        """
        정기보고서에서 직원 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            EmployeeStatus: 직원 현황 응답 객체
        """

        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/empSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"직원 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return EmployeeStatus.parse(payload, list_model=EmployeeStatusItem)

    def get_board_and_audit_compensation_above_500m(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> BoardAndAuditCompensationAbove500m:
        """
        정기보고서에서 이사·감사 개별 보수현황(5억 이상)을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            BoardAndAuditCompensationAbove500m: 이사·감사 개별 보수
        """

        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/hmvAuditIndvdlBySttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                f"이사·감사 개별 보수현황(5억 이상) 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}"
            )

        return BoardAndAuditCompensationAbove500m.parse(payload, list_model=BoardAndAuditCompensationAbove500mItem)

    def get_board_and_audit_total_compensation(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> BoardAndAuditTotalCompensation:
        """
        정기보고서에서 이사·감사 전체 보수지급금액을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            BoardAndAuditTotalCompensation: 이사·감사 전체 보수지급금
        """

        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/hmvAuditAllSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                f"이사·감사 전체 보수지급금액 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}"
            )

        return BoardAndAuditTotalCompensation.parse(payload, list_model=BoardAndAuditTotalCompensationItem)

    def get_top_five_individual_compensation(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> TopFiveIndividualCompensation:
        """
        정기보고서에서 개인별 보수지급 금액(5억 이상 상위 5인)을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            TopFiveIndividualCompensation: 개인별 보수지급 금액(5억 이상
        """

        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/indvdlByPay.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                f"개인별 보수지급 금액(5억 이상 상위 5인) 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}"
            )

        return TopFiveIndividualCompensation.parse(payload, list_model=TopFiveIndividualCompensationItem)

    def get_other_corporation_investments(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OtherCorporationInvestments:
        """
        정기보고서에서 타법인 출자현황을 조회합니다.
        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OtherCorporationInvestments: 타법인 출자현황 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/otrCprInvstmntSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"타법인 출자현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return OtherCorporationInvestments.parse(payload, list_model=OtherCorporationInvestmentsItem)

    def get_total_number_of_shares(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> TotalNumberOfShares:
        """
        정기보고서에서 주식의 총수 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            TotalNumberOfShares: 주식의 총수 현황 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/stockTotqySttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"주식의 총수 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return TotalNumberOfShares.parse(payload, list_model=TotalNumberOfSharesItem)

    def get_debt_securities_issuance_performance(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> DebtSecuritiesIssuancePerformance:
        """
        정기보고서에서 채무증권 발행실적을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            DebtSecuritiesIssuancePerformance: 채무증권 발행실적 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/detScritsIsuAcmslt.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"채무증권 발행실적 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return DebtSecuritiesIssuancePerformance.parse(payload, list_model=DebtSecuritiesIssuancePerformanceItem)

    def get_outstanding_commercial_paper_balance(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OutstandingCommercialPaperBalance:
        """
        정기보고서에서 기업어음증권 미상환 잔액을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OutstandingCommercialPaperBalance: 기업어음증권 미상환 잔액 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/entrprsBilScritsNrdmpBlce.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"기업어음증권 미상환 잔액 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return OutstandingCommercialPaperBalance.parse(payload, list_model=OutstandingCommercialPaperBalanceItem)

    def get_outstanding_short_term_bonds(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OutstandingShortTermBonds:
        """
        정기보고서에서 단기사채 미상환 잔액을 조회합니다

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OutstandingShortTermBonds: 단기사채 미상환 잔액 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/srtpdPsndbtNrdmpBlce.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"단기사채 미상환 잔액 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return OutstandingShortTermBonds.parse(payload, list_model=OutstandingShortTermBondsItem)

    def get_outstanding_corporate_bonds(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OutstandingCorporateBonds:
        """
        정기보고서에서 회사채 미상환 잔액을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OutstandingCorporateBonds: 회사채 미상환 잔액 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/cprndNrdmpBlce.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"회사채 미상환 잔액 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return OutstandingCorporateBonds.parse(payload, list_model=OutstandingCorporateBondsItem)

    def get_outstanding_hybrid_capital_securities(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OutstandingHybridCapitalSecurities:
        """
        정기보고서에서 신종자본증권 미상환 잔액을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OutstandingHybridCapitalSecurities: 신종자본증권 미상환 잔액 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/newCaplScritsNrdmpBlce.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"신종자본증권 미상환 잔액 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return OutstandingHybridCapitalSecurities.parse(payload, list_model=OutstandingHybridCapitalSecuritiesItem)

    def get_outstanding_contingent_capital_securities(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OutstandingContingentCapitalSecurities:
        """
        정기보고서에서 조건부 자본증권 미상환 잔액을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OutstandingContingentCapitalSecurities: 조건부 자본증권 미상환 잔액 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/cndlCaplScritsNrdmpBlce.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                f"조건부 자본증권 미상환 잔액 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}"
            )

        return OutstandingContingentCapitalSecurities.parse(
            payload, list_model=OutstandingContingentCapitalSecuritiesItem
        )

    def get_auditor_name_and_opinion(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> AuditorNameAndOpinion:
        """
        정기보고서에서 회계감사인 명칭과 감사의견을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            AuditorNameAndOpinion: 회계감사인 명칭과 감사의견 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/accnutAdtorNmNdAdtOpinion.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"회계감사인 명칭과 감사의견 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return AuditorNameAndOpinion.parse(
            payload,
            list_model=AuditorNameAndOpinionItem,
        )

    def get_audit_service_contracts(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> AuditServiceContracts:
        """
        정기보고서에서 감사용역 계약현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            AuditServiceContracts: 감사용역 계약현황 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/adtServcCnclsSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"감사용역 계약현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return AuditServiceContracts.parse(
            payload,
            list_model=AuditServiceContractsItem,
        )

    def get_non_audit_service_contracts(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> NonAuditServiceContracts:
        """
        정기보고서에서 회계감사인과의 비감사용역 계약체결 현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            NonAuditServiceContracts: 비감사용역 계약체결 현황 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/accnutAdtorNonAdtServcCnclsSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"비감사용역 계약체결 현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return NonAuditServiceContracts.parse(
            payload,
            list_model=NonAuditServiceContractsItem,
        )

    def get_outside_director_status(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> OutsideDirectorStatus:
        """
        정기보고서에서 사외이사 및 변동현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            OutsideDirectorStatus: 사외이사 및 변동현황 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/outcmpnyDrctrNdChangeSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"사외이사 및 변동현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return OutsideDirectorStatus.parse(
            payload,
            list_model=OutsideDirectorStatusItem,
        )

    def get_unregistered_executive_compensation(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> UnregisteredExecutiveCompensation:
        """
        정기보고서에서 미등기임원 보수현황을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            UnregisteredExecutiveCompensation: 미등기임원 보수현황 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/unrstExctvMendngSttus.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"미등기임원 보수현황 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return UnregisteredExecutiveCompensation.parse(
            payload,
            list_model=UnregisteredExecutiveCompensationItem,
        )

    def get_board_and_audit_compensation_shareholder_approved(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> BoardAndAuditCompensationShareholderApproved:
        """
        정기보고서에서 이사·감사 전체 보수현황(주주총회 승인금액)을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            BoardAndAuditCompensationShareholderApproved: 이사·감사 전체 보수현황(주주총회 승인금액) 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/drctrAdtAllMendngSttusGmtsckConfmAmount.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                "이사·감사 전체 보수현황(주주총회 승인금액) 응답은 매핑 타입이어야 합니다. "
                f"수신한 타입: {type(payload)!r}"
            )
        return BoardAndAuditCompensationShareholderApproved.parse(
            payload,
            list_model=BoardAndAuditCompensationShareholderApprovedItem,
        )

    def get_board_and_audit_compensation_by_type(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> BoardAndAuditCompensationByType:
        """
        정기보고서에서 이사·감사 전체 보수현황(보수지급금액 유형별)을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            BoardAndAuditCompensationByType: 이사·감사 전체 보수현황(보수지급금액 유형별) 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/drctrAdtAllMendngSttusMendngPymntamtTyCl.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                "이사·감사 전체 보수현황(보수지급금액 유형별) 응답은 매핑 타입이어야 합니다. "
                f"수신한 타입: {type(payload)!r}"
            )
        return BoardAndAuditCompensationByType.parse(
            payload,
            list_model=BoardAndAuditCompensationByTypeItem,
        )

    def get_public_offering_fund_usage(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> PublicOfferingFundUsage:
        """
        정기보고서에서 공모자금 사용내역을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            PublicOfferingFundUsage: 공모자금 사용내역 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/pssrpCptalUseDtls.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"공모자금 사용내역 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return PublicOfferingFundUsage.parse(payload, list_model=PublicOfferingFundUsageItem)

    def get_private_placement_fund_usage(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> PrivatePlacementFundUsage:
        """
        정기보고서에서 사모자금 사용내역을 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bsns_year (str): 사업연도(4자리) ※ 2015년 이후 부터 정보제공
            reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011)

        Returns:
            PrivatePlacementFundUsage: 사모자금 사용내역 응답
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/prvsrpCptalUseDtls.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"사모자금 사용내역 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return PrivatePlacementFundUsage.parse(payload, list_model=PrivatePlacementFundUsageItem)
