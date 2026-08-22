"""Unit tests for NH PLUG krstock quote APIs."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_PROD = "https://api.nhplug.com:8443"

CURRENT_PRICE_BODY = {
    "rsp_cd": "00000",
    "rsp_msg": "조회가 완료되었습니다.",
    "message": None,
    "Output_0": {
        "iem_cd": "005930",
        "iem_nm": "*삼성전자",
        "stck_prpr": 281500,
        "prdy_vrss_sign": "2",
    },
    "Output_1": [
        {
            "bsop_hour": "153000",
            "stck_prpr": 281500,
            "acml_vol": 12345678,
        }
    ],
    "Output_2": {
        "cncc_aspr_code": "1",
        "antc_cnpr": "281500",
    },
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="prod")


class TestCurrentPrice:
    def test_sends_input_envelope_and_parses_output(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/quote/v1/currentPrice", json=CURRENT_PRICE_BODY)
            response = client.krstock_quote.current_price(market_cd="KRX", iem_cd="005930")

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "market_cd": "KRX",
                "iem_cd": "005930",
            }
        }
        assert response.body.rsp_cd == "00000"
        assert response.body.output_0.stck_prpr == 281500
        assert response.body.output_0.iem_nm == "*삼성전자"
        assert len(response.body.output_1) == 1
        assert response.body.output_1[0].bsop_hour == "153000"
        # Output_2 은 스펙상 Array 지만 예시 응답은 Object — Object 로 온 케이스를 검증한다.
        assert not isinstance(response.body.output_2, list)
        assert response.body.output_2.cncc_aspr_code == "1"

    def test_parses_body_without_output_blocks(self, client):
        # Output_N 블록은 데이터가 있을 때만 내려온다.
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/krstock/quote/v1/currentPrice", json={"rsp_cd": "00000", "rsp_msg": "ok"})
            response = client.krstock_quote.current_price(market_cd="KRX", iem_cd="005930")

        assert response.body.output_0 is None
        assert response.body.output_1 is None
        assert response.body.output_2 is None

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/krstock/quote/v1/currentPrice",
                json={"rsp_cd": "IGW40018", "rsp_msg": "종목코드가 존재하지 않습니다."},
            )
            with pytest.raises(NHPlugAPIError, match="IGW40018"):
                client.krstock_quote.current_price(market_cd="KRX", iem_cd="999999")
