import pytest
import requests_mock

from cluefin_openapi.dart import _major_shareholder_disclosure_types as types
from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._major_shareholder_disclosure import MajorMattersReport, MajorShareholderDisclosure

from ._helpers import build_payload

BASE_URL = "https://opendart.fss.or.kr"
AUTH_KEY = "test-auth-key"

METHOD_SPECS = [
    (
        "asset_transfer_putback_option",
        "/api/astInhtrfEtcPtbkOpt.json",
        types.AssetTransferPutbackOption,
        types.AssetTransferPutbackOptionItem,
    ),
    (
        "default_occurrence",
        "/api/dfOcr.json",
        types.DefaultOccurrence,
        types.DefaultOccurrenceItem,
    ),
    (
        "business_suspension",
        "/api/bsnSp.json",
        types.BusinessSuspension,
        types.BusinessSuspensionItem,
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
        "paid_in_capital_increase_decision",
        "/api/piicDecsn.json",
        types.PaidInCapitalIncreaseDecision,
        types.PaidInCapitalIncreaseDecisionItem,
    ),
    (
        "free_capital_increase_decision",
        "/api/fricDecsn.json",
        types.FreeCapitalIncreaseDecision,
        types.FreeCapitalIncreaseDecisionItem,
    ),
    (
        "paid_in_and_free_capital_increase_decision",
        "/api/pifricDecsn.json",
        types.PaidInAndFreeCapitalIncreaseDecision,
        types.PaidInAndFreeCapitalIncreaseDecisionItem,
    ),
    (
        "capital_reduction_decision",
        "/api/crDecsn.json",
        types.CapitalReductionDecision,
        types.CapitalReductionDecisionItem,
    ),
    (
        "creditor_bank_management_procedure_commencement",
        "/api/bnkMngtPcbg.json",
        types.CreditorBankManagementProcedureCommencement,
        types.CreditorBankManagementProcedureCommencementItem,
    ),
    (
        "lawsuit_filing",
        "/api/lwstLg.json",
        types.LawsuitFiling,
        types.LawsuitFilingItem,
    ),
    (
        "overseas_securities_market_listing_decision",
        "/api/ovLstDecsn.json",
        types.OverseasSecuritiesMarketListingDecision,
        types.OverseasSecuritiesMarketListingDecisionItem,
    ),
    (
        "overseas_securities_market_delisting_decision",
        "/api/ovDlstDecsn.json",
        types.OverseasSecuritiesMarketDelistingDecision,
        types.OverseasSecuritiesMarketDelistingDecisionItem,
    ),
    (
        "overseas_securities_market_listing_status",
        "/api/ovLst.json",
        types.OverseasSecuritiesMarketListingStatus,
        types.OverseasSecuritiesMarketListingStatusItem,
    ),
    (
        "overseas_securities_market_delisting_status",
        "/api/ovDlst.json",
        types.OverseasSecuritiesMarketDelistingStatus,
        types.OverseasSecuritiesMarketDelistingStatusItem,
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
        "exchangeable_bond_issuance_decision",
        "/api/exbdIsDecsn.json",
        types.ExchangeableBondIssuanceDecision,
        types.ExchangeableBondIssuanceDecisionItem,
    ),
    (
        "creditor_bank_management_procedure_termination",
        "/api/bnkMngtPcsp.json",
        types.CreditorBankManagementProcedureTermination,
        types.CreditorBankManagementProcedureTerminationItem,
    ),
    (
        "write_down_contingent_capital_securities_issuance_decision",
        "/api/wdCocobdIsDecsn.json",
        types.WriteDownContingentCapitalSecuritiesIssuanceDecision,
        types.WriteDownContingentCapitalSecuritiesIssuanceDecisionItem,
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
        types.TreasuryStockTrustContractDecision,
        types.TreasuryStockTrustContractDecisionItem,
    ),
    (
        "treasury_stock_trust_contract_termination_decision",
        "/api/tsstkAqTrctrCcDecsn.json",
        types.TreasuryStockTrustContractTerminationDecision,
        types.TreasuryStockTrustContractTerminationDecisionItem,
    ),
    (
        "business_acquisition_decision",
        "/api/bsnInhDecsn.json",
        types.BusinessAcquisitionDecision,
        types.BusinessAcquisitionDecisionItem,
    ),
    (
        "business_transfer_decision",
        "/api/bsnTrfDecsn.json",
        types.BusinessTransferDecision,
        types.BusinessTransferDecisionItem,
    ),
    (
        "tangible_asset_acquisition_decision",
        "/api/tgastInhDecsn.json",
        types.TangibleAssetAcquisitionDecision,
        types.TangibleAssetAcquisitionDecisionItem,
    ),
    (
        "tangible_asset_transfer_decision",
        "/api/tgastTrfDecsn.json",
        types.TangibleAssetTransferDecision,
        types.TangibleAssetTransferDecisionItem,
    ),
    (
        "other_corporation_securities_acquisition_decision",
        "/api/otcprStkInvscrInhDecsn.json",
        types.OtherCorporationSecuritiesAcquisitionDecision,
        types.OtherCorporationSecuritiesAcquisitionDecisionItem,
    ),
    (
        "other_corporation_securities_transfer_decision",
        "/api/otcprStkInvscrTrfDecsn.json",
        types.OtherCorporationSecuritiesTransferDecision,
        types.OtherCorporationSecuritiesTransferDecisionItem,
    ),
    (
        "stock_related_bond_acquisition_decision",
        "/api/stkrtbdInhDecsn.json",
        types.StockRelatedBondAcquisitionDecision,
        types.StockRelatedBondAcquisitionDecisionItem,
    ),
    (
        "stock_related_bond_transfer_decision",
        "/api/stkrtbdTrfDecsn.json",
        types.StockRelatedBondTransferDecision,
        types.StockRelatedBondTransferDecisionItem,
    ),
    (
        "company_merger_decision",
        "/api/cmpMgDecsn.json",
        types.CompanyMergerDecision,
        types.CompanyMergerDecisionItem,
    ),
    (
        "corporate_division_decision",
        "/api/cmpDvDecsn.json",
        types.CorporateDivisionDecision,
        types.CorporateDivisionDecisionItem,
    ),
    (
        "company_division_merger_decision",
        "/api/cmpDvmgDecsn.json",
        types.CompanyDivisionMergerDecision,
        types.CompanyDivisionMergerDecisionItem,
    ),
    (
        "stock_exchange_transfer_decision",
        "/api/stkExtrDecsn.json",
        types.StockExchangeTransferDecision,
        types.StockExchangeTransferDecisionItem,
    ),
]


