import os
import time
from datetime import datetime

import dotenv
import pytest
import requests_mock

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_rank_info_types import (
    DomesticRankInfoAfterHoursSinglePriceChangeRateRanking,
    DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity,
    DomesticRankInfoRapidlyIncreasingTotalSellOrders,
    DomesticRankInfoRapidlyIncreasingTradingVolume,
    DomesticRankInfoSameNetBuySellRanking,
    DomesticRankInfoStockSpecificSecuritiesFirmRanking,
    DomesticRankInfoTopConsecutiveNetBuySellByForeigners,
    DomesticRankInfoTopCurrentDayDeviationSources,
    DomesticRankInfoTopCurrentDayMajorTraders,
    DomesticRankInfoTopCurrentDayTradingVolume,
    DomesticRankInfoTopExpectedConclusionPercentageChange,
    DomesticRankInfoTopForeignAccountGroupTrading,
    DomesticRankInfoTopForeignerLimitExhaustionRate,
    DomesticRankInfoTopForeignerPeriodTrading,
    DomesticRankInfoTopIntradayTradingByInvestor,
    DomesticRankInfoTopLimitExhaustionRateForeigner,
    DomesticRankInfoTopMarginRatio,
    DomesticRankInfoTopNetBuyTraderRanking,
    DomesticRankInfoTopPercentageChangeFromPreviousDay,
    DomesticRankInfoTopPreviousDayTradingVolume,
    DomesticRankInfoTopRemainingOrderQuantity,
    DomesticRankInfoTopSecuritiesFirmTrading,
    DomesticRankInfoTopTransactionValue,
)


@pytest.fixture
def client() -> Client:
    return Client(token="test_token", env="dev")


def test_get_top_remaining_order_quantity(client: Client):
    expected_data = {
        "bid_req_upper": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+65000",
                "pred_pre_sig": "2",
                "pred_pre": "+6300",
                "trde_qty": "214670",
                "tot_sel_req": "1",
                "tot_buy_req": "22287",
                "netprps_req": "22286",
                "buy_rt": "2228700.00",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+13335",
                "pred_pre_sig": "2",
                "pred_pre": "+385",
                "trde_qty": "0",
                "tot_sel_req": "0",
                "tot_buy_req": "9946",
                "netprps_req": "9946",
                "buy_rt": "0.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10020"},
        )
        response = client.rank_info.get_top_remaining_order_quantity(
            mrkt_tp="001", sort_tp="1", trde_qty_tp="0000", stk_cnd="0", crd_cnd="0", stex_tp="1"
        )

        assert isinstance(response.body, DomesticRankInfoTopRemainingOrderQuantity)
        assert response.body.bid_req_upper[0].cur_prc == "+65000"


def test_get_rapidly_increasing_remaining_order_quantity(client: Client):
    expected_data = {
        "bid_req_sdnin": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "8680",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "int": "5000",
                "now": "10000",
                "sdnin_qty": "5000",
                "sdnin_rt": "+100.00",
                "tot_buy_qty": "0",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10021"},
        )
        response = client.rank_info.get_rapidly_increasing_remaining_order_quantity(
            mrkt_tp="001", trde_tp="1", sort_tp="1", tm_tp="30", trde_qty_tp="1", stk_cnd="0", stex_tp="1"
        )

        assert isinstance(response.body, DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity)
        assert response.body.bid_req_sdnin[0].now == "10000"


def test_get_rapidly_increasing_total_sell_orders(client: Client):
    expected_data = {
        "req_rt_sdnin": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74300",
                "pred_pre_sig": "2",
                "pred_pre": "+17000",
                "int": "+12600.00",
                "now_rt": "-21474836.00",
                "sdnin_rt": "-21474836.00",
                "tot_sel_req": "74",
                "tot_buy_req": "74337920",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10022"},
        )
        response = client.rank_info.get_rapidly_increasing_total_sell_orders(
            mrkt_tp="001", rt_tp="1", tm_tp="1", trde_qty_tp="5", stk_cnd="0", stex_tp="1"
        )

        assert isinstance(response.body, DomesticRankInfoRapidlyIncreasingTotalSellOrders)
        assert response.body.req_rt_sdnin[0].cur_prc == "+74300"


