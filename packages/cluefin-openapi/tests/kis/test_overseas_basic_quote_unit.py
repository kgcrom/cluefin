import pytest

from cluefin_openapi.kis import _overseas_basic_quote as overseas_basic_quote_module
from cluefin_openapi.kis._overseas_basic_quote import BasicQuote

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
