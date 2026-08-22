"""Unit tests for NH PLUG overseas stock quote APIs (gbstock quote)."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_DEV = "https://moapi.nhplug.com:8443"

CURRENT_PRICE_URL = f"{BASE_DEV}/gbstock/quote/v1/current"
EXECUTION_TREND_URL = f"{BASE_DEV}/gbstock/quote/v1/executionTrend"

EXECUTION_TREND_OK_BODY = {
    "Output_0": [
        {
            "iem_cd": "AAPL",
            "trade_date": "20260821",
            "trade_time": "153000",
            "trdprc": 227.55,
            "netchng_cls": "2",
            "netchng": 1.25,
            "pctchng": 0.55,
            "turnover": 10251345000.0,
            "fill_size": 100,
            "acvol": 45123456,
            "open_prc": 226.5,
            "high": 228.0,
            "low": 225.75,
            "best_ask1": 227.6,
            "best_bid1": 227.5,
            "cont_rate": 105.3,
            "nextbutton": "0",
            "ctsz18": "000000000000000001",
        }
    ],
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}

CURRENT_PRICE_OK_BODY = {
    "Output_0": {
        "iem_cd": "AAPL",
        "kor_name": "애플",
        "industry_code": "0570",
        "industry_name": "컴퓨터와 주변기기",
        "trdprc": 227.55,
        "netchng_cls": "2",
        "netchng": 1.25,
        "pctchng": 0.55,
        "open_prc": 226.5,
        "high": 228.0,
        "low": 225.75,
        "acvol": 45123456,
        "uplimit": 0.0,
        "uplimit_rate": 0.0,
        "lolimit": 0.0,
        "lolimit_rate": 0.0,
        "w52high_prc": 237.23,
        "w52highprc_netchng": -9.68,
        "w52high_date": "20260115",
        "w52low_prc": 164.08,
        "w52lowprc_netchng": 63.47,
        "w52low_date": "20250422",
        "quote_time": "153000",
        "best_ask1": 227.6,
        "best_bid1": 227.5,
        "best_asiz1": 100,
        "best_bsiz1": 150,
        "asksize": 5000,
        "bidsize": 5200,
        "cov_pric": 227.55,
        "currency_prc": 1330.5,
        "list_num": 15000000000.0,
        "list_amt": 3413250000000.0,
        "list_amt_2": 4541674162500.0,
        "turnover": 10251345000.0,
        "currency_unit": "USD",
        "hst_trdprc": 226.3,
        "capital_amt": 0.0,
        "base_prc": 226.3,
        "eps_date": "20260101",
        "eps_prc": 6.13,
        "per_prc": 37.12,
        "trading_unit": 1.0,
        "hst_acvol": 40234567,
        "trade_date": "20260821",
        "exch_id": "NAS",
        "exch_name": "나스닥",
        "com_kind": "01",
        "com_kind_name": "보통주",
        "pf_jgubun": "0",
        "pf_trdprc": 227.6,
        "pf_netchng_cls": "2",
        "pf_netchng": 0.05,
        "pf_pctchng": 0.02,
        "marketperiod_cls": "1",
        "normal_trdprc": 227.55,
        "normal_netchng_cls": "2",
        "normal_netchng": 1.25,
        "normal_pctchng": 0.55,
        "normal_acvol": 45123456.0,
        "normal_open_prc": 226.5,
        "normal_high": 228.0,
        "normal_low": 225.75,
    },
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="dev")


class TestGetCurrentPrice:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(CURRENT_PRICE_URL, json=CURRENT_PRICE_OK_BODY)
            client.overseas_stock_quote.get_current_price(iem_cd="AAPL")

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "iem_cd": "AAPL",
            }
        }

    def test_parses_current_price_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(CURRENT_PRICE_URL, json=CURRENT_PRICE_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_quote.get_current_price(iem_cd="AAPL")

        assert response.body.output_0 is not None
        assert response.body.output_0.iem_cd == "AAPL"
        assert response.body.output_0.kor_name == "애플"
        assert response.body.output_0.trdprc == 227.55
        assert response.body.output_0.netchng == 1.25
        assert response.body.output_0.acvol == 45123456
        assert response.body.output_0.best_ask1 == 227.6
        assert response.body.output_0.best_bsiz1 == 150
        assert response.body.output_0.normal_trdprc == 227.55
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_parses_response_without_output_block(self, client):
        with requests_mock.Mocker() as m:
            m.post(CURRENT_PRICE_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_quote.get_current_price(iem_cd="AAPL")

        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(CURRENT_PRICE_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_quote.get_current_price(
                iem_cd="AAPL",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(CURRENT_PRICE_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_quote.get_current_price(iem_cd="AAPL")


class TestGetExecutionTrend:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(EXECUTION_TREND_URL, json=EXECUTION_TREND_OK_BODY)
            client.overseas_stock_quote.get_execution_trend(period_type="2", req_cnt=10, iem_cd="AAPL")

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "period_type": "2",
                "req_cnt": 10,
                "iem_cd": "AAPL",
            }
        }

    def test_parses_execution_trend_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(EXECUTION_TREND_URL, json=EXECUTION_TREND_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_quote.get_execution_trend(period_type="2", req_cnt=10, iem_cd="AAPL")

        assert response.body.output_0 is not None
        assert len(response.body.output_0) == 1
        item = response.body.output_0[0]
        assert item.iem_cd == "AAPL"
        assert item.trade_date == "20260821"
        assert item.trdprc == 227.55
        assert item.fill_size == 100
        assert item.acvol == 45123456
        assert item.cont_rate == 105.3
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_parses_response_without_output_block(self, client):
        with requests_mock.Mocker() as m:
            m.post(EXECUTION_TREND_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_quote.get_execution_trend(period_type="1", req_cnt=5, iem_cd="AAPL")

        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(EXECUTION_TREND_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_quote.get_execution_trend(
                period_type="1",
                req_cnt=5,
                iem_cd="AAPL",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(EXECUTION_TREND_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_quote.get_execution_trend(period_type="1", req_cnt=5, iem_cd="AAPL")