def test_get_rapidly_increasing_trading_volume(client: Client):
    expected_data = {
        "trde_qty_sdnin": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-152000",
                "pred_pre_sig": "5",
                "pred_pre": "-100",
                "flu_rt": "-0.07",
                "prev_trde_qty": "22532511",
                "now_trde_qty": "31103523",
                "sdnin_qty": "+8571012",
                "sdnin_rt": "+38.04",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-94400",
                "pred_pre_sig": "5",
                "pred_pre": "-100",
                "flu_rt": "-0.11",
                "prev_trde_qty": "25027263",
                "now_trde_qty": "30535372",
                "sdnin_qty": "+5508109",
                "sdnin_rt": "+22.01",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10023"},
        )

        response = client.rank_info.get_rapidly_increasing_trading_volume(
            mrkt_tp="000", sort_tp="1", tm_tp="2", trde_qty_tp="5", stk_cnd="0", pric_tp="0", stex_tp="1"
        )

        assert isinstance(response.body, DomesticRankInfoRapidlyIncreasingTradingVolume)
        assert response.body.trde_qty_sdnin[0].prev_trde_qty == "22532511"


def test_get_top_percentage_change_from_previous_day(client: Client):
    expected_data = {
        "pred_pre_flu_rt_upper": [
            {
                "stk_cls": "0",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "sel_req": "207",
                "buy_req": "3820638",
                "now_trde_qty": "446203",
                "cntr_str": "346.54",
                "cnt": "4",
            },
            {
                "stk_cls": "0",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+12000",
                "pred_pre_sig": "2",
                "pred_pre": "+2380",
                "flu_rt": "+24.74",
                "sel_req": "54",
                "buy_req": "0",
                "now_trde_qty": "6",
                "cntr_str": "500.00",
                "cnt": "1",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10027"},
        )
        response = client.rank_info.get_top_percentage_change_from_previous_day(
            mrkt_tp="000",
            sort_tp="1",
            trde_qty_cnd="0000",
            stk_cnd="0",
            crd_cnd="0",
            updown_incls="1",
            pric_cnd="0",
            trde_prica_cnd="0",
            stex_tp="1",
        )
        assert isinstance(response.body, DomesticRankInfoTopPercentageChangeFromPreviousDay)
        assert response.body.pred_pre_flu_rt_upper[0].buy_req == "3820638"


def test_get_top_expected_conclusion_percentage_change(client: Client):
    expected_data = {
        "exp_cntr_flu_rt_upper": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "exp_cntr_pric": "+48100",
                "base_pric": "37000",
                "pred_pre_sig": "1",
                "pred_pre": "+11100",
                "flu_rt": "+30.00",
                "exp_cntr_qty": "1",
                "sel_req": "0",
                "sel_bid": "0",
                "buy_bid": "0",
                "buy_req": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "exp_cntr_pric": "+40000",
                "base_pric": "34135",
                "pred_pre_sig": "2",
                "pred_pre": "+5865",
                "flu_rt": "+17.18",
                "exp_cntr_qty": "1",
                "sel_req": "1",
                "sel_bid": "+40000",
                "buy_bid": "+35370",
                "buy_req": "1",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10029"},
        )
        response = client.rank_info.get_top_expected_conclusion_percentage_change(
            mrkt_tp="000",
            sort_tp="1",
            trde_qty_cnd="0",
            stk_cnd="0",
            crd_cnd="0",
            pric_cnd="0",
            stex_tp="1",
        )
        assert isinstance(response.body, DomesticRankInfoTopExpectedConclusionPercentageChange)
        assert response.body.exp_cntr_flu_rt_upper[0].exp_cntr_pric == "+48100"


def test_get_top_current_day_trading_volume(client: Client):
    expected_data = {
        "tdy_trde_qty_upper": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-152000",
                "pred_pre_sig": "5",
                "pred_pre": "-100",
                "flu_rt": "-0.07",
                "trde_qty": "34954641",
                "pred_rt": "+155.13",
                "trde_tern_rt": "+48.21",
                "trde_amt": "5308092",
                "opmr_trde_qty": "0",
                "opmr_pred_rt": "0.00",
                "opmr_trde_rt": "+0.00",
                "opmr_trde_amt": "0",
                "af_mkrt_trde_qty": "0",
                "af_mkrt_pred_rt": "0.00",
                "af_mkrt_trde_rt": "+0.00",
                "af_mkrt_trde_amt": "0",
                "bf_mkrt_trde_qty": "0",
                "bf_mkrt_pred_rt": "0.00",
                "bf_mkrt_trde_rt": "+0.00",
                "bf_mkrt_trde_amt": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-42950",
                "pred_pre_sig": "5",
                "pred_pre": "-100",
                "flu_rt": "-0.23",
                "trde_qty": "34854261",
                "pred_rt": "+135.53",
                "trde_tern_rt": "+13.83",
                "trde_amt": "1501908",
                "opmr_trde_qty": "0",
                "opmr_pred_rt": "0.00",
                "opmr_trde_rt": "+0.00",
                "opmr_trde_amt": "0",
                "af_mkrt_trde_qty": "0",
                "af_mkrt_pred_rt": "0.00",
                "af_mkrt_trde_rt": "+0.00",
                "af_mkrt_trde_amt": "0",
                "bf_mkrt_trde_qty": "0",
                "bf_mkrt_pred_rt": "0.00",
                "bf_mkrt_trde_rt": "+0.00",
                "bf_mkrt_trde_amt": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10039"},
        )

        response = client.rank_info.get_top_current_day_trading_volume(
            mrkt_tp="000",
            sort_tp="1",
            mang_stk_incls="0",
            crd_tp="0",
            trde_qty_tp="0",
            pric_tp="0",
            trde_prica_tp="0",
            mrkt_open_tp="0",
            stex_tp="1",
        )
        assert isinstance(response.body, DomesticRankInfoTopCurrentDayTradingVolume)
        assert response.body.tdy_trde_qty_upper[0].trde_amt == "5308092"


def test_get_top_previous_day_trading_volume(client: Client):
    excepted_data = {
        "pred_trde_qty_upper": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "81",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "trde_qty": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "2050",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "trde_qty": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=excepted_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10031"},
        )
        response = client.rank_info.get_top_previous_day_trading_volume(
            mrkt_tp="101", qry_tp="1", rank_strt="0", rank_end="10", stex_tp="1"
        )
        assert isinstance(response.body, DomesticRankInfoTopPreviousDayTradingVolume)
        assert response.body.pred_trde_qty_upper[0].pred_pre_sig == "3"


def test_get_top_transaction_value(client: Client):
    expected_data = {
        "trde_prica_upper": [
            {
                "stk_cd": "005930",
                "now_rank": "1",
                "pred_rank": "1",
                "stk_nm": "삼성전자",
                "cur_prc": "-152000",
                "pred_pre_sig": "5",
                "pred_pre": "-100",
                "flu_rt": "-0.07",
                "sel_bid": "-152000",
                "buy_bid": "-150000",
                "now_trde_qty": "34954641",
                "pred_trde_qty": "22532511",
                "trde_prica": "5308092",
            },
            {
                "stk_cd": "005930",
                "now_rank": "2",
                "pred_rank": "2",
                "stk_nm": "삼성전자",
                "cur_prc": "-53700",
                "pred_pre_sig": "4",
                "pred_pre": "-23000",
                "flu_rt": "-29.99",
                "sel_bid": "-76500",
                "buy_bid": "+85100",
                "now_trde_qty": "31821639",
                "pred_trde_qty": "30279412",
                "trde_prica": "2436091",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10032"},
        )
        response = client.rank_info.get_top_transaction_value(
            mrkt_tp="001",
            mang_stk_incls="0",
            stex_tp="1",
        )
        assert isinstance(response.body, DomesticRankInfoTopTransactionValue)
        assert response.body.trde_prica_upper[0].buy_bid == "-150000"


def test_get_top_margin_ratio(client: Client):
    expected_data = {
        "crd_rt_upper": [
            {
                "stk_infr": "0",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "16420",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "crd_rt": "+9.49",
                "sel_req": "0",
                "buy_req": "0",
                "now_trde_qty": "0",
            },
            {
                "stk_infr": "0",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "3415",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "crd_rt": "+9.48",
                "sel_req": "1828",
                "buy_req": "0",
                "now_trde_qty": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10033"},
        )
        response = client.rank_info.get_top_margin_ratio(
            mrkt_tp="000",
            trde_qty_tp="0",
            stk_cnd="0",
            updown_incls="1",
            crd_cnd="0",
            stex_tp="1",
        )
        assert isinstance(response.body, DomesticRankInfoTopMarginRatio)
        assert response.body.crd_rt_upper[0].stk_cd == "005930"


def test_get_top_foreigner_period_trading(client: Client):
    expected_data = {
        "for_dt_trde_upper": [
            {
                "rank": "1",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "sel_bid": "0",
                "buy_bid": "+74800",
                "trde_qty": "435771",
                "netprps_qty": "+290232191",
                "gain_pos_stkcnt": "2548278006",
            },
            {
                "rank": "2",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-183500",
                "pred_pre_sig": "5",
                "pred_pre": "-900",
                "sel_bid": "+184900",
                "buy_bid": "0",
                "trde_qty": "135",
                "netprps_qty": "+167189864",
                "gain_pos_stkcnt": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10034"},
        )
        response = client.rank_info.get_top_foreigner_period_trading(
            mrkt_tp="001",
            trde_tp="2",
            dt="0",
            stex_tp="1",
        )

        assert isinstance(response.body, DomesticRankInfoTopForeignerPeriodTrading)
        assert response.body.for_dt_trde_upper[0].netprps_qty == "+290232191"


def test_get_top_consecutive_net_buy_sell_by_foreigners(client: Client):
    expected_data = {
        "for_cont_nettrde_upper": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "10200",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "dm1": "+33928250",
                "dm2": "+234840",
                "dm3": "+233891",
                "tot": "+34396981",
                "limit_exh_rt": "+71.53",
                "pred_pre_1": "",
                "pred_pre_2": "",
                "pred_pre_3": "",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-8540",
                "pred_pre_sig": "5",
                "pred_pre": "-140",
                "dm1": "+4033818",
                "dm2": "+12474308",
                "dm3": "+13173262",
                "tot": "+29681388",
                "limit_exh_rt": "+0.10",
                "pred_pre_1": "",
                "pred_pre_2": "",
                "pred_pre_3": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10035"},
        )
        response = client.rank_info.get_top_consecutive_net_buy_sell_by_foreigners(
            mrkt_tp="000",
            trde_tp="2",
            base_dt_tp="1",
            stex_tp="1",
        )

        assert isinstance(response.body, DomesticRankInfoTopConsecutiveNetBuySellByForeigners)
        assert len(response.body.for_cont_nettrde_upper) > 0


def test_get_top_limit_exhaustion_rate_foreigner(client: Client):
    expected_data = {
        "for_limit_exh_rt_incrs_upper": [
            {
                "rank": "1",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "14255",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "trde_qty": "0",
                "poss_stkcnt": "0",
                "gain_pos_stkcnt": "600000",
                "base_limit_exh_rt": "-283.33",
                "limit_exh_rt": "0.00",
                "exh_rt_incrs": "+283.33",
            },
            {
                "rank": "2",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "1590",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "trde_qty": "0",
                "poss_stkcnt": "519785",
                "gain_pos_stkcnt": "31404714",
                "base_limit_exh_rt": "-101.25",
                "limit_exh_rt": "+1.63",
                "exh_rt_incrs": "+102.87",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10036"},
        )
        response = client.rank_info.get_top_limit_exhaustion_rate_foreigner(
            mrkt_tp="000",
            dt="0",
            stex_tp="1",
        )

        assert isinstance(response.body, DomesticRankInfoTopLimitExhaustionRateForeigner)
        assert response.body.for_limit_exh_rt_incrs_upper[0].gain_pos_stkcnt == "600000"


def test_get_top_foreign_account_group_trading(client: Client):
    expected_data = {
        "frgn_wicket_trde_upper": [
            {
                "rank": "1",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "69",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "sel_trde_qty": "-0",
                "buy_trde_qty": "+0",
                "netprps_trde_qty": "0",
                "netprps_prica": "0",
                "trde_qty": "0",
                "trde_prica": "0",
            },
            {
                "rank": "2",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "316",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "sel_trde_qty": "-0",
                "buy_trde_qty": "+0",
                "netprps_trde_qty": "0",
                "netprps_prica": "0",
                "trde_qty": "0",
                "trde_prica": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10037"},
        )

        response = client.rank_info.get_top_foreign_account_group_trading(
            mrkt_tp="000", dt="0", trde_tp="1", sort_tp="2", stex_tp="1"
        )

        assert isinstance(response.body, DomesticRankInfoTopForeignAccountGroupTrading)
        assert response.body.frgn_wicket_trde_upper[0].cur_prc == "69"


def test_get_stock_specific_securities_firm_ranking(client: Client):
    expected_data = {
        "rank_1": "+34881",
        "rank_2": "-13253",
        "rank_3": "+21628",
        "prid_trde_qty": "43",
        "stk_sec_rank": [
            {"rank": "1", "mmcm_nm": "키움증권", "buy_qty": "+9800", "sell_qty": "-2813", "acc_netprps_qty": "+6987"},
            {"rank": "2", "mmcm_nm": "키움증권", "buy_qty": "+3459", "sell_qty": "-117", "acc_netprps_qty": "+3342"},
            {"rank": "3", "mmcm_nm": "키움증권", "buy_qty": "+3321", "sell_qty": "-125", "acc_netprps_qty": "+3196"},
            {"rank": "4", "mmcm_nm": "키움증권", "buy_qty": "+3941", "sell_qty": "-985", "acc_netprps_qty": "+2956"},
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10038"},
        )
        response = client.rank_info.get_stock_specific_securities_firm_ranking(
            stk_cd="005930", strt_dt="20250601", end_dt="20250602", qry_tp="2", dt="1"
        )

        assert isinstance(response.body, DomesticRankInfoStockSpecificSecuritiesFirmRanking)
        assert response.body.rank_1 == "+34881"
        assert response.body.stk_sec_rank[0].buy_qty == "+9800"


def test_get_top_securities_firm_trading(client: Client):
    expected_data = {
        "sec_trde_upper": [
            {
                "rank": "1",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "prid_stkpc_flu": "+1800",
                "flu_rt": "+0.93",
                "prid_trde_qty": "241",
                "netprps": "+27401",
                "buy_trde_qty": "+33131",
                "sel_trde_qty": "-5730",
            },
            {
                "rank": "2",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "prid_stkpc_flu": "0",
                "flu_rt": "0.00",
                "prid_trde_qty": "0",
                "netprps": "+154140",
                "buy_trde_qty": "+302708",
                "sel_trde_qty": "-148568",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10039"},
        )
        response = client.rank_info.get_top_securities_firm_trading(
            mmcm_cd="001", trde_qty_tp="0", trde_tp="1", dt="1", stex_tp="1"
        )

        assert isinstance(response.body, DomesticRankInfoTopSecuritiesFirmTrading)
        assert response.body.sec_trde_upper[0].flu_rt == "+0.93"


def test_get_top_current_day_major_traders(client: Client):
    expected_data = {
        "sel_trde_ori_irds_1": "0",
        "sel_trde_ori_qty_1": "-5689",
        "sel_trde_ori_1": "모건스탠리",
        "sel_trde_ori_cd_1": "036",
        "buy_trde_ori_1": "모건스탠리",
        "buy_trde_ori_cd_1": "036",
        "buy_trde_ori_qty_1": "+6305",
        "buy_trde_ori_irds_1": "+615",
        "sel_trde_ori_irds_2": "+615",
        "sel_trde_ori_qty_2": "-615",
        "sel_trde_ori_2": "신  영",
        "sel_trde_ori_cd_2": "006",
        "buy_trde_ori_2": "키움증권",
        "buy_trde_ori_cd_2": "050",
        "buy_trde_ori_qty_2": "+7",
        "buy_trde_ori_irds_2": "0",
        "sel_trde_ori_irds_3": "0",
        "sel_trde_ori_qty_3": "-8",
        "sel_trde_ori_3": "키움증권",
        "sel_trde_ori_cd_3": "050",
        "buy_trde_ori_3": "",
        "buy_trde_ori_cd_3": "000",
        "buy_trde_ori_qty_3": "0",
        "buy_trde_ori_irds_3": "0",
        "sel_trde_ori_irds_4": "0",
        "sel_trde_ori_qty_4": "0",
        "sel_trde_ori_4": "",
        "sel_trde_ori_cd_4": "000",
        "buy_trde_ori_4": "",
        "buy_trde_ori_cd_4": "000",
        "buy_trde_ori_qty_4": "0",
        "buy_trde_ori_irds_4": "0",
        "sel_trde_ori_irds_5": "0",
        "sel_trde_ori_qty_5": "0",
        "sel_trde_ori_5": "",
        "sel_trde_ori_cd_5": "000",
        "buy_trde_ori_5": "",
        "buy_trde_ori_cd_5": "000",
        "buy_trde_ori_qty_5": "0",
        "buy_trde_ori_irds_5": "0",
        "frgn_sel_prsm_sum_chang": "0",
        "frgn_sel_prsm_sum": "-5689",
        "frgn_buy_prsm_sum": "+6305",
        "frgn_buy_prsm_sum_chang": "+615",
        "tdy_main_trde_ori": [],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10040"},
        )

        response = client.rank_info.get_top_current_day_major_traders(stk_cd="005930")

        assert isinstance(response.body, DomesticRankInfoTopCurrentDayMajorTraders)
        assert response.body.sel_trde_ori_1 == "모건스탠리"
        assert response.body.tdy_main_trde_ori == []


def test_get_top_net_buy_trader_ranking(client: Client):
    expected_data = {
        "netprps_trde_ori_rank": [
            {"rank": "1", "mmcm_cd": "36", "mmcm_nm": "키움증권"},
            {"rank": "2", "mmcm_cd": "50", "mmcm_nm": "키움증권"},
            {"rank": "3", "mmcm_cd": "45", "mmcm_nm": "키움증권"},
            {"rank": "4", "mmcm_cd": "6", "mmcm_nm": "키움증권"},
            {"rank": "5", "mmcm_cd": "64", "mmcm_nm": "키움증권"},
            {"rank": "6", "mmcm_cd": "31", "mmcm_nm": "키움증권"},
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10041"},
        )

        response = client.rank_info.get_top_net_buy_trader_ranking(
            stk_cd="005930", strt_dt="20241031", end_dt="20241107", qry_dt_tp="0", pot_tp="0", dt="5", sort_base="1"
        )

        assert isinstance(response.body, DomesticRankInfoTopNetBuyTraderRanking)
        assert len(response.body.netprps_trde_ori_rank) == 6


def test_get_top_current_day_deviation_sources(client: Client):
    expected_data = {
        "tdy_upper_scesn_ori": [
            {
                "sel_scesn_tm": "154706",
                "sell_qty": "32",
                "sel_upper_scesn_ori": "키움증권",
                "buy_scesn_tm": "151615",
                "buy_qty": "48",
                "buy_upper_scesn_ori": "키움증권",
                "qry_dt": "012",
                "qry_tm": "012",
            },
            {
                "sel_scesn_tm": "145127",
                "sell_qty": "14",
                "sel_upper_scesn_ori": "키움증권",
                "buy_scesn_tm": "144055",
                "buy_qty": "21",
                "buy_upper_scesn_ori": "키움증권",
                "qry_dt": "017",
                "qry_tm": "046",
            },
            {
                "sel_scesn_tm": "145117",
                "sell_qty": "10",
                "sel_upper_scesn_ori": "키움증권",
                "buy_scesn_tm": "140901",
                "buy_qty": "3",
                "buy_upper_scesn_ori": "키움증권",
                "qry_dt": "050",
                "qry_tm": "056",
            },
            {
                "sel_scesn_tm": "",
                "sell_qty": "",
                "sel_upper_scesn_ori": "",
                "buy_scesn_tm": "135548",
                "buy_qty": "2",
                "buy_upper_scesn_ori": "키움증권",
                "qry_dt": "",
                "qry_tm": "001",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10053"},
        )

        response = client.rank_info.get_top_current_day_deviation_sources(
            stk_cd="005930",
        )

        assert isinstance(response.body, DomesticRankInfoTopCurrentDayDeviationSources)
        assert response.body.tdy_upper_scesn_ori[0].buy_upper_scesn_ori == "키움증권"


def test_get_same_net_buy_sell_ranking(client: Client):
    expected_data = {
        "eql_nettrde_rank": [
            {
                "stk_cd": "005930",
                "rank": "1",
                "stk_nm": "삼성전자",
                "cur_prc": "-206000",
                "pre_sig": "5",
                "pred_pre": "-500",
                "flu_rt": "-0.24",
                "acc_trde_qty": "85",
                "orgn_nettrde_qty": "+2",
                "orgn_nettrde_amt": "0",
                "orgn_nettrde_avg_pric": "206000",
                "for_nettrde_qty": "+275",
                "for_nettrde_amt": "+59",
                "for_nettrde_avg_pric": "213342",
                "nettrde_qty": "+277",
                "nettrde_amt": "+59",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10062"},
        )

        response = client.rank_info.get_same_net_buy_sell_ranking(
            strt_dt="20241106",
            end_dt="20241107",
            mrkt_tp="000",
            trde_tp="1",
            sort_cnd="1",
            unit_tp="1",
            stex_tp="1",
        )

        assert isinstance(response.body, DomesticRankInfoSameNetBuySellRanking)
        assert response.body.eql_nettrde_rank[0].cur_prc == "-206000"


def test_get_top_intraday_trading_by_investor(client: Client):
    expected_data = {
        "opmr_invsr_trde_upper": [
            {"stk_cd": "005930", "stk_nm": "삼성전자", "sel_qty": "-39420", "buy_qty": "+73452", "netslmt": "+34033"},
            {"stk_cd": "005930", "stk_nm": "삼성전자", "sel_qty": "-13970", "buy_qty": "+25646", "netslmt": "+11676"},
            {"stk_cd": "005930", "stk_nm": "삼성전자", "sel_qty": "-10063", "buy_qty": "+21167", "netslmt": "+11104"},
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10065"},
        )
        response = client.rank_info.get_top_intraday_trading_by_investor(
            trde_tp="1",
            mrkt_tp="000",
            orgn_tp="9000",
        )

        assert isinstance(response.body, DomesticRankInfoTopIntradayTradingByInvestor)
        assert response.body.opmr_invsr_trde_upper[0].netslmt == "+34033"


def test_get_after_hours_single_price_change_rate_ranking(client: Client):
    expected_data = {
        "ovt_sigpric_flu_rt_rank": [
            {
                "rank": "1",
                "stk_cd": "069500",
                "stk_nm": "KODEX 200",
                "cur_prc": "17140",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "sel_tot_req": "0",
                "buy_tot_req": "24",
                "acc_trde_qty": "42",
                "acc_trde_prica": "1",
                "tdy_close_pric": "17140",
                "tdy_close_pric_flu_rt": "-0.26",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10098"},
        )
        response = client.rank_info.get_after_hours_single_price_change_rate_ranking(
            mrkt_tp="000",
            sort_base="5",
            stk_cnd="0",
            trde_qty_cnd="0",
            crd_cnd="0",
            trde_prica="0",
        )

        assert isinstance(response.body, DomesticRankInfoAfterHoursSinglePriceChangeRateRanking)
        assert response.body.ovt_sigpric_flu_rt_rank[0].tdy_close_pric == "17140"


def test_get_top_foreigner_limit_exhaustion_rate(client: Client):
    expected_data = {
        "frgnr_orgn_trde_upper": [
            {
                "for_netslmt_stk_cd": "069500",
                "for_netslmt_stk_nm": "KODEX 200",
                "for_netslmt_amt": "-130811",
                "for_netslmt_qty": "-50312",
                "for_netprps_stk_cd": "069500",
                "for_netprps_stk_nm": "KODEX 200",
                "for_netprps_amt": "-130811",
                "for_netprps_qty": "-50312",
                "orgn_netslmt_stk_cd": "069500",
                "orgn_netslmt_stk_nm": "KODEX 200",
                "orgn_netslmt_amt": "-130811",
                "orgn_netslmt_qty": "-50312",
                "orgn_netprps_stk_cd": "069500",
                "orgn_netprps_stk_nm": "KODEX 200",
                "orgn_netprps_amt": "-130811",
                "orgn_netprps_qty": "-50312",
            },
            {
                "for_netslmt_stk_cd": "069500",
                "for_netslmt_stk_nm": "KODEX 200",
                "for_netslmt_amt": "-130811",
                "for_netslmt_qty": "-50312",
                "for_netprps_stk_cd": "069500",
                "for_netprps_stk_nm": "KODEX 200",
                "for_netprps_amt": "-130811",
                "for_netprps_qty": "-50312",
                "orgn_netslmt_stk_cd": "069500",
                "orgn_netslmt_stk_nm": "KODEX 200",
                "orgn_netslmt_amt": "-130811",
                "orgn_netslmt_qty": "-50312",
                "orgn_netprps_stk_cd": "069500",
                "orgn_netprps_stk_nm": "KODEX 200",
                "orgn_netprps_amt": "-130811",
                "orgn_netprps_qty": "-50312",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/rkinfo",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90099"},
        )
        response = client.rank_info.get_top_foreigner_limit_exhaustion_rate(mrkt_tp="001", dt="1", stex_tp="1")

        assert isinstance(response.body, DomesticRankInfoTopForeignerLimitExhaustionRate)
        assert response.body.frgnr_orgn_trde_upper[0].orgn_netprps_stk_cd == "069500"
