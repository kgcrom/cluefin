import pytest

from cluefin_openapi.kis import _overseas_market_analysis as overseas_market_analysis_module
from cluefin_openapi.kis._overseas_market_analysis import OverseasMarketAnalysis
from cluefin_openapi.kis._overseas_market_analysis_types import (
    StockPriceFluctuation,
    StockPriceFluctuationItem1,
    StockPriceFluctuationItem2,
)

from ._case_runner import CASE_FIELDS, load_cases, run_case

OVERSEAS_MARKET_ANALYSIS_CASES = load_cases("overseas_market_analysis_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, OVERSEAS_MARKET_ANALYSIS_CASES)
def test_overseas_market_analysis_builds_request(
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
    # run_case also asserts isinstance(result, KisHttpResponse) — see _case_runner.run_case.
    run_case(
        module=overseas_market_analysis_module,
        wrapper_cls=OverseasMarketAnalysis,
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


def test_stock_price_fluctuation_parses_real_response_model() -> None:
    """run_case 는 DummyResponseModel 로 검증해 실제 응답 모델은 한 번도 파싱되지 않는다."""
    item1 = {field_name: "" for field_name in StockPriceFluctuationItem1.model_fields}
    item1["nrec"] = "1"

    item2 = {field_name: "" for field_name in StockPriceFluctuationItem2.model_fields}
    item2["symb"] = "AAPL"
    item2["knam"] = "애플"
    item2["rate"] = "12.34"

    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": item1,
        "output2": [item2],
    }

    body = StockPriceFluctuation.model_validate(payload)

    assert body.output1.nrec == "1"
    assert body.output2[0].symb == "AAPL"
    assert body.output2[0].knam == "애플"
