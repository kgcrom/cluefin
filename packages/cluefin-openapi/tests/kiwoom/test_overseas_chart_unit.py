import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_chart as overseas_chart_module
from cluefin_openapi.kiwoom._overseas_chart import OverseasChart

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_tick_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "tic_scope": "1",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
    "get_minute_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "strt_dt": "20240102",
        "tic_scope": "1",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
    "get_daily_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "strt_dt": "20240102",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
    "get_weekly_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "strt_dt": "20240102",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
    "get_monthly_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "strt_dt": "20240102",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
    "get_yearly_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "strt_dt": "20240102",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
    "get_quarterly_chart": {
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "strt_dt": "20240102",
        "upd_stkpc_tp": "0",
        "exrt_appl_tp": "0",
    },
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasChart, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (OverseasChart\w+)\.model_validate", source).group(1)
    return api_id, model_attr


CHART_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    CHART_CASES.append(
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


@pytest.mark.parametrize("case", CHART_CASES, ids=lambda case: case.name)
def test_overseas_chart_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_chart_module,
        OverseasChart,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
