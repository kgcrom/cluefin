import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_order as overseas_order_module
from cluefin_openapi.kiwoom._overseas_order import OverseasOrder

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "request_buy_order": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "ord_qty": "1",
        "trde_tp": "00",
        "ord_uv": "1.00",
    },
    "request_sell_order": {
        "stk_cd": "AAPL",
        "stex_tp": "ND",
        "ord_qty": "1",
        "trde_tp": "00",
        "ord_uv": "1.00",
    },
    "request_modify_order": {
        "orig_ord_no": "0000000",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "mdfy_uv": "1.00",
    },
    "request_cancel_order": {
        "orig_ord_no": "0000000",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
    },
    "get_orderable_quantity": {
        "stk_cd": "AAPL",
        "uv": "1.00",
        "stex_tp": "ND",
    },
}

# Methods where the request body differs from the call kwargs.
EXPECTED_BODY = {
    "request_modify_order": {
        "orig_ord_no": "0000000",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "mdfy_uv": "1.00",
        "stop_pric": "",
    },
    "request_sell_order": {
        "stk_cd": "AAPL",
        "stex_tp": "ND",
        "ord_qty": "1",
        "ord_uv": "1.00",
        "stop_pric": "",
        "trde_tp": "00",
    },
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasOrder, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (OverseasOrder\w+)\.model_validate", source).group(1)
    return api_id, model_attr


ORDER_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("request_").removeprefix("get_")
    ORDER_CASES.append(
        EndpointCase(
            name=case_name,
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(kwargs),
            expected_body=dict(EXPECTED_BODY.get(method_name, kwargs)),
            response_payload=payload(case_name),
        )
    )


@pytest.mark.parametrize("case", ORDER_CASES, ids=lambda case: case.name)
def test_overseas_order_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_order_module,
        OverseasOrder,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
