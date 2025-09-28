import datetime
import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._major_shareholder_disclosure import MajorShareholderDisclosure
from cluefin_openapi.dart._major_shareholder_disclosure_types import (
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


@pytest.fixture(scope="module")
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture(scope="module")
def service(client: Client) -> MajorShareholderDisclosure:
    return MajorShareholderDisclosure(client)


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
            "treasury_stock_acquisition_disposal_plan",
            TreasuryStockAcquisitionDisposalPlan,
            TreasuryStockAcquisitionDisposalPlanItem,
        ),
        (
            "real_estate_development",
            RealEstateDevelopment,
            RealEstateDevelopmentItem,
        ),
        (
            "business_letter",
            BusinessLetter,
            BusinessLetterItem,
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
            "securities_granted_decision",
            SecuritiesGrantedDecision,
            SecuritiesGrantedDecisionItem,
        ),
        (
            "free_securities_decision",
            FreeSecuritiesDecision,
            FreeSecuritiesDecisionItem,
        ),
        (
            "paid_in_capital_reduction_decision",
            PaidInCapitalReductionDecision,
            PaidInCapitalReductionDecisionItem,
        ),
        (
            "capital_reduction_decision",
            CapitalReductionDecision,
            CapitalReductionDecisionItem,
        ),
        (
            "government_bond_manager_replacement",
            GovernmentBondManagerReplacement,
            GovernmentBondManagerReplacementItem,
        ),
        (
            "profit_revocation",
            ProfitRevocation,
            ProfitRevocationItem,
        ),
        (
            "overseas_securities_trading_resolution",
            OverseasSecuritiesTradingResolution,
            OverseasSecuritiesTradingResolutionItem,
        ),
        (
            "overseas_securities_trading_delisting_resolution",
            OverseasSecuritiesTradingDelistingResolution,
            OverseasSecuritiesTradingDelistingResolutionItem,
        ),
        (
            "overseas_securities_trading_status",
            OverseasSecuritiesTradingStatus,
            OverseasSecuritiesTradingStatusItem,
        ),
        (
            "overseas_securities_trading_status_delisting",
            OverseasSecuritiesTradingStatusDelisting,
            OverseasSecuritiesTradingStatusDelistingItem,
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
            "corporate_bond_issuance_decision",
            CorporateBondIssuanceDecision,
            CorporateBondIssuanceDecisionItem,
        ),
        (
            "government_bond_manager_transfer_termination",
            GovernmentBondManagerTransferTermination,
            GovernmentBondManagerTransferTerminationItem,
        ),
        (
            "reorganization_plan_approved_ruling",
            ReorganizationPlanApprovedRuling,
            ReorganizationPlanApprovedRulingItem,
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
            TreasuryStockAcquisitionDisposalPlan,
            TreasuryStockAcquisitionDisposalPlanItem,
        ),
        (
            "treasury_stock_trust_contract_termination_decision",
            TreasuryStockTrustContractTerminationDecision,
            TreasuryStockTrustContractTerminationDecisionItem,
        ),
        (
            "business_plan_decision",
            BusinessPlanDecision,
            BusinessPlanDecisionItem,
        ),
        (
            "business_transfer_decision",
            BusinessTransferDecision,
            BusinessTransferDecisionItem,
        ),
        (
            "tangible_asset_plan_decision",
            TangibleAssetPlanDecision,
            TangibleAssetPlanDecisionItem,
        ),
        (
            "tangible_asset_transfer_decision",
            TangibleAssetTransferDecision,
            TangibleAssetTransferDecisionItem,
        ),
        (
            "retirement_stock_investment_plan_decision",
            RetirementStockInvestmentPlanDecision,
            RetirementStockInvestmentPlanDecisionItem,
        ),
        (
            "retirement_stock_investment_transfer_decision",
            RetirementStockInvestmentTransferDecision,
            RetirementStockInvestmentTransferDecisionItem,
        ),
        (
            "stock_related_bond_plan_decision",
            StockRelatedBondPlanDecision,
            StockRelatedBondPlanDecisionItem,
        ),
        (
            "stock_related_bond_transfer_decision",
            StockRelatedBondTransferDecision,
            StockRelatedBondTransferDecisionItem,
        ),
        (
            "corporate_law_decision",
            CorporateLawDecision,
            CorporateLawDecisionItem,
        ),
        (
            "corporate_division_decision",
            CorporateDivisionDecision,
            CorporateDivisionDecisionItem,
        ),
        (
            "corporate_law_method_decision",
            CorporateLawMethodDecision,
            CorporateLawMethodDecisionItem,
        ),
        (
            "stock_trading_other_decision",
            StockTradingOtherDecision,
            StockTradingOtherDecisionItem,
        ),
    ],
)
def test_major_shareholder_disclosure_endpoints(
    service: MajorShareholderDisclosure,
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
