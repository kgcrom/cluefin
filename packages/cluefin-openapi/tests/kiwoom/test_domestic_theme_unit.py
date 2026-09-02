import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _domestic_theme as theme_module
from cluefin_openapi.kiwoom._domestic_theme import DomesticTheme
from cluefin_openapi.kiwoom._domestic_theme_types import DomesticThemeGroup, DomesticThemeGroupStocks

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
            "qry_tp": "1",
            "date_tp": "1",
            "thema_nm": "test",
            "flu_pl_amt_tp": "1",
            "stex_tp": "1",
        },
        expected_body={
            "qry_tp": "1",
            "date_tp": "1",
            "thema_nm": "test",
            "flu_pl_amt_tp": "1",
            "stex_tp": "1",
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


class TestResponseLengthTolerance:
    """문서의 길이 제약(20자)을 응답에 걸면 정상 데이터가 거부된다.

    2026-09-02 실측: 테마명이 20자를 넘는 그룹이 있어 `string_too_long` 으로 응답 전체가
    깨지고 desk 테마 탭이 빈 화면이 되었다.
    """

    def test_long_theme_name_is_accepted(self):
        long_name = "2차전지(전고체) 및 폐배터리 리사이클링 밸류체인"
        assert len(long_name) > 20

        body = DomesticThemeGroup.model_validate(
            {
                "return_code": 0,
                "return_msg": "OK",
                "thema_grp": [
                    {
                        "thema_grp_cd": "319",
                        "thema_nm": long_name,
                        "stk_num": "12",
                        "flu_sig": "2",
                        "flu_rt": "1.25",
                        "rising_stk_num": "8",
                        "fall_stk_num": "2",
                        "dt_prft_rt": "3.10",
                        "main_stk": "에코프로비엠, 포스코퓨처엠, 엘앤에프",
                    }
                ],
            }
        )
        assert body.thema_grp[0].thema_nm == long_name

    def test_long_stock_name_is_accepted(self):
        long_name = "코스닥글로벌세그먼트지수추종상장지수증권"
        body = DomesticThemeGroupStocks.model_validate(
            {
                "return_code": 0,
                "return_msg": "OK",
                "flu_rt": "1.25",
                "dt_prft_rt": "3.10",
                "thema_comp_stk": [{"stk_cd": "005930", "stk_nm": long_name, "cur_prc": "70000"}],
            }
        )
        assert body.thema_comp_stk[0].stk_nm == long_name
