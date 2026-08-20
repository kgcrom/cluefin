import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_stock_info as overseas_stock_info_module
from cluefin_openapi.kiwoom._overseas_stock_info import OverseasStockInfo

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_exchange_list": {"stk_cd": "AAPL"},
    "get_stock_list": {"stex_tp": "ND"},
    "get_stock": {"stk_cd": "AAPL", "stex_tp": "ND"},
    "get_stock_memo": {"input_list": [{"stex_tp": "ND", "stk_cd": "AAPL"}]},
    "get_sector_list": {"gubun": "%"},
    "get_index_list": {"index_qry_tp": "NQ"},
    "get_etf_etn_list": {"stex_tp": "ND"},
    "get_etf_category_list": {"gubun": "1"},
    "get_volume_surge_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "tm": "5",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_volume_surge_etf": {
        "stex_tp": "1",
        "tm": "5",
        "etf_cat1": "",
        "etf_cat2": "",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_price_by_range_stock": {
        "stex_tp": "1",
        "stk_tp": "0",
        "stk_cnd": "0",
        "inds_cd": "000",
        "trde_qty_tp": "0",
        "pric_cnd1": "",
        "pric_cnd2": "",
        "trde_prica_cnd": "0",
    },
    "get_price_by_range_etf": {
        "stex_tp": "1",
        "stk_cnd": "0",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "pric_cnd1": "",
        "pric_cnd2": "",
        "trde_prica_cnd": "0",
    },
    "get_price_surge_stock": {
        "stex_tp": "1",
        "stk_tp": "0",
        "inds_cd": "000",
        "stk_cnd": "0",
        "flu_tp": "1",
        "tm_tp": "1",
        "tm": "5",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
    },
    "get_price_surge_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "stk_cnd": "0",
        "flu_tp": "1",
        "tm_tp": "1",
        "tm": "5",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
    },
    "get_price_surge_watchlist": {
        "stex_tp": "1",
        "stk_cd": [{"stex_tp": "ND", "stk_cd": "AAPL"}],
        "flu_tp": "1",
        "tm_tp": "1",
        "tm": "5",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
    },
    "get_high_low_approach_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "high_low_tp": "1",
        "alacc_rt": "0.5",
        "stk_cnd": "0",
        "pric_cnd_st": "0",
        "pric_cnd_ed": "0",
        "trde_pric_cnd_st": "0",
        "trde_qty_cnd_fr": "0",
    },
    "get_high_low_approach_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "high_low_tp": "1",
        "alacc_rt": "0.5",
        "stk_cnd": "0",
        "pric_cnd_st": "0",
        "pric_cnd_ed": "0",
        "trde_pric_cnd_st": "0",
        "trde_qty_cnd_fr": "0",
    },
    "get_high_low_approach_watchlist": {
        "stex_tp": "1",
        "stk_cd": [{"stex_tp": "ND", "stk_cd": "AAPL"}],
        "high_low_tp": "1",
        "alacc_rt": "0.5",
        "stk_cnd": "0",
        "pric_cnd_st": "0",
        "pric_cnd_ed": "0",
        "trde_pric_cnd_st": "0",
        "trde_qty_cnd_fr": "0",
    },
    "get_volume_renewal_stock": {
        "stex_tp": "1",
        "stk_cd": "000",
        "trde_qty_tp": "0",
        "stk_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "dt_tp": "5",
    },
    "get_volume_renewal_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "dt_tp": "5",
    },
    "get_volume_renewal_watchlist": {
        "stex_tp": "1",
        "stk_cd": [{"stex_tp": "ND", "stk_cd": "AAPL"}],
        "trde_qty_tp": "0",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "dt_tp": "5",
    },
    "get_new_high_low_stock": {
        "stex_tp": "1",
        "stk_tp": "0",
        "inds_cd": "000",
        "stk_cnd": "0",
        "ntl_tp": "1",
        "high_low_tp": "1",
        "dt": "20",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
    },
    "get_new_high_low_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "stk_cnd": "0",
        "ntl_tp": "1",
        "high_low_tp": "1",
        "dt": "20",
        "pric_cnd": "0",
        "trde_qty_tp": "0",
        "trde_prica_cnd": "0",
    },
    "get_gap_up_down_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "sort_tp": "1",
        "updown_tp": "1",
        "alacc_rt": "3",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_gap_up_down_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "sort_tp": "1",
        "updown_tp": "1",
        "alacc_rt": "3",
        "stk_cnd": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
        "trde_qty_tp": "0",
    },
    "get_remaining_ratio_surge_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "rt_tp": "0",
        "stk_tp": "0",
        "tm": "5",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_remaining_ratio_surge_etf": {
        "stex_tp": "1",
        "rt_tp": "0",
        "etf_cat1": "",
        "etf_cat2": "",
        "tm": "5",
        "stk_cnd": "0",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_volume_concentration_stock": {
        "stex_tp": "1",
        "inds_cd": "000",
        "stk_tp": "0",
        "dt": "20",
        "prps_cnctr_rt": "50",
        "cond": "0",
        "prpscnt": "10",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_volume_concentration_etf": {
        "stex_tp": "1",
        "etf_cat1": "",
        "etf_cat2": "",
        "dt": "20",
        "prps_cnctr_rt": "50",
        "cond": "0",
        "prpscnt": "10",
        "trde_qty_tp": "0",
        "pric_cnd": "0",
        "trde_prica_cnd": "0",
    },
    "get_yearly_fluctuation_rate_stock": {"stex_tp": "ND", "stk_cd": "AAPL"},
    "get_yearly_fluctuation_rate_by_sector": {"inds_cd": "000", "srch_yr": "2024"},
    "get_yearly_fluctuation_rate_by_etf_category": {
        "etf_cat1": "",
        "etf_cat2": "",
        "srch_yr": "2024",
    },
    "get_yearly_fluctuation_rate_sector": {"inds_cd": "000"},
    "get_yearly_fluctuation_rate_etf": {"etf_cat1": "", "etf_cat2": ""},
}

# All body parameters are supplied in ``CALL_KWARGS`` and the request body is a
# 1:1 copy of those values (including the ``stk_cd`` watchlist Map list, which is
# emitted verbatim when not ``None``), so the expected body equals the call kwargs
# for every endpoint.
EXPECTED_BODY: dict[str, dict] = {}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasStockInfo, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (OverseasStockInfo\w+)\.model_validate", source).group(1)
    return api_id, model_attr


STOCK_INFO_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    STOCK_INFO_CASES.append(
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


@pytest.mark.parametrize("case", STOCK_INFO_CASES, ids=lambda case: case.name)
def test_overseas_stock_info_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_stock_info_module,
        OverseasStockInfo,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
