import pytest
import requests_mock
from _helpers import build_payload

from cluefin_openapi.dart import _major_shareholder_disclosure_types as types
from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._major_shareholder_disclosure import MajorShareholderDisclosure

BASE_URL = "https://opendart.fss.or.kr"
AUTH_KEY = "test-auth-key"

METHOD_SPECS = [
    (
        "treasury_stock_acquisition_disposal_plan",
        "/api/astInhtrfEtcPtbkOpt.json",
        types.TreasuryStockAcquisitionDisposalPlan,
        types.TreasuryStockAcquisitionDisposalPlanItem,
    ),
    (
        "real_estate_development",
        "/api/dfOcr.json",
        types.RealEstateDevelopment,
        types.RealEstateDevelopmentItem,
    ),
    (
        "business_letter",
        "/api/bsnSp.json",
        types.BusinessLetter,
        types.BusinessLetterItem,
    ),
    (
        "corporate_rehabilitation_proceedings",
        "/api/ctrcvsBgrq.json",
        types.CorporateRehabilitationProceedings,
        types.CorporateRehabilitationProceedingsItem,
    ),
    (
        "dissolution_occurrence",
        "/api/dsRsOcr.json",
        types.DissolutionOccurrence,
        types.DissolutionOccurrenceItem,
    ),
    (
        "securities_granted_decision",
        "/api/piicDecsn.json",
        types.SecuritiesGrantedDecision,
        types.SecuritiesGrantedDecisionItem,
    ),
    (
        "free_securities_decision",
        "/api/fricDecsn.json",
        types.FreeSecuritiesDecision,
        types.FreeSecuritiesDecisionItem,
    ),
    (
        "paid_in_capital_reduction_decision",
        "/api/pifricDecsn.json",
        types.PaidInCapitalReductionDecision,
        types.PaidInCapitalReductionDecisionItem,
    ),
    (
        "capital_reduction_decision",
        "/api/crDecsn.json",
        types.CapitalReductionDecision,
        types.CapitalReductionDecisionItem,
    ),
    (
        "government_bond_manager_replacement",
        "/api/bnkMngtPcbg.json",
        types.GovernmentBondManagerReplacement,
        types.GovernmentBondManagerReplacementItem,
    ),
    (
        "profit_revocation",
        "/api/lwstLg.json",
        types.ProfitRevocation,
        types.ProfitRevocationItem,
    ),
    (
        "overseas_securities_trading_resolution",
        "/api/ovLstDecsn.json",
        types.OverseasSecuritiesTradingResolution,
        types.OverseasSecuritiesTradingResolutionItem,
    ),
    (
        "overseas_securities_trading_delisting_resolution",
        "/api/ovDlstDecsn.json",
        types.OverseasSecuritiesTradingDelistingResolution,
        types.OverseasSecuritiesTradingDelistingResolutionItem,
    ),
    (
        "overseas_securities_trading_status",
        "/api/ovLst.json",
        types.OverseasSecuritiesTradingStatus,
        types.OverseasSecuritiesTradingStatusItem,
    ),
    (
        "overseas_securities_trading_status_delisting",
        "/api/ovDlst.json",
        types.OverseasSecuritiesTradingStatusDelisting,
        types.OverseasSecuritiesTradingStatusDelistingItem,
    ),
    (
        "convertible_bond_issuance_decision",
        "/api/cvbdIsDecsn.json",
        types.ConvertibleBondIssuanceDecision,
        types.ConvertibleBondIssuanceDecisionItem,
    ),
    (
        "new_stock_warrant_bond_issuance_decision",
        "/api/bdwtIsDecsn.json",
        types.NewStockWarrantBondIssuanceDecision,
        types.NewStockWarrantBondIssuanceDecisionItem,
    ),
    (
        "corporate_bond_issuance_decision",
        "/api/exbdIsDecsn.json",
        types.CorporateBondIssuanceDecision,
        types.CorporateBondIssuanceDecisionItem,
    ),
    (
        "government_bond_manager_transfer_termination",
        "/api/bnkMngtPcsp.json",
        types.GovernmentBondManagerTransferTermination,
        types.GovernmentBondManagerTransferTerminationItem,
    ),
    (
        "reorganization_plan_approved_ruling",
        "/api/wdCocobdIsDecsn.json",
        types.ReorganizationPlanApprovedRuling,
        types.ReorganizationPlanApprovedRulingItem,
    ),
    (
        "treasury_stock_acquisition_decision",
        "/api/tsstkAqDecsn.json",
        types.TreasuryStockAcquisitionDecision,
        types.TreasuryStockAcquisitionDecisionItem,
    ),
    (
        "treasury_stock_disposal_decision",
        "/api/tsstkDpDecsn.json",
        types.TreasuryStockDisposalDecision,
        types.TreasuryStockDisposalDecisionItem,
    ),
    (
        "treasury_stock_trust_contract_decision",
        "/api/tsstkAqTrctrCnsDecsn.json",
        types.TreasuryStockAcquisitionDisposalPlan,
        types.TreasuryStockAcquisitionDisposalPlanItem,
    ),
    (
        "treasury_stock_trust_contract_termination_decision",
        "/api/tsstkAqTrctrCcDecsn.json",
        types.TreasuryStockTrustContractTerminationDecision,
        types.TreasuryStockTrustContractTerminationDecisionItem,
    ),
    (
        "business_plan_decision",
        "/api/bsnInhDecsn.json",
        types.BusinessPlanDecision,
        types.BusinessPlanDecisionItem,
    ),
    (
        "business_transfer_decision",
        "/api/bsnTrfDecsn.json",
        types.BusinessTransferDecision,
        types.BusinessTransferDecisionItem,
    ),
    (
        "tangible_asset_plan_decision",
        "/api/tgastInhDecsn.json",
        types.TangibleAssetPlanDecision,
        types.TangibleAssetPlanDecisionItem,
    ),
    (
        "tangible_asset_transfer_decision",
        "/api/bsnTrfDecsn.json",
        types.TangibleAssetTransferDecision,
        types.TangibleAssetTransferDecisionItem,
    ),
    (
        "retirement_stock_investment_plan_decision",
        "/api/otcprStkInvscrInhDecsn.json",
        types.RetirementStockInvestmentPlanDecision,
        types.RetirementStockInvestmentPlanDecisionItem,
    ),
    (
        "retirement_stock_investment_transfer_decision",
        "/api/otcprStkInvscrTrfDecsn.json",
        types.RetirementStockInvestmentTransferDecision,
        types.RetirementStockInvestmentTransferDecisionItem,
    ),
    (
        "stock_related_bond_plan_decision",
        "/api/stkrtbdInhDecsn.json",
        types.StockRelatedBondPlanDecision,
        types.StockRelatedBondPlanDecisionItem,
    ),
    (
        "stock_related_bond_transfer_decision",
        "/api/stkrtbdTrfDecsn.json",
        types.StockRelatedBondTransferDecision,
        types.StockRelatedBondTransferDecisionItem,
    ),
    (
        "corporate_law_decision",
        "/api/cmpMgDecsn.json",
        types.CorporateLawDecision,
        types.CorporateLawDecisionItem,
    ),
    (
        "corporate_division_decision",
        "/api/cmpDvDecsn.json",
        types.CorporateDivisionDecision,
        types.CorporateDivisionDecisionItem,
    ),
    (
        "corporate_law_method_decision",
        "/api/cmpDvmgDecsn.json",
        types.CorporateLawMethodDecision,
        types.CorporateLawMethodDecisionItem,
    ),
    (
        "stock_trading_other_decision",
        "/api/stkExtrDecsn.json",
        types.StockTradingOtherDecision,
        types.StockTradingOtherDecisionItem,
    ),
]


