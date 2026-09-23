import pytest

from cluefin_openapi.kis import _onmarket_bond_basic_quote as onmarket_bond_basic_quote_module
from cluefin_openapi.kis._onmarket_bond_basic_quote import OnmarketBondBasicQuote

from ._case_runner import CASE_FIELDS, load_cases, run_case

ONMARKET_BOND_BASIC_QUOTE_CASES = load_cases("onmarket_bond_basic_quote_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, ONMARKET_BOND_BASIC_QUOTE_CASES)
def test_onmarket_bond_basic_quote_builds_request(
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
        module=onmarket_bond_basic_quote_module,
        wrapper_cls=OnmarketBondBasicQuote,
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
