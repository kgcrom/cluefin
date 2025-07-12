import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_market_condition import DomesticMarketCondition
from cluefin_openapi.kiwoom._domestic_market_condition_types import (
    DomesticMarketConditionAfterHoursSinglePrice,
    DomesticMarketConditionAfterMarketTradingByInvestor,
    DomesticMarketConditionDailyInstitutionalTrading,
    DomesticMarketConditionDailyStockPrice,
    DomesticMarketConditionExecutionIntensityTrendByDate,
    DomesticMarketConditionExecutionIntensityTrendByTime,
    DomesticMarketConditionInstitutionalTradingTrendByStock,
    DomesticMarketConditionIntradayTradingByInvestor,
    DomesticMarketConditionMarketSentimentInfo,
    DomesticMarketConditionNewStockWarrantPrice,
    DomesticMarketConditionProgramTradingArbitrageBalanceTrend,
    DomesticMarketConditionProgramTradingCumulativeTrend,
    DomesticMarketConditionProgramTradingTrendByDate,
    DomesticMarketConditionProgramTradingTrendByStockAndDate,
    DomesticMarketConditionProgramTradingTrendByStockAndTime,
    DomesticMarketConditionProgramTradingTrendByTime,
    DomesticMarketConditionSecuritiesFirmTradingTrendByStock,
    DomesticMarketConditionStockPrice,
    DomesticMarketConditionStockQuote,
    DomesticMarketConditionStockQuoteByDate,
)


@pytest.fixture
def market_condition() -> DomesticMarketCondition:
    return Client(
        token="test_token",
        env="dev",
    ).market_conditions


def test_get_stock_quote(market_condition: DomesticMarketCondition):
    expected_data = {
        "bid_req_base_tm": "162000",
        "sel_10th_pre_req_pre": "0",
        "sel_10th_pre_req": "0",
        "sel_10th_pre_bid": "0",
        "sel_9th_pre_req_pre": "0",
        "sel_9th_pre_req": "0",
        "sel_9th_pre_bid": "0",
        "sel_8th_pre_req_pre": "0",
        "sel_8th_pre_req": "0",
        "sel_8th_pre_bid": "0",
        "sel_7th_pre_req_pre": "0",
        "sel_7th_pre_req": "0",
        "sel_7th_pre_bid": "0",
        "sel_6th_pre_req_pre": "0",
        "sel_6th_pre_req": "0",
        "sel_6th_pre_bid": "0",
        "sel_5th_pre_req_pre": "0",
        "sel_5th_pre_req": "0",
        "sel_5th_pre_bid": "0",
        "sel_4th_pre_req_pre": "0",
        "sel_4th_pre_req": "0",
        "sel_4th_pre_bid": "0",
        "sel_3th_pre_req_pre": "0",
        "sel_3th_pre_req": "0",
        "sel_3th_pre_bid": "0",
        "sel_2th_pre_req_pre": "0",
        "sel_2th_pre_req": "0",
        "sel_2th_pre_bid": "0",
        "sel_1th_pre_req_pre": "0",
        "sel_fpr_req": "0",
        "sel_fpr_bid": "0",
        "buy_fpr_bid": "0",
        "buy_fpr_req": "0",
        "buy_1th_pre_req_pre": "0",
        "buy_2th_pre_bid": "0",
        "buy_2th_pre_req": "0",
        "buy_2th_pre_req_pre": "0",
        "buy_3th_pre_bid": "0",
        "buy_3th_pre_req": "0",
        "buy_3th_pre_req_pre": "0",
        "buy_4th_pre_bid": "0",
        "buy_4th_pre_req": "0",
        "buy_4th_pre_req_pre": "0",
        "buy_5th_pre_bid": "0",
        "buy_5th_pre_req": "0",
        "buy_5th_pre_req_pre": "0",
        "buy_6th_pre_bid": "0",
        "buy_6th_pre_req": "0",
        "buy_6th_pre_req_pre": "0",
        "buy_7th_pre_bid": "0",
        "buy_7th_pre_req": "0",
        "buy_7th_pre_req_pre": "0",
        "buy_8th_pre_bid": "0",
        "buy_8th_pre_req": "0",
        "buy_8th_pre_req_pre": "0",
        "buy_9th_pre_bid": "0",
        "buy_9th_pre_req": "0",
        "buy_9th_pre_req_pre": "0",
        "buy_10th_pre_bid": "0",
        "buy_10th_pre_req": "0",
        "buy_10th_pre_req_pre": "0",
        "tot_sel_req_jub_pre": "0",
        "tot_sel_req": "0",
        "tot_buy_req": "0",
        "tot_buy_req_jub_pre": "0",
        "ovt_sel_req_pre": "0",
        "ovt_sel_req": "0",
        "ovt_buy_req": "0",
        "ovt_buy_req_pre": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10004"},
        )

        response = market_condition.get_stock_quote("005930")

        assert isinstance(response.body, DomesticMarketConditionStockQuote)
        assert response.body.bid_req_base_tm == "162000"
        assert response.body.sel_10th_pre_req_pre == "0"


