import os
import time

import dotenv
import pytest
import requests_mock

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_theme_types import (
    DomesticThemeGroup,
    DomesticThemeGroupStocks,
)


@pytest.fixture
def client() -> Client:
    return Client(token="test_token", env="dev")


def test_get_theme_group(client: Client):
    expected_data = {
        "thema_grp": [
            {
                "thema_grp_cd": "319",
                "thema_nm": "건강식품",
                "stk_num": "5",
                "flu_sig": "2",
                "flu_rt": "+0.02",
                "rising_stk_num": "1",
                "fall_stk_num": "0",
                "dt_prft_rt": "+157.80",
                "main_stk": "삼성전자",
            },
            {
                "thema_grp_cd": "452",
                "thema_nm": "SNS(Social Network Service)",
                "stk_num": "3",
                "flu_sig": "5",
                "flu_rt": "-0.09",
                "rising_stk_num": "0",
                "fall_stk_num": "1",
                "dt_prft_rt": "+67.60",
                "main_stk": "삼성전자",
            },
            {
                "thema_grp_cd": "553",
                "thema_nm": "반도체_후공정장비",
                "stk_num": "5",
                "flu_sig": "5",
                "flu_rt": "-0.27",
                "rising_stk_num": "0",
                "fall_stk_num": "1",
                "dt_prft_rt": "+56.88",
                "main_stk": "삼성전자",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/thme",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90001"},
        )

        response = client.theme.get_theme_group(
            qry_tp=1,
            date_tp="1",
            thema_nm="test",
            flu_pl_amt_tp=1,
            stex_tp=1,
        )
        assert response.headers is not None
        assert response.body is not None
        assert isinstance(response.body, DomesticThemeGroup)


def test_get_theme_group_stocks(client: Client):
    expected_data = {
        "flu_rt": "0.00",
        "dt_prft_rt": "0.00",
        "thema_comp_stk": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "57800",
                "flu_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "0",
                "sel_bid": "0",
                "sel_req": "0",
                "buy_bid": "0",
                "buy_req": "0",
                "dt_prft_rt_n": "0.00",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "36700",
                "flu_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "0",
                "sel_bid": "0",
                "sel_req": "0",
                "buy_bid": "0",
                "buy_req": "0",
                "dt_prft_rt_n": "0.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/thme",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90002"},
        )

    response = client.theme.get_theme_group_stocks(date_tp="2", thema_grp_cd="100", stex_tp="1")
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticThemeGroupStocks)