@pytest.fixture
def client() -> Client:
    return Client(auth_key=AUTH_KEY)


@pytest.mark.parametrize(
    ("method_name", "endpoint", "response_model", "list_model"),
    METHOD_SPECS,
)
def test_major_shareholder_disclosure_calls_expected_endpoint(
    client: Client,
    method_name: str,
    endpoint: str,
    response_model,
    list_model,
) -> None:
    service = MajorMattersReport(client)
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
    service = MajorMattersReport(client)

    monkeypatch.setattr(client, "_get", lambda *_, **__: ["unexpected"])

    method = getattr(service, method_name)

    with pytest.raises(TypeError):
        method("00126380", "20240101", "20240131")


def test_major_shareholder_disclosure_endpoint_paths_are_unique() -> None:
    """서로 다른 메서드가 같은 경로를 부르면 한쪽이 엉뚱한 공시를 돌려준다 (유형자산 양도 ↔ 영업양도 사례)."""
    endpoints = [spec[1] for spec in METHOD_SPECS]

    assert len(set(endpoints)) == len(endpoints)


def test_corporate_law_decision_accepts_response_without_external_evaluation_opinion(client: Client) -> None:
    """회사합병결정 실응답에는 exevl_op(외부평가 의견)가 없다 — 분할합병결정에만 있는 필드다."""
    service = MajorMattersReport(client)
    payload = build_payload(types.CompanyMergerDecisionItem)
    del payload["list"][0]["exevl_op"]

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(f"{BASE_URL}/api/cmpMgDecsn.json", json=payload, status_code=200)

        result = service.company_merger_decision("00126380", "20240101", "20240131")

    assert result.result.list is not None
    assert result.result.list[0].exevl_op is None