def test_get_stock_quote_by_date(market_condition):
    expected_data = {
        "stk_ddwkmm": [
            {
                "date": "20241028",
                "open_pric": "95400",
                "high_pric": "95400",
                "low_pric": "95400",
                "close_pric": "95400",
                "pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "trde_prica": "0",
                "cntr_str": "0.00",
                "for_poss": "+26.07",
                "for_wght": "+26.07",
                "for_netprps": "0",
                "orgn_netprps": "",
                "ind_netprps": "",
                "frgn": "",
                "crd_remn_rt": "",
                "prm": "",
            },
            {
                "date": "20241025",
                "open_pric": "95400",
                "high_pric": "95400",
                "low_pric": "95400",
                "close_pric": "95400",
                "pre": "",
                "flu_rt": "",
                "trde_qty": "0",
                "trde_prica": "",
                "cntr_str": "",
                "for_poss": "",
                "for_wght": "",
                "for_netprps": "",
                "orgn_netprps": "",
                "ind_netprps": "",
                "frgn": "",
                "crd_remn_rt": "",
                "prm": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10005"},
        )
        response = market_condition.get_stock_quote_by_date("005930")

        assert isinstance(response.body, DomesticMarketConditionStockQuoteByDate)
        assert response.body.stk_ddwkmm[0].open_pric == "95400"
        assert response.body.stk_ddwkmm[0].date == "20241028"


def test_get_stock_price(market_condition):
    expected_data = {
        "date": "20241105",
        "open_pric": "0",
        "high_pric": "0",
        "low_pric": "0",
        "close_pric": "135300",
        "pre": "0",
        "flu_rt": "0.00",
        "trde_qty": "0",
        "trde_prica": "0",
        "cntr_str": "0.00",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10006"},
        )
        response = market_condition.get_stock_price("005930")

        assert isinstance(response.body, DomesticMarketConditionStockPrice)
        assert response.body.date == "20241105"
        assert response.body.close_pric == "135300"


def test_get_market_sentiment_info(market_condition):
    expected_data = {
        "stk_nm": "삼성전자",
        "stk_cd": "005930",
        "date": "20241105",
        "tm": "104000",
        "pred_close_pric": "135300",
        "pred_trde_qty": "88862",
        "upl_pric": "+175800",
        "lst_pric": "-94800",
        "pred_trde_prica": "11963",
        "flo_stkcnt": "25527",
        "cur_prc": "135300",
        "smbol": "3",
        "flu_rt": "0.00",
        "pred_rt": "0.00",
        "open_pric": "0",
        "high_pric": "0",
        "low_pric": "0",
        "cntr_qty": "",
        "trde_qty": "0",
        "trde_prica": "0",
        "exp_cntr_pric": "-0",
        "exp_cntr_qty": "0",
        "exp_sel_pri_bid": "0",
        "exp_buy_pri_bid": "0",
        "trde_strt_dt": "00000000",
        "exec_pric": "0",
        "hgst_pric": "",
        "lwst_pric": "",
        "hgst_pric_dt": "",
        "lwst_pric_dt": "",
        "sel_1bid": "0",
        "sel_2bid": "0",
        "sel_3bid": "0",
        "sel_4bid": "0",
        "sel_5bid": "0",
        "sel_6bid": "0",
        "sel_7bid": "0",
        "sel_8bid": "0",
        "sel_9bid": "0",
        "sel_10bid": "0",
        "buy_1bid": "0",
        "buy_2bid": "0",
        "buy_3bid": "0",
        "buy_4bid": "0",
        "buy_5bid": "0",
        "buy_6bid": "0",
        "buy_7bid": "0",
        "buy_8bid": "0",
        "buy_9bid": "0",
        "buy_10bid": "0",
        "sel_1bid_req": "0",
        "sel_2bid_req": "0",
        "sel_3bid_req": "0",
        "sel_4bid_req": "0",
        "sel_5bid_req": "0",
        "sel_6bid_req": "0",
        "sel_7bid_req": "0",
        "sel_8bid_req": "0",
        "sel_9bid_req": "0",
        "sel_10bid_req": "0",
        "buy_1bid_req": "0",
        "buy_2bid_req": "0",
        "buy_3bid_req": "0",
        "buy_4bid_req": "0",
        "buy_5bid_req": "0",
        "buy_6bid_req": "0",
        "buy_7bid_req": "0",
        "buy_8bid_req": "0",
        "buy_9bid_req": "0",
        "buy_10bid_req": "0",
        "sel_1bid_jub_pre": "0",
        "sel_2bid_jub_pre": "0",
        "sel_3bid_jub_pre": "0",
        "sel_4bid_jub_pre": "0",
        "sel_5bid_jub_pre": "0",
        "sel_6bid_jub_pre": "0",
        "sel_7bid_jub_pre": "0",
        "sel_8bid_jub_pre": "0",
        "sel_9bid_jub_pre": "0",
        "sel_10bid_jub_pre": "0",
        "buy_1bid_jub_pre": "0",
        "buy_2bid_jub_pre": "0",
        "buy_3bid_jub_pre": "0",
        "buy_4bid_jub_pre": "0",
        "buy_5bid_jub_pre": "0",
        "buy_6bid_jub_pre": "0",
        "buy_7bid_jub_pre": "0",
        "buy_8bid_jub_pre": "0",
        "buy_9bid_jub_pre": "0",
        "buy_10bid_jub_pre": "0",
        "sel_1bid_cnt": "",
        "sel_2bid_cnt": "",
        "sel_3bid_cnt": "",
        "sel_4bid_cnt": "",
        "sel_5bid_cnt": "",
        "buy_1bid_cnt": "",
        "buy_2bid_cnt": "",
        "buy_3bid_cnt": "",
        "buy_4bid_cnt": "",
        "buy_5bid_cnt": "",
        "lpsel_1bid_req": "0",
        "lpsel_2bid_req": "0",
        "lpsel_3bid_req": "0",
        "lpsel_4bid_req": "0",
        "lpsel_5bid_req": "0",
        "lpsel_6bid_req": "0",
        "lpsel_7bid_req": "0",
        "lpsel_8bid_req": "0",
        "lpsel_9bid_req": "0",
        "lpsel_10bid_req": "0",
        "lpbuy_1bid_req": "0",
        "lpbuy_2bid_req": "0",
        "lpbuy_3bid_req": "0",
        "lpbuy_4bid_req": "0",
        "lpbuy_5bid_req": "0",
        "lpbuy_6bid_req": "0",
        "lpbuy_7bid_req": "0",
        "lpbuy_8bid_req": "0",
        "lpbuy_9bid_req": "0",
        "lpbuy_10bid_req": "0",
        "tot_buy_req": "0",
        "tot_sel_req": "0",
        "tot_buy_cnt": "",
        "tot_sel_cnt": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10007"},
        )
        response = market_condition.get_market_sentiment_info("005930")

        assert isinstance(response.body, DomesticMarketConditionMarketSentimentInfo)
        assert response.body.stk_nm == "삼성전자"
        assert response.body.pred_close_pric == "135300"


def test_get_new_stock_warrant_price(market_condition):
    expected_data = {
        "newstk_recvrht_mrpr": [
            {
                "stk_cd": "J0036221D",
                "stk_nm": "KG모빌리티 122WR",
                "cur_prc": "988",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "fpr_sel_bid": "-0",
                "fpr_buy_bid": "-0",
                "acc_trde_qty": "0",
                "open_pric": "-0",
                "high_pric": "-0",
                "low_pric": "-0",
            },
            {
                "stk_cd": "J00532219",
                "stk_nm": "온타이드 9WR",
                "cur_prc": "12",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "fpr_sel_bid": "-0",
                "fpr_buy_bid": "-0",
                "acc_trde_qty": "0",
                "open_pric": "-0",
                "high_pric": "-0",
                "low_pric": "-0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10011"},
        )
        response = market_condition.get_new_stock_warrant_price("00")
        assert isinstance(response.body, DomesticMarketConditionNewStockWarrantPrice)
        assert response.body.newstk_recvrht_mrpr[0].stk_cd == "J0036221D"
        assert len(response.body.newstk_recvrht_mrpr) == 2


def test_get_daily_institutional_trading_items(market_condition):
    expected_data = {
        "daly_orgn_trde_stk": [
            {"stk_cd": "005930", "stk_nm": "삼성전자", "netprps_qty": "-0", "netprps_amt": "-1"},
            {"stk_cd": "005930", "stk_nm": "삼성전자", "netprps_qty": "-0", "netprps_amt": "-0"},
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10044"},
        )
        response = market_condition.get_daily_institutional_trading_items("20241106", "20241107", "1", "001", "3")
        assert isinstance(response.body, DomesticMarketConditionDailyInstitutionalTrading)
        assert response.body.daly_orgn_trde_stk[0].stk_cd == "005930"
        assert response.body.daly_orgn_trde_stk[0].netprps_amt == "-1"


def test_get_institutional_trading_trend_by_stock(market_condition):
    expected_data = {
        "orgn_prsm_avg_pric": "117052",
        "for_prsm_avg_pric": "0",
        "stk_orgn_trde_trnsn": [
            {
                "dt": "20241107",
                "close_pric": "133600",
                "pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "orgn_dt_acc": "158",
                "orgn_daly_nettrde_qty": "0",
                "for_dt_acc": "28315",
                "for_daly_nettrde_qty": "0",
                "limit_exh_rt": "+26.14",
            },
            {
                "dt": "20241106",
                "close_pric": "-132500",
                "pre_sig": "5",
                "pred_pre": "-600",
                "flu_rt": "-0.45",
                "trde_qty": "43",
                "orgn_dt_acc": "158",
                "orgn_daly_nettrde_qty": "0",
                "for_dt_acc": "28315",
                "for_daly_nettrde_qty": "11243",
                "limit_exh_rt": "+26.14",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10045"},
        )
        response = market_condition.get_institutional_trading_trend_by_stock("005930", "20241101", "20241107", "1", "1")

        assert isinstance(response.body, DomesticMarketConditionInstitutionalTradingTrendByStock)
        assert response.body.orgn_prsm_avg_pric == "117052"
        assert response.body.stk_orgn_trde_trnsn[0].dt == "20241107"


def test_get_execution_intensity_trend_by_time(market_condition):
    expected_data = {
        "cntr_str_tm": [
            {
                "cntr_tm": "163713",
                "cur_prc": "+156600",
                "pred_pre": "+34900",
                "pred_pre_sig": "2",
                "flu_rt": "+28.68",
                "trde_qty": "-1",
                "acc_trde_prica": "14449",
                "acc_trde_qty": "113636",
                "cntr_str": "172.01",
                "cntr_str_5min": "172.01",
                "cntr_str_20min": "172.01",
                "cntr_str_60min": "170.67",
                "stex_tp": "KRX",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10046"},
        )
        response = market_condition.get_execution_intensity_trend_by_time("005930", "20241107", "1")

        assert isinstance(response.body, DomesticMarketConditionExecutionIntensityTrendByTime)
        assert response.body.cntr_str_tm[0].cntr_tm == "163713"
        assert response.body.cntr_str_tm[0].cur_prc == "+156600"


def test_get_execution_intensity_trend_by_date(market_condition):
    expected_data = {
        "cntr_str_daly": [
            {
                "dt": "20241128",
                "cur_prc": "+219000",
                "pred_pre": "+14000",
                "pred_pre_sig": "2",
                "flu_rt": "+6.83",
                "trde_qty": "",
                "acc_trde_prica": "2",
                "acc_trde_qty": "8",
                "cntr_str": "0.00",
                "cntr_str_5min": "201.54",
                "cntr_str_20min": "139.37",
                "cntr_str_60min": "172.06",
            },
            {
                "dt": "20241127",
                "cur_prc": "+205000",
                "pred_pre": "+40300",
                "pred_pre_sig": "2",
                "flu_rt": "+24.47",
                "trde_qty": "",
                "acc_trde_prica": "9",
                "acc_trde_qty": "58",
                "cntr_str": "0.00",
                "cntr_str_5min": "209.54",
                "cntr_str_20min": "139.37",
                "cntr_str_60min": "180.40",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10047"},
        )
        response = market_condition.get_execution_intensity_trend_by_date("005930")

        assert isinstance(response.body, DomesticMarketConditionExecutionIntensityTrendByDate)
        assert response.body.cntr_str_daly[0].dt == "20241128"
        assert response.body.cntr_str_daly[0].cur_prc == "+219000"


def test_get_intraday_trading_by_investor(market_condition):
    expected_data = {
        "opmr_invsr_trde": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "64",
                "pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "1",
                "netprps_qty": "+1083000",
                "prev_pot_netprps_qty": "+1083000",
                "netprps_irds": "0",
                "buy_qty": "+1113000",
                "buy_qty_irds": "0",
                "sell_qty": "--30000",
                "sell_qty_irds": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "284",
                "pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "0",
                "netprps_qty": "--261000",
                "prev_pot_netprps_qty": "--347000",
                "netprps_irds": "+86000",
                "buy_qty": "+2728000",
                "buy_qty_irds": "+108000",
                "sell_qty": "--2989000",
                "sell_qty_irds": "+22000",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10063"},
        )
        response = market_condition.get_intraday_trading_by_investor("000", "1", "6", "1", "1", "1")

        assert isinstance(response.body, DomesticMarketConditionIntradayTradingByInvestor)
        assert response.body.opmr_invsr_trde[0].stk_cd == "005930"
        assert response.body.opmr_invsr_trde[0].cur_prc == "64"


def test_get_after_market_trading_by_investor(market_condition):
    expected_data = {
        "opaf_invsr_trde": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-7410",
                "pre_sig": "5",
                "pred_pre": "-50",
                "flu_rt": "-0.67",
                "trde_qty": "8",
                "ind_invsr": "0",
                "frgnr_invsr": "0",
                "orgn": "0",
                "fnnc_invt": "0",
                "insrnc": "0",
                "invtrt": "0",
                "etc_fnnc": "0",
                "bank": "0",
                "penfnd_etc": "0",
                "samo_fund": "0",
                "natn": "0",
                "etc_corp": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "542",
                "pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "ind_invsr": "0",
                "frgnr_invsr": "0",
                "orgn": "0",
                "fnnc_invt": "0",
                "insrnc": "0",
                "invtrt": "0",
                "etc_fnnc": "0",
                "bank": "0",
                "penfnd_etc": "0",
                "samo_fund": "0",
                "natn": "0",
                "etc_corp": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10066"},
        )
        response = market_condition.get_after_market_trading_by_investor("000", "1", "0", "1")

        assert isinstance(response.body, DomesticMarketConditionAfterMarketTradingByInvestor)
        assert response.body.opaf_invsr_trde[0].stk_cd == "005930"
        assert response.body.opaf_invsr_trde[0].cur_prc == "-7410"


def test_get_securities_firm_trading_trend_by_stock(market_condition):
    expected_data = {
        "sec_stk_trde_trend": [
            {
                "dt": "20241107",
                "cur_prc": "10050",
                "pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "0",
                "netprps_qty": "0",
                "buy_qty": "0",
                "sell_qty": "0",
            },
            {
                "dt": "20241106",
                "cur_prc": "10240",
                "pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "0",
                "netprps_qty": "-1016",
                "buy_qty": "951",
                "sell_qty": "1967",
            },
            {
                "dt": "20241105",
                "cur_prc": "10040",
                "pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "acc_trde_qty": "0",
                "netprps_qty": "2016",
                "buy_qty": "5002",
                "sell_qty": "2986",
            },
            {
                "dt": "20241101",
                "cur_prc": "-5880",
                "pre_sig": "4",
                "pred_pre": "-2520",
                "flu_rt": "-30.00",
                "acc_trde_qty": "16139969",
                "netprps_qty": "-532",
                "buy_qty": "2454",
                "sell_qty": "2986",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10078"},
        )
        response = market_condition.get_securities_firm_trading_trend_by_stock("001", "005930", "20241101", "20241107")

        assert isinstance(response.body, DomesticMarketConditionSecuritiesFirmTradingTrendByStock)
        assert response.body.sec_stk_trde_trend[0].dt == "20241107"
        assert response.body.sec_stk_trde_trend[0].cur_prc == "10050"


def test_get_daily_stock_price(market_condition):
    expected_data = {
        "daly_stkpc": [
            {
                "date": "20241125",
                "open_pric": "+78800",
                "high_pric": "+101100",
                "low_pric": "-54500",
                "close_pric": "-55000",
                "pred_rt": "-22800",
                "flu_rt": "-29.31",
                "trde_qty": "20278",
                "amt_mn": "1179",
                "crd_rt": "0.00",
                "ind": "--714",
                "orgn": "+693",
                "for_qty": "--266783",
                "frgn": "0",
                "prm": "0",
                "for_rt": "+51.56",
                "for_poss": "+51.56",
                "for_wght": "+51.56",
                "for_netprps": "--266783",
                "orgn_netprps": "+693",
                "ind_netprps": "--714",
                "crd_remn_rt": "0.00",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10086"},
        )
        response = market_condition.get_daily_stock_price("005930", "20241125", "0")

        assert isinstance(response.body, DomesticMarketConditionDailyStockPrice)
        assert response.body.daly_stkpc[0].date == "20241125"
        assert response.body.daly_stkpc[0].open_pric == "+78800"


def test_get_after_hours_single_price(market_condition):
    expected_data = {
        "bid_req_base_tm": "164000",
        "ovt_sigpric_sel_bid_jub_pre_5": "0",
        "ovt_sigpric_sel_bid_jub_pre_4": "0",
        "ovt_sigpric_sel_bid_jub_pre_3": "0",
        "ovt_sigpric_sel_bid_jub_pre_2": "0",
        "ovt_sigpric_sel_bid_jub_pre_1": "0",
        "ovt_sigpric_sel_bid_qty_5": "0",
        "ovt_sigpric_sel_bid_qty_4": "0",
        "ovt_sigpric_sel_bid_qty_3": "0",
        "ovt_sigpric_sel_bid_qty_2": "0",
        "ovt_sigpric_sel_bid_qty_1": "0",
        "ovt_sigpric_sel_bid_5": "-0",
        "ovt_sigpric_sel_bid_4": "-0",
        "ovt_sigpric_sel_bid_3": "-0",
        "ovt_sigpric_sel_bid_2": "-0",
        "ovt_sigpric_sel_bid_1": "-0",
        "ovt_sigpric_buy_bid_1": "-0",
        "ovt_sigpric_buy_bid_2": "-0",
        "ovt_sigpric_buy_bid_3": "-0",
        "ovt_sigpric_buy_bid_4": "-0",
        "ovt_sigpric_buy_bid_5": "-0",
        "ovt_sigpric_buy_bid_qty_1": "0",
        "ovt_sigpric_buy_bid_qty_2": "0",
        "ovt_sigpric_buy_bid_qty_3": "0",
        "ovt_sigpric_buy_bid_qty_4": "0",
        "ovt_sigpric_buy_bid_qty_5": "0",
        "ovt_sigpric_buy_bid_jub_pre_1": "0",
        "ovt_sigpric_buy_bid_jub_pre_2": "0",
        "ovt_sigpric_buy_bid_jub_pre_3": "0",
        "ovt_sigpric_buy_bid_jub_pre_4": "0",
        "ovt_sigpric_buy_bid_jub_pre_5": "0",
        "ovt_sigpric_sel_bid_tot_req": "0",
        "ovt_sigpric_buy_bid_tot_req": "0",
        "sel_bid_tot_req_jub_pre": "0",
        "sel_bid_tot_req": "24028",
        "buy_bid_tot_req": "26579",
        "buy_bid_tot_req_jub_pre": "0",
        "ovt_sel_bid_tot_req_jub_pre": "0",
        "ovt_sel_bid_tot_req": "0",
        "ovt_buy_bid_tot_req": "11",
        "ovt_buy_bid_tot_req_jub_pre": "0",
        "ovt_sigpric_cur_prc": "156600",
        "ovt_sigpric_pred_pre_sig": "0",
        "ovt_sigpric_pred_pre": "0",
        "ovt_sigpric_flu_rt": "0.00",
        "ovt_sigpric_acc_trde_qty": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10087"},
        )
        response = market_condition.get_after_hours_single_price("039490")

        assert isinstance(response.body, DomesticMarketConditionAfterHoursSinglePrice)
        assert response.body.bid_req_base_tm == "164000"
        assert response.body.ovt_sigpric_cur_prc == "156600"


def test_get_program_trading_trend_by_time(market_condition):
    expected_data = {
        "prm_trde_trnsn": [
            {
                "cntr_tm": "170500",
                "dfrt_trde_sel": "0",
                "dfrt_trde_buy": "0",
                "dfrt_trde_netprps": "0",
                "ndiffpro_trde_sel": "1",
                "ndiffpro_trde_buy": "17",
                "ndiffpro_trde_netprps": "+17",
                "dfrt_trde_sell_qty": "0",
                "dfrt_trde_buy_qty": "0",
                "dfrt_trde_netprps_qty": "0",
                "ndiffpro_trde_sell_qty": "0",
                "ndiffpro_trde_buy_qty": "0",
                "ndiffpro_trde_netprps_qty": "+0",
                "all_sel": "1",
                "all_buy": "17",
                "all_netprps": "+17",
                "kospi200": "+47839",
                "basis": "-146.59",
            },
            {
                "cntr_tm": "170400",
                "dfrt_trde_sel": "0",
                "dfrt_trde_buy": "0",
                "dfrt_trde_netprps": "0",
                "ndiffpro_trde_sel": "1",
                "ndiffpro_trde_buy": "17",
                "ndiffpro_trde_netprps": "+17",
                "dfrt_trde_sell_qty": "0",
                "dfrt_trde_buy_qty": "0",
                "dfrt_trde_netprps_qty": "0",
                "ndiffpro_trde_sell_qty": "0",
                "ndiffpro_trde_buy_qty": "0",
                "ndiffpro_trde_netprps_qty": "+0",
                "all_sel": "1",
                "all_buy": "17",
                "all_netprps": "+17",
                "kospi200": "+47839",
                "basis": "-146.59",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90005"},
        )
        response = market_condition.get_program_trading_trend_by_time("20250101", "1", "P00101", "0", "1")

        assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByTime)
        assert response.body.prm_trde_trnsn[0].cntr_tm == "170500"
        assert response.body.prm_trde_trnsn[0].dfrt_trde_sel == "0"


def test_get_program_trading_arbitrage_balance_trend(market_condition):
    expected_data = {
        "prm_trde_dfrt_remn_trnsn": [
            {
                "dt": "20241125",
                "buy_dfrt_trde_qty": "0",
                "buy_dfrt_trde_amt": "0",
                "buy_dfrt_trde_irds_amt": "0",
                "sel_dfrt_trde_qty": "0",
                "sel_dfrt_trde_amt": "0",
                "sel_dfrt_trde_irds_amt": "0",
            },
            {
                "dt": "20241122",
                "buy_dfrt_trde_qty": "0",
                "buy_dfrt_trde_amt": "0",
                "buy_dfrt_trde_irds_amt": "-25",
                "sel_dfrt_trde_qty": "0",
                "sel_dfrt_trde_amt": "0",
                "sel_dfrt_trde_irds_amt": "0",
            },
            {
                "dt": "20241121",
                "buy_dfrt_trde_qty": "0",
                "buy_dfrt_trde_amt": "25",
                "buy_dfrt_trde_irds_amt": "25",
                "sel_dfrt_trde_qty": "0",
                "sel_dfrt_trde_amt": "0",
                "sel_dfrt_trde_irds_amt": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90006"},
        )
        response = market_condition.get_program_trading_arbitrage_balance_trend("20250101", "1")

        assert isinstance(response.body, DomesticMarketConditionProgramTradingArbitrageBalanceTrend)
        assert response.body.prm_trde_dfrt_remn_trnsn[0].dt == "20241125"
        assert response.body.prm_trde_dfrt_remn_trnsn[0].buy_dfrt_trde_qty == "0"


def test_get_program_trading_cumulative_trend(market_condition):
    expected_data = {
        "prm_trde_acc_trnsn": [
            {
                "dt": "20241125",
                "kospi200": "0.00",
                "basis": "0.00",
                "dfrt_trde_tdy": "0",
                "dfrt_trde_acc": "+353665",
                "ndiffpro_trde_tdy": "0",
                "ndiffpro_trde_acc": "+671219",
                "all_tdy": "0",
                "all_acc": "+1024884",
            },
            {
                "dt": "20241122",
                "kospi200": "+341.13",
                "basis": "-8.48",
                "dfrt_trde_tdy": "+8444",
                "dfrt_trde_acc": "+353665",
                "ndiffpro_trde_tdy": "+36403",
                "ndiffpro_trde_acc": "+671219",
                "all_tdy": "+44846",
                "all_acc": "+1024884",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90007"},
        )
        response = market_condition.get_program_trading_cumulative_trend("20250101", "1", "0", "1")

        assert isinstance(response.body, DomesticMarketConditionProgramTradingCumulativeTrend)
        assert response.body.prm_trde_acc_trnsn[0].dt == "20241125"
        assert response.body.prm_trde_acc_trnsn[0].kospi200 == "0.00"


def test_get_program_trading_trend_by_stock_and_time(market_condition):
    expected_data = {
        "stk_tm_prm_trde_trnsn": [
            {
                "tm": "153029",
                "cur_prc": "+245500",
                "pre_sig": "2",
                "pred_pre": "+40000",
                "flu_rt": "+19.46",
                "trde_qty": "104006",
                "prm_sell_amt": "14245",
                "prm_buy_amt": "10773",
                "prm_netprps_amt": "--3472",
                "prm_netprps_amt_irds": "+771",
                "prm_sell_qty": "58173",
                "prm_buy_qty": "43933",
                "prm_netprps_qty": "--14240",
                "prm_netprps_qty_irds": "+3142",
                "base_pric_tm": "",
                "dbrt_trde_rpy_sum": "",
                "remn_rcvord_sum": "",
                "stex_tp": "KRX",
            },
            {
                "tm": "153001",
                "cur_prc": "+245500",
                "pre_sig": "2",
                "pred_pre": "+40000",
                "flu_rt": "+19.46",
                "trde_qty": "94024",
                "prm_sell_amt": "12596",
                "prm_buy_amt": "8353",
                "prm_netprps_amt": "--4243",
                "prm_netprps_amt_irds": "0",
                "prm_sell_qty": "51455",
                "prm_buy_qty": "34073",
                "prm_netprps_qty": "--17382",
                "prm_netprps_qty_irds": "0",
                "base_pric_tm": "",
                "dbrt_trde_rpy_sum": "",
                "remn_rcvord_sum": "",
                "stex_tp": "KRX",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90008"},
        )
        response = market_condition.get_program_trading_trend_by_stock_and_time("1", "039490", "20250101")

        assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByStockAndTime)
        assert response.body.stk_tm_prm_trde_trnsn[0].tm == "153029"
        assert response.body.stk_tm_prm_trde_trnsn[0].cur_prc == "+245500"


def test_get_program_trading_trend_by_date(market_condition):
    expected_data = {
        "prm_trde_trnsn": [
            {
                "cntr_tm": "20241125000000",
                "dfrt_trde_sel": "0",
                "dfrt_trde_buy": "0",
                "dfrt_trde_netprps": "0",
                "ndiffpro_trde_sel": "0",
                "ndiffpro_trde_buy": "0",
                "ndiffpro_trde_netprps": "0",
                "dfrt_trde_sell_qty": "0",
                "dfrt_trde_buy_qty": "0",
                "dfrt_trde_netprps_qty": "0",
                "ndiffpro_trde_sell_qty": "0",
                "ndiffpro_trde_buy_qty": "0",
                "ndiffpro_trde_netprps_qty": "0",
                "all_sel": "0",
                "all_buy": "0",
                "all_netprps": "0",
                "kospi200": "0.00",
                "basis": "",
            },
            {
                "cntr_tm": "20241122000000",
                "dfrt_trde_sel": "0",
                "dfrt_trde_buy": "0",
                "dfrt_trde_netprps": "-0",
                "ndiffpro_trde_sel": "96",
                "ndiffpro_trde_buy": "608",
                "ndiffpro_trde_netprps": "+512",
                "dfrt_trde_sell_qty": "0",
                "dfrt_trde_buy_qty": "0",
                "dfrt_trde_netprps_qty": "-0",
                "ndiffpro_trde_sell_qty": "1",
                "ndiffpro_trde_buy_qty": "7",
                "ndiffpro_trde_netprps_qty": "+6",
                "all_sel": "96",
                "all_buy": "608",
                "all_netprps": "512",
                "kospi200": "+341.13",
                "basis": "-8.48",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90010"},
        )
        response = market_condition.get_program_trading_trend_by_date("20250101", "1", "P00101", "0", "1")

        assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByDate)
        assert response.body.prm_trde_trnsn[0].cntr_tm == "20241125000000"
        assert response.body.prm_trde_trnsn[0].dfrt_trde_sel == "0"


def test_get_program_trading_trend_by_stock_and_date(market_condition):
    expected_data = {
        "stk_daly_prm_trde_trnsn": [
            {
                "dt": "20241125",
                "cur_prc": "+267000",
                "pre_sig": "2",
                "pred_pre": "+60000",
                "flu_rt": "+28.99",
                "trde_qty": "3",
                "prm_sell_amt": "0",
                "prm_buy_amt": "0",
                "prm_netprps_amt": "0",
                "prm_netprps_amt_irds": "0",
                "prm_sell_qty": "0",
                "prm_buy_qty": "0",
                "prm_netprps_qty": "0",
                "prm_netprps_qty_irds": "0",
                "base_pric_tm": "",
                "dbrt_trde_rpy_sum": "",
                "remn_rcvord_sum": "",
                "stex_tp": "통합",
            },
            {
                "dt": "20241122",
                "cur_prc": "0",
                "pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "prm_sell_amt": "0",
                "prm_buy_amt": "0",
                "prm_netprps_amt": "0",
                "prm_netprps_amt_irds": "--6",
                "prm_sell_qty": "0",
                "prm_buy_qty": "0",
                "prm_netprps_qty": "0",
                "prm_netprps_qty_irds": "--19",
                "base_pric_tm": "",
                "dbrt_trde_rpy_sum": "",
                "remn_rcvord_sum": "",
                "stex_tp": "KRX",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/mrkcond",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka90013"},
        )
        response = market_condition.get_program_trading_trend_by_stock_and_date("1", "039490", "20250101")
        assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByStockAndDate)
        assert response.body.stk_daly_prm_trde_trnsn[0].dt == "20241125"
        assert response.body.stk_daly_prm_trde_trnsn[0].cur_prc == "+267000"
