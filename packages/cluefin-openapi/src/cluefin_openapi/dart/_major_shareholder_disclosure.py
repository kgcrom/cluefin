from typing import Mapping

from ._client import Client
from ._major_shareholder_disclosure_types import (
    BusinessLetter,
    BusinessLetterItem,
    BusinessPlanDecision,
    BusinessPlanDecisionItem,
    BusinessTransferDecision,
    BusinessTransferDecisionItem,
    CapitalReductionDecision,
    CapitalReductionDecisionItem,
    ConvertibleBondIssuanceDecision,
    ConvertibleBondIssuanceDecisionItem,
    CorporateBondIssuanceDecision,
    CorporateBondIssuanceDecisionItem,
    CorporateDivisionDecision,
    CorporateDivisionDecisionItem,
    CorporateLawDecision,
    CorporateLawDecisionItem,
    CorporateLawMethodDecision,
    CorporateLawMethodDecisionItem,
    CorporateRehabilitationProceedings,
    CorporateRehabilitationProceedingsItem,
    DissolutionOccurrence,
    DissolutionOccurrenceItem,
    FreeSecuritiesDecision,
    FreeSecuritiesDecisionItem,
    GovernmentBondManagerReplacement,
    GovernmentBondManagerReplacementItem,
    GovernmentBondManagerTransferTermination,
    GovernmentBondManagerTransferTerminationItem,
    NewStockWarrantBondIssuanceDecision,
    NewStockWarrantBondIssuanceDecisionItem,
    OverseasSecuritiesTradingDelistingResolution,
    OverseasSecuritiesTradingDelistingResolutionItem,
    OverseasSecuritiesTradingResolution,
    OverseasSecuritiesTradingResolutionItem,
    OverseasSecuritiesTradingStatus,
    OverseasSecuritiesTradingStatusDelisting,
    OverseasSecuritiesTradingStatusDelistingItem,
    OverseasSecuritiesTradingStatusItem,
    PaidInCapitalReductionDecision,
    PaidInCapitalReductionDecisionItem,
    ProfitRevocation,
    ProfitRevocationItem,
    RealEstateDevelopment,
    RealEstateDevelopmentItem,
    ReorganizationPlanApprovedRuling,
    ReorganizationPlanApprovedRulingItem,
    RetirementStockInvestmentPlanDecision,
    RetirementStockInvestmentPlanDecisionItem,
    RetirementStockInvestmentTransferDecision,
    RetirementStockInvestmentTransferDecisionItem,
    SecuritiesGrantedDecision,
    SecuritiesGrantedDecisionItem,
    StockRelatedBondPlanDecision,
    StockRelatedBondPlanDecisionItem,
    StockRelatedBondTransferDecision,
    StockRelatedBondTransferDecisionItem,
    StockTradingOtherDecision,
    StockTradingOtherDecisionItem,
    TangibleAssetPlanDecision,
    TangibleAssetPlanDecisionItem,
    TangibleAssetTransferDecision,
    TangibleAssetTransferDecisionItem,
    TreasuryStockAcquisitionDecision,
    TreasuryStockAcquisitionDecisionItem,
    TreasuryStockAcquisitionDisposalPlan,
    TreasuryStockAcquisitionDisposalPlanItem,
    TreasuryStockDisposalDecision,
    TreasuryStockDisposalDecisionItem,
    TreasuryStockTrustContractTerminationDecision,
    TreasuryStockTrustContractTerminationDecisionItem,
)


