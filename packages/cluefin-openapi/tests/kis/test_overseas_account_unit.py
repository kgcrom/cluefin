import pytest

from cluefin_openapi.kis import _overseas_account as overseas_account_module
from cluefin_openapi.kis._overseas_account import OverseasAccount

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