# 2026-10-17 실측: 실서버는 금액·주식수를 콤마 문자열로, 값이 없으면 "-" 로 보낸다. 이 필드들을 int/float 로
# 선언했던 8종은 실데이터마다 int_parsing 으로 응답 전체가 거부됐다 (VENDOR_DOC_ERRATA.md).
LIVE_SHAPED_VALUES = [
    (
        "paid_in_capital_increase_decision",
        "/api/piicDecsn.json",
        types.PaidInCapitalIncreaseDecisionItem,
        {"fdpp_op": "12,345,678,900", "bfic_tisstk_estk": "-", "nstk_ostk_cnt": "1,234,567", "fv_ps": "500"},
    ),
    (
        "free_capital_increase_decision",
        "/api/fricDecsn.json",
        types.FreeCapitalIncreaseDecisionItem,
        {"nstk_ascnt_ps_ostk": "0.5", "nstk_ascnt_ps_estk": "-", "bfic_tisstk_ostk": "9,876,543"},
    ),
    (
        "paid_in_and_free_capital_increase_decision",
        "/api/pifricDecsn.json",
        types.PaidInAndFreeCapitalIncreaseDecisionItem,
        {"piic_fdpp_op": "1,000,000,000", "fric_nstk_estk_cnt": "-", "fric_od_a_at_t": "3"},
    ),
    (
        "capital_reduction_decision",
        "/api/crDecsn.json",
        types.CapitalReductionDecisionItem,
        {"bfcr_cpt": "123,456,789,000", "atcr_tisstk_estk": "-", "fv_ps": "5,000"},
    ),
    ("default_occurrence", "/api/dfOcr.json", types.DefaultOccurrenceItem, {"df_amt": "1,234,567,890"}),
    (
        "business_suspension",
        "/api/bsnSp.json",
        types.BusinessSuspensionItem,
        {"bsnsp_amt": "1,234,567,890,000", "rsl": "98,765,432,100", "od_a_at_b": "-"},
    ),
    ("dissolution_occurrence", "/api/dsRsOcr.json", types.DissolutionOccurrenceItem, {"od_a_at_t": "-"}),
    (
        "asset_transfer_putback_option",
        "/api/astInhtrfEtcPtbkOpt.json",
        types.AssetTransferPutbackOptionItem,
        {"ast_inhtrf_prc": "-"},
    ),
]


@pytest.mark.parametrize(("method_name", "endpoint", "item_type", "values"), LIVE_SHAPED_VALUES)
def test_major_event_amounts_pass_through_as_live_strings(
    client: Client, method_name: str, endpoint: str, item_type, values: dict
) -> None:
    service = MajorMattersReport(client)
    payload = build_payload(item_type, overrides=values)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(f"{BASE_URL}{endpoint}", json=payload, status_code=200)
        result = getattr(service, method_name)("00126380", "20240101", "20240131")

    item = result.result.list[0]
    for field_name, value in values.items():
        assert getattr(item, field_name) == value


def test_major_shareholder_disclosure_alias_warns_and_delegates(client: Client) -> None:
    """옛 클래스 이름(MajorShareholderDisclosure)은 지워지지 않고 경고와 함께 새 이름으로 위임한다."""
    with pytest.deprecated_call():
        service = MajorShareholderDisclosure(client)

    payload = build_payload(types.DefaultOccurrenceItem)
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(f"{BASE_URL}/api/dfOcr.json", json=payload, status_code=200)
        with pytest.deprecated_call():
            result = service.real_estate_development("00126380", "20240101", "20240131")

    assert isinstance(result, types.DefaultOccurrence)


def test_major_shareholder_disclosure_item_alias_warns(client: Client) -> None:
    """옛 Item 클래스 이름도 경고와 함께 새 모델로 그대로 쓸 수 있다."""
    payload = build_payload(types.DefaultOccurrenceItem)
    with pytest.deprecated_call():
        item = types.RealEstateDevelopmentItem(**payload["list"][0])

    assert isinstance(item, types.DefaultOccurrenceItem)
