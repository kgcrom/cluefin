import pytest

from cluefin_openapi.kiwoom import _domestic_etf as domestic_etf_module
from cluefin_openapi.kiwoom._domestic_etf import DomesticETF

from ._helpers import EndpointCase, run_post_case

ETF_CASES = [
    EndpointCase(
        name="return_rate",
        method_name="get_etf_return_rate",
        response_model_attr="DomesticEtfReturnRate",
        api_id="ka40001",
        call_kwargs={"stk_cd": "069500", "etfobjt_idex_cd": "001", "dt": 0},
        expected_body={"stk_cd": "069500", "etfobjt_idex_cd": "001", "dt": 0},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfprft_rt_lst": [{"etfprft_rt": "-1.33"}],
        },
    ),
    EndpointCase(
        name="item_info",
        method_name="get_etf_item_info",
        response_model_attr="DomesticEtfItemInfo",
        api_id="ka40002",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={"return_code": 0, "return_msg": "OK", "stk_nm": "KODEX 200"},
    ),
    EndpointCase(
        name="daily_trend",
        method_name="get_etf_daily_trend",
        response_model_attr="DomesticEtfDailyTrend",
        api_id="ka40003",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfdaly_trnsn": [{"cntr_dt": "20240101", "cur_prc": "100500"}],
        },
    ),
    EndpointCase(
        name="full_price",
        method_name="get_etf_full_price",
        response_model_attr="DomesticEtfFullPrice",
        api_id="ka40004",
        call_kwargs={
            "txon_type": "0",
            "navpre": "0",
            "mngmcomp": "0000",
            "txon_yn": "0",
            "trace_idex": "0",
            "stex_tp": "1",
        },
        expected_body={
            "txon_type": "0",
            "navpre": "0",
            "mngmcomp": "0000",
            "txon_yn": "0",
            "trace_idex": "0",
            "stex_tp": "1",
        },
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfall_mrpr": [{"stk_cd": "069500", "stk_nm": "KODEX 200"}],
        },
    ),
    EndpointCase(
        name="hourly_trend",
        method_name="get_etf_hourly_trend",
        response_model_attr="DomesticEtfHourlyTrend",
        api_id="ka40006",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfhrly_trnsn": [{"tm": "0930", "cur_prc": "100500"}],
        },
    ),
    EndpointCase(
        name="hourly_execution",
        method_name="get_etf_hourly_execution",
        response_model_attr="DomesticEtfHourlyExecution",
        api_id="ka40007",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfhrly_cntr": [{"tm": "0930", "trde_qty": "100"}],
        },
    ),
    EndpointCase(
        name="daily_execution",
        method_name="get_etf_daily_execution",
        response_model_attr="DomesticEtfDailyExecution",
        api_id="ka40008",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfdaly_cntr": [{"dt": "20240101", "trde_qty": "100"}],
        },
    ),
    EndpointCase(
        name="hourly_execution_v2",
        method_name="get_etf_hourly_execution_v2",
        response_model_attr="DomesticEtfHourlyExecutionV2",
        api_id="ka40009",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfhrly_cntr_v2": [{"tm": "0930", "trde_qty": "100"}],
        },
    ),
    EndpointCase(
        name="hourly_trend_v2",
        method_name="get_etf_hourly_trend_v2",
        response_model_attr="DomesticEtfHourlyTrendV2",
        api_id="ka40010",
        call_kwargs={"stk_cd": "069500"},
        expected_body={"stk_cd": "069500"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "etfhrly_trnsn_v2": [{"tm": "0930", "cur_prc": "100500"}],
        },
    ),
]


@pytest.mark.parametrize("case", ETF_CASES, ids=lambda case: case.name)
def test_domestic_etf_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        domestic_etf_module,
        DomesticETF,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
