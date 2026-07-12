import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_market_condition as overseas_market_condition_module
from cluefin_openapi.kiwoom._overseas_market_condition import OverseasMarketCondition

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_current_price_stock_info": {"stex_tp": "ND", "stk_cd": "AAPL"},
    "get_current_price_ten_quotes": {"stex_tp": "ND", "stk_cd": "AAPL"},
    "get_detailed_execution_history": {"stex_tp": "ND", "stk_cd": "AAPL"},
    "get_daily_execution_history": {"stex_tp": "ND", "stk_cd": "AAPL", "base_dt": "20240102"},
    "get_daily_stock_price": {"stex_tp": "ND", "stk_cd": "AAPL", "base_dt": "20240102"},
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasMarketCondition, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (OverseasMarketCondition\w+)\.model_validate", source).group(1)
    return api_id, model_attr


MARKET_CONDITION_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    MARKET_CONDITION_CASES.append(
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


@pytest.mark.parametrize("case", MARKET_CONDITION_CASES, ids=lambda case: case.name)
def test_overseas_market_condition_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_market_condition_module,
        OverseasMarketCondition,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
