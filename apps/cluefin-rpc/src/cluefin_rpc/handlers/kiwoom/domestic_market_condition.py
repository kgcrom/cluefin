"""RPC handlers for Kiwoom DomesticMarketCondition API (20 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Stock Quote
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.stock_quote",
    description="Get stock order book quote data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490, 039490_NX, 039490_AL)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_stock_quote(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_stock_quote(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Quote by Date
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.stock_quote_by_date",
    description="Get stock order book quote data by date.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490, 039490_NX, 039490_AL)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_stock_quote_by_date(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_stock_quote_by_date(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.stock_price",
    description="Get current stock price data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490, 039490_NX, 039490_AL)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_stock_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_stock_price(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Market Sentiment
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.market_sentiment",
    description="Get market sentiment information for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490, 039490_NX, 039490_AL)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_market_sentiment(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_market_sentiment_info(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# New Stock Warrant Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.new_stock_warrant_price",
    description="Get new stock warrant (preemptive rights) price data.",
    parameters={
        "type": "object",
        "properties": {
            "newstk_recvrht_tp": {
                "type": "string",
                "enum": ["00", "05", "07"],
                "description": "Warrant type (00:all, 05:warrant, 07:certificate).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["newstk_recvrht_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_new_stock_warrant_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_new_stock_warrant_price(
        params["newstk_recvrht_tp"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Institutional Trading
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.daily_institutional_trading",
    description="Get daily institutional trading items by date range.",
    parameters={
        "type": "object",
        "properties": {
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:net sell, 2:net buy).",
            },
            "market_type": {
                "type": "string",
                "enum": ["001", "101"],
                "description": "Market type (001:KOSPI, 101:KOSDAQ).",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["start_date", "end_date", "trde_tp", "market_type", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_daily_institutional_trading(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_daily_institutional_trading_items(
        params["start_date"],
        params["end_date"],
        params["trde_tp"],
        params["market_type"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Institutional Trend by Stock
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.institutional_trend_by_stock",
    description="Get institutional trading trend for a specific stock by date range.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "orgn_prsm_unp_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Institutional estimated unit price type (1:buy, 2:sell).",
            },
            "for_prsm_unp_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Foreign estimated unit price type (1:buy, 2:sell).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code", "start_date", "end_date", "orgn_prsm_unp_tp", "for_prsm_unp_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_institutional_trend_by_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_institutional_trading_trend_by_stock(
        params["stock_code"],
        params["start_date"],
        params["end_date"],
        params["orgn_prsm_unp_tp"],
        params["for_prsm_unp_tp"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Execution Intensity by Time
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.execution_intensity_by_time",
    description="Get execution intensity trend by time for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_execution_intensity_by_time(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_execution_intensity_trend_by_time(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Execution Intensity by Date
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.execution_intensity_by_date",
    description="Get execution intensity trend by date for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_execution_intensity_by_date(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_execution_intensity_trend_by_date(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Intraday Trading by Investor
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.intraday_trading_by_investor",
    description="Get intraday trading data grouped by investor type.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market type (000:all, 001:KOSPI, 101:KOSDAQ).",
            },
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "invsr": {
                "type": "string",
                "enum": ["6", "7", "1", "0", "2", "3", "4", "5"],
                "description": "Investor type code.",
            },
            "frgn_all": {
                "type": "string",
                "enum": ["1", "0"],
                "description": "Foreign all flag (1:foreign system, 0:all).",
            },
            "smtm_netprps_tp": {
                "type": "string",
                "enum": ["1", "0"],
                "description": "Simultaneous net buy type (1:simultaneous, 0:net).",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["market_type", "amount_qty_type", "invsr", "frgn_all", "smtm_netprps_tp", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_intraday_trading_by_investor(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_intraday_trading_by_investor(
        params["market_type"],
        params["amount_qty_type"],
        params["invsr"],
        params["frgn_all"],
        params["smtm_netprps_tp"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# After Market Trading by Investor
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.after_market_trading_by_investor",
    description="Get after-market trading data grouped by investor type.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market type (000:all, 001:KOSPI, 101:KOSDAQ).",
            },
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Trade type (0:all, 1:sell, 2:buy).",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["market_type", "amount_qty_type", "trde_tp", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_after_market_trading_by_investor(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_after_market_trading_by_investor(
        params["market_type"],
        params["amount_qty_type"],
        params["trde_tp"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Securities Firm Trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.securities_firm_trend",
    description="Get securities firm trading trend by stock.",
    parameters={
        "type": "object",
        "properties": {
            "mmcm_cd": {"type": "string", "description": "Member firm code (3-digit code)"},
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["mmcm_cd", "stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_securities_firm_trend(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_securities_firm_trading_trend_by_stock(
        params["mmcm_cd"],
        params["stock_code"],
        params["start_date"],
        params["end_date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Stock Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.daily_stock_price",
    description="Get daily stock price with optional indicator display.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "qry_dt": {"type": "string", "description": "Query date (YYYYMMDD)"},
            "indc_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Display type (0:quantity, 1:amount).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code", "qry_dt", "indc_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_daily_stock_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_daily_stock_price(
        params["stock_code"],
        params["qry_dt"],
        params["indc_tp"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# After Hours Single Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.after_hours_single_price",
    description="Get after-hours single price data for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_after_hours_single_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_after_hours_single_price(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program Trading Trend by Time
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.program_trading_trend_by_time",
    description="Get program trading trend by time period.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "market_type": {
                "type": "string",
                "enum": ["P00101", "P001_NX01", "P001_AL01", "P10102", "P101_NX02", "P001_AL02"],
                "description": "Market type code.",
            },
            "min_tic_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Minute/tick type (0:minute, 1:tick).",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["date", "amount_qty_type", "market_type", "min_tic_tp", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_program_trading_trend_by_time(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_program_trading_trend_by_time(
        params["date"],
        params["amount_qty_type"],
        params["market_type"],
        params["min_tic_tp"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program Arbitrage Balance
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.program_arbitrage_balance",
    description="Get program trading arbitrage balance trend.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["date", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_program_arbitrage_balance(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_program_trading_arbitrage_balance_trend(
        params["date"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program Cumulative
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.program_cumulative",
    description="Get program trading cumulative trend.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "market_type": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Market type (0:KOSPI, 1:KOSDAQ).",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["date", "amount_qty_type", "market_type", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_program_cumulative(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_program_trading_cumulative_trend(
        params["date"],
        params["amount_qty_type"],
        params["market_type"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program by Stock and Time
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.program_by_stock_and_time",
    description="Get program trading trend by stock and time.",
    parameters={
        "type": "object",
        "properties": {
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["amount_qty_type", "stock_code", "date"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_program_by_stock_and_time(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_program_trading_trend_by_stock_and_time(
        params["amount_qty_type"],
        params["stock_code"],
        params["date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program Trend by Date
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.program_trend_by_date",
    description="Get program trading trend by date.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "market_type": {
                "type": "string",
                "enum": ["P00101", "P001_NX01", "P001_AL01", "P10102", "P101_NX02", "P001_AL02"],
                "description": "Market type code.",
            },
            "min_tic_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Minute/tick type (0:minute, 1:tick).",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["date", "amount_qty_type", "market_type", "min_tic_tp", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_program_trend_by_date(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_program_trading_trend_by_date(
        params["date"],
        params["amount_qty_type"],
        params["market_type"],
        params["min_tic_tp"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program by Stock and Date
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.market_condition.program_by_stock_and_date",
    description="Get program trading trend by stock and date.",
    parameters={
        "type": "object",
        "properties": {
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity).",
            },
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["amount_qty_type", "stock_code", "date"],
    },
    returns={"type": "object"},
    category="kiwoom.market_condition",
    broker="kiwoom",
)
def handle_kiwoom_program_by_stock_and_date(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.market_conditions.get_program_trading_trend_by_stock_and_date(
        params["amount_qty_type"],
        params["stock_code"],
        params["date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_stock_quote,
    handle_kiwoom_stock_quote_by_date,
    handle_kiwoom_stock_price,
    handle_kiwoom_market_sentiment,
    handle_kiwoom_new_stock_warrant_price,
    handle_kiwoom_daily_institutional_trading,
    handle_kiwoom_institutional_trend_by_stock,
    handle_kiwoom_execution_intensity_by_time,
    handle_kiwoom_execution_intensity_by_date,
    handle_kiwoom_intraday_trading_by_investor,
    handle_kiwoom_after_market_trading_by_investor,
    handle_kiwoom_securities_firm_trend,
    handle_kiwoom_daily_stock_price,
    handle_kiwoom_after_hours_single_price,
    handle_kiwoom_program_trading_trend_by_time,
    handle_kiwoom_program_arbitrage_balance,
    handle_kiwoom_program_cumulative,
    handle_kiwoom_program_by_stock_and_time,
    handle_kiwoom_program_trend_by_date,
    handle_kiwoom_program_by_stock_and_date,
]


def register_kiwoom_market_condition_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
