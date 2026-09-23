import pytest

from cluefin_openapi.kis import _domestic_account as domestic_account_module
from cluefin_openapi.kis._domestic_account import DomesticAccount

from ._case_runner import CASE_FIELDS, load_cases, run_case

DOMESTIC_ACCOUNT_CASES = load_cases("domestic_account_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, DOMESTIC_ACCOUNT_CASES)
def test_domestic_account_builds_request(
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
        module=domestic_account_module,
        wrapper_cls=DomesticAccount,
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
