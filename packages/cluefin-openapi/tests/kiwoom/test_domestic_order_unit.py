import pytest

from cluefin_openapi.kiwoom import _domestic_order as domestic_order_module
from cluefin_openapi.kiwoom._domestic_order import DomesticOrder

from ._helpers import EndpointCase, run_post_case


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


ORDER_CASES = [
    EndpointCase(
        name="buy_order",
        method_name="request_buy_order",
        response_model_attr="DomesticOrderBuy",
        api_id="kt10000",
        call_kwargs={
            "dmst_stex_tp": "KRX",
            "stk_cd": "005930",
            "ord_qty": "10",
            "trde_tp": "0",
            "ord_uv": "70000",
            "cond_uv": "69000",
        },
        expected_body={
            "dmst_stex_tp": "KRX",
            "stk_cd": "005930",
            "ord_qty": "10",
            "trde_tp": "0",
            "ord_uv": "70000",
            "cond_uv": "69000",
        },
        response_payload=payload("buy_order"),
    ),
    EndpointCase(
        name="sell_order",
        method_name="request_sell_order",
        response_model_attr="DomesticOrderSell",
        api_id="kt10001",
        call_kwargs={
            "dmst_stex_tp": "KRX",
            "stk_cd": "005930",
            "ord_qty": "5",
            "trde_tp": "0",
            "ord_uv": "71000",
            "cond_uv": "70500",
        },
        expected_body={
            "dmst_stex_tp": "KRX",
            "stk_cd": "005930",
            "ord_qty": "5",
            "trde_tp": "0",
            "ord_uv": "71000",
            "cond_uv": "70500",
        },
        response_payload=payload("sell_order"),
    ),
    EndpointCase(
        name="modify_order",
        method_name="request_modify_order",
        response_model_attr="DomesticOrderModify",
        api_id="kt10002",
        call_kwargs={
            "dmst_stex_tp": "KRX",
            "orig_ord_no": "123456",
            "stk_cd": "005930",
            "mdfy_qty": "5",
            "mdfy_uv": "70500",
            "mdfy_cond_uv": "69500",
        },
        expected_body={
            "dmst_stex_tp": "KRX",
            "orig_ord_no": "123456",
            "stk_cd": "005930",
            "mdfy_qty": "5",
            "mdfy_uv": "70500",
            "mdfy_cond_uv": "69500",
        },
        response_payload=payload("modify_order"),
    ),
    EndpointCase(
        name="cancel_order",
        method_name="request_cancel_order",
        response_model_attr="DomesticOrderCancel",
        api_id="kt10003",
        call_kwargs={
            "dmst_stex_tp": "KRX",
            "orig_ord_no": "123456",
            "stk_cd": "005930",
            "cncl_qty": "0",
        },
        expected_body={
            "dmst_stex_tp": "KRX",
            "orig_ord_no": "123456",
            "stk_cd": "005930",
            "cncl_qty": "0",
        },
        response_payload=payload("cancel_order"),
    ),
]


@pytest.mark.parametrize("case", ORDER_CASES, ids=lambda case: case.name)
def test_domestic_order_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        domestic_order_module,
        DomesticOrder,
        case,
        base_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