@pytest.fixture
def client() -> Client:
    return Client(auth_key=AUTH_KEY)


@pytest.mark.parametrize(
    "method_name, endpoint, response_model, list_model",
    METHOD_SPECS,
)
def test_major_shareholder_disclosure_calls_expected_endpoint(
    client: Client,
    method_name: str,
    endpoint: str,
    response_model,
    list_model,
) -> None:
    service = MajorShareholderDisclosure(client)
    payload = build_payload(list_model)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(f"{BASE_URL}{endpoint}", json=payload, status_code=200)

        method = getattr(service, method_name)
        result = method("00126380", "20240101", "20240131")

        assert isinstance(result, response_model)
        assert result.result.status == "000"
        assert result.result.message == "정상적으로 처리되었습니다"
        assert result.result.list is not None
        assert len(result.result.list) == 1

        item = result.result.list[0]
        assert isinstance(item, list_model)
        payload_list = payload["list"]
        assert item.model_dump(by_alias=True) == payload_list[0]

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == [AUTH_KEY]
        assert last_request.qs["corp_code"] == ["00126380"]
        assert last_request.qs["bgn_de"] == ["20240101"]
        assert last_request.qs["end_de"] == ["20240131"]


@pytest.mark.parametrize("method_name", [spec[0] for spec in METHOD_SPECS])
def test_major_shareholder_disclosure_rejects_non_mapping(
    client: Client,
    monkeypatch: pytest.MonkeyPatch,
    method_name: str,
) -> None:
    service = MajorShareholderDisclosure(client)

    monkeypatch.setattr(client, "_get", lambda *_, **__: ["unexpected"])

    method = getattr(service, method_name)

    with pytest.raises(TypeError):
        method("00126380", "20240101", "20240131")
