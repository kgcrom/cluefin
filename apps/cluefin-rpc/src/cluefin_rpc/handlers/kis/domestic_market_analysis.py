from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_output, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# kis.market_analysis.condition_search_list
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.condition_search_list",
    description="Get condition search list from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "HTS user ID"},
        },
        "required": ["user_id"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_condition_search_list(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_condition_search_list(
        user_id=params["user_id"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.condition_search_result
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.condition_search_result",
    description="Get condition search result from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "HTS user ID"},
            "seq": {"type": "string", "description": "Condition sequence key (from condition_search_list output)"},
        },
        "required": ["user_id", "seq"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_condition_search_result(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_condition_search_result(
        user_id=params["user_id"],
        seq=params["seq"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.watchlist_groups
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.watchlist_groups",
    description="Get watchlist groups from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "HTS user ID"},
            "interest_type": {"type": "string", "description": "Interest type code (default 1)"},
            "etc_cls_code": {"type": "string", "description": "FID etc classification code (default 00)"},
        },
        "required": ["user_id"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_watchlist_groups(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_watchlist_groups(
        interest_type=params.get("interest_type", "1"),
        fid_etc_cls_code=params.get("etc_cls_code", "00"),
        user_id=params["user_id"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.watchlist_multi_quote
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.watchlist_multi_quote",
    description="Get multi-stock watchlist quotes from KIS (up to 30 stocks).",
    parameters={
        "type": "object",
        "properties": {
            "stocks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "market": {"type": "string", "description": "Market code (J/NX/UN)"},
                        "stock_code": {"type": "string", "description": "6-digit stock code"},
                    },
                    "required": ["market", "stock_code"],
                },
                "description": "List of stocks (max 30). Each has market and stock_code.",
                "maxItems": 30,
            },
        },
        "required": ["stocks"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_watchlist_multi_quote(params: dict, session) -> dict:
    kis = session.get_kis()
    stocks = params["stocks"]
    kwargs = {}
    for i in range(1, 31):
        if i <= len(stocks):
            kwargs[f"fid_cond_mrkt_div_code_{i}"] = stocks[i - 1]["market"]
            kwargs[f"fid_input_iscd_{i}"] = stocks[i - 1]["stock_code"]
        else:
            kwargs[f"fid_cond_mrkt_div_code_{i}"] = ""
            kwargs[f"fid_input_iscd_{i}"] = ""
    response = kis.domestic_market_analysis.get_watchlist_multi_quote(**kwargs)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.watchlist_stocks_by_group
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.watchlist_stocks_by_group",
    description="Get stocks in a watchlist group from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "HTS user ID"},
            "group_code": {"type": "string", "description": "Interest group code (from watchlist_groups)"},
            "interest_type": {"type": "string", "description": "Interest type code (default 1)"},
            "etc_cls_code": {"type": "string", "description": "FID etc classification code (default 4)"},
        },
        "required": ["user_id", "group_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_watchlist_stocks_by_group(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_watchlist_stocks_by_group(
        type=params.get("interest_type", "1"),
        user_id=params["user_id"],
        data_rank="",
        inter_grp_code=params["group_code"],
        inter_grp_name="",
        hts_kor_isnm="",
        cntg_cls_code="",
        fid_etc_cls_code=params.get("etc_cls_code", "4"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.institutional_foreign_aggregate
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.institutional_foreign_aggregate",
    description="Get institutional/foreign trading aggregate from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "HTS user ID"},
            "group_code": {"type": "string", "description": "Interest group code"},
            "interest_type": {"type": "string", "description": "Interest type code (default 1)"},
            "etc_cls_code": {"type": "string", "description": "FID etc classification code (default 4)"},
        },
        "required": ["user_id", "group_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_institutional_foreign_aggregate(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_institutional_foreign_trading_aggregate(
        type=params.get("interest_type", "1"),
        user_id=params["user_id"],
        data_rank="",
        inter_grp_code=params["group_code"],
        inter_grp_name="",
        hts_kor_isnm="",
        cntg_cls_code="",
        fid_etc_cls_code=params.get("etc_cls_code", "4"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.foreign_brokerage_aggregate
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.foreign_brokerage_aggregate",
    description="Get foreign brokerage trading aggregate from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:net-buy-top, 1:net-sell-top",
            },
            "sort_by_2": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:buy-order, 1:sell-order",
            },
        },
        "required": ["sector_code", "sort_by", "sort_by_2"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_foreign_brokerage_aggregate(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_foreign_brokerage_trading_aggregate(
        fid_input_iscd=params["sector_code"],
        fid_rank_sort_cls_code=params["sort_by"],
        fid_rank_sort_cls_code_2=params["sort_by_2"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.investor_trend_by_stock_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.investor_trend_by_stock_daily",
    description="Get daily investor trading trend by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "market": {"type": "string", "enum": ["J", "NX", "UN"], "description": "Market code. Default J."},
        },
        "required": ["stock_code", "date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_investor_trend_by_stock_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_investor_trading_trend_by_stock_daily(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
        fid_input_date_1=params["date"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.investor_trend_by_market_intraday
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.investor_trend_by_market_intraday",
    description="Get intraday investor trading trend by market from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market_code": {
                "type": "string",
                "description": "Market code (KSP:KOSPI, KSQ:KOSDAQ, ETF, ELW, ETN, etc.)",
            },
            "sector_code": {
                "type": "string",
                "description": "Sub-sector code (e.g. 0001:composite)",
            },
        },
        "required": ["market_code", "sector_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_investor_trend_by_market_intraday(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_investor_trading_trend_by_market_intraday(
        fid_input_iscd=params["market_code"],
        fid_input_iscd_2=params["sector_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.investor_trend_by_market_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.investor_trend_by_market_daily",
    description="Get daily investor trading trend by market from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {
                "type": "string",
                "description": "Market classification code (U:sector)",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector classification code (KOSPI/KOSDAQ sub-codes)",
            },
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "market_code": {
                "type": "string",
                "description": "Market code (KSP:KOSPI, KSQ:KOSDAQ)",
            },
            "end_date": {"type": "string", "description": "End date (same as start_date)"},
            "sub_sector_code": {
                "type": "string",
                "description": "Sub-sector classification code",
            },
        },
        "required": ["market", "sector_code", "start_date", "market_code", "end_date", "sub_sector_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_investor_trend_by_market_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_investor_trading_trend_by_market_daily(
        fid_cond_mrkt_div_code=params["market"],
        fid_input_iscd=params["sector_code"],
        fid_input_date_1=params["start_date"],
        fid_input_iscd_1=params["market_code"],
        fid_input_date_2=params["end_date"],
        fid_input_iscd_2=params["sub_sector_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.foreign_net_buy_trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.foreign_net_buy_trend",
    description="Get foreign net buy trend by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "brokerage_code": {
                "type": "string",
                "description": "Brokerage code (99999 for all foreign)",
            },
            "market": {"type": "string", "enum": ["J"], "description": "Market code (J only). Default J."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_foreign_net_buy_trend(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_foreign_net_buy_trend_by_stock(
        fid_input_iscd=params["stock_code"],
        fid_input_iscd_2=params.get("brokerage_code", "99999"),
        fid_cond_mrkt_div_code=params.get("market", "J"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.member_trend_tick
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.member_trend_tick",
    description="Get member trading trend tick from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (use stock_code or market_cls_code, not both)",
            },
            "brokerage_code": {
                "type": "string",
                "description": "Member/brokerage code (99999 for all)",
            },
            "market_cls_code": {
                "type": "string",
                "description": "Market cls code (A:all, K:KOSPI, Q:KOSDAQ, K2:KOSPI200, W:ELW)",
            },
            "volume_min": {"type": "string", "description": "Minimum volume filter"},
            "market": {"type": "string", "description": "Market code. Default J."},
        },
        "required": [],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_member_trend_tick(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_member_trading_trend_tick(
        fid_cond_scr_div_code="20432",
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params.get("stock_code", ""),
        fid_input_iscd_2=params.get("brokerage_code", "99999"),
        fid_mrkt_cls_code=params.get("market_cls_code", ""),
        fid_vol_cnt=params.get("volume_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.member_trend_by_stock
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.member_trend_by_stock",
    description="Get member trading trend by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "brokerage_code": {"type": "string", "description": "Member/brokerage code"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
        },
        "required": ["stock_code", "brokerage_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_member_trend_by_stock(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_member_trading_trend_by_stock(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
        fid_input_iscd_2=params["brokerage_code"],
        fid_input_date_1=params["start_date"],
        fid_input_date_2=params["end_date"],
        fid_sctn_cls_code="",
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.program_trend_by_stock_intraday
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.program_trend_by_stock_intraday",
    description="Get intraday program trading trend by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_program_trend_by_stock_intraday(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_program_trading_trend_by_stock_intraday(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.program_trend_by_stock_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.program_trend_by_stock_daily",
    description="Get daily program trading trend by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "date": {
                "type": "string",
                "description": "Base date (YYYYMMDD with leading 00, e.g. 0020240308). Empty for today.",
            },
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_program_trend_by_stock_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_program_trading_trend_by_stock_daily(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
        fid_input_date_1=params.get("date", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.foreign_institutional_estimate
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.foreign_institutional_estimate",
    description="Get foreign/institutional estimate by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_foreign_institutional_estimate(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_foreign_institutional_estimate_by_stock(
        mksc_shrn_iscd=params["stock_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.buy_sell_volume_by_stock_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.buy_sell_volume_by_stock_daily",
    description="Get daily buy/sell volume by stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "period": {"type": "string", "description": "Period code (D). Default D."},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_buy_sell_volume_by_stock_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_buy_sell_volume_by_stock_daily(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
        fid_input_date_1=params["start_date"],
        fid_input_date_2=params["end_date"],
        fid_period_div_code=params.get("period", "D"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.program_summary_intraday
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.program_summary_intraday",
    description="Get intraday program trading summary from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market_cls_code": {
                "type": "string",
                "enum": ["K", "Q"],
                "description": "K:KOSPI, Q:KOSDAQ",
            },
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
            "hour": {"type": "string", "description": "Hour filter (empty for all)"},
        },
        "required": ["market_cls_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_program_summary_intraday(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_program_trading_summary_intraday(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_mrkt_cls_code=params["market_cls_code"],
        fid_sctn_cls_code="",
        fid_input_iscd="",
        fid_cond_mrkt_div_code1="",
        fid_input_hour_1=params.get("hour", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.program_summary_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.program_summary_daily",
    description="Get daily program trading summary from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market_cls_code": {
                "type": "string",
                "enum": ["K", "Q"],
                "description": "K:KOSPI, Q:KOSDAQ",
            },
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD, empty for default)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD, empty for default)"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
        },
        "required": ["market_cls_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_program_summary_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_program_trading_summary_daily(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_mrkt_cls_code=params["market_cls_code"],
        fid_input_date_1=params.get("start_date", ""),
        fid_input_date_2=params.get("end_date", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.program_investor_trend_today
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.program_investor_trend_today",
    description="Get today's program trading investor trend from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "exchange_code": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Exchange code (J:KRX, NX:NXT, UN:Combined)",
            },
            "market_code": {
                "type": "string",
                "enum": ["1", "4"],
                "description": "1:KOSPI, 4:KOSDAQ",
            },
        },
        "required": ["exchange_code", "market_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_program_investor_trend_today(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_program_trading_investor_trend_today(
        exch_div_cls_code=params["exchange_code"],
        mrkt_div_cls_code=params["market_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.credit_balance_trend_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.credit_balance_trend_daily",
    description="Get daily credit balance trend from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "date": {"type": "string", "description": "Settlement date (YYYYMMDD)"},
            "market": {"type": "string", "description": "Market code. Default J."},
        },
        "required": ["stock_code", "date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_credit_balance_trend_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_credit_balance_trend_daily(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_cond_scr_div_code="20476",
        fid_input_iscd=params["stock_code"],
        fid_input_date_1=params["date"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.expected_price_trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.expected_price_trend",
    description="Get expected price trend from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market_operation_code": {
                "type": "string",
                "enum": ["0", "4"],
                "description": "0:all, 4:exclude zero volume",
            },
            "market": {"type": "string", "description": "Market code. Default J."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_expected_price_trend(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_expected_price_trend(
        fid_mkop_cls_code=params.get("market_operation_code", "0"),
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.short_selling_trend_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.short_selling_trend_daily",
    description="Get daily short selling trend from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD, empty for all)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "market": {"type": "string", "description": "Market code. Default J."},
        },
        "required": ["stock_code", "end_date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_short_selling_trend_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_short_selling_trend_daily(
        fid_input_date_2=params["end_date"],
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
        fid_input_date_1=params.get("start_date", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.after_hours_expected_fluctuation
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.after_hours_expected_fluctuation",
    description="Get after-hours expected fluctuation from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ)",
            },
            "sort_by": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4"],
                "description": "0:rise-rate, 1:rise-amount, 2:flat, 3:decline-rate, 4:decline-amount",
            },
            "classification": {
                "type": "string",
                "description": "Classification code (0:all, 1~7). Default 0.",
            },
            "price_min": {"type": "string", "description": "Min price filter"},
            "price_max": {"type": "string", "description": "Max price filter"},
            "volume_min": {"type": "string", "description": "Min volume filter"},
            "market": {"type": "string", "description": "Market code. Default J."},
        },
        "required": ["sector_code", "sort_by"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_after_hours_expected_fluctuation(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_after_hours_expected_fluctuation(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_cond_scr_div_code="11186",
        fid_input_iscd=params["sector_code"],
        fid_rank_sort_cls_code=params["sort_by"],
        fid_div_cls_code=params.get("classification", "0"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_input_vol_1=params.get("volume_min", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.trading_weight_by_amount
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.trading_weight_by_amount",
    description="Get trading weight by execution amount from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_trading_weight_by_amount(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_trading_weight_by_amount(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_cond_scr_div_code="11119",
        fid_input_iscd=params["stock_code"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.market_fund_summary
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.market_fund_summary",
    description="Get market fund summary from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
        },
        "required": ["date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_market_fund_summary(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_market_fund_summary(
        fid_input_date_1=params["date"],
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.stock_loan_trend_daily
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.stock_loan_trend_daily",
    description="Get daily stock loan trend from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market_div_code": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "1:KOSPI, 2:KOSDAQ, 3:by stock",
            },
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "cts": {"type": "string", "description": "Continuation key for pagination"},
        },
        "required": ["market_div_code", "stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_stock_loan_trend_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_stock_loan_trend_daily(
        mrkt_div_cls_code=params["market_div_code"],
        mksc_shrn_iscd=params["stock_code"],
        start_date=params["start_date"],
        end_date=params["end_date"],
        cts=params.get("cts", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.limit_price_stocks
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.limit_price_stocks",
    description="Get limit price (upper/lower) stocks from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "price_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "0:upper-limit, 1:lower-limit",
            },
            "classification": {
                "type": "string",
                "description": "0:limit-stocks, 6:8%-near, 5:10%-near, 1:15%-near, 2:20%-near, 3:25%-near",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ)",
            },
            "market": {"type": "string", "description": "Market code. Default J."},
        },
        "required": ["price_cls_code", "classification", "sector_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_limit_price_stocks(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_limit_price_stocks(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_cond_scr_div_code="11300",
        fid_prc_cls_code=params["price_cls_code"],
        fid_div_cls_code=params["classification"],
        fid_input_iscd=params["sector_code"],
        fid_trgt_cls_code="",
        fid_trgt_exls_cls_code="",
        fid_input_price_1="",
        fid_input_price_2="",
        fid_vol_cnt="",
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.market_analysis.resistance_level_trading_weight
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.market_analysis.resistance_level_trading_weight",
    description="Get resistance level / trading weight from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
            "hour": {"type": "string", "description": "Hour filter (empty for all)"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.market_analysis",
    broker="kis",
)
def handle_kis_resistance_level_trading_weight(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_market_analysis.get_resistance_level_trading_weight(
        fid_cond_mrkt_div_code=params.get("market", "J"),
        fid_input_iscd=params["stock_code"],
        fid_cond_scr_div_code="20113",
        fid_input_hour_1=params.get("hour", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kis_condition_search_list,
    handle_kis_condition_search_result,
    handle_kis_watchlist_groups,
    handle_kis_watchlist_multi_quote,
    handle_kis_watchlist_stocks_by_group,
    handle_kis_institutional_foreign_aggregate,
    handle_kis_foreign_brokerage_aggregate,
    handle_kis_investor_trend_by_stock_daily,
    handle_kis_investor_trend_by_market_intraday,
    handle_kis_investor_trend_by_market_daily,
    handle_kis_foreign_net_buy_trend,
    handle_kis_member_trend_tick,
    handle_kis_member_trend_by_stock,
    handle_kis_program_trend_by_stock_intraday,
    handle_kis_program_trend_by_stock_daily,
    handle_kis_foreign_institutional_estimate,
    handle_kis_buy_sell_volume_by_stock_daily,
    handle_kis_program_summary_intraday,
    handle_kis_program_summary_daily,
    handle_kis_program_investor_trend_today,
    handle_kis_credit_balance_trend_daily,
    handle_kis_expected_price_trend,
    handle_kis_short_selling_trend_daily,
    handle_kis_after_hours_expected_fluctuation,
    handle_kis_trading_weight_by_amount,
    handle_kis_market_fund_summary,
    handle_kis_stock_loan_trend_daily,
    handle_kis_limit_price_stocks,
    handle_kis_resistance_level_trading_weight,
]


def register_kis_market_analysis_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
