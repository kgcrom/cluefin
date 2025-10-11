import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _domestic_theme as theme_module
from cluefin_openapi.kiwoom._domestic_theme import DomesticTheme

from ._helpers import EndpointCase, run_post_case


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(DomesticTheme, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (DomesticTheme\w+)\.model_validate", source).group(1)
    return api_id, model_attr


theme_group_api, theme_group_model = method_metadata("get_theme_group")
theme_group_stocks_api, theme_group_stocks_model = method_metadata("get_theme_group_stocks")

THEME_CASES = [
    EndpointCase(
        name="theme_group",
        method_name="get_theme_group",
        response_model_attr=theme_group_model,
        api_id=theme_group_api,
        call_kwargs={
            "qry_tp": 1,
            "date_tp": "1",
            "thema_nm": "test",
            "flu_pl_amt_tp": 1,
            "stex_tp": 1,
        },
        expected_body={
            "qry_tp": 1,
            "date_tp": "1",
            "thema_nm": "test",
            "flu_pl_amt_tp": 1,
            "stex_tp": 1,
            "stk_cd": "",
        },
        response_payload=payload("theme_group"),
    ),
    EndpointCase(
        name="theme_group_stocks",
        method_name="get_theme_group_stocks",
        response_model_attr=theme_group_stocks_model,
        api_id=theme_group_stocks_api,
        call_kwargs={
            "date_tp": "2",
            "thema_grp_cd": "100",
            "stex_tp": "1",
        },
        expected_body={
            "thema_grp_cd": "100",
            "stex_tp": "1",
            "date_tp": "2",
        },
        response_payload=payload("theme_group_stocks"),
        cont_flag_key="cond-yn",
    ),
]


@pytest.mark.parametrize("case", THEME_CASES, ids=lambda case: case.name)
def test_domestic_theme_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        theme_module,
        DomesticTheme,
        case,
        base_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
