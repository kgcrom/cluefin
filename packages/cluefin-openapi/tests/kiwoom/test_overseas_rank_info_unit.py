import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_rank_info as overseas_rank_info_module
from cluefin_openapi.kiwoom._overseas_rank_info import OverseasRankInfo

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_realtime_symbol_query_rank": {"svc_type": "B286"},
    "get_watchlist_registration_top": {"dt_unit_tp": "D", "stk_tp": "A"},
    "get_period_fluctuation_rank_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "stk_cnd": "0",
        "tm": "1",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_period_fluctuation_rank_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "stk_cnd": "0",
        "tm": "1",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_period_fluctuation_rank_watchlist": {
        "stex_tp": "1",
        "stk_cd": [{"stex_tp": "ND", "stk_cd": "AAPL"}],
        "tm": "1",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_today_trading_volume_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "trde_qty_tp": "0",
        "qry_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_today_trading_volume_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "qry_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_today_trading_value_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_today_trading_value_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_market_cap_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_market_cap_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_kiwoom_trading_top_stock": {"qry_tp": "1", "dt_unit_tp": "1"},
    "get_kiwoom_trading_top_etf": {"qry_tp": "1", "dt_unit_tp": "1"},
    "get_previous_day_fluctuation_rank_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "inds_cls_tp": "0",
        "sort_tp": "1",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_previous_day_fluctuation_rank_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "sort_tp": "1",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_open_price_fluctuation_rank_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "trde_qty_tp": "0",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "1",
    },
    "get_open_price_fluctuation_rank_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "1",
    },
    "get_open_price_fluctuation_rank_watchlist": {
        "stex_tp": "1",
        "stk_cd": [{"stex_tp": "ND", "stk_cd": "AAPL"}],
        "sort_tp": "1",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_cumulative_fluctuation_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "sort_tp": "0",
        "pric_cnd1": "",
        "pric_cnd2": "",
        "base_dt": "20240102",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_cumulative_fluctuation_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "sort_tp": "0",
        "pric_cnd1": "",
        "pric_cnd2": "",
        "base_dt": "20240102",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_previous_day_trading_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "qry_tp": "0",
    },
    "get_previous_day_trading_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "qry_tp": "0",
    },
    "get_high_low_price_rise_fall_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "sort_tp": "0",
        "dt_tp": "0",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_high_low_price_rise_fall_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "sort_tp": "0",
        "dt_tp": "0",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_specific_date_rise_fall_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
        "base_dt": "20240102",
        "sort_tp": "0",
    },
    "get_specific_date_rise_fall_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
        "base_dt": "20240102",
        "sort_tp": "0",
    },
    "get_turnover_rate_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "trde_qty_tp": "0",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_turnover_rate_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_consecutive_rise_fall_rank_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "0",
    },
    "get_consecutive_rise_fall_rank_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "0",
    },
    "get_consecutive_rise_fall_rank_watchlist": {
        "stex_tp": "1",
        "stk_cd": [{"stex_tp": "ND", "stk_cd": "AAPL"}],
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "0",
    },
    "get_quote_remaining_volume_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "sort_tp": "1",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_quote_remaining_volume_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "sort_tp": "1",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_daytime_trading_disparity_top_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "inds_cls_tp": "0",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "0",
    },
    "get_daytime_trading_disparity_top_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
        "sort_tp": "0",
    },
}

# All body parameters are supplied in ``CALL_KWARGS`` and the request body is a
# 1:1 copy of those values (including the ``stk_cd`` watchlist Map list), so the
# expected body equals the call kwargs for every endpoint.
EXPECTED_BODY: dict[str, dict] = {}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasRankInfo, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (OverseasRankInfo\w+)\.model_validate", source).group(1)
    return api_id, model_attr


RANK_INFO_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    RANK_INFO_CASES.append(
        EndpointCase(
            name=case_name,
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(kwargs),
            expected_body=dict(EXPECTED_BODY.get(method_name, kwargs)),
            response_payload=payload(case_name),
        )
    )


@pytest.mark.parametrize("case", RANK_INFO_CASES, ids=lambda case: case.name)
def test_overseas_rank_info_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_rank_info_module,
        OverseasRankInfo,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
