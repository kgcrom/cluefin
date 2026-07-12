import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_exchange as overseas_exchange_module
from cluefin_openapi.kiwoom._overseas_exchange import OverseasExchange

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_estimated_exchange_amount": {"exch_tp": "1", "fc_exmn_amt": "10"},
    "get_exchange_rate": {"exch_tp": "1"},
    "request_exchange": {"exch_tp": "1", "fc_exmn_amt": "10"},
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasExchange, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"res_body = (\w+)\.model_validate", source).group(1)
    return api_id, model_attr


EXCHANGE_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_").removeprefix("request_")
    EXCHANGE_CASES.append(
        EndpointCase(
            name=case_name,
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(kwargs),
            expected_body=dict(kwargs),
            response_payload=payload(case_name),
        )
    )


@pytest.mark.parametrize("case", EXCHANGE_CASES, ids=lambda case: case.name)
def test_overseas_exchange_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_exchange_module,
        OverseasExchange,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
