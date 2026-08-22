"""Unit tests for NH PLUG krstock inquiry APIs."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_PROD = "https://api.nhplug.com:8443"

BALANCE_BODY = {
    "rsp_cd": "00000",
    "rsp_msg": "조회가 완료되었습니다.",
    "message": None,
    "Output_0": {
        "dca": 1000000,
        "nas_amt": 5000000,
        "tot_aet_amt": 5200000,
        "act_no": "50051036881",
    },
    "Output_1": [
        {
            "iem_nm": "삼성전자",
            "iem_cd": "005930",
            "rsdl_qty": 10.0,
            "phs_pr": 70000,
            "now_pr": 71000,
            "eal_amt": 710000,
        }
    ],
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="prod")


class TestBalance:
    def test_sends_input_envelope_and_parses_output(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/inquiry/v1/balance", json=BALANCE_BODY, headers={"cts_flag": "N"})
            response = client.krstock_inquiry.balance(
                act_no="50051036881",
                bnc_bse_cd="1",
                ltg_aot_dit_cd="1",
                aet_bse="1",
                qut_dit_cd="UNT",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "bnc_bse_cd": "1",
                "ltg_aot_dit_cd": "1",
                "aet_bse": "1",
                "qut_dit_cd": "UNT",
            }
        }
        assert response.body.rsp_cd == "00000"
        assert response.body.output_0.act_no == "50051036881"
        assert response.body.output_0.nas_amt == 5000000
        assert len(response.body.output_1) == 1
        assert response.body.output_1[0].iem_cd == "005930"
        assert response.header.cts_flag == "N"

    def test_passes_cts_to_request_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/inquiry/v1/balance", json=BALANCE_BODY)
            client.krstock_inquiry.balance(
                act_no="50051036881",
                bnc_bse_cd="1",
                ltg_aot_dit_cd="1",
                aet_bse="1",
                qut_dit_cd="UNT",
                cts="NEXT-KEY",
            )

        request = m.request_history[0]
        assert request.headers["cts"] == "NEXT-KEY"
        assert request.headers["cts_flag"] == "Y"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/inquiry/v1/balance",
                json={"rsp_cd": "IGW40018", "rsp_msg": "계좌정보가 존재하지 않습니다."},
            )
            with pytest.raises(NHPlugAPIError, match="IGW40018"):
                client.krstock_inquiry.balance(
                    act_no="00000000000",
                    bnc_bse_cd="1",
                    ltg_aot_dit_cd="1",
                    aet_bse="1",
                    qut_dit_cd="UNT",
                )


DAILY_ORDER_EXECUTION_BODY = {
    "rsp_cd": "00000",
    "rsp_msg": "조회가 완료되었습니다.",
    "message": None,
    "Output_0": [{"cus_fnm": "홍길동"}],
    "Output_1": [
        {
            "itg_orr_no": 12345,
            "iem_cd": "005930",
            "iem_nm": "삼성전자",
            "orr_qty": 1,
            "tot_cns_qty": 1,
            "cns_amt": 71000,
        }
    ],
}


class TestDailyOrderExecution:
    def test_sends_input_envelope_and_parses_output(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/inquiry/v1/dailyOrderExecution",
                json=DAILY_ORDER_EXECUTION_BODY,
                headers={"cts_flag": "N"},
            )
            response = client.krstock_inquiry.daily_order_execution(
                act_no="50051036881",
                orr_dt="20260822",
                ost_cns_dit="0",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "orr_dt": "20260822",
                "act_no": "50051036881",
                "ost_cns_dit": "0",
            }
        }
        assert response.body.rsp_cd == "00000"
        # Output_0 은 스펙상 Object 지만 예시 응답은 Array — Array 로 온 케이스를 검증한다.
        assert isinstance(response.body.output_0, list)
        assert response.body.output_0[0].cus_fnm == "홍길동"
        assert len(response.body.output_1) == 1
        assert response.body.output_1[0].iem_cd == "005930"
        assert response.header.cts_flag == "N"

    def test_passes_cts_to_request_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/inquiry/v1/dailyOrderExecution", json=DAILY_ORDER_EXECUTION_BODY)
            client.krstock_inquiry.daily_order_execution(
                act_no="50051036881",
                orr_dt="20260822",
                ost_cns_dit="0",
                cts="NEXT-KEY",
            )

        request = m.request_history[0]
        assert request.headers["cts"] == "NEXT-KEY"
        assert request.headers["cts_flag"] == "Y"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/inquiry/v1/dailyOrderExecution",
                json={"rsp_cd": "IGW40018", "rsp_msg": "계좌정보가 존재하지 않습니다."},
            )
            with pytest.raises(NHPlugAPIError, match="IGW40018"):
                client.krstock_inquiry.daily_order_execution(
                    act_no="00000000000",
                    orr_dt="20260822",
                    ost_cns_dit="0",
                )

    def test_accepts_mock_success_code_xa102(self, client):
        # 모의서버는 조회 성공에 XA102("모의투자 조회가 완료되었습니다")를
        # 반환한다 (2026-08-22 실측) — 에러로 올리면 안 된다.
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/inquiry/v1/dailyOrderExecution",
                json={"rsp_cd": "XA102", "rsp_msg": "모의투자 조회가 완료되었습니다", "Output_0": []},
            )
            response = client.krstock_inquiry.daily_order_execution(
                act_no="50051036881",
                orr_dt="20260822",
                ost_cns_dit="0",
            )

        assert response.body.rsp_cd == "XA102"
