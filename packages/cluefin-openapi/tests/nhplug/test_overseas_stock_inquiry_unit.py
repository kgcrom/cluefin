"""Unit tests for NH PLUG overseas stock inquiry APIs (gbstock inquiry)."""

import json

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

BASE_DEV = "https://moapi.nhplug.com:8443"

BUYABLE_AMOUNT_URL = f"{BASE_DEV}/gbstock/inquiry/v1/buyableAmount"
ORDER_EXECUTIONS_URL = f"{BASE_DEV}/gbstock/inquiry/v1/unexecuted"
BALANCE_URL = f"{BASE_DEV}/gbstock/inquiry/v1/balance"
RESERVED_ORDERS_URL = f"{BASE_DEV}/gbstock/inquiry/v1/reservedInquiry"
DAILY_TRANSACTIONS_URL = f"{BASE_DEV}/gbstock/inquiry/v1/dailyTransaction"
PERIOD_PNL_URL = f"{BASE_DEV}/gbstock/inquiry/v1/periodPnl"
PERIOD_PNL_DETAIL_URL = f"{BASE_DEV}/gbstock/inquiry/v1/periodPnlDetail"
MARGIN_URL = f"{BASE_DEV}/gbstock/inquiry/v1/margin"

ORDER_EXECUTIONS_OK_BODY = {
    "Output_0": [
        {
            "rgs_tm": "13024500",
            "oss_orr_knd_cd": "1",
            "orr_knd_nm": "지정가",
            "orr_no": 123456789,
            "org_orr_no": 0,
            "oss_sby_dit_cd": "2",
            "sby_dit_nm": "매수",
            "fc_sec_trd_nat_cd": "200",
            "mkt_dit_cd_nm": "나스닥",
            "iem_cd": "AAPL",
            "iem_nm": "애플",
            "orr_qty": 10,
            "fc_orr_uit_pr": 150.25,
            "cns_qty": 10,
            "cns_pr": 150.25,
            "ny_cns_orr_qty": 0,
            "cor_can_dit_cd": "0",
            "cor_can_dit_nm": "정상",
            "cor_qty": 0,
            "can_qty": 0,
            "oss_ato_orr_sts_cd": "1",
            "orr_sts_nm": "체결",
            "oms_cus_orr_no": "OMS0001",
            "rjt_rsn_cts": "",
            "ivs_nat_krx_dit_cd": "US",
            "fix_sgy_tgt_sgy_nm": "",
            "fix_orr_pcs_mtd_cd": "1",
            "orr_pcs_mtd_cd_nm": "일반",
            "rut_orr_krx_cd": "NAS",
            "hts_usr_id": "USER0001",
            "usr_ip_adr": "127.0.0.1",
            "cuc_mdi_cd": "01",
            "cuc_mdi_cd_nm": "HTS",
            "ahi_nmn_pr_tp_cd": "00",
            "ahi_nmn_pr_tp_cd_nm": "지정가",
            "fc_stop_orr_bse_pr": 0.0,
            "orr_pdt_dit_cd": "01",
            "orr_dt": "20260821",
            "csh_wtm_rt": 0.25,
            "cfd_lon_cd": "00",
            "cfd_lon_cd_nm": "현금",
            "lon_dt": "",
        }
    ],
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}

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


