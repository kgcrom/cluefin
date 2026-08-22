"""Unit tests for NH PLUG overseas stock order APIs (gbstock order)."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_DEV = "https://moapi.nhplug.com:8443"

BUY_URL = f"{BASE_DEV}/gbstock/order/v1/buy"
SELL_URL = f"{BASE_DEV}/gbstock/order/v1/sell"
MODIFY_URL = f"{BASE_DEV}/gbstock/order/v1/modify"

ORDER_OK_BODY = {
    "Output_0": {"amn_tab_cd": "0001", "orr_no": 12345},
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="dev")


class TestBuy:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUY_URL, json=ORDER_OK_BODY)
            client.overseas_stock_order.buy(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=1,
                ahi_nmn_pr_tp_cd="00",
                wtm_cur_knd_cd="1",
                fc_orr_uit_pr=150.25,
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "fc_sec_trd_nat_cd": "200",
                "iem_cd": "AAPL",
                "orr_qty": 1,
                "ahi_nmn_pr_tp_cd": "00",
                "wtm_cur_knd_cd": "1",
                "fc_orr_uit_pr": 150.25,
            }
        }

    def test_omits_price_when_market_order(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUY_URL, json=ORDER_OK_BODY)
            client.overseas_stock_order.buy(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=1,
                ahi_nmn_pr_tp_cd="03",
                wtm_cur_knd_cd="1",
            )

        assert "fc_orr_uit_pr" not in json.loads(m.request_history[0].text)["Input_0"]

    def test_parses_order_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUY_URL, json=ORDER_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_order.buy(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=1,
                ahi_nmn_pr_tp_cd="03",
                wtm_cur_knd_cd="1",
            )

        assert response.body.output_0.orr_no == 12345
        assert response.body.output_0.amn_tab_cd == "0001"
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_parses_body_without_output_block(self, client):
        # 응답 블록은 데이터가 있을 때만 내려온다.
        with requests_mock.Mocker() as m:
            m.post(BUY_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_order.buy(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=1,
                ahi_nmn_pr_tp_cd="03",
                wtm_cur_knd_cd="1",
            )

        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUY_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_order.buy(
                    act_no="50051036881",
                    fc_sec_trd_nat_cd="200",
                    iem_cd="AAPL",
                    orr_qty=1,
                    ahi_nmn_pr_tp_cd="03",
                    wtm_cur_knd_cd="1",
                )


class TestSell:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(SELL_URL, json=ORDER_OK_BODY)
            client.overseas_stock_order.sell(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=2,
                ahi_nmn_pr_tp_cd="00",
                fc_orr_uit_pr=151.5,
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "fc_sec_trd_nat_cd": "200",
                "iem_cd": "AAPL",
                "orr_qty": 2,
                "ahi_nmn_pr_tp_cd": "00",
                "fc_orr_uit_pr": 151.5,
            }
        }

    def test_omits_price_when_market_order(self, client):
        with requests_mock.Mocker() as m:
            m.post(SELL_URL, json=ORDER_OK_BODY)
            client.overseas_stock_order.sell(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=2,
                ahi_nmn_pr_tp_cd="03",
            )

        assert "fc_orr_uit_pr" not in json.loads(m.request_history[0].text)["Input_0"]

    def test_parses_order_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(SELL_URL, json=ORDER_OK_BODY)
            response = client.overseas_stock_order.sell(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                orr_qty=2,
                ahi_nmn_pr_tp_cd="03",
            )

        assert response.body.output_0.orr_no == 12345

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(SELL_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_order.sell(
                    act_no="50051036881",
                    fc_sec_trd_nat_cd="200",
                    iem_cd="AAPL",
                    orr_qty=2,
                    ahi_nmn_pr_tp_cd="03",
                )


class TestModify:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(MODIFY_URL, json=ORDER_OK_BODY)
            client.overseas_stock_order.modify(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                org_orr_no=12345,
                fc_orr_uit_pr=149.5,
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "fc_sec_trd_nat_cd": "200",
                "iem_cd": "AAPL",
                "org_orr_no": 12345,
                "fc_orr_uit_pr": 149.5,
            }
        }

    def test_sends_stop_base_price_when_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(MODIFY_URL, json=ORDER_OK_BODY)
            client.overseas_stock_order.modify(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                org_orr_no=12345,
                fc_orr_uit_pr=149.5,
                fc_stop_orr_bse_pr=148.0,
            )

        assert json.loads(m.request_history[0].text)["Input_0"]["fc_stop_orr_bse_pr"] == 148.0

    def test_parses_order_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(MODIFY_URL, json=ORDER_OK_BODY)
            response = client.overseas_stock_order.modify(
                act_no="50051036881",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                org_orr_no=12345,
                fc_orr_uit_pr=149.5,
            )

        assert response.body.output_0.orr_no == 12345

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(MODIFY_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_order.modify(
                    act_no="50051036881",
                    fc_sec_trd_nat_cd="200",
                    iem_cd="AAPL",
                    org_orr_no=12345,
                    fc_orr_uit_pr=149.5,
                )
