import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _domestic_stock_info as stock_info_module
from cluefin_openapi.kiwoom._domestic_stock_info import DomesticStockInfo

from ._helpers import EndpointCase, run_post_case


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


CALL_KWARGS = {
    "get_stock_info": {"stk_cd": "005930"},
    "get_stock_trading_member": {"stk_cd": "005930"},
    "get_execution": {"stk_cd": "005930"},
    "get_margin_trading_trend": {"stk_cd": "005930", "dt": "20250701", "qry_tp": "1"},
    "get_daily_trading_details": {"stk_cd": "005930", "strt_dt": "20250701"},
    "get_new_high_low_price": {
        "mrkt_tp": "001",
        "ntl_tp": "1",
        "high_low_close_tp": "1",
        "stk_cnd": "0",
        "trde_qty_tp": "00000",
        "crd_cnd": "0",
        "updown_incls": "0",
        "dt": "5",
        "stex_tp": "1",
    },
    "get_upper_lower_limit_price": {
        "mrkt_tp": "001",
        "updown_tp": "1",
        "sort_tp": "1",
        "stk_cnd": "0",
        "trde_qty_tp": "00000",
        "crd_cnd": "0",
        "trde_gold_tp": "0",
        "stex_tp": "1",
    },
    "get_high_low_price_approach": {
        "high_low_tp": "1",
        "alacc_rt": "05",
        "mrkt_tp": "001",
        "trde_qty_tp": "00000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "stex_tp": "1",
    },
    "get_price_volatility": {
        "mrkt_tp": "000",
        "flu_tp": "1",
        "tm_tp": "1",
        "tm": "60",
        "trde_qty_tp": "00000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "pric_cnd": "0",
        "updown_incls": "1",
        "stex_tp": "1",
    },
    "get_trading_volume_renewal": {
        "mrkt_tp": "001",
        "cycle_tp": "5",
        "trde_qty_tp": "5",
        "stex_tp": "1",
    },
    "get_supply_demand_concentration": {
        "mrkt_tp": "001",
        "prps_cnctr_rt": "50",
        "cur_prc_entry": "0",
        "prpscnt": "10",
        "cycle_tp": "100",
        "stex_tp": "1",
    },
    "get_high_per": {
        "pertp": "4",
        "stex_tp": "1",
    },
    "get_change_rate_from_open": {
        "sort_tp": "1",
        "trde_qty_cnd": "0000",
        "mrkt_tp": "001",
        "updown_incls": "0",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "trde_prica_cnd": "0",
        "flu_cnd": "1",
        "stex_tp": "1",
    },
    "get_trading_member_supply_demand_analysis": {
        "stk_cd": "005930",
        "strt_dt": "20250701",
        "end_dt": "20250731",
        "qry_dt_tp": "0",
        "pot_tp": "0",
        "dt": "10",
        "sort_base": "1",
        "mmcm_cd": "001",
        "stex_tp": "1",
    },
    "get_trading_member_instant_volume": {
        "mmcm_cd": "001",
        "stk_cd": "005930",
        "mrkt_tp": "0",
        "qty_tp": "0",
        "pric_tp": "0",
        "stex_tp": "1",
    },
    "get_volatility_control_event": {
        "mrkt_tp": "001",
        "bf_mkrt_tp": "0",
        "motn_tp": "0",
        "skip_stk": "000000000",
        "trde_qty_tp": "0",
        "min_trde_qty": "",
        "max_trde_qty": "",
        "trde_prica_tp": "0",
        "min_trde_prica": "",
        "max_trde_prica": "",
        "motn_drc": "0",
        "stex_tp": "1",
    },
    "get_daily_previous_day_execution_volume": {
        "stk_cd": "005930",
        "tdy_pred": "1",
    },
    "get_daily_trading_items_by_investor": {
        "strt_dt": "20250701",
        "end_dt": "20250731",
        "trde_tp": "2",
        "mrkt_tp": "001",
        "invsr_tp": "8000",
        "stex_tp": "1",
    },
    "get_institutional_investor_by_stock": {
        "dt": "20250701",
        "stk_cd": "005930",
        "amt_qty_tp": "1",
        "trde_tp": "0",
        "unit_tp": "1000",
    },
    "get_total_institutional_investor_by_stock": {
        "stk_cd": "005930",
        "strt_dt": "20250701",
        "end_dt": "20250731",
        "amt_qty_tp": "1",
        "trde_tp": "0",
        "unit_tp": "1000",
    },
    "get_daily_previous_day_conclusion": {
        "stk_cd": "005930",
        "tdy_pred": "1",
    },
    "get_interest_stock_info": {"stk_cd": "005930"},
    "get_stock_info_summary": {"mrkt_tp": "0"},
    "get_stock_info_v1": {"stk_cd": "005930"},
    "get_industry_code": {"mrkt_tp": "0"},
    "get_member_company": {},
    "get_top_50_program_net_buy": {
        "trde_upper_tp": "2",
        "amt_qty_tp": "1",
        "mrkt_tp": "P00101",
        "stex_tp": "1",
    },
    "get_program_trading_status_by_stock": {
        "dt": "20250701",
        "mrkt_tp": "P00101",
        "stex_tp": "1",
    },
}


def method_metadata(method_name: str) -> tuple[str, str, str]:
    method = getattr(DomesticStockInfo, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (DomesticStockInfo\w+)\.model_validate", source).group(1)
    if '"con-yn"' in source:
        cont_key = "con-yn"
    elif '"cond-yn"' in source:
        cont_key = "cond-yn"
    else:
        cont_key = "cont-yn"
    return api_id, model_attr, cont_key


STOCK_CASES = []
for method_name in sorted(CALL_KWARGS):
    api_id, model_attr, cont_key = method_metadata(method_name)
    raw_kwargs = dict(CALL_KWARGS[method_name])
    cont_value = raw_kwargs.pop("cont_yn", "N")
    next_key = raw_kwargs.pop("next_key", "")
    STOCK_CASES.append(
        EndpointCase(
            name=method_name.removeprefix("get_"),
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(raw_kwargs),
            expected_body=dict(raw_kwargs),
            response_payload=payload(method_name.removeprefix("get_")),
            cont_flag_key=cont_key,
            cont_flag_value=cont_value,
            next_key=next_key,
        )
    )


@pytest.mark.parametrize("case", STOCK_CASES, ids=lambda case: case.name)
def test_domestic_stock_info_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        stock_info_module,
        DomesticStockInfo,
        case,
        base_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
