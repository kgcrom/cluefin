import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_account_types import (
    DomesticAccountAvailableOrderQuantityByMarginLoanStock,
    DomesticAccountAvailableOrderQuantityByMarginRate,
    DomesticAccountAvailableWithdrawalAmount,
    DomesticAccountConsignmentComprehensiveTransactionHistory,
    DomesticAccountCurrentDayStatus,
    DomesticAccountCurrentDayTradingJournal,
    DomesticAccountDailyEstimatedDepositAssetBalance,
    DomesticAccountDailyProfitRateDetails,
    DomesticAccountDailyRealizedProfitLoss,
    DomesticAccountDailyRealizedProfitLossDetails,
    DomesticAccountDailyStockRealizedProfitLossByDate,
    DomesticAccountDailyStockRealizedProfitLossByPeriod,
    DomesticAccountDepositBalanceDetails,
    DomesticAccountEstimatedAssetBalance,
    DomesticAccountEvaluationBalanceDetails,
    DomesticAccountEvaluationStatus,
    DomesticAccountExecuted,
    DomesticAccountExecutionBalance,
    DomesticAccountMarginDetails,
    DomesticAccountNextDaySettlementDetails,
    DomesticAccountOrderExecutionDetails,
    DomesticAccountOrderExecutionStatus,
    DomesticAccountProfitRate,
    DomesticAccountUnexecuted,
    DomesticAccountUnexecutedSplitOrderDetails,
)


@pytest.fixture
def client():
    return Client(
        token="test_token",
        env="dev",
    )


def test_get_daily_stock_realized_profit_loss_by_date(client: Client):
    expected_data = {
        "dt_stk_div_rlzt_pl": [
            {
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.96",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.04",
                "pl_rt": "+61.28",
                "stk_cd": "A005930",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "wthd_alowa": "0",
                "loan_dt": "",
                "crd_tp": "현금잔고",
                "stk_cd_1": "A005930",
                "tdy_sel_pl_1": "59813.04",
            },
            {
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.96",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.04",
                "pl_rt": "+61.28",
                "stk_cd": "A005930",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "wthd_alowa": "0",
                "loan_dt": "",
                "crd_tp": "현금잔고",
                "stk_cd_1": "A005930",
                "tdy_sel_pl_1": "59813.04",
            },
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10072"},
        )

        response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")

        assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByDate)
        assert response.body.dt_stk_div_rlzt_pl[0].stk_nm == "삼성전자"
        assert response.body.dt_stk_div_rlzt_pl[0].cntr_qty == "1"


