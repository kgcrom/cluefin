import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_etf_types import (
    DomesticEtfDailyExecution,
    DomesticEtfDailyTrend,
    DomesticEtfFullPrice,
    DomesticEtfHourlyExecution,
    DomesticEtfHourlyExecutionV2,
    DomesticEtfHourlyTrend,
    DomesticEtfHourlyTrendV2,
    DomesticEtfItemInfo,
    DomesticEtfReturnRate,
)


@pytest.fixture
def client():
    return Client(
        token="test_token",
        env="dev",
    )


def test_get_etf_return_rate(client: Client):
    expected_data = {
        "etfprft_rt_lst": [
            {"etfprft_rt": "-1.33", "cntr_prft_rt": "-1.75", "for_netprps_qty": "0", "orgn_netprps_qty": ""}
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10008",
            },
        )

        response = client.etf.get_etf_return_rate("069500", "001", "0")
        assert response is not None
        assert isinstance(response.body, DomesticEtfReturnRate)
        assert response.body.etfprft_rt_lst[0].etfprft_rt == "-1.33"


def test_get_etf_item_info(client: Client):
    expected_data = {
        "stk_nm": "KODEX 200",
        "etfobjt_idex_nm": "",
        "wonju_pric": "10",
        "etftxon_type": "보유기간과세",
        "etntxon_type": "보유기간과세",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40002",
            },
        )

        response = client.etf.get_etf_item_info("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfItemInfo)
        assert response.body.stk_nm == "KODEX 200"


def test_get_etf_daily_trend(client: Client):
    expected_data = {
        "etfdaly_trnsn": [
            {
                "cntr_dt": "20241125",
                "cur_prc": "100535",
                "pre_sig": "0",
                "pred_pre": "0",
                "pre_rt": "0.00",
                "trde_qty": "0",
                "nav": "0.00",
                "acc_trde_prica": "0",
                "navidex_dispty_rt": "0.00",
                "navetfdispty_rt": "0.00",
                "trace_eor_rt": "0",
                "trace_cur_prc": "0",
                "trace_pred_pre": "0",
                "trace_pre_sig": "3",
            },
            {
                "cntr_dt": "20241122",
                "cur_prc": "100535",
                "pre_sig": "0",
                "pred_pre": "0",
                "pre_rt": "0.00",
                "trde_qty": "0",
                "nav": "+100584.57",
                "acc_trde_prica": "0",
                "navidex_dispty_rt": "0.00",
                "navetfdispty_rt": "-0.05",
                "trace_eor_rt": "0",
                "trace_cur_prc": "0",
                "trace_pred_pre": "0",
                "trace_pre_sig": "3",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40003",
            },
        )

        response = client.etf.get_etf_daily_trend("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfDailyTrend)
        assert response.body.etfdaly_trnsn[0].cntr_dt == "20241125"


def test_get_etf_full_price(client: Client):
    expected_data = {
        "etfall_mrpr": [
            {
                "stk_cd": "069500",
                "stk_cls": "19",
                "stk_nm": "KODEX 200",
                "close_pric": "24200",
                "pre_sig": "3",
                "pred_pre": "0",
                "pre_rt": "0.00",
                "trde_qty": "0",
                "nav": "25137.83",
                "trace_eor_rt": "0.00",
                "txbs": "",
                "dvid_bf_base": "",
                "pred_dvida": "",
                "trace_idex_nm": "KOSPI100",
                "drng": "",
                "trace_idex_cd": "",
                "trace_idex": "24200",
                "trace_flu_rt": "0.00",
            },
            {
                "stk_cd": "069500",
                "stk_cls": "19",
                "stk_nm": "KODEX 200",
                "close_pric": "33120",
                "pre_sig": "3",
                "pred_pre": "0",
                "pre_rt": "0.00",
                "trde_qty": "0",
                "nav": "33351.27",
                "trace_eor_rt": "0.00",
                "txbs": "",
                "dvid_bf_base": "",
                "pred_dvida": "",
                "trace_idex_nm": "KOSPI200",
                "drng": "",
                "trace_idex_cd": "",
                "trace_idex": "33120",
                "trace_flu_rt": "0.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40004",
            },
        )

        response = client.etf.get_etf_full_price("0", "0", "0000", "0", "0", "1")
        assert response is not None
        assert isinstance(response.body, DomesticEtfFullPrice)


def test_get_etf_hourly_trend(client: Client):
    expected_data = {
        "stk_nm": "KODEX 200",
        "etfobjt_idex_nm": "KOSPI200",
        "wonju_pric": "-10",
        "etftxon_type": "보유기간과세",
        "etntxon_type": "보유기간과세",
        "etftisl_trnsn": [
            {
                "tm": "132211",
                "close_pric": "+4900",
                "pre_sig": "2",
                "pred_pre": "+450",
                "flu_rt": "+10.11",
                "trde_qty": "1",
                "nav": "-4548.33",
                "trde_prica": "0",
                "navidex": "-72.38",
                "navetf": "+7.18",
                "trace": "0.00",
                "trace_idex": "+164680",
                "trace_idex_pred_pre": "+123",
                "trace_idex_pred_pre_sig": "2",
            },
            {
                "tm": "132210",
                "close_pric": "+4900",
                "pre_sig": "2",
                "pred_pre": "+450",
                "flu_rt": "+10.11",
                "trde_qty": "1",
                "nav": "-4548.33",
                "trde_prica": "0",
                "navidex": "-72.38",
                "navetf": "+7.18",
                "trace": "0.00",
                "trace_idex": "+164680",
                "trace_idex_pred_pre": "+123",
                "trace_idex_pred_pre_sig": "2",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40005",
            },
        )

        response = client.etf.get_etf_hourly_trend("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfHourlyTrend)
        assert response.body.etftisl_trnsn[0].tm == "132211"


def test_get_etf_hourly_execution(client: Client):
    expected_data = {
        "stk_cls": "20",
        "stk_nm": "KODEX 200",
        "etfobjt_idex_nm": "KOSPI200",
        "etfobjt_idex_cd": "207",
        "objt_idex_pre_rt": "10.00",
        "wonju_pric": "-10",
        "etftisl_cntr_array": [
            {
                "cntr_tm": "130747",
                "cur_prc": "+4900",
                "pre_sig": "2",
                "pred_pre": "+450",
                "trde_qty": "1",
                "stex_tp": "KRX",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40006",
            },
        )

        response = client.etf.get_etf_hourly_execution("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfHourlyExecution)
        assert response.body.etfobjt_idex_nm == "KOSPI200"


def test_get_etf_daily_execution(client: Client):
    expected_data = {
        "cntr_tm": "130747",
        "cur_prc": "+4900",
        "pre_sig": "2",
        "pred_pre": "+450",
        "trde_qty": "1",
        "etfnetprps_qty_array": [
            {
                "dt": "20241125",
                "cur_prc_n": "+4900",
                "pre_sig_n": "2",
                "pred_pre_n": "+450",
                "acc_trde_qty": "1",
                "for_netprps_qty": "0",
                "orgn_netprps_qty": "0",
            },
            {
                "dt": "20241122",
                "cur_prc_n": "-4450",
                "pre_sig_n": "5",
                "pred_pre_n": "-60",
                "acc_trde_qty": "46",
                "for_netprps_qty": "--10558895",
                "orgn_netprps_qty": "0",
            },
            {
                "dt": "20241121",
                "cur_prc_n": "4510",
                "pre_sig_n": "3",
                "pred_pre_n": "0",
                "acc_trde_qty": "0",
                "for_netprps_qty": "--8894146",
                "orgn_netprps_qty": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40007",
            },
        )

        response = client.etf.get_etf_daily_execution("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfDailyExecution)
        assert response.body.etfnetprps_qty_array[0].dt == "20241125"


def test_get_etf_hourly_execution_v2(client: Client):
    expected_data = {
        "etfnavarray": [
            {
                "nav": "",
                "navpred_pre": "",
                "navflu_rt": "",
                "trace_eor_rt": "",
                "dispty_rt": "",
                "stkcnt": "133100",
                "base_pric": "4450",
                "for_rmnd_qty": "",
                "repl_pric": "",
                "conv_pric": "",
                "drstk": "",
                "wonju_pric": "",
            },
            {
                "nav": "",
                "navpred_pre": "",
                "navflu_rt": "",
                "trace_eor_rt": "",
                "dispty_rt": "",
                "stkcnt": "133100",
                "base_pric": "4510",
                "for_rmnd_qty": "",
                "repl_pric": "",
                "conv_pric": "",
                "drstk": "",
                "wonju_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40008",
            },
        )

        response = client.etf.get_etf_hourly_execution_v2("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfHourlyExecutionV2)


def test_get_etf_hourly_trend_v2(client: Client):
    expected_data = {
        "etftisl_trnsn": [
            {"cur_prc": "4450", "pre_sig": "3", "pred_pre": "0", "trde_qty": "0", "for_netprps": "0"},
            {"cur_prc": "-4450", "pre_sig": "5", "pred_pre": "-60", "trde_qty": "46", "for_netprps": "--10558895"},
            {"cur_prc": "4510", "pre_sig": "3", "pred_pre": "0", "trde_qty": "0", "for_netprps": "--8894146"},
            {"cur_prc": "-4510", "pre_sig": "5", "pred_pre": "-160", "trde_qty": "0", "for_netprps": "--3073507"},
            {"cur_prc": "+4670", "pre_sig": "2", "pred_pre": "+160", "trde_qty": "94", "for_netprps": "--2902200"},
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/etf",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka40009",
            },
        )

        response = client.etf.get_etf_hourly_trend_v2("069500")
        assert response is not None
        assert isinstance(response.body, DomesticEtfHourlyTrendV2)
        assert response.body.etftisl_trnsn[0].cur_prc == "4450"
        assert response.body.etftisl_trnsn[1].pre_sig == "5"
