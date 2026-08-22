"""Unit tests for NH PLUG overseas stock inquiry APIs (gbstock inquiry)."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_DEV = "https://moapi.nhplug.com:8443"

BUYABLE_AMOUNT_URL = f"{BASE_DEV}/gbstock/inquiry/v1/buyableAmount"

BUYABLE_AMOUNT_OK_BODY = {
    "Output_0": {
        "fc_dca": 10000.5,
        "mgg_fc_amt": 0.0,
        "csh_wtm": 500.25,
        "re_use_obj_amt": 0.0,
        "re_use_rtr_use_amt": 0.0,
        "ect_use_amt": 0.0,
        "orr_pbl_amt": 9500.25,
        "wtm_cur_cd": "USD",
        "hld_qty": 10,
        "orr_pbl_qty": 63,
        "sll_pbl_qty": 10,
        "sll_pbl_qty1": 10,
        "byn_cns_qty": 0,
        "sll_cns_qty": 0,
        "sll_orr_qty": 0,
        "dps_rsc_qty": 0,
        "byn_pbl_qty": 63,
        "max_pbl_amt": 9500.25,
        "max_pbl_qty": 63,
        "csh_wtm_rt": 0.25,
    },
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


@pytest.fixture
def client() -> HttpClient:
    return HttpClient(token="TOKEN", app_key="test-app-key", secret_key="test-secret", env="dev")


class TestGetBuyableAmount:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUYABLE_AMOUNT_URL, json=BUYABLE_AMOUNT_OK_BODY)
            client.overseas_stock_inquiry.get_buyable_amount(
                act_no="50051036881",
                pcs_dit="1",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                wtm_cur_knd_cd="1",
                oss_orr_knd_cd="1",
                ahi_nmn_pr_tp_cd="00",
                fc_orr_uit_pr=150.25,
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "pcs_dit": "1",
                "fc_sec_trd_nat_cd": "200",
                "iem_cd": "AAPL",
                "wtm_cur_knd_cd": "1",
                "oss_orr_knd_cd": "1",
                "ahi_nmn_pr_tp_cd": "00",
                "fc_orr_uit_pr": 150.25,
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUYABLE_AMOUNT_URL, json=BUYABLE_AMOUNT_OK_BODY)
            client.overseas_stock_inquiry.get_buyable_amount(
                act_no="50051036881",
                pcs_dit="2",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                wtm_cur_knd_cd="1",
                oss_orr_knd_cd="1",
                ahi_nmn_pr_tp_cd="03",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "fc_orr_uit_pr" not in sent
        assert "cfd_lon_cd" not in sent
        assert "lon_dt" not in sent

    def test_parses_buyable_amount_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUYABLE_AMOUNT_URL, json=BUYABLE_AMOUNT_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_buyable_amount(
                act_no="50051036881",
                pcs_dit="1",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                wtm_cur_knd_cd="1",
                oss_orr_knd_cd="1",
                ahi_nmn_pr_tp_cd="03",
            )

        assert response.body.output_0.orr_pbl_amt == 9500.25
        assert response.body.output_0.byn_pbl_qty == 63
        assert response.body.output_0.wtm_cur_cd == "USD"
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUYABLE_AMOUNT_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_buyable_amount(
                act_no="50051036881",
                pcs_dit="1",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                wtm_cur_knd_cd="1",
                oss_orr_knd_cd="1",
                ahi_nmn_pr_tp_cd="03",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(BUYABLE_AMOUNT_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_buyable_amount(
                    act_no="50051036881",
                    pcs_dit="1",
                    fc_sec_trd_nat_cd="200",
                    iem_cd="AAPL",
                    wtm_cur_knd_cd="1",
                    oss_orr_knd_cd="1",
                    ahi_nmn_pr_tp_cd="03",
                )
