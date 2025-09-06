"""Tests for the Auth class."""

import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_foreign import DomesticForeign
from cluefin_openapi.kiwoom._domestic_foreign_types import (
    DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner,
    DomesticForeignInvestorTradingTrendByStock,
    DomesticForeignStockInstitution,
)


@pytest.fixture
def client():
    return Client(
        token="test_token",
        env="dev",
    )


def test_get_foreign_investor_trading_trend_by_stock(client: Client):
    expected_data = {
        "stk_frgnr": [
            {
                "dt": "20241105",
                "close_pric": "135300",
                "pred_pre": "0",
                "trde_qty": "0",
                "chg_qty": "0",
                "poss_stkcnt": "6663509",
                "wght": "+26.10",
                "gain_pos_stkcnt": "18863197",
                "frgnr_limit": "25526706",
                "frgnr_limit_irds": "0",
                "limit_exh_rt": "+26.10",
            },
            {
                "dt": "20241101",
                "close_pric": "65100",
                "pred_pre": "0",
                "trde_qty": "0",
                "chg_qty": "-3441",
                "poss_stkcnt": "6642402",
                "wght": "+26.02",
                "gain_pos_stkcnt": "18884304",
                "frgnr_limit": "25526706",
                "frgnr_limit_irds": "0",
                "limit_exh_rt": "+26.02",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/frgnistt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10008"},
        )

        response = client.foreign.get_foreign_investor_trading_trend_by_stock("005930")

        assert isinstance(response.body, DomesticForeignInvestorTradingTrendByStock)
        assert response.body.stk_frgnr[0].dt == "20241105"
        assert response.body.stk_frgnr[0].close_pric == "135300"


def test_get_stock_institution(client: Client):
    expected_data = {
        "date": "20241105",
        "close_pric": "135300",
        "pre": "0",
        "orgn_dt_acc": "",
        "orgn_daly_nettrde": "",
        "frgnr_daly_nettrde": "",
        "frgnr_qota_rt": "",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/frgnistt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10009"},
        )

        response = client.foreign.get_stock_institution("005930")

        assert isinstance(response.body, DomesticForeignStockInstitution)
        assert response.body.date == "20241105"
        assert response.body.close_pric == "135300"


def test_get_consecutive_net_buy_sell_status_by_institution_foreigner(client: Client):
    expected_data = {
        "orgn_frgnr_cont_trde_prst": [
            {
                "rank": "1",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "prid_stkpc_flu_rt": "-5.80",
                "orgn_nettrde_amt": "+48",
                "orgn_nettrde_qty": "+173",
                "orgn_cont_netprps_dys": "+1",
                "orgn_cont_netprps_qty": "+173",
                "orgn_cont_netprps_amt": "+48",
                "frgnr_nettrde_qty": "+0",
                "frgnr_nettrde_amt": "+0",
                "frgnr_cont_netprps_dys": "+1",
                "frgnr_cont_netprps_qty": "+1",
                "frgnr_cont_netprps_amt": "+0",
                "nettrde_qty": "+173",
                "nettrde_amt": "+48",
                "tot_cont_netprps_dys": "+2",
                "tot_cont_nettrde_qty": "+174",
                "tot_cont_netprps_amt": "+48",
            },
            {
                "rank": "2",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "prid_stkpc_flu_rt": "-4.21",
                "orgn_nettrde_amt": "+41",
                "orgn_nettrde_qty": "+159",
                "orgn_cont_netprps_dys": "+1",
                "orgn_cont_netprps_qty": "+159",
                "orgn_cont_netprps_amt": "+41",
                "frgnr_nettrde_qty": "+0",
                "frgnr_nettrde_amt": "+0",
                "frgnr_cont_netprps_dys": "+1",
                "frgnr_cont_netprps_qty": "+1",
                "frgnr_cont_netprps_amt": "+0",
                "nettrde_qty": "+159",
                "nettrde_amt": "+41",
                "tot_cont_netprps_dys": "+2",
                "tot_cont_nettrde_qty": "+160",
                "tot_cont_netprps_amt": "+42",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/frgnistt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10131"},
        )

        response = client.foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner(
            "1", "001", "0", "0", "1"
        )

        assert isinstance(response.body, DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner)
        assert response.body.orgn_frgnr_cont_trde_prst[0].stk_cd == "005930"
        assert response.body.orgn_frgnr_cont_trde_prst[0].stk_nm == "삼성전자"
