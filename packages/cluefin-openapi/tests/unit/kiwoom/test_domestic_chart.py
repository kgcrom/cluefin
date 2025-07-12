"""Tests for the Auth class."""

import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_chart_types import (
    DomesticChartIndividualStockInstitutional,
    DomesticChartIndustryDaily,
    DomesticChartIndustryMinute,
    DomesticChartIndustryMonthly,
    DomesticChartIndustryTick,
    DomesticChartIndustryWeekly,
    DomesticChartIndustryYearly,
    DomesticChartIntradayInvestorTrading,
    DomesticChartStockDaily,
    DomesticChartStockMinute,
    DomesticChartStockMonthly,
    DomesticChartStockTick,
    DomesticChartStockWeekly,
    DomesticChartStockYearly,
)


@pytest.fixture
def client():
    return Client(
        token="test_token",
        env="dev",
    )


def test_get_individual_stock_institutional_chart(client: Client):
    expected_data = {
        "stk_invsr_orgn_chart": [
            {
                "dt": "20241107",
                "cur_prc": "+61300",
                "pred_pre": "+4000",
                "acc_trde_prica": "1105968",
                "ind_invsr": "1584",
                "frgnr_invsr": "-61779",
                "orgn": "60195",
                "fnnc_invt": "25514",
                "insrnc": "0",
                "invtrt": "0",
                "etc_fnnc": "34619",
                "bank": "4",
                "penfnd_etc": "-1",
                "samo_fund": "58",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "1",
            },
            {
                "dt": "20241106",
                "cur_prc": "+74800",
                "pred_pre": "+17200",
                "acc_trde_prica": "448203",
                "ind_invsr": "-639",
                "frgnr_invsr": "-7",
                "orgn": "646",
                "fnnc_invt": "-47",
                "insrnc": "15",
                "invtrt": "-2",
                "etc_fnnc": "730",
                "bank": "-51",
                "penfnd_etc": "1",
                "samo_fund": "0",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10060"},
        )

        response = client.chart.get_individual_stock_institutional_chart("20241107", "005930", "1", "0", "1000")

        assert isinstance(response.body, DomesticChartIndividualStockInstitutional)
        assert response.body.stk_invsr_orgn_chart[0].dt == "20241107"
        assert response.body.stk_invsr_orgn_chart[0].cur_prc == "+61300"


def test_get_intraday_investor_trading(client: Client):
    expected_data = {
        "stk_invsr_orgn_chart": [
            {
                "dt": "20241107",
                "cur_prc": "+61300",
                "pred_pre": "+4000",
                "acc_trde_prica": "1105968",
                "ind_invsr": "1584",
                "frgnr_invsr": "-61779",
                "orgn": "60195",
                "fnnc_invt": "25514",
                "insrnc": "0",
                "invtrt": "0",
                "etc_fnnc": "34619",
                "bank": "4",
                "penfnd_etc": "-1",
                "samo_fund": "58",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "1",
            },
            {
                "dt": "20241106",
                "cur_prc": "+74800",
                "pred_pre": "+17200",
                "acc_trde_prica": "448203",
                "ind_invsr": "-639",
                "frgnr_invsr": "-7",
                "orgn": "646",
                "fnnc_invt": "-47",
                "insrnc": "15",
                "invtrt": "-2",
                "etc_fnnc": "730",
                "bank": "-51",
                "penfnd_etc": "1",
                "samo_fund": "0",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10064"},
        )

        response = client.chart.get_individual_stock_institutional_chart("20250630", "005930", "1", "0", "1000")

        assert isinstance(response.body, DomesticChartIndividualStockInstitutional)
        assert response.body.stk_invsr_orgn_chart[0].dt == "20241107"
        assert response.body.stk_invsr_orgn_chart[0].cur_prc == "+61300"


def test_intraday_investor_trading(client: Client):
    expected_data = {
        "opmr_invsr_trde_chart": [
            {
                "tm": "090000",
                "frgnr_invsr": "0",
                "orgn": "0",
                "invtrt": "0",
                "insrnc": "0",
                "bank": "0",
                "penfnd_etc": "0",
                "etc_corp": "0",
                "natn": "0",
            },
            {
                "tm": "092200",
                "frgnr_invsr": "3",
                "orgn": "0",
                "invtrt": "0",
                "insrnc": "0",
                "bank": "0",
                "penfnd_etc": "0",
                "etc_corp": "0",
                "natn": "0",
            },
            {
                "tm": "095200",
                "frgnr_invsr": "-68",
                "orgn": "0",
                "invtrt": "0",
                "insrnc": "0",
                "bank": "0",
                "penfnd_etc": "0",
                "etc_corp": "0",
                "natn": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10064"},
        )

        response = client.chart.get_intraday_investor_trading("0000", "1", "0", "005930")

        assert isinstance(response.body, DomesticChartIntradayInvestorTrading)
        assert response.body.opmr_invsr_trde_chart[0].tm == "090000"
        assert response.body.opmr_invsr_trde_chart[0].frgnr_invsr == "0"


def test_get_stock_tick(client: Client):
    excepted_data = {
        "stk_cd": "005930",
        "last_tic_cnt": "",
        "stk_tic_chart_qry": [
            {
                "cur_prc": "132500",
                "trde_qty": "1",
                "cntr_tm": "20241106141853",
                "open_pric": "132500",
                "high_pric": "132500",
                "low_pric": "132500",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "132600",
                "trde_qty": "10",
                "cntr_tm": "20241106111111",
                "open_pric": "132600",
                "high_pric": "132600",
                "low_pric": "132600",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=excepted_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10079"},
        )

        response = client.chart.get_stock_tick("005930", "1", "1")

        assert isinstance(response.body, DomesticChartStockTick)
        assert response.body.stk_tic_chart_qry[0].cntr_tm == "20241106141853"
        assert response.body.stk_tic_chart_qry[0].cur_prc == "132500"


def test_get_stock_minute(client: Client):
    excepted_data = {
        "stk_cd": "005930",
        "stk_min_pole_chart_qry": [
            {
                "cur_prc": "-132500",
                "trde_qty": "1",
                "cntr_tm": "20241106141800",
                "open_pric": "-132500",
                "high_pric": "-132500",
                "low_pric": "-132500",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "-132600",
                "trde_qty": "10",
                "cntr_tm": "20241106111100",
                "open_pric": "-132600",
                "high_pric": "-132600",
                "low_pric": "-132600",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=excepted_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10080"},
        )

        response = client.chart.get_stock_minute("005930", "1", "1")

        assert isinstance(response.body, DomesticChartStockMinute)
        assert response.body.stk_min_pole_chart_qry[0].cntr_tm == "20241106141800"
        assert response.body.stk_min_pole_chart_qry[0].cur_prc == "-132500"


def test_get_stock_daily(client: Client):
    expected_data = {
        "stk_cd": "005930",
        "stk_dt_pole_chart_qry": [
            {
                "cur_prc": "133600",
                "trde_qty": "0",
                "trde_prica": "0",
                "dt": "20241107",
                "open_pric": "133600",
                "high_pric": "133600",
                "low_pric": "133600",
                "upd_stkpc_tp": "",
                "upd_rt": "+0.83",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "133600",
                "trde_qty": "53",
                "trde_prica": "7",
                "dt": "20241106",
                "open_pric": "134205",
                "high_pric": "134205",
                "low_pric": "133600",
                "upd_stkpc_tp": "",
                "upd_rt": "-1.63",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10081"},
        )

        response = client.chart.get_stock_daily("005930", "20250630", "1")

        assert isinstance(response.body, DomesticChartStockDaily)
        assert response.body.stk_dt_pole_chart_qry[0].cur_prc == "133600"
        assert response.body.stk_dt_pole_chart_qry[0].open_pric == "133600"


def test_get_stock_weekly(client: Client):
    expected_data = {
        "stk_cd": "005930",
        "stk_stk_pole_chart_qry": [
            {
                "cur_prc": "127600",
                "trde_qty": "53",
                "trde_prica": "7043700",
                "dt": "20241105",
                "open_pric": "134199",
                "high_pric": "134205",
                "low_pric": "127600",
                "upd_stkpc_tp": "",
                "upd_rt": "+106.14",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "134197",
                "trde_qty": "49",
                "trde_prica": "9292500",
                "dt": "20241028",
                "open_pric": "196658",
                "high_pric": "196658",
                "low_pric": "133991",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10082"},
        )

        response = client.chart.get_stock_weekly("005930", "20250630", "1")

        assert isinstance(response.body, DomesticChartStockWeekly)
        assert response.body.stk_stk_pole_chart_qry[0].cur_prc == "127600"
        assert response.body.stk_stk_pole_chart_qry[0].open_pric == "134199"


def test_get_stock_monthly(client: Client):
    expected_data = {
        "stk_cd": "005930",
        "stk_mth_pole_chart_qry": [
            {
                "cur_prc": "127600",
                "trde_qty": "55",
                "trde_prica": "7043700",
                "dt": "20241101",
                "open_pric": "128171",
                "high_pric": "128179",
                "low_pric": "127600",
                "upd_stkpc_tp": "",
                "upd_rt": "+96.88",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "128169",
                "trde_qty": "455",
                "trde_prica": "87853100",
                "dt": "20241002",
                "open_pric": "264016",
                "high_pric": "274844",
                "low_pric": "127972",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10083"},
        )

        response = client.chart.get_stock_monthly("005930", "20250630", "1")

        assert isinstance(response.body, DomesticChartStockMonthly)
        assert response.body.stk_mth_pole_chart_qry[0].cur_prc == "127600"
        assert response.body.stk_mth_pole_chart_qry[0].open_pric == "128171"


def test_get_stock_yearly(client: Client):
    expected_data = {
        "stk_cd": "005930",
        "stk_yr_pole_chart_qry": [
            {
                "cur_prc": "11510",
                "trde_qty": "83955682",
                "trde_prica": "1473889778085",
                "dt": "20240102",
                "open_pric": "38950",
                "high_pric": "39100",
                "low_pric": "10500",
                "upd_stkpc_tp": "",
                "upd_rt": "",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "39000",
                "trde_qty": "337617963",
                "trde_prica": "16721059332050",
                "dt": "20230102",
                "open_pric": "20369",
                "high_pric": "93086",
                "low_pric": "20369",
                "upd_stkpc_tp": "1,4,256",
                "upd_rt": "-1.60",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "upd_stkpc_event": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10094"},
        )

        response = client.chart.get_stock_yearly("005930", "20250630", "1")

        assert isinstance(response.body, DomesticChartStockYearly)
        assert response.body.stk_yr_pole_chart_qry[0].cur_prc == "11510"
        assert response.body.stk_yr_pole_chart_qry[0].open_pric == "38950"


def test_get_industry_tick(client: Client):
    expected_data = {
        "inds_cd": "001",
        "inds_tic_chart_qry": [
            {
                "cur_prc": "239326",
                "trde_qty": "0",
                "cntr_tm": "20241122144300",
                "open_pric": "239326",
                "high_pric": "239326",
                "low_pric": "239326",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "239326",
                "trde_qty": "0",
                "cntr_tm": "20241122144250",
                "open_pric": "239326",
                "high_pric": "239326",
                "low_pric": "239326",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "239326",
                "trde_qty": "0",
                "cntr_tm": "20241122144240",
                "open_pric": "239326",
                "high_pric": "239326",
                "low_pric": "239326",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20004"},
        )

        response = client.chart.get_industry_tick("001", "1")

        assert isinstance(response.body, DomesticChartIndustryTick)
        assert response.body.inds_tic_chart_qry[0].cur_prc == "239326"
        assert response.body.inds_tic_chart_qry[0].cntr_tm == "20241122144300"


def test_get_industry_minute(client: Client):
    expected_data = {
        "inds_cd": "001",
        "inds_min_pole_qry": [
            {
                "cur_prc": "-239417",
                "trde_qty": "2",
                "cntr_tm": "20241122144500",
                "open_pric": "+239252",
                "high_pric": "+239417",
                "low_pric": "+239250",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "-239326",
                "trde_qty": "1",
                "cntr_tm": "20241122144000",
                "open_pric": "+239329",
                "high_pric": "+239329",
                "low_pric": "+239326",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20005"},
        )

        response = client.chart.get_industry_minute("001", "1")

        assert isinstance(response.body, DomesticChartIndustryMinute)
        assert response.body.inds_min_pole_qry[0].cur_prc == "-239417"
        assert response.body.inds_min_pole_qry[0].cntr_tm == "20241122144500"


def test_get_industry_daily(client: Client):
    expected_data = {
        "inds_cd": "001",
        "inds_dt_pole_qry": [
            {
                "cur_prc": "239260",
                "trde_qty": "996",
                "dt": "20241122",
                "open_pric": "266953",
                "high_pric": "266953",
                "low_pric": "237521",
                "trde_prica": "46668",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "267296",
                "trde_qty": "444",
                "dt": "20241121",
                "open_pric": "264741",
                "high_pric": "278714",
                "low_pric": "254751",
                "trde_prica": "8961",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20006"},
        )

        response = client.chart.get_industry_daily("001", "20250630")

        assert isinstance(response.body, DomesticChartIndustryDaily)
        assert response.body.inds_dt_pole_qry[0].cur_prc == "239260"
        assert response.body.inds_dt_pole_qry[0].trde_qty == "996"


def test_get_industry_weekly(client: Client):
    expected_data = {
        "inds_cd": "001",
        "inds_stk_pole_qry": [
            {
                "cur_prc": "238457",
                "trde_qty": "1988",
                "dt": "20241118",
                "open_pric": "244182",
                "high_pric": "279354",
                "low_pric": "237521",
                "trde_prica": "86023",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "248731",
                "trde_qty": "491",
                "dt": "20241111",
                "open_pric": "256115",
                "high_pric": "275840",
                "low_pric": "241690",
                "trde_prica": "31221",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20007"},
        )
        response = client.chart.get_industry_weekly("001", "20250630")

        assert isinstance(response.body, DomesticChartIndustryWeekly)
        assert response.body.inds_stk_pole_qry[0].cur_prc == "238457"
        assert response.body.inds_stk_pole_qry[0].trde_qty == "1988"


def test_get_industry_monthly(client: Client):
    expected_data = {
        "inds_cd": "002",
        "inds_mth_pole_qry": [
            {
                "cur_prc": "237044",
                "trde_qty": "4586",
                "dt": "20241101",
                "open_pric": "167825",
                "high_pric": "285472",
                "low_pric": "154868",
                "trde_prica": "310647",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
            {
                "cur_prc": "164837",
                "trde_qty": "10944",
                "dt": "20241002",
                "open_pric": "264799",
                "high_pric": "307362",
                "low_pric": "151279",
                "trde_prica": "726698",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20008"},
        )

        response = client.chart.get_industry_monthly("002", "20250630")
        assert isinstance(response.body, DomesticChartIndustryMonthly)
        assert response.body.inds_mth_pole_qry[0].cur_prc == "237044"
        assert response.body.inds_mth_pole_qry[0].trde_qty == "4586"


def test_get_industry_yearly(client: Client):
    expected_data = {
        "inds_cd": "001",
        "inds_yr_pole_qry": [
            {
                "cur_prc": "238630",
                "trde_qty": "50610088",
                "dt": "20240313",
                "open_pric": "269471",
                "high_pric": "300191",
                "low_pric": "160807",
                "trde_prica": "1150879139",
                "bic_inds_tp": "",
                "sm_inds_tp": "",
                "stk_infr": "",
                "pred_close_pric": "",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/chart",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20009"},
        )

        response = client.chart.get_industry_yearly("001", "20250630")
        assert isinstance(response.body, DomesticChartIndustryYearly)
        assert response.body.inds_yr_pole_qry[0].cur_prc == "238630"
        assert response.body.inds_yr_pole_qry[0].trde_qty == "50610088"
