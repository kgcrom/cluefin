"""Unit tests for NH PLUG krstock order APIs."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_PROD = "https://api.nhplug.com:8443"

CASH_BUY_BODY = {
    "rsp_cd": "00000",
    "rsp_msg": "정상 처리되었습니다.",
    "message": None,
    "Output_0": {
        "orr_gno_tab_cd": "0001",
        "mkt_orr_no": 12345,
        "orr_qty1": 1,
    },
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="prod")


class TestCashBuy:
    def test_sends_input_envelope_and_parses_output(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/order/v1/cashBuy", json=CASH_BUY_BODY)
            response = client.krstock_order.cash_buy(
                act_no="50051036881",
                iem_cd="005930",
                orr_qty=1,
                nmn_pr_tp_cd="01",
                rmt_mkt_cd="KRX",
                sor_mkt_sli_yn="N",
                orr_pr=50000,
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "iem_cd": "005930",
                "orr_qty": 1,
                "orr_pr": 50000,
                "nmn_pr_tp_cd": "01",
                "orr_cnd_dit_cd": "00",
                "ssl_nmn_pr_dit_cd": "00",
                "rmt_mkt_cd": "KRX",
                "sor_mkt_sli_yn": "N",
            }
        }
        assert response.body.rsp_cd == "00000"
        assert response.body.output_0.mkt_orr_no == 12345
        assert response.body.output_0.orr_gno_tab_cd == "0001"

    def test_market_order_omits_none_params(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/order/v1/cashBuy", json=CASH_BUY_BODY)
            client.krstock_order.cash_buy(
                act_no="50051036881",
                iem_cd="005930",
                orr_qty=1,
                nmn_pr_tp_cd="05",
                rmt_mkt_cd="KRX",
                sor_mkt_sli_yn="N",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "orr_pr" not in sent
        assert "orr_amt" not in sent
        assert "sop_cnd_pr" not in sent

    def test_parses_body_without_output_block(self, client):
        # Output_N 블록은 데이터가 있을 때만 내려온다.
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/order/v1/cashBuy", json={"rsp_cd": "00000", "rsp_msg": "ok"})
            response = client.krstock_order.cash_buy(
                act_no="50051036881",
                iem_cd="005930",
                orr_qty=1,
                nmn_pr_tp_cd="05",
                rmt_mkt_cd="KRX",
                sor_mkt_sli_yn="N",
            )

        assert response.body.output_0 is None

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/order/v1/cashBuy",
                json={"rsp_cd": "IGW40018", "rsp_msg": "계좌정보가 존재하지 않습니다."},
            )
            with pytest.raises(NHPlugAPIError, match="IGW40018"):
                client.krstock_order.cash_buy(
                    act_no="00000000000",
                    iem_cd="005930",
                    orr_qty=1,
                    nmn_pr_tp_cd="05",
                    rmt_mkt_cd="KRX",
                    sor_mkt_sli_yn="N",
                )


class TestCashSell:
    def test_sends_input_envelope_and_parses_output(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/order/v1/cashSell", json=CASH_BUY_BODY)
            response = client.krstock_order.cash_sell(
                act_no="50051036881",
                iem_cd="005930",
                orr_qty=1,
                nmn_pr_tp_cd="01",
                rmt_mkt_cd="KRX",
                sor_mkt_sli_yn="N",
                orr_pr=50000,
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert sent["iem_cd"] == "005930"
        assert sent["orr_pr"] == 50000
        assert "orr_amt" not in sent
        assert response.body.output_0.mkt_orr_no == 12345

    def test_raises_on_failing_rsp_cd_kept_as_env_code(self, client):
        # 주문 거부(휴일 등)는 HTTP 200 + rsp_cd 로 온다 (2026-08-22 실측: 14100).
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/order/v1/cashSell",
                json={"rsp_cd": "14100", "rsp_msg": "모의투자 영업일이 아닙니다."},
            )
            with pytest.raises(NHPlugAPIError, match="14100"):
                client.krstock_order.cash_sell(
                    act_no="50051036881",
                    iem_cd="005930",
                    orr_qty=1,
                    nmn_pr_tp_cd="05",
                    rmt_mkt_cd="KRX",
                    sor_mkt_sli_yn="N",
                )


class TestCreditBuy:
    def test_sends_input_envelope_and_parses_output(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/order/v1/creditBuy", json=CASH_BUY_BODY)
            response = client.krstock_order.credit_buy(
                act_no="50051036881",
                iem_cd="005930",
                orr_qty=1,
                nmn_pr_tp_cd="01",
                cfd_lon_cd="01",
                rmt_mkt_cd="KRX",
                sor_mkt_sli_yn="N",
                orr_pr=50000,
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "iem_cd": "005930",
                "orr_qty": 1,
                "orr_pr": 50000,
                "nmn_pr_tp_cd": "01",
                "orr_cnd_dit_cd": "00",
                "cfd_lon_cd": "01",
                "rmt_mkt_cd": "KRX",
                "sor_mkt_sli_yn": "N",
            }
        }
        assert response.body.rsp_cd == "00000"
        assert response.body.output_0.mkt_orr_no == 12345
        assert response.body.output_0.orr_gno_tab_cd == "0001"

    def test_market_order_omits_none_params(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/order/v1/creditBuy", json=CASH_BUY_BODY)
            client.krstock_order.credit_buy(
                act_no="50051036881",
                iem_cd="005930",
                orr_qty=1,
                nmn_pr_tp_cd="05",
                cfd_lon_cd="03",
                rmt_mkt_cd="KRX",
                sor_mkt_sli_yn="N",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "orr_pr" not in sent
        assert "orr_amt" not in sent
        assert "lon_dt" not in sent
        assert "sop_cnd_pr" not in sent

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/order/v1/creditBuy",
                json={"rsp_cd": "IGW40018", "rsp_msg": "계좌정보가 존재하지 않습니다."},
            )
            with pytest.raises(NHPlugAPIError, match="IGW40018"):
                client.krstock_order.credit_buy(
                    act_no="00000000000",
                    iem_cd="005930",
                    orr_qty=1,
                    nmn_pr_tp_cd="05",
                    cfd_lon_cd="01",
                    rmt_mkt_cd="KRX",
                    sor_mkt_sli_yn="N",
                )
