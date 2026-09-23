import pytest

from cluefin_openapi.kis import _overseas_market_analysis as overseas_market_analysis_module
from cluefin_openapi.kis._overseas_market_analysis import OverseasMarketAnalysis

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
