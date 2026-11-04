import warnings
from collections.abc import Mapping

from ._client import Client
from ._major_shareholder_disclosure_types import (
    AssetTransferPutbackOption,
    AssetTransferPutbackOptionItem,
    BusinessAcquisitionDecision,
    BusinessAcquisitionDecisionItem,
    BusinessSuspension,
    BusinessSuspensionItem,
    BusinessTransferDecision,
    BusinessTransferDecisionItem,
    CapitalReductionDecision,
    CapitalReductionDecisionItem,
    CompanyDivisionMergerDecision,
    CompanyDivisionMergerDecisionItem,
    CompanyMergerDecision,
    CompanyMergerDecisionItem,
    ConvertibleBondIssuanceDecision,
    ConvertibleBondIssuanceDecisionItem,
    CorporateDivisionDecision,
    CorporateDivisionDecisionItem,
    CorporateRehabilitationProceedings,
    CorporateRehabilitationProceedingsItem,
    CreditorBankManagementProcedureCommencement,
    CreditorBankManagementProcedureCommencementItem,
    CreditorBankManagementProcedureTermination,
    CreditorBankManagementProcedureTerminationItem,
    DefaultOccurrence,
    DefaultOccurrenceItem,
    DissolutionOccurrence,
    DissolutionOccurrenceItem,
    ExchangeableBondIssuanceDecision,
    ExchangeableBondIssuanceDecisionItem,
    FreeCapitalIncreaseDecision,
    FreeCapitalIncreaseDecisionItem,
    LawsuitFiling,
    LawsuitFilingItem,
    NewStockWarrantBondIssuanceDecision,
    NewStockWarrantBondIssuanceDecisionItem,
    OtherCorporationSecuritiesAcquisitionDecision,
    OtherCorporationSecuritiesAcquisitionDecisionItem,
    OtherCorporationSecuritiesTransferDecision,
    OtherCorporationSecuritiesTransferDecisionItem,
    OverseasSecuritiesMarketDelistingDecision,
    OverseasSecuritiesMarketDelistingDecisionItem,
    OverseasSecuritiesMarketDelistingStatus,
    OverseasSecuritiesMarketDelistingStatusItem,
    OverseasSecuritiesMarketListingDecision,
    OverseasSecuritiesMarketListingDecisionItem,
    OverseasSecuritiesMarketListingStatus,
    OverseasSecuritiesMarketListingStatusItem,
    PaidInAndFreeCapitalIncreaseDecision,
    PaidInAndFreeCapitalIncreaseDecisionItem,
    PaidInCapitalIncreaseDecision,
    PaidInCapitalIncreaseDecisionItem,
    StockExchangeTransferDecision,
    StockExchangeTransferDecisionItem,
    StockRelatedBondAcquisitionDecision,
    StockRelatedBondAcquisitionDecisionItem,
    StockRelatedBondTransferDecision,
    StockRelatedBondTransferDecisionItem,
    TangibleAssetAcquisitionDecision,
    TangibleAssetAcquisitionDecisionItem,
    TangibleAssetTransferDecision,
    TangibleAssetTransferDecisionItem,
    TreasuryStockAcquisitionDecision,
    TreasuryStockAcquisitionDecisionItem,
    TreasuryStockDisposalDecision,
    TreasuryStockDisposalDecisionItem,
    TreasuryStockTrustContractDecision,
    TreasuryStockTrustContractDecisionItem,
    TreasuryStockTrustContractTerminationDecision,
    TreasuryStockTrustContractTerminationDecisionItem,
    WriteDownContingentCapitalSecuritiesIssuanceDecision,
    WriteDownContingentCapitalSecuritiesIssuanceDecisionItem,
)


