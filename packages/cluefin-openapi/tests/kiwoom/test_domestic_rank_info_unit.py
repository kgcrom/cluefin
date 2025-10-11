import inspect
import re
from typing import Dict

import pytest

from cluefin_openapi.kiwoom import _domestic_rank_info as rank_info_module
from cluefin_openapi.kiwoom._domestic_rank_info import DomesticRankInfo

from ._helpers import EndpointCase, run_post_case


def payload(name: str) -> Dict[str, str]:
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


CALL_KWARGS: Dict[str, Dict[str, str]] = {
    "get_top_remaining_order_quantity": {
        "mrkt_tp": "001",
        "sort_tp": "1",
        "trde_qty_tp": "0000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "stex_tp": "1",
    },
    "get_rapidly_increasing_remaining_order_quantity": {
        "mrkt_tp": "001",
        "trde_tp": "1",
        "sort_tp": "1",
        "tm_tp": "30",
        "trde_qty_tp": "1",
        "stk_cnd": "0",
        "stex_tp": "1",
    },
    "get_rapidly_increasing_total_sell_orders": {
        "mrkt_tp": "001",
        "rt_tp": "1",
        "tm_tp": "1",
        "trde_qty_tp": "5",
        "stk_cnd": "0",
        "stex_tp": "1",
    },
    "get_rapidly_increasing_trading_volume": {
        "mrkt_tp": "000",
        "sort_tp": "1",
        "tm_tp": "2",
        "trde_qty_tp": "5",
        "stk_cnd": "0",
        "pric_tp": "0",
        "stex_tp": "1",
    },
    "get_top_percentage_change_from_previous_day": {
        "mrkt_tp": "000",
        "sort_tp": "1",
        "trde_qty_cnd": "0000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "updown_incls": "1",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "stex_tp": "1",
    },
    "get_top_expected_conclusion_percentage_change": {
        "mrkt_tp": "000",
        "sort_tp": "1",
        "trde_qty_cnd": "0",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "pric_cnd": "0",
        "stex_tp": "1",
    },
    "get_top_current_day_trading_volume": {
        "mrkt_tp": "000",
        "sort_tp": "1",
        "mang_stk_incls": "0",
        "crd_tp": "0",
        "trde_qty_tp": "0",
        "pric_tp": "0",
        "trde_prica_tp": "0",
        "mrkt_open_tp": "0",
        "stex_tp": "1",
    },
    "get_top_previous_day_trading_volume": {
        "mrkt_tp": "101",
        "qry_tp": "1",
        "rank_strt": "0",
        "rank_end": "10",
        "stex_tp": "1",
    },
    "get_top_transaction_value": {
        "mrkt_tp": "001",
        "mang_stk_incls": "0",
        "stex_tp": "1",
    },
    "get_top_margin_ratio": {
        "mrkt_tp": "000",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "updown_incls": "1",
        "crd_cnd": "0",
        "stex_tp": "1",
    },
    "get_top_foreigner_period_trading": {
        "mrkt_tp": "001",
        "trde_tp": "2",
        "dt": "0",
        "stex_tp": "1",
    },
    "get_top_consecutive_net_buy_sell_by_foreigners": {
        "mrkt_tp": "000",
        "trde_tp": "2",
        "base_dt_tp": "1",
        "stex_tp": "1",
    },
    "get_top_limit_exhaustion_rate_foreigner": {
        "mrkt_tp": "000",
        "dt": "0",
        "stex_tp": "1",
    },
    "get_top_foreign_account_group_trading": {
        "mrkt_tp": "000",
        "dt": "0",
        "trde_tp": "1",
        "sort_tp": "2",
        "stex_tp": "1",
    },
    "get_stock_specific_securities_firm_ranking": {
        "stk_cd": "005930",
        "strt_dt": "20250601",
        "end_dt": "20250602",
        "qry_tp": "2",
        "dt": "1",
    },
    "get_top_securities_firm_trading": {
        "mmcm_cd": "001",
        "trde_qty_tp": "0",
        "trde_tp": "1",
        "dt": "1",
        "stex_tp": "1",
    },
    "get_top_current_day_major_traders": {
        "stk_cd": "005930",
    },
    "get_top_net_buy_trader_ranking": {
        "stk_cd": "005930",
        "strt_dt": "20241031",
        "end_dt": "20241107",
        "qry_dt_tp": "0",
        "pot_tp": "0",
        "dt": "5",
        "sort_base": "1",
    },
    "get_top_current_day_deviation_sources": {
        "stk_cd": "005930",
    },
    "get_same_net_buy_sell_ranking": {
        "strt_dt": "20241106",
        "end_dt": "20241107",
        "mrkt_tp": "000",
        "trde_tp": "1",
        "sort_cnd": "1",
        "unit_tp": "1",
        "stex_tp": "1",
    },
    "get_top_intraday_trading_by_investor": {
        "trde_tp": "1",
        "mrkt_tp": "000",
        "orgn_tp": "9000",
    },
    "get_after_hours_single_price_change_rate_ranking": {
        "mrkt_tp": "000",
        "sort_base": "5",
        "stk_cnd": "0",
        "trde_qty_cnd": "0",
        "crd_cnd": "0",
        "trde_prica": "0",
    },
    "get_top_foreigner_limit_exhaustion_rate": {
        "mrkt_tp": "001",
        "dt": "1",
        "stex_tp": "1",
    },
}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(DomesticRankInfo, method_name)
    source = inspect.getsource(method)
    api_id_match = re.search(r'"api-id":\s*"([^"]+)"', source)
    model_match = re.search(r"= (DomesticRankInfo\w+)\.model_validate", source)
    if not api_id_match or not model_match:
        raise ValueError(f"Could not extract metadata for {method_name}")
    return api_id_match.group(1), model_match.group(1)


RANK_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    RANK_CASES.append(
        EndpointCase(
            name=case_name,
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(kwargs),
            expected_body=dict(kwargs),
            response_payload=payload(case_name),
        )
    )


@pytest.mark.parametrize("case", RANK_CASES, ids=lambda case: case.name)
def test_domestic_rank_info_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        rank_info_module,
        DomesticRankInfo,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
