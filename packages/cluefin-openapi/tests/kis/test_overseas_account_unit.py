import pytest

from cluefin_openapi.kis import _overseas_account as overseas_account_module
from cluefin_openapi.kis._overseas_account import OverseasAccount
from cluefin_openapi.kis._overseas_account_types import StockBalance, StockBalanceItem1, StockBalanceItem2

from ._case_runner import CASE_FIELDS, load_cases, run_case

OVERSEAS_ACCOUNT_CASES = load_cases("overseas_account_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, OVERSEAS_ACCOUNT_CASES)
def test_overseas_account_builds_request(
    monkeypatch,
    method_name,
    response_model_attr,
    endpoint,
    method,
    call_kwargs,
    expected_headers,
    expected_body,
    response_payload,
):
    run_case(
        module=overseas_account_module,
        wrapper_cls=OverseasAccount,
        monkeypatch=monkeypatch,
        method_name=method_name,
        response_model_attr=response_model_attr,
        endpoint=endpoint,
        method=method,
        call_kwargs=call_kwargs,
        expected_headers=expected_headers,
        expected_body=expected_body,
        response_payload=response_payload,
    )


def test_stock_balance_parses_real_response_model() -> None:
    """run_case 는 DummyResponseModel 로 검증해 실제 응답 모델은 한 번도 파싱되지 않는다.

    StockBalance 를 실제 모델로 검증해 output1(list)/output2(단일 객체) 파싱을 확인한다.
    """
    item1 = {field_name: "" for field_name in StockBalanceItem1.model_fields}
    item1["ovrs_pdno"] = "AAPL"
    item1["ovrs_item_name"] = "Apple Inc"
    item1["ovrs_cblc_qty"] = "10"

    item2 = {field_name: "" for field_name in StockBalanceItem2.model_fields}
    item2["tot_evlu_pfls_amt"] = "1234.56"

    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "ctx_area_fk200": "",
        "ctx_area_nk200": "",
        "output1": [item1],
        "output2": item2,
    }

    body = StockBalance.model_validate(payload)

    assert body.output1[0].ovrs_pdno == "AAPL"
    assert body.output1[0].ovrs_item_name == "Apple Inc"
    assert body.output2.tot_evlu_pfls_amt == "1234.56"
