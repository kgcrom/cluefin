"""Unit tests for NH PLUG common APIs (account list, websocket session close)."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import (
    NHPlugAPIError,
    NHPlugAuthenticationError,
    NHPlugRateLimitError,
)
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_PROD = "https://api.nhplug.com:8443"
BASE_DEV = "https://moapi.nhplug.com:8443"

ACCTINFO_BODY = {
    "rsp_cd": "00000",
    "rsp_msg": "조회가 완료되었습니다.",
    "cust_no": "100805701",
    "Output_0": [
        {"acct_no": "20101036881", "acct_type": "01"},
        {"acct_no": "50051036881", "acct_type": "03"},
    ],
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="prod")


class TestHttpClient:
    def test_base_url_by_env(self, client):
        assert client.base_url == BASE_PROD
        dev = HttpClient(token="t", app_key="k", secret_key="s", env="dev")
        assert dev.base_url == BASE_DEV

    def test_post_wraps_input_envelope_and_auth_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", json=ACCTINFO_BODY)
            client.post("/n2/acctinfo", body={"foo": "bar"})

        request = m.request_history[0]
        assert json.loads(request.text) == {"Input_0": {"foo": "bar"}}
        assert request.headers["Authorization"] == "Bearer TOKEN"
        assert request.headers["x-client-id"] == "test-app-key"
        assert request.headers["x-client-secret"] == "test-secret"

    def test_post_sends_cts_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", json=ACCTINFO_BODY)
            client.post("/n2/acctinfo", cts="NEXT-KEY")

        request = m.request_history[0]
        assert request.headers["cts"] == "NEXT-KEY"
        assert request.headers["cts_flag"] == "Y"

    def test_post_maps_401_to_authentication_error(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", status_code=401, json={})
            with pytest.raises(NHPlugAuthenticationError):
                client.post("/n2/acctinfo")

    def test_post_retries_429_then_raises(self):
        client = HttpClient(token="t", app_key="k", secret_key="s", env="prod", max_retries=1)
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", status_code=429, json={})
            with pytest.raises(NHPlugRateLimitError):
                client.post("/n2/acctinfo")

        # initial attempt + 1 retry
        assert m.call_count == 2


class TestGetAccountList:
    def test_parses_accounts(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", json=ACCTINFO_BODY, headers={"cts_flag": "N"})
            response = client.common.get_account_list()

        assert response.body.cust_no == "100805701"
        assert len(response.body.output_0) == 2
        assert response.body.output_0[0].acct_no == "20101036881"
        assert response.body.output_0[1].acct_type == "03"
        assert response.header.cts_flag == "N"

    def test_parses_body_without_envelope_fields(self, client):
        # 응답 예시에는 rsp_cd 없이 Output_0 만 오는 경우가 있다.
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", json={"Output_0": [{"acct_no": "1", "acct_type": "01"}]})
            response = client.common.get_account_list()

        assert response.body.rsp_cd is None
        assert response.body.output_0[0].acct_no == "1"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(f"{BASE_PROD}/n2/acctinfo", json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.common.get_account_list()


class TestCloseWebsocketSession:
    def test_parses_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                f"{BASE_PROD}/websocket/close/session",
                json={"rsp_cd": "00000", "rsp_msg": "정상처리 되었습니다."},
            )
            response = client.common.close_websocket_session()

        assert response.body.rsp_cd == "00000"
        assert json.loads(m.request_history[0].text) == {"Input_0": {}}