class MajorShareholderDisclosure:
    """주요사항보고서 주요정보"""

    def __init__(self, client: Client):
        self.client = client

    def treasury_stock_acquisition_disposal_plan(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> TreasuryStockAcquisitionDisposalPlan:
        """
        자산양수도(기타), 풋백옵션 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            TreasuryStockAcquisitionDisposalPlan: 자산양수도(기타), 풋백옵션 응답

        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/astInhtrfEtcPtbkOpt.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자산양수도(기타), 풋백옵션 응답이 올바르지 않습니다: {payload!r}")

        return TreasuryStockAcquisitionDisposalPlan.parse(payload, list_model=TreasuryStockAcquisitionDisposalPlanItem)

    def real_estate_development(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> RealEstateDevelopment:
        """
        부도발생 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            RealEstateDevelopment: 부도발생 응답

        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/dfOcr.json", params=params)

        if not isinstance(payload, Mapping):
            raise TypeError(f"부도발생 응답이 올바르지 않습니다: {payload!r}")

        return RealEstateDevelopment.parse(payload, list_model=RealEstateDevelopmentItem)

    def business_letter(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> BusinessLetter:
        """
        영업정지 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            BusinessLetter: 영업정지 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bsnSp.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"영업정지 응답이 올바르지 않습니다: {payload!r}")
        return BusinessLetter.parse(payload, list_model=BusinessLetterItem)

    def corporate_rehabilitation_proceedings(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> CorporateRehabilitationProceedings:
        """
        회생절차 개시신청 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            CorporateRehabilitationProceedings: 회생절차 개시신청 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ctrcvsBgrq.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"회생절차 개시신청 응답이 올바르지 않습니다: {payload!r}")
        return CorporateRehabilitationProceedings.parse(payload, list_model=CorporateRehabilitationProceedingsItem)

    def dissolution_occurrence(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        해산사유 발생 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            DissolutionOccurrence: 해산사유 발생 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/dsRsOcr.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해산사유 발생 응답이 올바르지 않습니다: {payload!r}")
        return DissolutionOccurrence.parse(payload, list_model=DissolutionOccurrenceItem)

    def securities_granted_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> SecuritiesGrantedDecision:
        """
        유상증자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            SecuritiesGrantedDecision: 유상증자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/piicDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유상증자 결정 응답이 올바르지 않습니다: {payload!r}")
        return SecuritiesGrantedDecision.parse(payload, list_model=SecuritiesGrantedDecisionItem)

    def free_securities_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> FreeSecuritiesDecision:
        """
        무상증자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            FreeSecuritiesDecision: 무상증자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/fricDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"무상증자 결정 응답이 올바르지 않습니다: {payload!r}")
        return FreeSecuritiesDecision.parse(payload, list_model=FreeSecuritiesDecisionItem)

    def paid_in_capital_reduction_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> PaidInCapitalReductionDecision:
        """
        유무상증자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            PaidInCapitalReductionDecision: 유무상증자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/pifricDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유무상증자 결정 응답이 올바르지 않습니다: {payload!r}")
        return PaidInCapitalReductionDecision.parse(payload, list_model=PaidInCapitalReductionDecisionItem)

    def capital_reduction_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> CapitalReductionDecision:
        """
        감자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            CapitalReductionDecision: 감자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/crDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"감자 결정 응답이 올바르지 않습니다: {payload!r}")
        return CapitalReductionDecision.parse(payload, list_model=CapitalReductionDecisionItem)

    def government_bond_manager_replacement(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> GovernmentBondManagerReplacement:
        """
        재권은행 등의 관리절차 개시 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            GovernmentBondManagerReplacement: 재권은행 등의 관리절차 개시 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bnkMngtPcbg.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"재권은행 등의 관리절차 개시 응답이 올바르지 않습니다: {payload!r}")
        return GovernmentBondManagerReplacement.parse(payload, list_model=GovernmentBondManagerReplacementItem)

    def profit_revocation(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> ProfitRevocation:
        """
        소송 등의 제기 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제 제공

        Returns:
            ProfitRevocation: 소송 등의 제기 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/lwstLg.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"소송 등의 제기 응답이 올바르지 않습니다: {payload!r}")
        return ProfitRevocation.parse(payload, list_model=ProfitRevocationItem)

    def overseas_securities_trading_resolution(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesTradingResolution:
        """
        해외 증권시장 주권등 상장 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesTradingResolution: 해외 증권시장 주권등 상장 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovLstDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장 결정 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesTradingResolution.parse(payload, list_model=OverseasSecuritiesTradingResolutionItem)

    def overseas_securities_trading_delisting_resolution(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesTradingDelistingResolution:
        """
        해외 증권시장 주권등 상장폐지 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesTradingDelistingResolution: 해외 증권시장 주권등 상장폐지 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovDlstDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장폐지 결정 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesTradingDelistingResolution.parse(
            payload, list_model=OverseasSecuritiesTradingDelistingResolutionItem
        )

    def overseas_securities_trading_status(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesTradingStatus:
        """
        해외 증권시장 주권등 상장 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesTradingStatus: 해외 증권시장 주권등 상장 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovLst.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesTradingStatus.parse(payload, list_model=OverseasSecuritiesTradingStatusItem)

    def overseas_securities_trading_status_delisting(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesTradingStatusDelisting:
        """
        해외 증권시장 주권등 상장폐지 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesTradingStatusDelisting: 해외 증권시장 주권등 상장폐지 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovDlst.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장폐지 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesTradingStatusDelisting.parse(
            payload, list_model=OverseasSecuritiesTradingStatusDelistingItem
        )

    def convertible_bond_issuance_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> ConvertibleBondIssuanceDecision:
        """
        전환사채권 발행결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            ConvertibleBondIssuanceDecision: 전환사채권 발행결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/cvbdIsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"전환사채권 발행결정 응답이 올바르지 않습니다: {payload!r}")
        return ConvertibleBondIssuanceDecision.parse(payload, list_model=ConvertibleBondIssuanceDecisionItem)

    def new_stock_warrant_bond_issuance_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> NewStockWarrantBondIssuanceDecision:
        """
        신주인수권부사채권 발행결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            NewStockWarrantBondIssuanceDecision: 신주인수권부사채권 발행결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bdwtIsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"신주인수권부사채권 발행결정 응답이 올바르지 않습니다: {payload!r}")
        return NewStockWarrantBondIssuanceDecision.parse(payload, list_model=NewStockWarrantBondIssuanceDecisionItem)

    def corporate_bond_issuance_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> CorporateBondIssuanceDecision:
        """
        교환사채권 발행결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            CorporateBondIssuanceDecision: 교환사채권 발행결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/exbdIsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"교환사채권 발행결정 응답이 올바르지 않습니다: {payload!r}")
        return CorporateBondIssuanceDecision.parse(payload, list_model=CorporateBondIssuanceDecisionItem)

    def government_bond_manager_transfer_termination(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> GovernmentBondManagerTransferTermination:
        """
        채권은행 등의 관리절차 종단 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            GovernmentBondManagerTransferTermination: 채권은행 등의 관리절차 종단 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bnkMngtPcsp.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"채권은행 등의 관리절차 종단 응답이 올바르지 않습니다: {payload!r}")
        return GovernmentBondManagerTransferTermination.parse(
            payload, list_model=GovernmentBondManagerTransferTerminationItem
        )

    def reorganization_plan_approved_ruling(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> ReorganizationPlanApprovedRuling:
        """
        상각형 조건부자본증권 발행결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            ReorganizationPlanApprovedRuling: 상각형 조건부자본증권 발행결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/wdCocobdIsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"상각형 조건부자본증권 발행결정 응답이 올바르지 않습니다: {payload!r}")
        return ReorganizationPlanApprovedRuling.parse(payload, list_model=ReorganizationPlanApprovedRulingItem)

    def treasury_stock_acquisition_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> TreasuryStockAcquisitionDecision:
        """
        자기주식 취득 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            TreasuryStockAcquisitionDecision: 자기주식 취득 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/tsstkAqDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자기주식 취득 결정 응답이 올바르지 않습니다: {payload!r}")
        return TreasuryStockAcquisitionDecision.parse(payload, list_model=TreasuryStockAcquisitionDecisionItem)

    def treasury_stock_disposal_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        자기주식 처분 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            자기주식 처분 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/tsstkDpDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자기주식 처분 결정 응답이 올바르지 않습니다: {payload!r}")
        return TreasuryStockDisposalDecision.parse(payload, list_model=TreasuryStockDisposalDecisionItem)

    def treasury_stock_trust_contract_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        자기주식취득 신탁계약 체결 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            자기주식취득 신탁계약 체결 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/tsstkAqTrctrCnsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자기주식취득 신탁계약 체결 결정 응답이 올바르지 않습니다: {payload!r}")
        return TreasuryStockAcquisitionDisposalPlan.parse(payload, list_model=TreasuryStockAcquisitionDisposalPlanItem)

    def treasury_stock_trust_contract_termination_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        자기주식취득 신탁계약 해지 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            자기주식취득 신탁계약 해지 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/tsstkAqTrctrCcDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자기주식취득 신탁계약 해지 결정 응답이 올바르지 않습니다: {payload!r}")
        return TreasuryStockTrustContractTerminationDecision.parse(
            payload, list_model=TreasuryStockTrustContractTerminationDecisionItem
        )

    def business_plan_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        영업양수 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            영업양수 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bsnInhDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"영업양수 결정 응답이 올바르지 않습니다: {payload!r}")
        return BusinessPlanDecision.parse(payload, list_model=BusinessPlanDecisionItem)

    def business_transfer_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        영업양도 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            영업양도 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bsnTrfDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"영업양도 결정 응답이 올바르지 않습니다: {payload!r}")
        return BusinessTransferDecision.parse(payload, list_model=BusinessTransferDecisionItem)

    def tangible_asset_plan_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        유형자산 양수 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            유형자산 양수 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/tgastInhDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유형자산 양수 결정 응답이 올바르지 않습니다: {payload!r}")
        return TangibleAssetPlanDecision.parse(payload, list_model=TangibleAssetPlanDecisionItem)

    def tangible_asset_transfer_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        유형자산 양도 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            유형자산 양도 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bsnTrfDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유형자산 양도 결정 응답이 올바르지 않습니다: {payload!r}")
        return TangibleAssetTransferDecision.parse(payload, list_model=TangibleAssetTransferDecisionItem)

    def retirement_stock_investment_plan_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        타법인 주식 및 출자증권 양수결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            타법인 주식 및 출자증권 양수결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/otcprStkInvscrInhDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"타법인 주식 및 출자증권 양수결정 응답이 올바르지 않습니다: {payload!r}")
        return RetirementStockInvestmentPlanDecision.parse(
            payload, list_model=RetirementStockInvestmentPlanDecisionItem
        )

    def retirement_stock_investment_transfer_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        타법인 주식 및 출자증권 양도결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            타법인 주식 및 출자증권 양도결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/otcprStkInvscrTrfDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"타법인 주식 및 출자증권 양도결정 응답이 올바르지 않습니다: {payload!r}")
        return RetirementStockInvestmentTransferDecision.parse(
            payload, list_model=RetirementStockInvestmentTransferDecisionItem
        )

    def stock_related_bond_plan_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        주권 관련 사채권 양수 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            주권 관련 사채권 양수 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/stkrtbdInhDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"주권 관련 사채권 양수 결정 응답이 올바르지 않습니다: {payload!r}")
        return StockRelatedBondPlanDecision.parse(payload, list_model=StockRelatedBondPlanDecisionItem)

    def stock_related_bond_transfer_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        주권 관련 사채권 양도 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            주권 관련 사채권 양도 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/stkrtbdTrfDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"주권 관련 사채권 양도 결정 응답이 올바르지 않습니다: {payload!r}")
        return StockRelatedBondTransferDecision.parse(payload, list_model=StockRelatedBondTransferDecisionItem)

    def corporate_law_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        회사합병 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            회사합병 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/cmpMgDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"회사합병 결정 응답이 올바르지 않습니다: {payload!r}")
        return CorporateLawDecision.parse(payload, list_model=CorporateLawDecisionItem)

    def corporate_division_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        회사분할 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            회사분할 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/cmpDvDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"회사분할 결정 응답이 올바르지 않습니다: {payload!r}")
        return CorporateDivisionDecision.parse(payload, list_model=CorporateDivisionDecisionItem)

    def corporate_law_method_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        회사분할합병 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            회사분할합병 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/cmpDvmgDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"회사분할합병 결정 응답이 올바르지 않습니다: {payload!r}")
        return CorporateLawMethodDecision.parse(payload, list_model=CorporateLawMethodDecisionItem)

    def stock_trading_other_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ):
        """
        주식교환·이전 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            주식교환·이전 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/stkExtrDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"주식교환·이전 결정 응답이 올바르지 않습니다: {payload!r}")

        return StockTradingOtherDecision.parse(payload, list_model=StockTradingOtherDecisionItem)
