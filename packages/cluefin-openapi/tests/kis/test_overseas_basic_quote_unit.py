import pytest

from cluefin_openapi.kis import _overseas_basic_quote as overseas_basic_quote_module
from cluefin_openapi.kis._overseas_basic_quote import BasicQuote
from cluefin_openapi.kis._overseas_basic_quote_types import (
    ConclusionTrend,
    ConclusionTrendMeta,
    StockCurrentPriceDetail,
    StockCurrentPriceDetailItem,
)

from ._case_runner import CASE_FIELDS, load_cases, run_case

OVERSEAS_BASIC_QUOTE_CASES = load_cases("overseas_basic_quote_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, OVERSEAS_BASIC_QUOTE_CASES)
def test_overseas_basic_quote_builds_request(
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
        module=overseas_basic_quote_module,
        wrapper_cls=BasicQuote,
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


def test_stock_current_price_detail_parses_real_response_model() -> None:
    """run_case 는 DummyResponseModel 로 검증해 실제 응답 모델은 한 번도 파싱되지 않는다."""
    item = {field_name: "" for field_name in StockCurrentPriceDetailItem.model_fields}
    item["rsym"] = "DNASAAPL"
    item["last"] = "150.00"
    item["curr"] = "USD"

    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": item,
    }

    body = StockCurrentPriceDetail.model_validate(payload)

    assert body.output.rsym == "DNASAAPL"
    assert body.output.last == "150.00"
    assert body.output.curr == "USD"


def test_conclusion_trend_empty_list_output1_becomes_none() -> None:
    """서버가 output1 을 객체 대신 빈 리스트로 보내는 경우가 있다."""
    payload = {"rt_cd": "0", "msg_cd": "MCA00000", "msg1": "정상처리 되었습니다.", "output1": [], "output2": []}

    body = ConclusionTrend.model_validate(payload)

    assert body.output1 is None
    assert body.output2 == []


def test_conclusion_trend_object_output1_is_parsed() -> None:
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": {"rsym": "DNASTSLA", "zdiv": "4", "nrec": "0"},
        "output2": [],
    }

    body = ConclusionTrend.model_validate(payload)

    assert body.output1 == ConclusionTrendMeta(rsym="DNASTSLA", zdiv="4", nrec="0")
