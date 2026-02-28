from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_output, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# kis.ranking.trading_volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.trading_volume",
    description="Get trading volume ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {"type": "string", "description": "Sector code. 0000 for all."},
            "classification": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "0:all, 1:common, 2:preferred",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4"],
                "description": "Sort criterion",
            },
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_trading_volume_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_trading_volume_rank(
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20171",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_blng_cls_code=params.get("sort_by", "0"),
        fid_trgt_cls_code=params.get("target_cls", "111111111"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0000000000"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_input_date_1=params.get("date", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.stock_fluctuation
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.stock_fluctuation",
    description="Get stock fluctuation (rise/decline rate) ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4"],
                "description": "0:rise-rate, 1:decline-rate, 2:open-rise, 3:open-decline, 4:volatility",
            },
            "days": {"type": "string", "description": "Accumulation days (0:all)"},
            "price_cls_code": {
                "type": "string",
                "description": "Price cls (rise:0=low-based/1=close-based, decline:0=high-based/1=close-based)",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
            "fluctuation_rate_min": {"type": "string", "description": "Min fluctuation rate"},
            "fluctuation_rate_max": {"type": "string", "description": "Max fluctuation rate"},
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_stock_fluctuation_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_fluctuation_rank(
        fid_rsfl_rate2=params.get("fluctuation_rate_max", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20170",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_rank_sort_cls_code=params.get("sort_by", "0"),
        fid_input_cnt_1=params.get("days", "0"),
        fid_prc_cls_code=params.get("price_cls_code", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_rsfl_rate1=params.get("fluctuation_rate_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.hoga_quantity
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.hoga_quantity",
    description="Get hoga (order book) quantity ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "0:net-buy-balance, 1:net-sell-balance, 2:buy-ratio, 3:sell-ratio",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_hoga_quantity_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_hoga_quantity_rank(
        fid_vol_cnt=params.get("volume_min", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20172",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_rank_sort_cls_code=params.get("sort_by", "0"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.profitability_indicator
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.profitability_indicator",
    description="Get profitability/asset indicator ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "fiscal_year": {"type": "string", "description": "Fiscal year (e.g. 2023)"},
            "quarter": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "0:Q1, 1:H1, 2:Q3, 3:annual",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "5", "6"],
                "description": "0:sales, 1:operating, 2:ordinary, 3:net-income, 4:total-assets, 5:total-debt, 6:total-equity",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
        },
        "required": ["market", "fiscal_year", "quarter", "sort_by"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_profitability_indicator_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_profitability_indicator_rank(
        fid_cond_mrkt_div_code=params["market"],
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_cond_scr_div_code="20173",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_input_option_1=params["fiscal_year"],
        fid_input_option_2=params["quarter"],
        fid_rank_sort_cls_code=params["sort_by"],
        fid_blng_cls_code=params.get("belong_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.market_cap
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.market_cap",
    description="Get market cap top ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "classification": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "0:all, 1:common, 2:preferred",
            },
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_market_cap_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_market_cap_top(
        fid_input_price_2=params.get("price_max", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20174",
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_vol_cnt=params.get("volume_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.finance_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.finance_ratio",
    description="Get finance ratio ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "fiscal_year": {"type": "string", "description": "Fiscal year (e.g. 2023)"},
            "quarter": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "0:Q1, 1:H1, 2:Q3, 3:annual",
            },
            "sort_by": {
                "type": "string",
                "description": "7:profitability, 11:stability, 15:growth, 20:activity",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
        },
        "required": ["market", "fiscal_year", "quarter", "sort_by"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_finance_ratio_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_finance_ratio_rank(
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20175",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_input_option_1=params["fiscal_year"],
        fid_input_option_2=params["quarter"],
        fid_rank_sort_cls_code=params["sort_by"],
        fid_blng_cls_code=params.get("belong_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.time_hoga
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.time_hoga",
    description="Get after-hours hoga (order book balance) ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["1", "2", "3", "4"],
                "description": "1:pre-market, 2:post-market, 3:sell-balance, 4:buy-balance",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
        },
        "required": ["market", "sort_by"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_time_hoga_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_time_hoga_rank(
        fid_input_price_1=params.get("price_min", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20176",
        fid_rank_sort_cls_code=params["sort_by"],
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_input_price_2=params.get("price_max", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.preferred_stock_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.preferred_stock_ratio",
    description="Get preferred stock / disparity ratio top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_preferred_stock_ratio_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_preferred_stock_ratio_top(
        fid_vol_cnt=params.get("volume_min", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20177",
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.disparity_index
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.disparity_index",
    description="Get disparity index ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:disparity-top, 1:disparity-bottom",
            },
            "disparity_period": {
                "type": "string",
                "enum": ["5", "10", "20", "60", "120"],
                "description": "Disparity period (5/10/20/60/120 day)",
            },
            "classification": {
                "type": "string",
                "description": "0:all, 1:managed, 2:caution, 3:warning, 4:risk-alert, 5:risk, 6:common, 7:preferred",
            },
        },
        "required": ["market", "sort_by", "disparity_period"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_disparity_index_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_disparity_index_rank(
        fid_input_price_2=params.get("price_max", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20178",
        fid_div_cls_code=params.get("classification", "0"),
        fid_rank_sort_cls_code=params["sort_by"],
        fid_hour_cls_code=params["disparity_period"],
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_vol_cnt=params.get("volume_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.market_price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.market_price",
    description="Get market value ranking (PER/PBR/PCR/PSR/EPS etc.) from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "fiscal_year": {"type": "string", "description": "Fiscal year (e.g. 2023)"},
            "quarter": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "0:Q1, 1:H1, 2:Q3, 3:annual",
            },
            "sort_by": {
                "type": "string",
                "description": "23:PER, 24:PBR, 25:PCR, 26:PSR, 27:EPS, 28:EVA, 29:EBITDA, 30:EV/EBITDA, 31:EBITDA/finance",
            },
            "classification": {
                "type": "string",
                "description": "0:all, 1:managed, 2:caution, 3:warning, 4:risk-alert, 5:risk, 6:common, 7:preferred",
            },
        },
        "required": ["market", "fiscal_year", "quarter", "sort_by"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_market_price_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_market_price_rank(
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20179",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_input_option_1=params["fiscal_year"],
        fid_input_option_2=params["quarter"],
        fid_rank_sort_cls_code=params["sort_by"],
        fid_blng_cls_code=params.get("belong_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.execution_strength
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.execution_strength",
    description="Get execution strength top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "classification": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "0:all, 1:common, 2:preferred",
            },
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_execution_strength_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_execution_strength_top(
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20168",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_trgt_cls_code=params.get("target_cls", "0"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.watchlist_registration
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.watchlist_registration",
    description="Get watchlist registration top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "classification": {
                "type": "string",
                "description": "0:all, 1:managed, 2:caution, 3:warning, 4:risk-alert, 5:risk, 6:common, 7:preferred",
            },
            "rank_start": {"type": "string", "description": "Rank start position (1:from 1st, 10:from 10th)"},
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_watchlist_registration_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_watchlist_registration_top(
        fid_input_iscd_2="000000",
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20180",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_cnt_1=params.get("rank_start", "1"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.expected_execution_rise_decline
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.expected_execution_rise_decline",
    description="Get expected execution rise/decline top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "5", "6"],
                "description": "0:rise-rate, 1:rise-amount, 2:flat, 3:decline-rate, 4:decline-amount, 5:volume, 6:trade-amount",
            },
            "classification": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "0:all, 1:common, 2:preferred",
            },
            "market_operation_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:pre-market, 1:post-market",
            },
        },
        "required": ["market", "sort_by"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_expected_execution_rise_decline_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_expected_execution_rise_decline_top(
        fid_rank_sort_cls_code=params["sort_by"],
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20182",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_aply_rang_prc_1=params.get("price_min", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_pbmn=params.get("trade_amount_min", ""),
        fid_blng_cls_code=params.get("belong_cls", "0"),
        fid_mkop_cls_code=params.get("market_operation_code", "0"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.proprietary_trading
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.proprietary_trading",
    description="Get proprietary (company) trading top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:sell-top, 1:buy-top",
            },
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "classification": {
                "type": "string",
                "description": "0:all, 1:managed, 2:caution, 3:warning, 4:risk-alert, 5:risk, 6:common, 7:preferred",
            },
        },
        "required": ["market", "sort_by", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_proprietary_trading_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_proprietary_trading_top(
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20186",
        fid_div_cls_code=params.get("classification", "0"),
        fid_rank_sort_cls_code=params["sort_by"],
        fid_input_date_1=params["start_date"],
        fid_input_date_2=params["end_date"],
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_aply_rang_vol=params.get("volume_min", "0"),
        fid_aply_rang_prc_2=params.get("price_max", ""),
        fid_aply_rang_prc_1=params.get("price_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.new_high_low_approaching
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.new_high_low_approaching",
    description="Get new high/low approaching stocks top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100)",
            },
            "price_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:new-high-near, 1:new-low-near",
            },
            "classification": {
                "type": "string",
                "description": "0:all, 1:managed, 2:caution, 3:warning",
            },
            "disparity_min": {"type": "string", "description": "Min disparity rate"},
            "disparity_max": {"type": "string", "description": "Max disparity rate"},
        },
        "required": ["market", "price_cls_code"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_new_high_low_approaching_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_new_high_low_approaching_top(
        fid_aply_rang_vol=params.get("volume_min", "0"),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20187",
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_cnt_1=params.get("disparity_min", ""),
        fid_input_cnt_2=params.get("disparity_max", ""),
        fid_prc_cls_code=params["price_cls_code"],
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_aply_rang_prc_1=params.get("price_min", ""),
        fid_aply_rang_prc_2=params.get("price_max", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.dividend_yield
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.dividend_yield",
    description="Get dividend yield top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "0:all, 1:KOSPI, 2:KOSPI200, 3:KOSDAQ",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (KOSPI:0001~0027, KOSDAQ:1001~1041, KOSPI200:2001/2007/2008)",
            },
            "stock_type": {
                "type": "string",
                "enum": ["0", "6", "7"],
                "description": "0:all, 6:common, 7:preferred",
            },
            "dividend_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "1:stock-dividend, 2:cash-dividend",
            },
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "settlement_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "0:all, 1:annual-dividend, 2:interim-dividend",
            },
        },
        "required": ["market_type", "sector_code", "dividend_type", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_dividend_yield_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_dividend_yield_top(
        cts_area="",
        gb1=params["market_type"],
        upjong=params["sector_code"],
        gb2=params.get("stock_type", "0"),
        gb3=params["dividend_type"],
        f_dt=params["start_date"],
        t_dt=params["end_date"],
        gb4=params.get("settlement_type", "0"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.large_execution_count
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.large_execution_count",
    description="Get large execution count top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:buy-top, 1:sell-top",
            },
            "classification": {"type": "string", "description": "Classification code (0:all)"},
            "amount_per_trade": {"type": "string", "description": "Amount per trade filter"},
            "stock_code_filter": {"type": "string", "description": "Stock code filter (empty for all)"},
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_large_execution_count_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_large_execution_count_top(
        fid_aply_rang_prc_2=params.get("price_max", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="11909",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_rank_sort_cls_code=params.get("sort_by", "0"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_price_1=params.get("amount_per_trade", ""),
        fid_aply_rang_prc_1=params.get("price_min", ""),
        fid_input_iscd_2=params.get("stock_code_filter", ""),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0"),
        fid_trgt_cls_code=params.get("target_cls", "0"),
        fid_vol_cnt=params.get("volume_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.credit_balance
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.credit_balance",
    description="Get credit balance top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:exchange, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "sort_by": {
                "type": "string",
                "description": "Loan: 0:balance-ratio, 1:balance-qty, 2:balance-amount, 3:ratio-increase, 4:ratio-decrease. "
                "Borrow: 5:balance-ratio, 6:balance-qty, 7:balance-amount, 8:ratio-increase, 9:ratio-decrease",
            },
            "increase_rate_period": {
                "type": "string",
                "description": "Increase rate period in days (2~999)",
            },
        },
        "required": ["market", "sort_by", "increase_rate_period"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_credit_balance_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_credit_balance_top(
        fid_cond_scr_div_code="11701",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_option=params["increase_rate_period"],
        fid_cond_mrkt_div_code=params["market"],
        fid_rank_sort_cls_code=params["sort_by"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.short_selling
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.short_selling",
    description="Get short selling top from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100, 3003:KOSDAQ150)",
            },
            "period_type": {
                "type": "string",
                "enum": ["D", "M"],
                "description": "D:daily, M:monthly",
            },
            "period_days": {
                "type": "string",
                "description": "Period days (D:0~14, M:1~3). D-0:1day, D-4:1week, D-9:2weeks, D-14:3weeks. M-1:1month, M-2:2months, M-3:3months",
            },
        },
        "required": ["market", "period_type", "period_days"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_short_selling_top(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_short_selling_top(
        fid_aply_rang_vol=params.get("volume_min", ""),
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20482",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_period_div_code=params["period_type"],
        fid_input_cnt_1=params["period_days"],
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", ""),
        fid_trgt_cls_code=params.get("target_cls", ""),
        fid_aply_rang_prc_1=params.get("price_min", ""),
        fid_aply_rang_prc_2=params.get("price_max", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.after_hours_fluctuation
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.after_hours_fluctuation",
    description="Get after-hours fluctuation ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ)",
            },
            "classification": {
                "type": "string",
                "enum": ["1", "2", "3", "4", "5"],
                "description": "1:upper-limit, 2:rise-rate, 3:flat, 4:lower-limit, 5:decline-rate",
            },
        },
        "required": ["market", "classification"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_after_hours_fluctuation_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_after_hours_fluctuation_rank(
        fid_cond_mrkt_div_code=params["market"],
        fid_mrkt_cls_code="",
        fid_cond_scr_div_code="20234",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params["classification"],
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_trgt_cls_code=params.get("target_cls", ""),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.after_hours_volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.after_hours_volume",
    description="Get after-hours volume ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "0:buy-balance, 1:sell-balance, 2:volume",
            },
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_after_hours_volume_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_stock_after_hours_volume_rank(
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20235",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_rank_sort_cls_code=params.get("sort_by", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_trgt_cls_code=params.get("target_cls", ""),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.ranking.hts_inquiry_top_20
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.ranking.hts_inquiry_top_20",
    description="Get HTS inquiry top 20 stocks from KIS.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_hts_inquiry_top_20(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_hts_inquiry_top_20()
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kis_trading_volume_rank,
    handle_kis_stock_fluctuation_rank,
    handle_kis_hoga_quantity_rank,
    handle_kis_profitability_indicator_rank,
    handle_kis_market_cap_top,
    handle_kis_finance_ratio_rank,
    handle_kis_time_hoga_rank,
    handle_kis_preferred_stock_ratio_top,
    handle_kis_disparity_index_rank,
    handle_kis_market_price_rank,
    handle_kis_execution_strength_top,
    handle_kis_watchlist_registration_top,
    handle_kis_expected_execution_rise_decline_top,
    handle_kis_proprietary_trading_top,
    handle_kis_new_high_low_approaching_top,
    handle_kis_dividend_yield_top,
    handle_kis_large_execution_count_top,
    handle_kis_credit_balance_top,
    handle_kis_short_selling_top,
    handle_kis_after_hours_fluctuation_rank,
    handle_kis_after_hours_volume_rank,
    handle_kis_hts_inquiry_top_20,
]


def register_kis_ranking_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