def test_get_daily_stock_realized_profit_loss_by_period(client: Client):
    expected_data = {
        "dt_stk_rlzt_pl": [
            {
                "dt": "20241128",
                "tdy_htssel_cmsn": "현금",
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.96",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.04",
                "pl_rt": "+61.28",
                "stk_cd": "A005930",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "wthd_alowa": "0",
                "loan_dt": "",
                "crd_tp": "현금잔고",
            },
            {
                "dt": "20241128",
                "tdy_htssel_cmsn": "현금",
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.96",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.04",
                "pl_rt": "+61.28",
                "stk_cd": "A005930",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "wthd_alowa": "0",
                "loan_dt": "",
                "crd_tp": "현금잔고",
            },
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10073"},
        )
        response = client.account.get_daily_stock_realized_profit_loss_by_period(
            "005930",
            "20241101",
            "20241130",
        )

        assert isinstance(response.body, DomesticAccountDailyStockRealizedProfitLossByPeriod)
        assert response.body.dt_stk_rlzt_pl[0].stk_nm == "삼성전자"
        assert response.body.dt_stk_rlzt_pl[0].buy_uv == "97602.96"


def test_get_daily_realized_profit_loss(client: Client):
    expected_data = {
        "tot_buy_amt": "0",
        "tot_sell_amt": "474600",
        "rlzt_pl": "179419",
        "trde_cmsn": "940",
        "trde_tax": "852",
        "dt_rlzt_pl": [
            {
                "dt": "20241128",
                "buy_amt": "0",
                "sell_amt": "474600",
                "tdy_sel_pl": "179419",
                "tdy_trde_cmsn": "940",
                "tdy_trde_tax": "852",
            }
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10074"},
        )
        response = client.account.get_daily_realized_profit_loss("20250601", "20250630")

        assert isinstance(response.body, DomesticAccountDailyRealizedProfitLoss)
        assert response.body.tot_sell_amt == "474600"
        assert response.body.dt_rlzt_pl[0].tdy_sel_pl == "179419"


def test_get_unexecuted(client: Client):
    expected_data = {
        "oso": [
            {
                "acnt_no": "1234567890",
                "ord_no": "0000069",
                "mang_empno": "",
                "stk_cd": "005930",
                "tsk_tp": "",
                "ord_stt": "접수",
                "stk_nm": "삼성전자",
                "ord_qty": "1",
                "ord_pric": "0",
                "oso_qty": "1",
                "cntr_tot_amt": "0",
                "orig_ord_no": "0000000",
                "io_tp_nm": "+매수",
                "trde_tp": "시장가",
                "tm": "154113",
                "cntr_no": "",
                "cntr_pric": "0",
                "cntr_qty": "0",
                "cur_prc": "+74100",
                "sel_bid": "0",
                "buy_bid": "+74100",
                "unit_cntr_pric": "",
                "unit_cntr_qty": "",
                "tdy_trde_cmsn": "0",
                "tdy_trde_tax": "0",
                "ind_invsr": "",
                "stex_tp": "1",
                "stex_tp_txt": "KRX",
                "sor_yn": "N",
            }
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10075"},
        )
        response = client.account.get_unexecuted("0", "0", "005930", "0")

        assert isinstance(response.body, DomesticAccountUnexecuted)
        assert response.body.oso[0].stk_nm == "삼성전자"
        assert response.body.oso[0].ord_qty == "1"


def test_get_executed(client: Client):
    expected_data = {
        "cntr": [
            {
                "ord_no": "0000037",
                "stk_nm": "삼성전자",
                "io_tp_nm": "-매도",
                "ord_pric": "158200",
                "ord_qty": "1",
                "cntr_pric": "158200",
                "cntr_qty": "1",
                "oso_qty": "0",
                "tdy_trde_cmsn": "310",
                "tdy_trde_tax": "284",
                "ord_stt": "체결",
                "trde_tp": "보통",
                "orig_ord_no": "0000000",
                "ord_tm": "153815",
                "stk_cd": "005930",
                "stex_tp": "0",
                "stex_tp_txt": "SOR",
                "sor_yn": "Y",
            },
            {
                "ord_no": "0000036",
                "stk_nm": "삼성전자",
                "io_tp_nm": "-매도",
                "ord_pric": "158200",
                "ord_qty": "1",
                "cntr_pric": "158200",
                "cntr_qty": "1",
                "oso_qty": "0",
                "tdy_trde_cmsn": "310",
                "tdy_trde_tax": "284",
                "ord_stt": "체결",
                "trde_tp": "보통",
                "orig_ord_no": "0000000",
                "ord_tm": "153806",
                "stk_cd": "005930",
                "stex_tp": "0",
                "stex_tp_txt": "SOR",
                "sor_yn": "Y",
            },
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10076"},
        )

        response = client.account.get_executed("005930", "0", "0", "0", "0")

        assert response is not None
        assert isinstance(response.body, DomesticAccountExecuted)
        assert response.body.cntr[0].ord_no == "0000037"
        assert response.body.cntr[0].cntr_pric == "158200"


def test_get_daily_realized_profit_loss_details(client: Client):
    expected_data = {
        "tdy_rlzt_pl": "179439",
        "tdy_rlzt_pl_dtl": [
            {
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.9573459",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.0426541",
                "pl_rt": "+61.28",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "stk_cd": "A005930",
            },
            {
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.9573459",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.0426541",
                "pl_rt": "+61.28",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "stk_cd": "A005930",
            },
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10077"},
        )
        response = client.account.get_daily_realized_profit_loss_details("005930", "20241128")
        assert isinstance(response.body, DomesticAccountDailyRealizedProfitLossDetails)
        assert response.body.tdy_rlzt_pl_dtl[0].buy_uv == "97602.9573459"
        assert response.body.tdy_rlzt_pl_dtl[0].tdy_sel_pl == "59813.0426541"


def test_get_account_profit_rate(client: Client):
    expected_data = {
        "acnt_prft_rt": [
            {
                "dt": "",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-63000",
                "pur_pric": "124500",
                "pur_amt": "373500",
                "rmnd_qty": "3",
                "tdy_sel_pl": "0",
                "tdy_trde_cmsn": "0",
                "tdy_trde_tax": "0",
                "crd_tp": "00",
                "loan_dt": "00000000",
                "setl_remn": "3",
                "clrn_alow_qty": "3",
                "crd_amt": "0",
                "crd_int": "0",
                "expr_dt": "00000000",
            },
            {
                "dt": "",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+256500",
                "pur_pric": "209179",
                "pur_amt": "1673429",
                "rmnd_qty": "8",
                "tdy_sel_pl": "0",
                "tdy_trde_cmsn": "0",
                "tdy_trde_tax": "0",
                "crd_tp": "00",
                "loan_dt": "00000000",
                "setl_remn": "8",
                "clrn_alow_qty": "8",
                "crd_amt": "0",
                "crd_int": "0",
                "expr_dt": "00000000",
            },
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10085"},
        )
        response = client.account.get_account_profit_rate("20240601", "20240630", "1")

        assert isinstance(response.body, DomesticAccountProfitRate)
        assert response.body.acnt_prft_rt[0].pur_pric == "124500"
        assert response.body.acnt_prft_rt[0].cur_prc == "-63000"


def test_get_unexecuted_split_order_details(client: Client):
    expected_data = {
        "osop": [
            {
                "stk_cd": "005930",
                "acnt_no": "1234567890",
                "stk_nm": "삼성전자",
                "ord_no": "0000008",
                "ord_qty": "1",
                "ord_pric": "5150",
                "osop_qty": "1",
                "io_tp_nm": "+매수정정",
                "trde_tp": "보통",
                "sell_tp": "2",
                "cntr_qty": "0",
                "ord_stt": "접수",
                "cur_prc": "5250",
                "stex_tp": "1",
                "stex_tp_txt": "S-KRX",
            }
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10088"},
        )
        response = client.account.get_unexecuted_split_order_details("1234567890")

        assert isinstance(response.body, DomesticAccountUnexecutedSplitOrderDetails)
        assert response.body.osop[0].ord_no == "0000008"
        assert response.body.osop[0].io_tp_nm == "+매수정정"


def test_get_current_day_trading_journal(client: Client):
    expected_data = {
        "tot_sell_amt": "48240",
        "tot_buy_amt": "48240",
        "tot_cmsn_tax": "174",
        "tot_exct_amt": "-174",
        "tot_pl_amt": "-174",
        "tot_prft_rt": "-0.36",
        "tdy_trde_diary": [
            {
                "stk_nm": "삼성전자",
                "buy_avg_pric": "16080",
                "buy_qty": "3",
                "sel_avg_pric": "16080",
                "sell_qty": "3",
                "cmsn_alm_tax": "174",
                "pl_amt": "-174",
                "sell_amt": "48240",
                "buy_amt": "48240",
                "prft_rt": "-0.36",
                "stk_cd": "005930",
            }
        ],
        "return_code": 0,
        "return_msg": " 조회가 완료되었습니다.",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10170"},
        )
        response = client.account.get_current_day_trading_journal("20240601", "0", "0")

        assert isinstance(response.body, DomesticAccountCurrentDayTradingJournal)
        assert response.body.tot_sell_amt == "48240"
        assert response.body.tdy_trde_diary[0].sel_avg_pric == "16080"


def test_get_deposit_balance_details(client: Client):
    expected_data = {
        "entr": "000000000017534",
        "profa_ch": "000000000032193",
        "bncr_profa_ch": "000000000000000",
        "nxdy_bncr_sell_exct": "000000000000000",
        "fc_stk_krw_repl_set_amt": "000000000000000",
        "crd_grnta_ch": "000000000000000",
        "crd_grnt_ch": "000000000000000",
        "add_grnt_ch": "000000000000000",
        "etc_profa": "000000000000000",
        "uncl_stk_amt": "000000000000000",
        "shrts_prica": "000000000000000",
        "crd_set_grnta": "000000000000000",
        "chck_ina_amt": "000000000000000",
        "etc_chck_ina_amt": "000000000000000",
        "crd_grnt_ruse": "000000000000000",
        "knx_asset_evltv": "000000000000000",
        "elwdpst_evlta": "000000000031269",
        "crd_ls_rght_frcs_amt": "000000000000000",
        "lvlh_join_amt": "000000000000000",
        "lvlh_trns_alowa": "000000000000000",
        "repl_amt": "000000003915500",
        "remn_repl_evlta": "000000003915500",
        "trst_remn_repl_evlta": "000000000000000",
        "bncr_remn_repl_evlta": "000000000000000",
        "profa_repl": "000000000000000",
        "crd_grnta_repl": "000000000000000",
        "crd_grnt_repl": "000000000000000",
        "add_grnt_repl": "000000000000000",
        "rght_repl_amt": "000000000000000",
        "pymn_alow_amt": "000000000085341",
        "wrap_pymn_alow_amt": "000000000000000",
        "ord_alow_amt": "000000000085341",
        "bncr_buy_alowa": "000000000085341",
        "20stk_ord_alow_amt": "000000000012550",
        "30stk_ord_alow_amt": "000000000012550",
        "40stk_ord_alow_amt": "000000000012550",
        "100stk_ord_alow_amt": "000000000012550",
        "ch_uncla": "000000000000000",
        "ch_uncla_dlfe": "000000000000000",
        "ch_uncla_tot": "000000000000000",
        "crd_int_npay": "000000000000000",
        "int_npay_amt_dlfe": "000000000000000",
        "int_npay_amt_tot": "000000000000000",
        "etc_loana": "000000000000000",
        "etc_loana_dlfe": "000000000000000",
        "etc_loan_tot": "000000000000000",
        "nrpy_loan": "000000000000000",
        "loan_sum": "000000000000000",
        "ls_sum": "000000000000000",
        "crd_grnt_rt": "0.00",
        "mdstrm_usfe": "000000000388388",
        "min_ord_alow_yn": "000000000000000",
        "loan_remn_evlt_amt": "000000000000000",
        "dpst_grntl_remn": "000000000000000",
        "sell_grntl_remn": "000000000000000",
        "d1_entra": "000000000017450",
        "d1_slby_exct_amt": "-00000000000084",
        "d1_buy_exct_amt": "000000000048240",
        "d1_out_rep_mor": "000000000000000",
        "d1_sel_exct_amt": "000000000048156",
        "d1_pymn_alow_amt": "000000000012550",
        "d2_entra": "000000000012550",
        "d2_slby_exct_amt": "-00000000004900",
        "d2_buy_exct_amt": "000000000004900",
        "d2_out_rep_mor": "000000000000000",
        "d2_sel_exct_amt": "000000000000000",
        "d2_pymn_alow_amt": "000000000012550",
        "50stk_ord_alow_amt": "000000000012550",
        "60stk_ord_alow_amt": "000000000012550",
        "stk_entr_prst": [],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00001"},
        )
        response = client.account.get_deposit_balance_details("3")
        assert isinstance(response.body, DomesticAccountDepositBalanceDetails)
        assert response.body.entr == "000000000017534"
        assert response.body.d1_pymn_alow_amt == "000000000012550"


def test_get_daily_estimated_deposit_asset_balance(client: Client):
    expected_data = {
        "daly_prsm_dpst_aset_amt_prst": [
            {
                "dt": "20241111",
                "entr": "000000100000",
                "grnt_use_amt": "000000000000",
                "crd_loan": "000000000000",
                "ls_grnt": "000000000000",
                "repl_amt": "000000000000",
                "prsm_dpst_aset_amt": "000000000000",
                "prsm_dpst_aset_amt_bncr_skip": "000000000000",
            },
            {
                "dt": "20241112",
                "entr": "000000100000",
                "grnt_use_amt": "000000000000",
                "crd_loan": "000000000000",
                "ls_grnt": "000000000000",
                "repl_amt": "000000000000",
                "prsm_dpst_aset_amt": "000000000000",
                "prsm_dpst_aset_amt_bncr_skip": "000000000000",
            },
            {
                "dt": "20241113",
                "entr": "000000100000",
                "grnt_use_amt": "000000000000",
                "crd_loan": "000000000000",
                "ls_grnt": "000000000000",
                "repl_amt": "000000000000",
                "prsm_dpst_aset_amt": "000000000000",
                "prsm_dpst_aset_amt_bncr_skip": "000000000000",
            },
            {
                "dt": "20241114",
                "entr": "000000999748",
                "grnt_use_amt": "000000000000",
                "crd_loan": "000000000000",
                "ls_grnt": "000000000000",
                "repl_amt": "000000000165",
                "prsm_dpst_aset_amt": "000000000000",
                "prsm_dpst_aset_amt_bncr_skip": "000000000000",
            },
        ],
        "return_code": 0,
        "return_msg": "일자별 계좌별 추정예탁자산 내역이 조회 되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00002"},
        )
        response = client.account.get_daily_estimated_deposit_asset_balance("000000100000", "20241111", "20241114")
        assert isinstance(response.body, DomesticAccountDailyEstimatedDepositAssetBalance)
        assert response.body.daly_prsm_dpst_aset_amt_prst[0].dt == "20241111"
        assert response.body.daly_prsm_dpst_aset_amt_prst[0].entr == "000000100000"


def test_get_estimated_asset_balance(client: Client):
    expected_data = {"prsm_dpst_aset_amt": "00000530218", "return_code": 0, "return_msg": "조회가 완료되었습니다.."}

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00003"},
        )
        response = client.account.get_estimated_asset_balance("1")
        assert isinstance(response.body, DomesticAccountEstimatedAssetBalance)
        assert response.body.prsm_dpst_aset_amt == "00000530218"


def test_get_account_evaluation_status(client: Client):
    expected_data = {
        "acnt_nm": "김키움",
        "brch_nm": "키움은행",
        "entr": "000000017534",
        "d2_entra": "000000012550",
        "tot_est_amt": "000000000342",
        "aset_evlt_amt": "000000761950",
        "tot_pur_amt": "000000002786",
        "prsm_dpst_aset_amt": "000000749792",
        "tot_grnt_sella": "000000000000",
        "tdy_lspft_amt": "000000000000",
        "invt_bsamt": "000000000000",
        "lspft_amt": "000000000000",
        "tdy_lspft": "000000000000",
        "lspft2": "000000000000",
        "lspft": "000000000000",
        "tdy_lspft_rt": "0.00",
        "lspft_ratio": "0.00",
        "lspft_rt": "0.00",
        "stk_acnt_evlt_prst": [
            {
                "stk_cd": "A005930",
                "stk_nm": "삼성전자",
                "rmnd_qty": "000000000003",
                "avg_prc": "000000124500",
                "cur_prc": "000000070000",
                "evlt_amt": "000000209542",
                "pl_amt": "-00000163958",
                "pl_rt": "-43.8977",
                "loan_dt": "",
                "pur_amt": "000000373500",
                "setl_remn": "000000000003",
                "pred_buyq": "000000000000",
                "pred_sellq": "000000000000",
                "tdy_buyq": "000000000000",
                "tdy_sellq": "000000000000",
            }
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00004"},
        )
        response = client.account.get_account_evaluation_status("0", "KRX")
        assert isinstance(response.body, DomesticAccountEvaluationStatus)
        assert response.body.entr == "000000017534"
        assert response.body.stk_acnt_evlt_prst[0].rmnd_qty == "000000000003"


def test_get_execution_balance(client: Client):
    expected_data = {
        "entr": "000000017534",
        "entr_d1": "000000017450",
        "entr_d2": "000000012550",
        "pymn_alow_amt": "000000085341",
        "uncl_stk_amt": "000000000000",
        "repl_amt": "000003915500",
        "rght_repl_amt": "000000000000",
        "ord_alowa": "000000085341",
        "ch_uncla": "000000000000",
        "crd_int_npay_gold": "000000000000",
        "etc_loana": "000000000000",
        "nrpy_loan": "000000000000",
        "profa_ch": "000000032193",
        "repl_profa": "000000000000",
        "stk_buy_tot_amt": "000006122786",
        "evlt_amt_tot": "000006236342",
        "tot_pl_tot": "000000113556",
        "tot_pl_rt": "1.8546",
        "tot_re_buy_alowa": "000000135970",
        "20ord_alow_amt": "000000012550",
        "30ord_alow_amt": "000000012550",
        "40ord_alow_amt": "000000012550",
        "50ord_alow_amt": "000000012550",
        "60ord_alow_amt": "000000012550",
        "100ord_alow_amt": "000000012550",
        "crd_loan_tot": "000000000000",
        "crd_loan_ls_tot": "000000000000",
        "crd_grnt_rt": "0.00",
        "dpst_grnt_use_amt_amt": "000000000000",
        "grnt_loan_amt": "000000000000",
        "stk_cntr_remn": [
            {
                "crd_tp": "00",
                "loan_dt": "",
                "expr_dt": "",
                "stk_cd": "A005930",
                "stk_nm": "삼성전자",
                "setl_remn": "000000000003",
                "cur_qty": "000000000003",
                "cur_prc": "000000070000",
                "buy_uv": "000000124500",
                "pur_amt": "000000373500",
                "evlt_amt": "000000209542",
                "evltv_prft": "-00000163958",
                "pl_rt": "-43.8977",
            }
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00005"},
        )
        response = client.account.get_execution_balance("KRX")
        assert isinstance(response.body, DomesticAccountExecutionBalance)
        assert response.body.entr == "000000017534"
        assert response.body.stk_cntr_remn[0].cur_qty == "000000000003"


def test_get_account_order_execution_details(client: Client):
    expected_data = {
        "acnt_ord_cntr_prps_dtl": [
            {
                "ord_no": "0000050",
                "stk_cd": "A069500",
                "trde_tp": "시장가",
                "crd_tp": "보통매매",
                "ord_qty": "0000000001",
                "ord_uv": "0000000000",
                "cnfm_qty": "0000000000",
                "acpt_tp": "접수",
                "rsrv_tp": "",
                "ord_tm": "13:05:43",
                "ori_ord": "0000000",
                "stk_nm": "KODEX 200",
                "io_tp_nm": "현금매수",
                "loan_dt": "",
                "cntr_qty": "0000000001",
                "cntr_uv": "0000004900",
                "ord_remnq": "0000000000",
                "comm_ord_tp": "영웅문4",
                "mdfy_cncl": "",
                "cnfm_tm": "",
                "dmst_stex_tp": "KRX",
                "cond_uv": "0000000000",
            }
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00007"},
        )
        response = client.account.get_account_order_execution_details(
            ord_dt="20240630",
            qry_tp="1",
            stk_bond_tp="0",
            sell_tp="0",
            stk_cd="005930",
            fr_ord_no="0",
            dmst_stex_tp="%",
        )

        assert isinstance(response.body, DomesticAccountOrderExecutionDetails)
        assert response.body.acnt_ord_cntr_prps_dtl[0].ord_no == "0000050"
        assert response.body.acnt_ord_cntr_prps_dtl[0].cntr_qty == "0000000001"


def test_get_account_next_day_settlement_details(client: Client):
    expected_data = {
        "acnt_ord_cntr_prps_dtl": [
            {
                "ord_no": "0000050",
                "stk_cd": "A069500",
                "trde_tp": "시장가",
                "crd_tp": "보통매매",
                "ord_qty": "0000000001",
                "ord_uv": "0000000000",
                "cnfm_qty": "0000000000",
                "acpt_tp": "접수",
                "rsrv_tp": "",
                "ord_tm": "13:05:43",
                "ori_ord": "0000000",
                "stk_nm": "KODEX 200",
                "io_tp_nm": "현금매수",
                "loan_dt": "",
                "cntr_qty": "0000000001",
                "cntr_uv": "0000004900",
                "ord_remnq": "0000000000",
                "comm_ord_tp": "영웅문4",
                "mdfy_cncl": "",
                "cnfm_tm": "",
                "dmst_stex_tp": "KRX",
                "cond_uv": "0000000000",
            }
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00008"},
        )
        response = client.account.get_account_next_day_settlement_details()
        assert isinstance(response.body, DomesticAccountNextDaySettlementDetails)
        assert response.body.acnt_ord_cntr_prps_dtl[0].ord_qty == "0000000001"
        assert response.body.acnt_ord_cntr_prps_dtl[0].io_tp_nm == "현금매수"


def test_get_account_order_execution_status(client: Client):
    expected_data = {
        "sell_grntl_engg_amt": "000000000000",
        "buy_engg_amt": "000000004900",
        "engg_amt": "000000004900",
        "acnt_ord_cntr_prst": [
            {
                "stk_bond_tp": "1",
                "ord_no": "0000050",
                "stk_cd": "A069500",
                "trde_tp": "시장가",
                "io_tp_nm": "현금매수",
                "ord_qty": "0000000001",
                "ord_uv": "0000000000",
                "cnfm_qty": "0000000000",
                "rsrv_oppo": "",
                "cntr_no": "0000001",
                "acpt_tp": "접수",
                "orig_ord_no": "0000000",
                "stk_nm": "KODEX 200",
                "setl_tp": "삼일결제",
                "crd_deal_tp": "보통매매",
                "cntr_qty": "0000000001",
                "cntr_uv": "0000004900",
                "comm_ord_tp": "영웅문4",
                "mdfy_cncl_tp": "",
                "cntr_tm": "13:07:47",
                "dmst_stex_tp": "KRX",
                "cond_uv": "0000000000",
            }
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00009"},
        )
        response = client.account.get_account_order_execution_status(
            ord_dt="20240630",
            stk_bond_tp="0",
            mrkt_tp="0",
            sell_tp="0",
            qry_tp="0",
            stk_cd="005930",
            fr_ord_no="0",
            dmst_stex_tp="%",
        )
        assert isinstance(response.body, DomesticAccountOrderExecutionStatus)
        assert response.body.sell_grntl_engg_amt == "000000000000"
        assert response.body.acnt_ord_cntr_prst[0].ord_no == "0000050"


def test_get_available_withdrawal_amount(client: Client):
    expected_data = {
        "profa_20ord_alow_amt": "000000012550",
        "profa_20ord_alowq": "0000000000",
        "profa_30ord_alow_amt": "000000012550",
        "profa_30ord_alowq": "0000000000",
        "profa_40ord_alow_amt": "000000012550",
        "profa_40ord_alowq": "0000000000",
        "profa_50ord_alow_amt": "000000012550",
        "profa_50ord_alowq": "0000000000",
        "profa_60ord_alow_amt": "000000012550",
        "profa_60ord_alowq": "0000000000",
        "profa_rdex_60ord_alow_amt": "000000012550",
        "profa_rdex_60ord_alowq": "0000000000",
        "profa_100ord_alow_amt": "000000012550",
        "profa_100ord_alowq": "0000000000",
        "pred_reu_alowa": "000000027194",
        "tdy_reu_alowa": "000000000000",
        "entr": "000000017534",
        "repl_amt": "000003915500",
        "uncla": "000000000000",
        "ord_pos_repl": "000003915500",
        "ord_alowa": "000000085341",
        "wthd_alowa": "000000085341",
        "nxdy_wthd_alowa": "000000012550",
        "pur_amt": "000000000000",
        "cmsn": "000000000000",
        "pur_exct_amt": "000000000000",
        "d2entra": "000000012550",
        "profa_rdex_aplc_tp": "0",
        "return_code": 0,
        "return_msg": "주문/인출가능금액 시뮬레이션 조회완료하였습니다.",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00010"},
        )
        response = client.account.get_available_withdrawal_amount(
            io_amt="000000000000",
            stk_cd="005930",
            trde_tp="1",
            trde_qty="0000000000",
            uv="000000124500",
            exp_buy_unp="000000124500",
        )

        assert isinstance(response.body, DomesticAccountAvailableWithdrawalAmount)
        assert response.body.profa_20ord_alow_amt == "000000012550"
        assert response.body.ord_pos_repl == "000003915500"


def test_get_available_order_quantity_by_margin_rate(client: Client):
    expected_data = {
        "stk_profa_rt": "20%",
        "profa_rt": "100%",
        "aplc_rt": "100%",
        "profa_20ord_alow_amt": "",
        "profa_20ord_alowq": "",
        "profa_20pred_reu_amt": "",
        "profa_20tdy_reu_amt": "",
        "profa_30ord_alow_amt": "",
        "profa_30ord_alowq": "",
        "profa_30pred_reu_amt": "",
        "profa_30tdy_reu_amt": "",
        "profa_40ord_alow_amt": "",
        "profa_40ord_alowq": "",
        "profa_40pred_reu_amt": "",
        "profa_40tdy_reu_amt": "",
        "profa_50ord_alow_amt": "",
        "profa_50ord_alowq": "",
        "profa_50pred_reu_amt": "",
        "profa_50tdy_reu_amt": "",
        "profa_60ord_alow_amt": "",
        "profa_60ord_alowq": "",
        "profa_60pred_reu_amt": "",
        "profa_60tdy_reu_amt": "",
        "profa_100ord_alow_amt": "",
        "profa_100ord_alowq": "",
        "profa_100pred_reu_amt": "",
        "profa_100tdy_reu_amt": "",
        "min_ord_alow_amt": "000000063380",
        "min_ord_alowq": "000000000000",
        "min_pred_reu_amt": "000000027194",
        "min_tdy_reu_amt": "000000000000",
        "entr": "000000017534",
        "repl_amt": "000003915500",
        "uncla": "000000000000",
        "ord_pos_repl": "000003915500",
        "ord_alowa": "000000085341",
        "return_code": 0,
        "return_msg": "자료를 조회하였습니다.",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00011"},
        )
        response = client.account.get_available_order_quantity_by_margin_rate(stk_cd="005930", uv="000000124500")

        assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginRate)
        assert response.body.stk_profa_rt == "20%"
        assert response.body.ord_pos_repl == "000003915500"


def test_get_available_order_quantity_by_margin_loan_stock(client: Client):
    expected_data = {
        "stk_assr_rt": "B",
        "stk_assr_rt_nm": "45%",
        "assr_30ord_alow_amt": "003312045139",
        "assr_30ord_alowq": "000000000000",
        "assr_30pred_reu_amt": "000000000000",
        "assr_30tdy_reu_amt": "000000048994",
        "assr_40ord_alow_amt": "002208030092",
        "assr_40ord_alowq": "000000000000",
        "assr_40pred_reu_amt": "000000000000",
        "assr_40tdy_reu_amt": "000000048994",
        "assr_50ord_alow_amt": "001987227084",
        "assr_50ord_alowq": "000000000000",
        "assr_50pred_reu_amt": "000000000000",
        "assr_50tdy_reu_amt": "000000048994",
        "assr_60ord_alow_amt": "001656022569",
        "assr_60ord_alowq": "000000000000",
        "assr_60pred_reu_amt": "000000000000",
        "assr_60tdy_reu_amt": "000000048994",
        "entr": "000994946131",
        "repl_amt": "000001643660",
        "uncla": "000000000000",
        "ord_pos_repl": "000002420949",
        "ord_alowa": "000993564548",
        "out_alowa": "002208030092",
        "out_pos_qty": "000000000000",
        "min_amt": "002207294240",
        "min_qty": "000000000000",
        "return_code": 0,
        "return_msg": "신용보증금율별 주문가능수량 조회(한도정상)",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00012"},
        )
        response = client.account.get_available_order_quantity_by_margin_loan_stock(stk_cd="005930", uv="000000124500")

        assert isinstance(response.body, DomesticAccountAvailableOrderQuantityByMarginLoanStock)
        assert response.body.stk_assr_rt == "B"
        assert response.body.assr_60ord_alow_amt == "001656022569"


def test_get_margin_details(client: Client):
    expected_data = {
        "tdy_reu_objt_amt": "000000000000000",
        "tdy_reu_use_amt": "000000000000000",
        "tdy_reu_alowa": "000000000000000",
        "tdy_reu_lmtt_amt": "000000000000000",
        "tdy_reu_alowa_fin": "000000000000000",
        "pred_reu_objt_amt": "000000000048141",
        "pred_reu_use_amt": "000000000020947",
        "pred_reu_alowa": "000000000027194",
        "pred_reu_lmtt_amt": "000000000000000",
        "pred_reu_alowa_fin": "000000000027194",
        "ch_amt": "000000000017534",
        "ch_profa": "000000000032193",
        "use_pos_ch": "000000000085341",
        "ch_use_lmtt_amt": "000000000000000",
        "use_pos_ch_fin": "000000000085341",
        "repl_amt_amt": "000000003915500",
        "repl_profa": "000000000000000",
        "use_pos_repl": "000000003915500",
        "repl_use_lmtt_amt": "000000000000000",
        "use_pos_repl_fin": "000000003915500",
        "crd_grnta_ch": "000000000000000",
        "crd_grnta_repl": "000000000000000",
        "crd_grnt_ch": "000000000000000",
        "crd_grnt_repl": "000000000000000",
        "uncla": "000000000000",
        "ls_grnt_reu_gold": "000000000000000",
        "20ord_alow_amt": "000000000012550",
        "30ord_alow_amt": "000000000012550",
        "40ord_alow_amt": "000000000012550",
        "50ord_alow_amt": "000000000012550",
        "60ord_alow_amt": "000000000012550",
        "100ord_alow_amt": "000000000012550",
        "tdy_crd_rpya_loss_amt": "000000000000000",
        "pred_crd_rpya_loss_amt": "000000000000000",
        "tdy_ls_rpya_loss_repl_profa": "000000000000000",
        "pred_ls_rpya_loss_repl_profa": "000000000000000",
        "evlt_repl_amt_spg_use_skip": "000000006193400",
        "evlt_repl_rt": "0.6322053",
        "crd_repl_profa": "000000000000000",
        "ch_ord_repl_profa": "000000000000000",
        "crd_ord_repl_profa": "000000000000000",
        "crd_repl_conv_gold": "000000000000000",
        "repl_alowa": "000000003915500",
        "repl_alowa_2": "000000003915500",
        "ch_repl_lck_gold": "000000000000000",
        "crd_repl_lck_gold": "000000000000000",
        "ch_ord_alow_repla": "000000003915500",
        "crd_ord_alow_repla": "000000006193400",
        "d2vexct_entr": "000000000012550",
        "d2ch_ord_alow_amt": "000000000012550",
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00013"},
        )
        response = client.account.get_margin_details()

        assert isinstance(response.body, DomesticAccountMarginDetails)
        assert response.body.tdy_reu_objt_amt == "000000000000000"
        assert response.body.d2vexct_entr == "000000000012550"


def test_get_consignment_comprehensive_transaction_history(client: Client):
    expected_data = {
        "acnt_no": "6081-2***-11 [김키움]",
        "trst_ovrl_trde_prps_array": [
            {
                "trde_dt": "20241121",
                "trde_no": "000000001",
                "rmrk_nm": "장내매도",
                "crd_deal_tp_nm": "보통매매",
                "exct_amt": "000000000056798",
                "loan_amt_rpya": "000000000000000",
                "fc_trde_amt": "0.00",
                "fc_exct_amt": "0.00",
                "entra_remn": "000000994658290",
                "crnc_cd": "KRW",
                "trde_ocr_tp": "9",
                "trde_kind_nm": "매매",
                "stk_nm": "삼성전자",
                "trde_amt": "000000000056900",
                "trde_agri_tax": "000000000000102",
                "rpy_diffa": "000000000000000",
                "fc_trde_tax": "0.00",
                "dly_sum": "000000000000000",
                "fc_entra": "0.00",
                "mdia_tp_nm": "REST API",
                "io_tp": "1",
                "io_tp_nm": "매도",
                "orig_deal_no": "000000000",
                "stk_cd": "A005930",
                "trde_qty_jwa_cnt": "1",
                "cmsn": "000000000000000",
                "int_ls_usfe": "000000000000000",
                "fc_cmsn": "0.00",
                "fc_dly_sum": "0.00",
                "vlbl_nowrm": "21",
                "proc_tm": "08:12:35",
                "isin_cd": "KR7005930003",
                "stex_cd": "",
                "stex_nm": "",
                "trde_unit": "56,900",
                "incm_resi_tax": "000000000000000",
                "loan_dt": "",
                "uncl_ocr": "",
                "rpym_sum": "",
                "cntr_dt": "20241119",
                "rcpy_no": "",
                "prcsr": "DAILY",
                "proc_brch": "키움은행",
                "trde_stle": "",
                "txon_base_pric": "0.00",
                "tax_sum_cmsn": "000000000000102",
                "frgn_pay_txam": "0.00",
                "fc_uncl_ocr": "0.00",
                "rpym_sum_fr": "",
                "rcpmnyer": "",
                "trde_prtc_tp": "11",
            }
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00015"},
        )
        response = client.account.get_consignment_comprehensive_transaction_history(
            strt_dt="20240601",
            end_dt="20240630",
            tp="0",
            gds_tp="0",
            dmst_stex_tp="%",
            stk_cd="005930",
            crnc_cd="KRW",
            frgn_stex_code="",
        )
        assert isinstance(response.body, DomesticAccountConsignmentComprehensiveTransactionHistory)
        assert response.body.acnt_no == "6081-2***-11 [김키움]"
        assert response.body.trst_ovrl_trde_prps_array[0].trde_dt == "20241121"


def test_get_daily_account_profit_rate_details(client: Client):
    expected_data = {
        "mang_empno": "081",
        "mngr_nm": "키움은행",
        "dept_nm": "키움은행",
        "entr_fr": "000000000000",
        "entr_to": "000000017534",
        "scrt_evlt_amt_fr": "000000000000",
        "scrt_evlt_amt_to": "000000000000",
        "ls_grnt_fr": "000000000000",
        "ls_grnt_to": "000000000000",
        "crd_loan_fr": "000000000000",
        "crd_loan_to": "000000000000",
        "ch_uncla_fr": "000000000000",
        "ch_uncla_to": "000000000000",
        "krw_asgna_fr": "000000000000",
        "krw_asgna_to": "000000000000",
        "ls_evlta_fr": "000000000000",
        "ls_evlta_to": "000000000000",
        "rght_evlta_fr": "000000000000",
        "rght_evlta_to": "000000000000",
        "loan_amt_fr": "000000000000",
        "loan_amt_to": "000000000000",
        "etc_loana_fr": "000000000000",
        "etc_loana_to": "000000000000",
        "crd_int_npay_gold_fr": "000000000000",
        "crd_int_npay_gold_to": "000000000000",
        "crd_int_fr": "000000000000",
        "crd_int_to": "000000000000",
        "tot_amt_fr": "000000000000",
        "tot_amt_to": "000000017534",
        "invt_bsamt": "000000000000",
        "evltv_prft": "-00005482466",
        "prft_rt": "-0.91",
        "tern_rt": "0.84",
        "termin_tot_trns": "000000000000",
        "termin_tot_pymn": "000000000000",
        "termin_tot_inq": "000000000000",
        "termin_tot_outq": "000000000000",
        "futr_repl_sella": "000000000000",
        "trst_repl_sella": "000000000000",
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00016"},
        )
        response = client.account.get_daily_account_profit_rate_details(fr_dt="20240601", to_dt="20240630")

        assert isinstance(response.body, DomesticAccountDailyProfitRateDetails)
        assert response.body.evltv_prft == "-00005482466"
        assert response.body.tot_amt_to == "000000017534"


def test_get_account_current_day_status(client: Client):
    expected_data = {
        "d2_entra": "000000012550",
        "crd_int_npay_gold": "000000000000",
        "etc_loana": "000000000000",
        "gnrl_stk_evlt_amt_d2": "000005724100",
        "dpst_grnt_use_amt_d2": "000000000000",
        "crd_stk_evlt_amt_d2": "000000000000",
        "crd_loan_d2": "000000000000",
        "crd_loan_evlta_d2": "000000000000",
        "crd_ls_grnt_d2": "000000000000",
        "crd_ls_evlta_d2": "000000000000",
        "ina_amt": "000000000000",
        "outa": "000000000000",
        "inq_amt": "000000000000",
        "outq_amt": "000000000000",
        "sell_amt": "000000000000",
        "buy_amt": "000000000000",
        "cmsn": "000000000000",
        "tax": "000000000000",
        "stk_pur_cptal_loan_amt": "000000000000",
        "rp_evlt_amt": "000000000000",
        "bd_evlt_amt": "000000000000",
        "elsevlt_amt": "000000000000",
        "crd_int_amt": "000000000000",
        "sel_prica_grnt_loan_int_amt_amt": "000000000000",
        "dvida_amt": "000000000000",
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다..",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00017"},
        )
        response = client.account.get_account_current_day_status()
        assert isinstance(response.body, DomesticAccountCurrentDayStatus)
        assert response.body.d2_entra == "000000012550"
        assert response.body.gnrl_stk_evlt_amt_d2 == "000005724100"


def test_get_account_evaluation_balance_details(client: Client):
    expected_data = {
        "tot_pur_amt": "000000017598258",
        "tot_evlt_amt": "000000025789890",
        "tot_evlt_pl": "000000008138825",
        "tot_prft_rt": "46.25",
        "prsm_dpst_aset_amt": "000001012632507",
        "tot_loan_amt": "000000000000000",
        "tot_crd_loan_amt": "000000000000000",
        "tot_crd_ls_amt": "000000000000000",
        "acnt_evlt_remn_indv_tot": [
            {
                "stk_cd": "A005930",
                "stk_nm": "삼성전자",
                "evltv_prft": "-00000000196888",
                "prft_rt": "-52.71",
                "pur_pric": "000000000124500",
                "pred_close_pric": "000000045400",
                "rmnd_qty": "000000000000003",
                "trde_able_qty": "000000000000003",
                "cur_prc": "000000059000",
                "pred_buyq": "000000000000000",
                "pred_sellq": "000000000000000",
                "tdy_buyq": "000000000000000",
                "tdy_sellq": "000000000000000",
                "pur_amt": "000000000373500",
                "pur_cmsn": "000000000000050",
                "evlt_amt": "000000000177000",
                "sell_cmsn": "000000000000020",
                "tax": "000000000000318",
                "sum_cmsn": "000000000000070",
                "poss_rt": "2.12",
                "crd_tp": "00",
                "crd_tp_nm": "",
                "crd_loan_dt": "",
            },
            {
                "stk_cd": "A005930",
                "stk_nm": "삼성전자",
                "evltv_prft": "-00000000995004",
                "prft_rt": "-59.46",
                "pur_pric": "000000000209178",
                "pred_close_pric": "000000097600",
                "rmnd_qty": "000000000000008",
                "trde_able_qty": "000000000000008",
                "cur_prc": "000000085000",
                "pred_buyq": "000000000000000",
                "pred_sellq": "000000000000000",
                "tdy_buyq": "000000000000000",
                "tdy_sellq": "000000000000000",
                "pur_amt": "000000001673430",
                "pur_cmsn": "000000000000250",
                "evlt_amt": "000000000680000",
                "sell_cmsn": "000000000000100",
                "tax": "000000000001224",
                "sum_cmsn": "000000000000350",
                "poss_rt": "9.51",
                "crd_tp": "00",
                "crd_tp_nm": "",
                "crd_loan_dt": "",
            },
        ],
        "return_code": 0,
        "return_msg": "조회가 완료되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/acnt",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt00018"},
        )
        response = client.account.get_account_evaluation_balance_details(qry_tp="1", dmst_stex_tp="KRX")
        assert isinstance(response.body, DomesticAccountEvaluationBalanceDetails)
        assert response.body.tot_pur_amt == "000000017598258"
        assert response.body.acnt_evlt_remn_indv_tot[0].stk_cd == "A005930"
