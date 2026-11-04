import datetime
import os
import time
from pathlib import Path

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._major_shareholder_disclosure import MajorMattersReport
from cluefin_openapi.dart._major_shareholder_disclosure_types import (
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


@pytest.fixture(scope="module")
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture(scope="module")
def service(client: Client) -> MajorMattersReport:
    return MajorMattersReport(client)


@pytest.fixture(scope="module")
def default_query() -> dict[str, str]:
    end_date = datetime.date.today().strftime("%Y%m%d")
    return {
        "corp_code": "00126380",
        "bgn_de": "20150101",
        "end_de": end_date,
    }


@pytest.mark.integration
@pytest.mark.parametrize(
    ("method_name", "response_model", "item_model"),
    [
        (
            "asset_transfer_putback_option",
            AssetTransferPutbackOption,
            AssetTransferPutbackOptionItem,
        ),
        (
            "default_occurrence",
            DefaultOccurrence,
            DefaultOccurrenceItem,
        ),
        (
            "business_suspension",
            BusinessSuspension,
            BusinessSuspensionItem,
        ),
        (
            "corporate_rehabilitation_proceedings",
            CorporateRehabilitationProceedings,
            CorporateRehabilitationProceedingsItem,
        ),
        (
            "dissolution_occurrence",
            DissolutionOccurrence,
            DissolutionOccurrenceItem,
        ),
        (
            "paid_in_capital_increase_decision",
            PaidInCapitalIncreaseDecision,
            PaidInCapitalIncreaseDecisionItem,
        ),
        (
            "free_capital_increase_decision",
            FreeCapitalIncreaseDecision,
            FreeCapitalIncreaseDecisionItem,
        ),
        (
            "paid_in_and_free_capital_increase_decision",
            PaidInAndFreeCapitalIncreaseDecision,
            PaidInAndFreeCapitalIncreaseDecisionItem,
        ),
        (
            "capital_reduction_decision",
            CapitalReductionDecision,
            CapitalReductionDecisionItem,
        ),
        (
            "creditor_bank_management_procedure_commencement",
            CreditorBankManagementProcedureCommencement,
            CreditorBankManagementProcedureCommencementItem,
        ),
        (
            "lawsuit_filing",
            LawsuitFiling,
            LawsuitFilingItem,
        ),
        (
            "overseas_securities_market_listing_decision",
            OverseasSecuritiesMarketListingDecision,
            OverseasSecuritiesMarketListingDecisionItem,
        ),
        (
            "overseas_securities_market_delisting_decision",
            OverseasSecuritiesMarketDelistingDecision,
            OverseasSecuritiesMarketDelistingDecisionItem,
        ),
        (
            "overseas_securities_market_listing_status",
            OverseasSecuritiesMarketListingStatus,
            OverseasSecuritiesMarketListingStatusItem,
        ),
        (
            "overseas_securities_market_delisting_status",
            OverseasSecuritiesMarketDelistingStatus,
            OverseasSecuritiesMarketDelistingStatusItem,
        ),
        (
            "convertible_bond_issuance_decision",
            ConvertibleBondIssuanceDecision,
            ConvertibleBondIssuanceDecisionItem,
        ),
        (
            "new_stock_warrant_bond_issuance_decision",
            NewStockWarrantBondIssuanceDecision,
            NewStockWarrantBondIssuanceDecisionItem,
        ),
        (
            "exchangeable_bond_issuance_decision",
            ExchangeableBondIssuanceDecision,
            ExchangeableBondIssuanceDecisionItem,
        ),
        (
            "creditor_bank_management_procedure_termination",
            CreditorBankManagementProcedureTermination,
            CreditorBankManagementProcedureTerminationItem,
        ),
        (
            "write_down_contingent_capital_securities_issuance_decision",
            WriteDownContingentCapitalSecuritiesIssuanceDecision,
            WriteDownContingentCapitalSecuritiesIssuanceDecisionItem,
        ),
        (
            "treasury_stock_acquisition_decision",
            TreasuryStockAcquisitionDecision,
            TreasuryStockAcquisitionDecisionItem,
        ),
        (
            "treasury_stock_disposal_decision",
            TreasuryStockDisposalDecision,
            TreasuryStockDisposalDecisionItem,
        ),
        (
            "treasury_stock_trust_contract_decision",
            AssetTransferPutbackOption,
            AssetTransferPutbackOptionItem,
        ),
        (
            "treasury_stock_trust_contract_termination_decision",
            TreasuryStockTrustContractTerminationDecision,
            TreasuryStockTrustContractTerminationDecisionItem,
        ),
        (
            "business_acquisition_decision",
            BusinessAcquisitionDecision,
            BusinessAcquisitionDecisionItem,
        ),
        (
            "business_transfer_decision",
            BusinessTransferDecision,
            BusinessTransferDecisionItem,
        ),
        (
            "tangible_asset_acquisition_decision",
            TangibleAssetAcquisitionDecision,
            TangibleAssetAcquisitionDecisionItem,
        ),
        (
            "tangible_asset_transfer_decision",
            TangibleAssetTransferDecision,
            TangibleAssetTransferDecisionItem,
        ),
        (
            "other_corporation_securities_acquisition_decision",
            OtherCorporationSecuritiesAcquisitionDecision,
            OtherCorporationSecuritiesAcquisitionDecisionItem,
        ),
        (
            "other_corporation_securities_transfer_decision",
            OtherCorporationSecuritiesTransferDecision,
            OtherCorporationSecuritiesTransferDecisionItem,
        ),
        (
            "stock_related_bond_acquisition_decision",
            StockRelatedBondAcquisitionDecision,
            StockRelatedBondAcquisitionDecisionItem,
        ),
        (
            "stock_related_bond_transfer_decision",
            StockRelatedBondTransferDecision,
            StockRelatedBondTransferDecisionItem,
        ),
        (
            "company_merger_decision",
            CompanyMergerDecision,
            CompanyMergerDecisionItem,
        ),
        (
            "corporate_division_decision",
            CorporateDivisionDecision,
            CorporateDivisionDecisionItem,
        ),
        (
            "company_division_merger_decision",
            CompanyDivisionMergerDecision,
            CompanyDivisionMergerDecisionItem,
        ),
        (
            "stock_exchange_transfer_decision",
            StockExchangeTransferDecision,
            StockExchangeTransferDecisionItem,
        ),
    ],
)
def test_major_shareholder_disclosure_endpoints(
    service: MajorMattersReport,
    method_name: str,
    response_model,
    item_model,
    default_query: dict[str, str],
) -> None:
    time.sleep(1)

    response = getattr(service, method_name)(**default_query)

    assert isinstance(response, response_model)
    assert response.result.status in {"000", "013"}
    assert response.result.message

    items = response.result.list or []
    assert all(isinstance(item, item_model) for item in items)

    if items and hasattr(items[0], "corp_code"):
        assert all(item.corp_code == default_query["corp_code"] for item in items)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("method_name", "response_model", "item_model", "corp_code", "rcept_dt"),
    [
        # 2025 년 실제 공시 샘플 — 삼성전자 기본 조회는 013 이라 모델·경로 오류를 가린다.
        (
            "treasury_stock_trust_contract_decision",
            TreasuryStockTrustContractDecision,
            TreasuryStockTrustContractDecisionItem,
            "00446901",
            "20250331",
        ),
        (
            "tangible_asset_transfer_decision",
            TangibleAssetTransferDecision,
            TangibleAssetTransferDecisionItem,
            "00132725",
            "20250325",
        ),
        (
            "company_merger_decision",
            CompanyMergerDecision,
            CompanyMergerDecisionItem,
            "01204056",
            "20250331",
        ),
        (
            "company_division_merger_decision",
            CompanyDivisionMergerDecision,
            CompanyDivisionMergerDecisionItem,
            "00138792",
            "20250116",
        ),
    ],
)
def test_major_shareholder_disclosure_real_samples(
    service: MajorMattersReport,
    method_name: str,
    response_model,
    item_model,
    corp_code: str,
    rcept_dt: str,
) -> None:
    time.sleep(1)

    response = getattr(service, method_name)(corp_code=corp_code, bgn_de=rcept_dt, end_de=rcept_dt)

    assert isinstance(response, response_model)
    assert response.result.status == "000"
    assert response.result.list
    assert all(isinstance(item, item_model) for item in response.result.list)
