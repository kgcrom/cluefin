import pytest

from cluefin_openapi.kiwoom import _domestic_chart as domestic_chart_module
from cluefin_openapi.kiwoom._domestic_chart import DomesticChart

from ._helpers import EndpointCase, run_post_case

CHART_CASES = [
    EndpointCase(
        name="individual_stock_institutional",
        method_name="get_individual_stock_institutional_chart",
        response_model_attr="DomesticChartIndividualStockInstitutional",
        api_id="ka10060",
        call_kwargs={
            "dt": "20240101",
            "stk_cd": "005930",
            "amt_qty_tp": "1",
            "trde_tp": "0",
            "unit_tp": "1000",
        },
        expected_body={
            "dt": "20240101",
            "stk_cd": "005930",
            "amt_qty_tp": "1",
            "trde_tp": "0",
            "unit_tp": "1000",
        },
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_invsr_orgn_chart": [{"dt": "20240101", "cur_prc": "+100"}],
        },
    ),
    EndpointCase(
        name="intraday_investor_trading",
        method_name="get_intraday_investor_trading",
        response_model_attr="DomesticChartIntradayInvestorTrading",
        api_id="ka10064",
        call_kwargs={
            "mrkt_tp": "000",
            "amt_qty_tp": "1",
            "trde_tp": "0",
            "stk_cd": "005930",
        },
        expected_body={
            "stk_cd": "005930",
            "amt_qty_tp": "1",
            "trde_tp": "0",
            "mrkt_tp": "000",
        },
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "opmr_invsr_trde_chart": [{"tm": "090000", "frgnr_invsr": "0"}],
        },
    ),
    EndpointCase(
        name="stock_tick",
        method_name="get_stock_tick",
        response_model_attr="DomesticChartStockTick",
        api_id="ka10079",
        call_kwargs={"stk_cd": "005930", "tic_scope": "1", "upd_stkpc_tp": "0"},
        expected_body={"stk_cd": "005930", "tic_scope": "1", "upd_stkpc_tp": "0"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_tic_chart_qry": [{"cntr_tm": "20240101120000", "cur_prc": "100000"}],
        },
    ),
    EndpointCase(
        name="stock_minute",
        method_name="get_stock_minute",
        response_model_attr="DomesticChartStockMinute",
        api_id="ka10080",
        call_kwargs={"stk_cd": "005930", "tic_scope": "1", "upd_stkpc_tp": "0"},
        expected_body={"stk_cd": "005930", "tic_scope": "1", "upd_stkpc_tp": "0"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_min_pole_chart_qry": [{"cntr_tm": "202401011200", "cur_prc": "100000"}],
        },
    ),
    EndpointCase(
        name="stock_daily",
        method_name="get_stock_daily",
        response_model_attr="DomesticChartStockDaily",
        api_id="ka10081",
        call_kwargs={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        expected_body={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_dt_pole_chart_qry": [{"dt": "20240101", "cur_prc": "100000"}],
        },
    ),
    EndpointCase(
        name="stock_weekly",
        method_name="get_stock_weekly",
        response_model_attr="DomesticChartStockWeekly",
        api_id="ka10082",
        call_kwargs={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        expected_body={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_stk_pole_chart_qry": [{"dt": "2024W01", "cur_prc": "100000"}],
        },
    ),
    EndpointCase(
        name="stock_monthly",
        method_name="get_stock_monthly",
        response_model_attr="DomesticChartStockMonthly",
        api_id="ka10083",
        call_kwargs={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        expected_body={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_mth_pole_chart_qry": [{"dt": "202401", "cur_prc": "100000"}],
        },
    ),
    EndpointCase(
        name="stock_yearly",
        method_name="get_stock_yearly",
        response_model_attr="DomesticChartStockYearly",
        api_id="ka10094",
        call_kwargs={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        expected_body={"stk_cd": "005930", "base_dt": "20240101", "upd_stkpc_tp": "0"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_yr_pole_chart_qry": [{"dt": "2024", "cur_prc": "100000"}],
        },
    ),
    EndpointCase(
        name="industry_tick",
        method_name="get_industry_tick",
        response_model_attr="DomesticChartIndustryTick",
        api_id="ka20004",
        call_kwargs={"inds_cd": "001", "tic_scope": "1"},
        expected_body={"inds_cd": "001", "tic_scope": "1"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "inds_tic_pole_chart_qry": [{"tm": "20240101120000", "cur_prc": "1000"}],
        },
    ),
    EndpointCase(
        name="industry_minute",
        method_name="get_industry_minute",
        response_model_attr="DomesticChartIndustryMinute",
        api_id="ka20005",
        call_kwargs={"inds_cd": "001", "tic_scope": "1"},
        expected_body={"inds_cd": "001", "tic_scope": "1"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "inds_min_pole_chart_qry": [{"tm": "202401011200", "cur_prc": "1000"}],
        },
    ),
    EndpointCase(
        name="industry_daily",
        method_name="get_industry_daily",
        response_model_attr="DomesticChartIndustryDaily",
        api_id="ka20006",
        call_kwargs={"inds_cd": "001", "base_dt": "20240101"},
        expected_body={"inds_cd": "001", "base_dt": "20240101"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "inds_dt_pole_chart_qry": [{"dt": "20240101", "cur_prc": "1000"}],
        },
    ),
    EndpointCase(
        name="industry_weekly",
        method_name="get_industry_weekly",
        response_model_attr="DomesticChartIndustryWeekly",
        api_id="ka20007",
        call_kwargs={"inds_cd": "001", "base_dt": "20240101"},
        expected_body={"inds_cd": "001", "base_dt": "20240101"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "inds_stk_pole_chart_qry": [{"dt": "2024W01", "cur_prc": "1000"}],
        },
    ),
    EndpointCase(
        name="industry_monthly",
        method_name="get_industry_monthly",
        response_model_attr="DomesticChartIndustryMonthly",
        api_id="ka20008",
        call_kwargs={"inds_cd": "001", "base_dt": "20240101"},
        expected_body={"inds_cd": "001", "base_dt": "20240101"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "inds_mth_pole_chart_qry": [{"dt": "202401", "cur_prc": "1000"}],
        },
    ),
    EndpointCase(
        name="industry_yearly",
        method_name="get_industry_yearly",
        response_model_attr="DomesticChartIndustryYearly",
        api_id="ka20019",
        call_kwargs={"inds_cd": "001", "base_dt": "20240101"},
        expected_body={"inds_cd": "001", "base_dt": "20240101"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "inds_yr_pole_chart_qry": [{"dt": "2024", "cur_prc": "1000"}],
        },
    ),
]


@pytest.mark.parametrize("case", CHART_CASES, ids=lambda case: case.name)
def test_domestic_chart_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        domestic_chart_module,
        DomesticChart,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