BALANCE_OK_BODY = {
    "Output_0": {
        "abk_amt": 10000000,
        "eal_amt_sum": 10500000,
        "eal_pls_sum_amt": 500000,
        "krw_pft_rt": 5.0,
        "krw_dca": 1000000,
        "krw_ny_stl_xcl_amt": 0,
        "tot_aet_amt": 11500000,
        "fc_abk_amt": 7500.5,
        "fc_eal_amt": 7875.75,
        "fc_eal_pls_amt": 375.25,
        "pft_rt": 5.0,
        "fc_dca": 750.0,
        "fc_ny_stl_xcl_amt": 0.0,
        "fc_aet_amt": 8625.75,
        "ptps_ttn_amt": 0.0,
        "ptps_ttn_amt1": 0.0,
    },
    "Output_1": [
        {
            "fc_sec_trd_nat_cd": "200",
            "fc_sec_trd_nat_nm": "미국",
            "iem_cd": "AAPL",
            "oss_iem_eng_nm": "APPLE INC",
            "iem_nm": "애플",
            "cns_bse_bnc_qty": 10,
            "sll_cns_qty": 0,
            "byn_cns_qty": 10,
            "sll_pbl_qty1": 10,
            "fc_abk_amt": 1500.25,
            "krw_abk_amt1": 2000000,
            "fc_phs_uit_pr": 150.025,
            "phs_uit_pr": 200000,
            "fc_sec_end_pr": 157.5,
            "end_pr": 210000,
            "fc_eal_amt": 1575.0,
            "krw_eal_amt": 2100000,
            "fc_eal_pls_amt": 74.75,
            "krw_eal_pls_amt": 100000,
            "eal_pft_rt": 4.98,
            "eal_pft_rt1": 4.98,
            "cur_cd": "USD",
            "phs_xcg_rt": 1330.5,
            "tdt_sby_bse_xcg_rt": 1332.0,
            "fc_mkt_dit_cd": "200",
            "fc_sll_pls_amt": 0.0,
            "krw_sll_pls_amt": 0,
            "fc_sll_pft_rt": 0.0,
            "krw_sll_pft_rt": 0.0,
            "fc_cns_bse_phs_xps": 1500.25,
            "krw_cns_bse_phs_xps": 2000000,
            "fc_avg_phs_pr": 150.025,
            "krw_avg_phs_pr": 200000,
            "fc_fee": 1.5,
            "krw_fee": 2000,
            "fc_tax_amt": 0.5,
            "krw_tax_amt": 700,
            "fc_pls_qtr_phs_pr": 150.5,
            "krw_pls_qtr_phs_pr": 200500,
            "sby_fee_rt": 0.001,
            "fc_stk_lws_sby_fee": 0.5,
            "cfd_lon_cd_nm": "현금",
            "lon_dt": "",
            "xrn_dt": "",
        },
        {
            "fc_sec_trd_nat_cd": "070",
            "fc_sec_trd_nat_nm": "일본",
            "iem_cd": "7203",
            "oss_iem_eng_nm": "TOYOTA MOTOR CORP",
            "iem_nm": "토요타자동차",
            "cns_bse_bnc_qty": 5,
            "sll_cns_qty": 0,
            "byn_cns_qty": 5,
            "sll_pbl_qty1": 5,
            "fc_abk_amt": 100000.0,
            "krw_abk_amt1": 900000,
            "fc_phs_uit_pr": 20000.0,
            "phs_uit_pr": 180000,
            "fc_sec_end_pr": 21000.0,
            "end_pr": 189000,
            "fc_eal_amt": 105000.0,
            "krw_eal_amt": 945000,
            "fc_eal_pls_amt": 5000.0,
            "krw_eal_pls_amt": 45000,
            "eal_pft_rt": 5.0,
            "eal_pft_rt1": 5.0,
            "cur_cd": "JPY",
            "phs_xcg_rt": 9.0,
            "tdt_sby_bse_xcg_rt": 9.05,
            "fc_mkt_dit_cd": "070",
            "fc_sll_pls_amt": 0.0,
            "krw_sll_pls_amt": 0,
            "fc_sll_pft_rt": 0.0,
            "krw_sll_pft_rt": 0.0,
            "fc_cns_bse_phs_xps": 100000.0,
            "krw_cns_bse_phs_xps": 900000,
            "fc_avg_phs_pr": 20000.0,
            "krw_avg_phs_pr": 180000,
            "fc_fee": 100.0,
            "krw_fee": 900,
            "fc_tax_amt": 50.0,
            "krw_tax_amt": 450,
            "fc_pls_qtr_phs_pr": 20050.0,
            "krw_pls_qtr_phs_pr": 180450,
            "sby_fee_rt": 0.001,
            "fc_stk_lws_sby_fee": 50.0,
            "cfd_lon_cd_nm": "현금",
            "lon_dt": "",
            "xrn_dt": "",
        },
    ],
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


RESERVED_ORDERS_OK_BODY = {
    "Output_0": [
        {
            "fc_mkt_dit_cd": "200",
            "bkg_orr_dt": "20260821",
            "act_no": "50051036881",
            "cus_fnm": "홍길동",
            "iem_cd": "AAPL",
            "iem_nm": "애플",
            "cur_cd": "USD",
            "sby_dit_cd": "2",
            "sby_dit_nm": "매수",
            "orr_qty": 10,
            "orr_pr": 150.25,
            "cns_qty": 10,
            "cns_pr": 150.25,
            "bkg_orr_can_yn": "7",
            "orr_can_dit_nm": "완료",
            "bkg_orr_rtn_dt": "20260821",
            "bkg_orr_rtn_tm": "090000",
            "rgs_tab_cd": "0001",
            "rgs_emp_no": "000001",
            "rgs_emp_fnm": "김직원",
            "cct_dt": "",
            "cct_tm": "",
            "cct_emp_no": "",
            "cct_emp_fnm": "",
            "bkg_rtn_orr_no": 1234567890,
            "orr_sno": 1,
            "ost_orr_mdi": "01",
            "orr_cpl_yn": "Y",
            "ost_pcs_cd": "00000",
            "pcs_msg_cts": "정상처리",
            "aca_tel_no": "01000000000",
            "ahi_nmn_pr_tp_cd": "00",
            "ahi_nmn_pr_tp_cd_nm": "지정가",
            "oss_orr_knd_cd_nm": "GTS(미국시장주문)",
            "ivs_sgy_cd_nm": "",
            "fc_csh_wtm": 0.0,
            "fc_csh_wtm_fee": 0.0,
            "fc_csh_wtm_tax_amt": 0.0,
            "fc_csh_wtm_trd_tax": 0.0,
            "fc_mkt_dit_cd_nm": "미국",
            "bkg_orr_tp_cd": "1",
            "bkg_orr_tp_cd_nm": "일반예약주문",
            "orr_enf_sta_dt": "20260821",
            "orr_enf_end_dt": "20260821",
            "acl_cns_qty": 10,
            "lst_orr_enf_dt": "20260821",
            "rmn_qty": 0,
            "wtm_cur_knd_cd": "1",
            "cd_nm": "",
            "fc_stop_orr_bse_pr": 0.0,
            "orr_pdt_dit_cd": "00",
            "cfd_lon_cd": "00",
            "cfd_lon_cd_nm": "일반거래",
            "lon_dt": "",
        }
    ],
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


DAILY_TRANSACTIONS_OK_BODY = {
    "Output_0": [
        {
            "trd_dt": "20260821",
            "trd_sno": 1,
            "act_trd_tp_nm": "매수",
            "sps_cd_nm": "해외주식매수",
            "iem_krl_nm": "애플",
            "iem_cd": "AAPL",
            "trd_qty": 10.0,
            "trd_uit_pr": 150.25,
            "cur_cd_nm": "달러",
            "aly_xcg_rt": 1330.5,
            "trd_bf_bnc_qty": 0.0,
            "trd_af_bnc_qty": 10.0,
            "fc_trd_amt": 1502.5,
            "krw_trd_amt": 1999576,
            "trd_af_fc_dca": 8497.5,
            "trd_af_dca": 11305192,
            "trd_af_fc_mgg_amt": 0.0,
            "trd_af_krw_mgg_amt": 0,
            "abd_sdr_xps_fc_amt": 0.0,
            "tsl_mgg_amt": 0.0,
            "ose_fee": 1.5,
            "dmt_fee": 0,
            "icm_tax": 0.0,
            "rsd_tax": 0.0,
            "rgs_cuc_mdi_cd_nm": "HTS",
            "rgs_tm": "13024500",
            "rgs_tab_cd": "0001",
            "rgs_emp_no": "000001",
            "oss_iem_cd": "AAPL",
            "oss_iem_nm": "APPLE INC",
            "trd_bf_fc_dca": 10000.0,
            "trd_bf_dca": 13300000,
            "oss_stm_tax": 0.0,
            "fc_tsl_txa": 0.0,
            "fc_amt": 1502.5,
            "krw_amt": 1999576.0,
            "fc_tax_sum": 0.0,
            "tax_sum": 0,
            "fc_icm_tax": 0.0,
            "fc_rsd_tax": 0.0,
            "fc_sas_amt": 0.0,
            "krw_sas_amt": 0,
            "tsl_cmu_txa": 0,
            "fc_trd_dit_cd": "05",
            "ral_trd_dt": "20260821",
        }
    ],
    "Output_1": {
        "cus_fnm": "홍길동",
        "rnm_cfm_no": "1234567890123",
        "rpm_tal": 10000000,
        "drn_tal": 0,
        "amt_sum": 1999576,
        "tax_sum_amt": 0,
        "fee_sum_amt": 2000,
    },
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


PERIOD_PNL_OK_BODY = {
    "Output_0": {
        "act_fnm": "홍길동",
        "byn_qty_sum": 20,
        "fc_byn_amt_sum": 3005.0,
        "sll_qty_sum": 10,
        "fc_sll_amt_sum": 1575.0,
        "fc_sby_pls_sum": 74.75,
        "fc_sby_pft_rt": 4.98,
        "fc_sdr_xps_sum": 1.5,
        "fc_rzt_pls_sum": 73.25,
        "fc_rzt_pft_rt": 4.65,
    },
    "Output_1": [
        {
            "orr_dt": "20260821",
            "fc_sec_trd_nat_cd": "200",
            "fc_sec_trd_nat_nm": "미국",
            "trd_cur_cd": "USD",
            "byn_qty": 10,
            "byn_uit_pr": 150.25,
            "fc_byn_amt1": 1502.5,
            "sll_qty": 10,
            "sll_uit_pr": 157.5,
            "fc_sll_amt": 1575.0,
            "fc_sby_pls": 74.75,
            "fc_sby_pft_rt": 4.98,
            "fc_sdr_xps": 1.5,
            "fc_rzt_pls": 73.25,
            "fc_rzt_pft_rt": 4.65,
        }
    ],
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


PERIOD_PNL_DETAIL_OK_BODY = {
    "Output_0": [
        {
            "iem_cd": "AAPL",
            "iem_nm": "애플",
            "byn_qty": 10,
            "byn_uit_pr": 150.25,
            "fc_byn_amt1": 1502.5,
            "sll_qty": 10,
            "sll_uit_pr": 157.5,
            "fc_sll_amt": 1575.0,
            "fc_sby_pls": 74.75,
            "fc_sby_pft_rt": 4.98,
            "fc_sdr_xps": 1.5,
            "fc_rzt_pls": 73.25,
            "fc_rzt_pft_rt": 4.65,
        }
    ],
    "message": {"msg_code": "0000", "usr_msg": "정상 처리되었습니다."},
}


MARGIN_OK_BODY = {
    "Output_0": [
        {
            "cur_cd": "USD",
            "dca": 10000,
            "orr_wtm": 500,
            "ect_mgg_amt": 0,
            "drn_pbl_amt": 9500,
            "fc_dca": 10000.5,
            "fc_mgg_amt": 0.0,
            "ect_mgg_fc_amt": 0.0,
            "fc_drn_pbl_amt": 9500.25,
            "sby_bse_xcg_rt": 1330.5,
            "fc_rba": 0.0,
            "rba": 0,
            "fc_rvb_odu_fee": 0.0,
            "rvb_odu_fee": 0,
            "stl_af_dca": 10000,
            "stl_af_drn_pbl_amt": 9500,
            "stl_af_fc_dca": 10000.5,
            "stl_af_fc_drn_pbl_amt": 9500.25,
        },
        {
            "cur_cd": "JPY",
            "dca": 900000,
            "orr_wtm": 50000,
            "ect_mgg_amt": 0,
            "drn_pbl_amt": 850000,
            "fc_dca": 900000.0,
            "fc_mgg_amt": 0.0,
            "ect_mgg_fc_amt": 0.0,
            "fc_drn_pbl_amt": 850000.0,
            "sby_bse_xcg_rt": 9.05,
            "fc_rba": 0.0,
            "rba": 0,
            "fc_rvb_odu_fee": 0.0,
            "rvb_odu_fee": 0,
            "stl_af_dca": 900000,
            "stl_af_drn_pbl_amt": 850000,
            "stl_af_fc_dca": 900000.0,
            "stl_af_fc_drn_pbl_amt": 850000.0,
        },
    ],
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

    def test_accepts_mock_success_code_xa102(self, client):
        # 실측(moapi): 모의투자 성공 시 rsp_cd="XA102" 를 내려준다.
        with requests_mock.Mocker() as m:
            m.post(
                BUYABLE_AMOUNT_URL,
                json={**BUYABLE_AMOUNT_OK_BODY, "rsp_cd": "XA102", "rsp_msg": "모의투자 조회가 완료되었습니다"},
            )
            response = client.overseas_stock_inquiry.get_buyable_amount(
                act_no="50051036881",
                pcs_dit="1",
                fc_sec_trd_nat_cd="200",
                iem_cd="AAPL",
                wtm_cur_knd_cd="1",
                oss_orr_knd_cd="1",
                ahi_nmn_pr_tp_cd="03",
            )

        assert response.body.rsp_cd == "XA102"
        assert response.body.output_0.wtm_cur_cd == "USD"

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


class TestGetOrderExecutions:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(ORDER_EXECUTIONS_URL, json=ORDER_EXECUTIONS_OK_BODY)
            client.overseas_stock_inquiry.get_order_executions(
                orr_dt="20260821",
                act_no="50051036881",
                oss_sby_dit_cd="0",
                sot_dit="0",
                ost_cns_dit="0",
                iem_cd="AAPL",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "orr_dt": "20260821",
                "act_no": "50051036881",
                "oss_sby_dit_cd": "0",
                "sot_dit": "0",
                "ost_cns_dit": "0",
                "iem_cd": "AAPL",
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(ORDER_EXECUTIONS_URL, json=ORDER_EXECUTIONS_OK_BODY)
            client.overseas_stock_inquiry.get_order_executions(
                orr_dt="20260821",
                act_no="50051036881",
                oss_sby_dit_cd="0",
                sot_dit="0",
                ost_cns_dit="0",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "iem_cd" not in sent
        assert "orr_no" not in sent

    def test_parses_order_executions_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(ORDER_EXECUTIONS_URL, json=ORDER_EXECUTIONS_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_order_executions(
                orr_dt="20260821",
                act_no="50051036881",
                oss_sby_dit_cd="0",
                sot_dit="0",
                ost_cns_dit="0",
            )

        assert response.body.output_0 is not None
        assert len(response.body.output_0) == 1
        item = response.body.output_0[0]
        assert item.orr_no == 123456789
        assert item.iem_cd == "AAPL"
        assert item.cns_qty == 10
        assert item.cns_pr == 150.25
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(ORDER_EXECUTIONS_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_order_executions(
                orr_dt="20260821",
                act_no="50051036881",
                oss_sby_dit_cd="0",
                sot_dit="0",
                ost_cns_dit="0",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(ORDER_EXECUTIONS_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_order_executions(
                    orr_dt="20260821",
                    act_no="50051036881",
                    oss_sby_dit_cd="0",
                    sot_dit="0",
                    ost_cns_dit="0",
                )


class TestGetBalance:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(BALANCE_URL, json=BALANCE_OK_BODY)
            client.overseas_stock_inquiry.get_balance(
                act_no="50051036881",
                qut_iqr_dit_cd="1",
                fc_sec_trd_nat_cd="200",
                cur_cd="USD",
                xns_dit_cd="0",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "qut_iqr_dit_cd": "1",
                "fc_sec_trd_nat_cd": "200",
                "cur_cd": "USD",
                "xns_dit_cd": "0",
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(BALANCE_URL, json=BALANCE_OK_BODY)
            client.overseas_stock_inquiry.get_balance(
                act_no="50051036881",
                qut_iqr_dit_cd="1",
                fc_sec_trd_nat_cd="200",
                cur_cd="USD",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "xns_dit_cd" not in sent

    def test_parses_balance_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(BALANCE_URL, json=BALANCE_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_balance(
                act_no="50051036881",
                qut_iqr_dit_cd="1",
                fc_sec_trd_nat_cd="200",
                cur_cd="USD",
            )

        assert response.body.output_0 is not None
        assert response.body.output_0.tot_aet_amt == 11500000
        assert response.body.output_0.krw_pft_rt == 5.0

        assert response.body.output_1 is not None
        assert len(response.body.output_1) == 2
        first, second = response.body.output_1
        assert first.iem_cd == "AAPL"
        assert first.krw_eal_amt == 2100000
        assert second.iem_cd == "7203"
        assert second.cur_cd == "JPY"

        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_parses_response_without_output_blocks(self, client):
        with requests_mock.Mocker() as m:
            m.post(BALANCE_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_balance(
                act_no="50051036881",
                qut_iqr_dit_cd="1",
                fc_sec_trd_nat_cd="200",
                cur_cd="USD",
            )

        assert response.body.output_0 is None
        assert response.body.output_1 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(BALANCE_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_balance(
                    act_no="50051036881",
                    qut_iqr_dit_cd="1",
                    fc_sec_trd_nat_cd="200",
                    cur_cd="USD",
                )


class TestGetReservedOrders:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(RESERVED_ORDERS_URL, json=RESERVED_ORDERS_OK_BODY)
            client.overseas_stock_inquiry.get_reserved_orders(
                fc_mkt_dit_cd="200",
                bkg_orr_dt="20260821",
                act_no="50051036881",
                sby_dit_cd="0",
                bkg_orr_can_yn="0",
                oss_orr_knd_cd="0",
                bkg_orr_tp_cd="0",
                wtm_cur_knd_cd="0",
                iem_cd="AAPL",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "fc_mkt_dit_cd": "200",
                "bkg_orr_dt": "20260821",
                "act_no": "50051036881",
                "sby_dit_cd": "0",
                "bkg_orr_can_yn": "0",
                "oss_orr_knd_cd": "0",
                "bkg_orr_tp_cd": "0",
                "wtm_cur_knd_cd": "0",
                "iem_cd": "AAPL",
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(RESERVED_ORDERS_URL, json=RESERVED_ORDERS_OK_BODY)
            client.overseas_stock_inquiry.get_reserved_orders(
                fc_mkt_dit_cd="200",
                bkg_orr_dt="20260821",
                act_no="50051036881",
                sby_dit_cd="0",
                bkg_orr_can_yn="0",
                oss_orr_knd_cd="0",
                bkg_orr_tp_cd="0",
                wtm_cur_knd_cd="0",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "iem_cd" not in sent

    def test_parses_reserved_orders_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(RESERVED_ORDERS_URL, json=RESERVED_ORDERS_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_reserved_orders(
                fc_mkt_dit_cd="200",
                bkg_orr_dt="20260821",
                act_no="50051036881",
                sby_dit_cd="0",
                bkg_orr_can_yn="0",
                oss_orr_knd_cd="0",
                bkg_orr_tp_cd="0",
                wtm_cur_knd_cd="0",
            )

        assert response.body.output_0 is not None
        assert len(response.body.output_0) == 1
        item = response.body.output_0[0]
        assert item.iem_cd == "AAPL"
        assert item.orr_qty == 10
        assert item.cns_pr == 150.25
        assert item.bkg_rtn_orr_no == 1234567890
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(RESERVED_ORDERS_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_reserved_orders(
                fc_mkt_dit_cd="200",
                bkg_orr_dt="20260821",
                act_no="50051036881",
                sby_dit_cd="0",
                bkg_orr_can_yn="0",
                oss_orr_knd_cd="0",
                bkg_orr_tp_cd="0",
                wtm_cur_knd_cd="0",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(RESERVED_ORDERS_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_reserved_orders(
                    fc_mkt_dit_cd="200",
                    bkg_orr_dt="20260821",
                    act_no="50051036881",
                    sby_dit_cd="0",
                    bkg_orr_can_yn="0",
                    oss_orr_knd_cd="0",
                    bkg_orr_tp_cd="0",
                    wtm_cur_knd_cd="0",
                )


class TestGetDailyTransactions:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(DAILY_TRANSACTIONS_URL, json=DAILY_TRANSACTIONS_OK_BODY)
            client.overseas_stock_inquiry.get_daily_transactions(
                act_no="50051036881",
                iqr_sta_dt="20260801",
                iqr_end_dt="20260821",
                act_trd_cfc_cd="00",
                iem_mlf_cd="00001",
                iem_cd="AAPL",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "iqr_sta_dt": "20260801",
                "iqr_end_dt": "20260821",
                "act_trd_cfc_cd": "00",
                "iem_mlf_cd": "00001",
                "iem_cd": "AAPL",
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(DAILY_TRANSACTIONS_URL, json=DAILY_TRANSACTIONS_OK_BODY)
            client.overseas_stock_inquiry.get_daily_transactions(
                act_no="50051036881",
                iqr_sta_dt="20260801",
                iqr_end_dt="20260821",
                act_trd_cfc_cd="00",
                iem_mlf_cd="00001",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "iem_cd" not in sent

    def test_parses_daily_transactions_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(DAILY_TRANSACTIONS_URL, json=DAILY_TRANSACTIONS_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_daily_transactions(
                act_no="50051036881",
                iqr_sta_dt="20260801",
                iqr_end_dt="20260821",
                act_trd_cfc_cd="00",
                iem_mlf_cd="00001",
            )

        assert response.body.output_0 is not None
        assert len(response.body.output_0) == 1
        item = response.body.output_0[0]
        assert item.trd_dt == "20260821"
        assert item.iem_cd == "AAPL"
        assert item.trd_qty == 10.0
        assert item.krw_trd_amt == 1999576

        assert response.body.output_1 is not None
        assert response.body.output_1.cus_fnm == "홍길동"
        assert response.body.output_1.amt_sum == 1999576

        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(DAILY_TRANSACTIONS_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_daily_transactions(
                act_no="50051036881",
                iqr_sta_dt="20260801",
                iqr_end_dt="20260821",
                act_trd_cfc_cd="00",
                iem_mlf_cd="00001",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.output_1 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(DAILY_TRANSACTIONS_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_daily_transactions(
                    act_no="50051036881",
                    iqr_sta_dt="20260801",
                    iqr_end_dt="20260821",
                    act_trd_cfc_cd="00",
                    iem_mlf_cd="00001",
                )


class TestGetPeriodPnl:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_URL, json=PERIOD_PNL_OK_BODY)
            client.overseas_stock_inquiry.get_period_pnl(
                act_no="50051036881",
                iqr_dit="1",
                sta_orr_dt="20260801",
                end_orr_dt="20260821",
                iem_cd="AAPL",
                trd_cur_cd="USD",
                fc_sec_trd_nat_cd="200",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "iqr_dit": "1",
                "sta_orr_dt": "20260801",
                "end_orr_dt": "20260821",
                "iem_cd": "AAPL",
                "trd_cur_cd": "USD",
                "fc_sec_trd_nat_cd": "200",
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_URL, json=PERIOD_PNL_OK_BODY)
            client.overseas_stock_inquiry.get_period_pnl(
                act_no="50051036881",
                iqr_dit="1",
                sta_orr_dt="20260801",
                end_orr_dt="20260821",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "iem_cd" not in sent
        assert "trd_cur_cd" not in sent
        assert "fc_sec_trd_nat_cd" not in sent

    def test_parses_period_pnl_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_URL, json=PERIOD_PNL_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_period_pnl(
                act_no="50051036881",
                iqr_dit="1",
                sta_orr_dt="20260801",
                end_orr_dt="20260821",
            )

        assert response.body.output_0 is not None
        assert response.body.output_0.act_fnm == "홍길동"
        assert response.body.output_0.fc_rzt_pls_sum == 73.25

        assert response.body.output_1 is not None
        assert len(response.body.output_1) == 1
        item = response.body.output_1[0]
        assert item.orr_dt == "20260821"
        assert item.fc_sby_pls == 74.75
        assert item.fc_rzt_pft_rt == 4.65

        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_period_pnl(
                act_no="50051036881",
                iqr_dit="1",
                sta_orr_dt="20260801",
                end_orr_dt="20260821",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.output_1 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_period_pnl(
                    act_no="50051036881",
                    iqr_dit="1",
                    sta_orr_dt="20260801",
                    end_orr_dt="20260821",
                )


class TestGetPeriodPnlDetail:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_DETAIL_URL, json=PERIOD_PNL_DETAIL_OK_BODY)
            client.overseas_stock_inquiry.get_period_pnl_detail(
                act_no="50051036881",
                iqr_dit="1",
                orr_dt="20260821",
                fc_sec_trd_nat_cd="200",
                trd_cur_cd="USD",
                iem_cd="AAPL",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
                "iqr_dit": "1",
                "orr_dt": "20260821",
                "fc_sec_trd_nat_cd": "200",
                "trd_cur_cd": "USD",
                "iem_cd": "AAPL",
            }
        }

    def test_omits_optional_fields_when_not_given(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_DETAIL_URL, json=PERIOD_PNL_DETAIL_OK_BODY)
            client.overseas_stock_inquiry.get_period_pnl_detail(
                act_no="50051036881",
                iqr_dit="1",
                orr_dt="20260821",
                fc_sec_trd_nat_cd="200",
                trd_cur_cd="USD",
            )

        sent = json.loads(m.request_history[0].text)["Input_0"]
        assert "iem_cd" not in sent

    def test_parses_period_pnl_detail_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_DETAIL_URL, json=PERIOD_PNL_DETAIL_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_period_pnl_detail(
                act_no="50051036881",
                iqr_dit="1",
                orr_dt="20260821",
                fc_sec_trd_nat_cd="200",
                trd_cur_cd="USD",
            )

        assert response.body.output_0 is not None
        assert len(response.body.output_0) == 1
        item = response.body.output_0[0]
        assert item.iem_cd == "AAPL"
        assert item.byn_qty == 10
        assert item.fc_sby_pls == 74.75
        assert item.fc_rzt_pft_rt == 4.65
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_DETAIL_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_period_pnl_detail(
                act_no="50051036881",
                iqr_dit="1",
                orr_dt="20260821",
                fc_sec_trd_nat_cd="200",
                trd_cur_cd="USD",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(PERIOD_PNL_DETAIL_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_period_pnl_detail(
                    act_no="50051036881",
                    iqr_dit="1",
                    orr_dt="20260821",
                    fc_sec_trd_nat_cd="200",
                    trd_cur_cd="USD",
                )


class TestGetMarginByCurrency:
    def test_sends_input_envelope(self, client):
        with requests_mock.Mocker() as m:
            m.post(MARGIN_URL, json=MARGIN_OK_BODY)
            client.overseas_stock_inquiry.get_margin_by_currency(
                act_no="50051036881",
            )

        assert json.loads(m.request_history[0].text) == {
            "Input_0": {
                "act_no": "50051036881",
            }
        }

    def test_parses_margin_response(self, client):
        with requests_mock.Mocker() as m:
            m.post(MARGIN_URL, json=MARGIN_OK_BODY, headers={"cts_flag": "N"})
            response = client.overseas_stock_inquiry.get_margin_by_currency(
                act_no="50051036881",
            )

        assert response.body.output_0 is not None
        assert len(response.body.output_0) == 2
        first, second = response.body.output_0
        assert first.cur_cd == "USD"
        assert first.dca == 10000
        assert first.fc_drn_pbl_amt == 9500.25
        assert second.cur_cd == "JPY"
        assert second.sby_bse_xcg_rt == 9.05
        assert response.body.message.usr_msg == "정상 처리되었습니다."
        assert response.header.cts_flag == "N"

    def test_sends_cts_header_for_continuation(self, client):
        with requests_mock.Mocker() as m:
            m.post(MARGIN_URL, json={"rsp_cd": "00000", "rsp_msg": "정상"})
            response = client.overseas_stock_inquiry.get_margin_by_currency(
                act_no="50051036881",
                cts="CTS_TOKEN_1",
            )

        sent_headers = m.request_history[0].headers
        assert sent_headers["cts"] == "CTS_TOKEN_1"
        assert sent_headers["cts_flag"] == "Y"
        assert response.body.output_0 is None
        assert response.body.rsp_cd == "00000"

    def test_raises_on_failing_rsp_cd(self, client):
        with requests_mock.Mocker() as m:
            m.post(MARGIN_URL, json={"rsp_cd": "40310", "rsp_msg": "권한이 없습니다."})
            with pytest.raises(NHPlugAPIError, match="40310"):
                client.overseas_stock_inquiry.get_margin_by_currency(
                    act_no="50051036881",
                )