class MajorMattersReport:
    """주요사항보고서 주요정보"""

    def __init__(self, client: Client):
        self.client = client

    def asset_transfer_putback_option(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> AssetTransferPutbackOption:
        """
        자산양수도(기타), 풋백옵션 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            AssetTransferPutbackOption: 자산양수도(기타), 풋백옵션 응답

        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/astInhtrfEtcPtbkOpt.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자산양수도(기타), 풋백옵션 응답이 올바르지 않습니다: {payload!r}")

        return AssetTransferPutbackOption.parse(payload, list_model=AssetTransferPutbackOptionItem)

    def default_occurrence(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> DefaultOccurrence:
        """
        부도발생 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            DefaultOccurrence: 부도발생 응답

        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/dfOcr.json", params=params)

        if not isinstance(payload, Mapping):
            raise TypeError(f"부도발생 응답이 올바르지 않습니다: {payload!r}")

        return DefaultOccurrence.parse(payload, list_model=DefaultOccurrenceItem)

    def business_suspension(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> BusinessSuspension:
        """
        영업정지 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            BusinessSuspension: 영업정지 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bsnSp.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"영업정지 응답이 올바르지 않습니다: {payload!r}")
        return BusinessSuspension.parse(payload, list_model=BusinessSuspensionItem)

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

    def paid_in_capital_increase_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> PaidInCapitalIncreaseDecision:
        """
        유상증자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            PaidInCapitalIncreaseDecision: 유상증자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/piicDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유상증자 결정 응답이 올바르지 않습니다: {payload!r}")
        return PaidInCapitalIncreaseDecision.parse(payload, list_model=PaidInCapitalIncreaseDecisionItem)

    def free_capital_increase_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> FreeCapitalIncreaseDecision:
        """
        무상증자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            FreeCapitalIncreaseDecision: 무상증자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/fricDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"무상증자 결정 응답이 올바르지 않습니다: {payload!r}")
        return FreeCapitalIncreaseDecision.parse(payload, list_model=FreeCapitalIncreaseDecisionItem)

    def paid_in_and_free_capital_increase_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> PaidInAndFreeCapitalIncreaseDecision:
        """
        유무상증자 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            PaidInAndFreeCapitalIncreaseDecision: 유무상증자 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/pifricDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유무상증자 결정 응답이 올바르지 않습니다: {payload!r}")
        return PaidInAndFreeCapitalIncreaseDecision.parse(payload, list_model=PaidInAndFreeCapitalIncreaseDecisionItem)

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

    def creditor_bank_management_procedure_commencement(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> CreditorBankManagementProcedureCommencement:
        """
        재권은행 등의 관리절차 개시 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제

        Returns:
            CreditorBankManagementProcedureCommencement: 재권은행 등의 관리절차 개시 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bnkMngtPcbg.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"재권은행 등의 관리절차 개시 응답이 올바르지 않습니다: {payload!r}")
        return CreditorBankManagementProcedureCommencement.parse(
            payload, list_model=CreditorBankManagementProcedureCommencementItem
        )

    def lawsuit_filing(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> LawsuitFiling:
        """
        소송 등의 제기 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제 제공

        Returns:
            LawsuitFiling: 소송 등의 제기 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/lwstLg.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"소송 등의 제기 응답이 올바르지 않습니다: {payload!r}")
        return LawsuitFiling.parse(payload, list_model=LawsuitFilingItem)

    def overseas_securities_market_listing_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesMarketListingDecision:
        """
        해외 증권시장 주권등 상장 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesMarketListingDecision: 해외 증권시장 주권등 상장 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovLstDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장 결정 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesMarketListingDecision.parse(
            payload, list_model=OverseasSecuritiesMarketListingDecisionItem
        )

    def overseas_securities_market_delisting_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesMarketDelistingDecision:
        """
        해외 증권시장 주권등 상장폐지 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesMarketDelistingDecision: 해외 증권시장 주권등 상장폐지 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovDlstDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장폐지 결정 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesMarketDelistingDecision.parse(
            payload, list_model=OverseasSecuritiesMarketDelistingDecisionItem
        )

    def overseas_securities_market_listing_status(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesMarketListingStatus:
        """
        해외 증권시장 주권등 상장 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesMarketListingStatus: 해외 증권시장 주권등 상장 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovLst.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesMarketListingStatus.parse(
            payload, list_model=OverseasSecuritiesMarketListingStatusItem
        )

    def overseas_securities_market_delisting_status(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> OverseasSecuritiesMarketDelistingStatus:
        """
        해외 증권시장 주권등 상장폐지 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            OverseasSecuritiesMarketDelistingStatus: 해외 증권시장 주권등 상장폐지 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/ovDlst.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"해외 증권시장 주권등 상장폐지 응답이 올바르지 않습니다: {payload!r}")
        return OverseasSecuritiesMarketDelistingStatus.parse(
            payload, list_model=OverseasSecuritiesMarketDelistingStatusItem
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

    def exchangeable_bond_issuance_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> ExchangeableBondIssuanceDecision:
        """
        교환사채권 발행결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            ExchangeableBondIssuanceDecision: 교환사채권 발행결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/exbdIsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"교환사채권 발행결정 응답이 올바르지 않습니다: {payload!r}")
        return ExchangeableBondIssuanceDecision.parse(payload, list_model=ExchangeableBondIssuanceDecisionItem)

    def creditor_bank_management_procedure_termination(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> CreditorBankManagementProcedureTermination:
        """
        채권은행 등의 관리절차 종단 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            CreditorBankManagementProcedureTermination: 채권은행 등의 관리절차 종단 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/bnkMngtPcsp.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"채권은행 등의 관리절차 종단 응답이 올바르지 않습니다: {payload!r}")
        return CreditorBankManagementProcedureTermination.parse(
            payload, list_model=CreditorBankManagementProcedureTerminationItem
        )

    def write_down_contingent_capital_securities_issuance_decision(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
    ) -> WriteDownContingentCapitalSecuritiesIssuanceDecision:
        """
        상각형 조건부자본증권 발행결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            WriteDownContingentCapitalSecuritiesIssuanceDecision: 상각형 조건부자본증권 발행결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/wdCocobdIsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"상각형 조건부자본증권 발행결정 응답이 올바르지 않습니다: {payload!r}")
        return WriteDownContingentCapitalSecuritiesIssuanceDecision.parse(
            payload, list_model=WriteDownContingentCapitalSecuritiesIssuanceDecisionItem
        )

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
    ) -> TreasuryStockTrustContractDecision:
        """
        자기주식취득 신탁계약 체결 결정 정보를 조회합니다.

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공

        Returns:
            TreasuryStockTrustContractDecision: 자기주식취득 신탁계약 체결 결정 응답
        """
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
        }
        payload = self.client._get("/api/tsstkAqTrctrCnsDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"자기주식취득 신탁계약 체결 결정 응답이 올바르지 않습니다: {payload!r}")
        return TreasuryStockTrustContractDecision.parse(payload, list_model=TreasuryStockTrustContractDecisionItem)

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

    def business_acquisition_decision(
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
        return BusinessAcquisitionDecision.parse(payload, list_model=BusinessAcquisitionDecisionItem)

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

    def tangible_asset_acquisition_decision(
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
        return TangibleAssetAcquisitionDecision.parse(payload, list_model=TangibleAssetAcquisitionDecisionItem)

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
        payload = self.client._get("/api/tgastTrfDecsn.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"유형자산 양도 결정 응답이 올바르지 않습니다: {payload!r}")
        return TangibleAssetTransferDecision.parse(payload, list_model=TangibleAssetTransferDecisionItem)

    def other_corporation_securities_acquisition_decision(
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
        return OtherCorporationSecuritiesAcquisitionDecision.parse(
            payload, list_model=OtherCorporationSecuritiesAcquisitionDecisionItem
        )

    def other_corporation_securities_transfer_decision(
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
        return OtherCorporationSecuritiesTransferDecision.parse(
            payload, list_model=OtherCorporationSecuritiesTransferDecisionItem
        )

    def stock_related_bond_acquisition_decision(
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
        return StockRelatedBondAcquisitionDecision.parse(payload, list_model=StockRelatedBondAcquisitionDecisionItem)

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

    def company_merger_decision(
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
        return CompanyMergerDecision.parse(payload, list_model=CompanyMergerDecisionItem)

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

    def company_division_merger_decision(
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
        return CompanyDivisionMergerDecision.parse(payload, list_model=CompanyDivisionMergerDecisionItem)

    def stock_exchange_transfer_decision(
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

        return StockExchangeTransferDecision.parse(payload, list_model=StockExchangeTransferDecisionItem)

    # ------------------------------------------------------------------
    # 2026-11-04: 아래는 엔드포인트와 맞지 않던 옛 이름이다 (B-13). 삭제하지 않고
    # DeprecationWarning 별칭으로 남긴다 — 외부 사용자 호환.
    # ------------------------------------------------------------------

    def treasury_stock_acquisition_disposal_plan(self, *args, **kwargs):
        """``asset_transfer_putback_option`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``asset_transfer_putback_option`` instead."""
        warnings.warn(
            "treasury_stock_acquisition_disposal_plan() is deprecated; use asset_transfer_putback_option() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset_transfer_putback_option(*args, **kwargs)

    def real_estate_development(self, *args, **kwargs):
        """``default_occurrence`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``default_occurrence`` instead."""
        warnings.warn(
            "real_estate_development() is deprecated; use default_occurrence() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.default_occurrence(*args, **kwargs)

    def business_letter(self, *args, **kwargs):
        """``business_suspension`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``business_suspension`` instead."""
        warnings.warn(
            "business_letter() is deprecated; use business_suspension() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.business_suspension(*args, **kwargs)

    def securities_granted_decision(self, *args, **kwargs):
        """``paid_in_capital_increase_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``paid_in_capital_increase_decision`` instead."""
        warnings.warn(
            "securities_granted_decision() is deprecated; use paid_in_capital_increase_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.paid_in_capital_increase_decision(*args, **kwargs)

    def free_securities_decision(self, *args, **kwargs):
        """``free_capital_increase_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``free_capital_increase_decision`` instead."""
        warnings.warn(
            "free_securities_decision() is deprecated; use free_capital_increase_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.free_capital_increase_decision(*args, **kwargs)

    def paid_in_capital_reduction_decision(self, *args, **kwargs):
        """``paid_in_and_free_capital_increase_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``paid_in_and_free_capital_increase_decision`` instead."""
        warnings.warn(
            "paid_in_capital_reduction_decision() is deprecated; use paid_in_and_free_capital_increase_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.paid_in_and_free_capital_increase_decision(*args, **kwargs)

    def government_bond_manager_replacement(self, *args, **kwargs):
        """``creditor_bank_management_procedure_commencement`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``creditor_bank_management_procedure_commencement`` instead."""
        warnings.warn(
            "government_bond_manager_replacement() is deprecated; use creditor_bank_management_procedure_commencement() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.creditor_bank_management_procedure_commencement(*args, **kwargs)

    def profit_revocation(self, *args, **kwargs):
        """``lawsuit_filing`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``lawsuit_filing`` instead."""
        warnings.warn(
            "profit_revocation() is deprecated; use lawsuit_filing() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.lawsuit_filing(*args, **kwargs)

    def overseas_securities_trading_resolution(self, *args, **kwargs):
        """``overseas_securities_market_listing_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``overseas_securities_market_listing_decision`` instead."""
        warnings.warn(
            "overseas_securities_trading_resolution() is deprecated; use overseas_securities_market_listing_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.overseas_securities_market_listing_decision(*args, **kwargs)

    def overseas_securities_trading_delisting_resolution(self, *args, **kwargs):
        """``overseas_securities_market_delisting_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``overseas_securities_market_delisting_decision`` instead."""
        warnings.warn(
            "overseas_securities_trading_delisting_resolution() is deprecated; use overseas_securities_market_delisting_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.overseas_securities_market_delisting_decision(*args, **kwargs)

    def overseas_securities_trading_status_delisting(self, *args, **kwargs):
        """``overseas_securities_market_delisting_status`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``overseas_securities_market_delisting_status`` instead."""
        warnings.warn(
            "overseas_securities_trading_status_delisting() is deprecated; use overseas_securities_market_delisting_status() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.overseas_securities_market_delisting_status(*args, **kwargs)

    def overseas_securities_trading_status(self, *args, **kwargs):
        """``overseas_securities_market_listing_status`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``overseas_securities_market_listing_status`` instead."""
        warnings.warn(
            "overseas_securities_trading_status() is deprecated; use overseas_securities_market_listing_status() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.overseas_securities_market_listing_status(*args, **kwargs)

    def corporate_bond_issuance_decision(self, *args, **kwargs):
        """``exchangeable_bond_issuance_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``exchangeable_bond_issuance_decision`` instead."""
        warnings.warn(
            "corporate_bond_issuance_decision() is deprecated; use exchangeable_bond_issuance_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.exchangeable_bond_issuance_decision(*args, **kwargs)

    def government_bond_manager_transfer_termination(self, *args, **kwargs):
        """``creditor_bank_management_procedure_termination`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``creditor_bank_management_procedure_termination`` instead."""
        warnings.warn(
            "government_bond_manager_transfer_termination() is deprecated; use creditor_bank_management_procedure_termination() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.creditor_bank_management_procedure_termination(*args, **kwargs)

    def reorganization_plan_approved_ruling(self, *args, **kwargs):
        """``write_down_contingent_capital_securities_issuance_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``write_down_contingent_capital_securities_issuance_decision`` instead."""
        warnings.warn(
            "reorganization_plan_approved_ruling() is deprecated; use write_down_contingent_capital_securities_issuance_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.write_down_contingent_capital_securities_issuance_decision(*args, **kwargs)

    def business_plan_decision(self, *args, **kwargs):
        """``business_acquisition_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``business_acquisition_decision`` instead."""
        warnings.warn(
            "business_plan_decision() is deprecated; use business_acquisition_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.business_acquisition_decision(*args, **kwargs)

    def tangible_asset_plan_decision(self, *args, **kwargs):
        """``tangible_asset_acquisition_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``tangible_asset_acquisition_decision`` instead."""
        warnings.warn(
            "tangible_asset_plan_decision() is deprecated; use tangible_asset_acquisition_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.tangible_asset_acquisition_decision(*args, **kwargs)

    def retirement_stock_investment_plan_decision(self, *args, **kwargs):
        """``other_corporation_securities_acquisition_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``other_corporation_securities_acquisition_decision`` instead."""
        warnings.warn(
            "retirement_stock_investment_plan_decision() is deprecated; use other_corporation_securities_acquisition_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.other_corporation_securities_acquisition_decision(*args, **kwargs)

    def retirement_stock_investment_transfer_decision(self, *args, **kwargs):
        """``other_corporation_securities_transfer_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``other_corporation_securities_transfer_decision`` instead."""
        warnings.warn(
            "retirement_stock_investment_transfer_decision() is deprecated; use other_corporation_securities_transfer_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.other_corporation_securities_transfer_decision(*args, **kwargs)

    def stock_related_bond_plan_decision(self, *args, **kwargs):
        """``stock_related_bond_acquisition_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``stock_related_bond_acquisition_decision`` instead."""
        warnings.warn(
            "stock_related_bond_plan_decision() is deprecated; use stock_related_bond_acquisition_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.stock_related_bond_acquisition_decision(*args, **kwargs)

    def corporate_law_decision(self, *args, **kwargs):
        """``company_merger_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``company_merger_decision`` instead."""
        warnings.warn(
            "corporate_law_decision() is deprecated; use company_merger_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.company_merger_decision(*args, **kwargs)

    def corporate_law_method_decision(self, *args, **kwargs):
        """``company_division_merger_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``company_division_merger_decision`` instead."""
        warnings.warn(
            "corporate_law_method_decision() is deprecated; use company_division_merger_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.company_division_merger_decision(*args, **kwargs)

    def stock_trading_other_decision(self, *args, **kwargs):
        """``stock_exchange_transfer_decision`` 의 옛 이름 (엔드포인트와 맞지 않았다). Deprecated, use ``stock_exchange_transfer_decision`` instead."""
        warnings.warn(
            "stock_trading_other_decision() is deprecated; use stock_exchange_transfer_decision() instead (endpoint-accurate name, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.stock_exchange_transfer_decision(*args, **kwargs)


class MajorShareholderDisclosure(MajorMattersReport):
    """``MajorMattersReport`` 의 옛 이름 (주요사항보고서는 주요주주 공시가 아니다). Deprecated, use ``MajorMattersReport`` instead."""

    def __init__(self, client: Client):
        warnings.warn(
            "MajorShareholderDisclosure is deprecated; use MajorMattersReport instead "
            "(it covers 주요사항보고서, not major-shareholder disclosures, 2026-11-04).",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(client)
