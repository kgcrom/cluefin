"""RPC handlers for Kiwoom DomesticStockInfo API (28 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Stock Basic Info
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.basic",
    description="Get basic stock information from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_stock_basic(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_stock_info(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Trading Member
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.trading_member",
    description="Get stock trading member (brokerage firm) data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_trading_member(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_stock_trading_member(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Execution Info
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.execution",
    description="Get stock execution (trade conclusion) data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_execution(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_execution(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Margin Trading Trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.margin_trading_trend",
    description="Get margin (credit) trading trend for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "dt": {"type": "string", "description": "Date (YYYYMMDD)"},
            "qry_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Query type (1:margin loan, 2:stock lending)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "dt", "qry_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_margin_trading_trend(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_margin_trading_trend(
        stk_cd=params["stock_code"],
        dt=params["dt"],
        qry_tp=params["qry_tp"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Trading Details
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.daily_trading_details",
    description="Get daily trading details for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "start_date"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_daily_trading_details(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_daily_trading_details(
        stk_cd=params["stock_code"],
        strt_dt=params["start_date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# New High / Low Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.new_high_low_price",
    description="Get stocks hitting new high or low prices.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)"},
            "ntl_tp": {"type": "string", "description": "High/low type (1:new high, 2:new low)"},
            "high_low_close_tp": {"type": "string", "description": "Criterion (1:high/low, 2:close)"},
            "stk_cnd": {"type": "string", "description": "Stock condition. Default 0."},
            "trde_qty_tp": {"type": "string", "description": "Volume filter. Default 00000."},
            "crd_cnd": {"type": "string", "description": "Credit condition. Default 0."},
            "updown_incls": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Include upper/lower limit (0:no, 1:yes). Default 0.",
            },
            "dt": {"type": "string", "description": "Period (5/10/20/60/250 days)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "ntl_tp", "high_low_close_tp", "dt"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_new_high_low_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_new_high_low_price(
        mrkt_tp=params["market_type"],
        ntl_tp=params["ntl_tp"],
        high_low_close_tp=params["high_low_close_tp"],
        stk_cnd=params.get("stk_cnd", "0"),
        trde_qty_tp=params.get("trde_qty_tp", "00000"),
        crd_cnd=params.get("crd_cnd", "0"),
        updown_incls=params.get("updown_incls", "0"),
        dt=params["dt"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Upper / Lower Limit Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.upper_lower_limit",
    description="Get stocks at upper or lower limit prices.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)"},
            "updown_tp": {
                "type": "string",
                "description": "Limit type (1:upper, 2:rise, 3:flat, 4:lower, 5:fall, 6:prev upper, 7:prev lower)",
            },
            "sort_tp": {
                "type": "string",
                "description": "Sort (1:code, 2:consecutive count top100, 3:change rate)",
            },
            "stk_cnd": {"type": "string", "description": "Stock condition. Default 0."},
            "trde_qty_tp": {"type": "string", "description": "Volume filter. Default 00000."},
            "crd_cnd": {"type": "string", "description": "Credit condition. Default 0."},
            "trde_gold_tp": {"type": "string", "description": "Trade amount filter. Default 0."},
            "exchange_type": {"type": "string", "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1."},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "updown_tp", "sort_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_upper_lower_limit(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_upper_lower_limit_price(
        mrkt_tp=params["market_type"],
        updown_tp=params["updown_tp"],
        sort_tp=params["sort_tp"],
        stk_cnd=params.get("stk_cnd", "0"),
        trde_qty_tp=params.get("trde_qty_tp", "00000"),
        crd_cnd=params.get("crd_cnd", "0"),
        trde_gold_tp=params.get("trde_gold_tp", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# High / Low Price Approach
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.high_low_approach",
    description="Get stocks approaching high or low price levels.",
    parameters={
        "type": "object",
        "properties": {
            "high_low_tp": {"type": "string", "description": "Type (1:high, 2:low)"},
            "alacc_rt": {"type": "string", "description": "Approach rate (05:0.5%, 10:1.0%, 15:1.5%, etc.)"},
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)"},
            "trde_qty_tp": {"type": "string", "description": "Volume filter. Default 00000."},
            "stk_cnd": {"type": "string", "description": "Stock condition. Default 0."},
            "crd_cnd": {"type": "string", "description": "Credit condition. Default 0."},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["high_low_tp", "alacc_rt", "market_type"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_high_low_approach(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_high_low_price_approach(
        high_low_tp=params["high_low_tp"],
        alacc_rt=params["alacc_rt"],
        mrkt_tp=params["market_type"],
        trde_qty_tp=params.get("trde_qty_tp", "00000"),
        stk_cnd=params.get("stk_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Price Volatility (Rapid Rise/Fall)
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.price_volatility",
    description="Get stocks with rapid price rise or fall.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ, 201:KOSPI200)"},
            "flu_tp": {"type": "string", "enum": ["1", "2"], "description": "Direction (1:surge, 2:plunge)"},
            "tm_tp": {"type": "string", "enum": ["1", "2"], "description": "Time type (1:minutes ago, 2:days ago)"},
            "tm": {"type": "string", "description": "Time value (minutes or days)"},
            "trde_qty_tp": {"type": "string", "description": "Volume filter. Default 00000."},
            "stk_cnd": {"type": "string", "description": "Stock condition. Default 0."},
            "crd_cnd": {"type": "string", "description": "Credit condition. Default 0."},
            "pric_cnd": {"type": "string", "description": "Price condition. Default 0."},
            "updown_incls": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Include upper/lower limit (0:no, 1:yes). Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "flu_tp", "tm_tp", "tm"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_price_volatility(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_price_volatility(
        mrkt_tp=params["market_type"],
        flu_tp=params["flu_tp"],
        tm_tp=params["tm_tp"],
        tm=params["tm"],
        trde_qty_tp=params.get("trde_qty_tp", "00000"),
        stk_cnd=params.get("stk_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        pric_cnd=params.get("pric_cnd", "0"),
        updown_incls=params.get("updown_incls", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Trading Volume Renewal
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.volume_renewal",
    description="Get stocks with trading volume renewal (exceeding historical levels).",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)"},
            "cycle_tp": {"type": "string", "description": "Cycle (5/10/20/60/250 days)"},
            "trde_qty_tp": {"type": "string", "description": "Volume filter"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "cycle_tp", "trde_qty_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_volume_renewal(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_trading_volume_renewal(
        mrkt_tp=params["market_type"],
        cycle_tp=params["cycle_tp"],
        trde_qty_tp=params["trde_qty_tp"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Supply Demand Concentration
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.supply_demand_concentration",
    description="Get stocks with concentrated supply/demand price zones.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)"},
            "prps_cnctr_rt": {"type": "string", "description": "Supply concentration ratio (0-100)"},
            "cur_prc_entry": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Include current price entry (0:no, 1:yes)",
            },
            "prpscnt": {"type": "string", "description": "Number of supply zones"},
            "cycle_tp": {"type": "string", "description": "Cycle (50/100/150/200/250/300 days)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "prps_cnctr_rt", "cur_prc_entry", "prpscnt", "cycle_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_supply_demand_concentration(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_supply_demand_concentration(
        mrkt_tp=params["market_type"],
        prps_cnctr_rt=params["prps_cnctr_rt"],
        cur_prc_entry=params["cur_prc_entry"],
        prpscnt=params["prpscnt"],
        cycle_tp=params["cycle_tp"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# High PER / PBR / ROE
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.high_per",
    description="Get stocks by PER/PBR/ROE ranking (high or low).",
    parameters={
        "type": "object",
        "properties": {
            "pertp": {
                "type": "string",
                "enum": ["1", "2", "3", "4", "5", "6"],
                "description": "Type (1:low PBR, 2:high PBR, 3:low PER, 4:high PER, 5:low ROE, 6:high ROE)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["pertp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_high_per(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_high_per(
        pertp=params["pertp"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Change Rate From Open
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.change_rate_from_open",
    description="Get stocks ranked by change rate from opening price.",
    parameters={
        "type": "object",
        "properties": {
            "sort_tp": {
                "type": "string",
                "enum": ["1", "2", "3", "4"],
                "description": "Sort base (1:open, 2:high, 3:low, 4:base price)",
            },
            "trde_qty_cnd": {"type": "string", "description": "Volume condition. Default 0000."},
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "updown_incls": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Include upper/lower limit (0:no, 1:yes). Default 0.",
            },
            "stk_cnd": {"type": "string", "description": "Stock condition. Default 0."},
            "crd_cnd": {"type": "string", "description": "Credit condition. Default 0."},
            "trde_prica_cnd": {"type": "string", "description": "Trade amount condition. Default 0."},
            "flu_cnd": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Direction (1:top, 2:bottom)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["sort_tp", "market_type", "flu_cnd"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_change_rate_from_open(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_change_rate_from_open(
        sort_tp=params["sort_tp"],
        trde_qty_cnd=params.get("trde_qty_cnd", "0000"),
        mrkt_tp=params["market_type"],
        updown_incls=params.get("updown_incls", "0"),
        stk_cnd=params.get("stk_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        trde_prica_cnd=params.get("trde_prica_cnd", "0"),
        flu_cnd=params["flu_cnd"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Trading Member Supply Demand Analysis
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.trading_member_supply_demand",
    description="Get trading member supply/demand analysis for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "qry_dt_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Query period type (0:by period, 1:by start/end date)",
            },
            "pot_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Point of time (0:today, 1:prev day)",
            },
            "dt": {
                "type": "string",
                "enum": ["5", "10", "20", "40", "60", "120"],
                "description": "Period days",
            },
            "sort_base": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Sort base (1:by close price, 2:by date)",
            },
            "member_company_code": {"type": "string", "description": "3-digit member company code"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": [
            "stock_code",
            "start_date",
            "end_date",
            "qry_dt_tp",
            "pot_tp",
            "dt",
            "sort_base",
            "member_company_code",
        ],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_trading_member_supply_demand(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_trading_member_supply_demand_analysis(
        stk_cd=params["stock_code"],
        strt_dt=params["start_date"],
        end_dt=params["end_date"],
        qry_dt_tp=params["qry_dt_tp"],
        pot_tp=params["pot_tp"],
        dt=params["dt"],
        sort_base=params["sort_base"],
        mmcm_cd=params["member_company_code"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Trading Member Instant Volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.trading_member_instant_volume",
    description="Get trading member instant volume data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "member_company_code": {"type": "string", "description": "3-digit member company code"},
            "market_type": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "Market (0:all, 1:KOSPI, 2:KOSDAQ, 3:specific stock). Default 0.",
            },
            "qty_tp": {"type": "string", "description": "Quantity filter. Default 0."},
            "pric_tp": {"type": "string", "description": "Price filter. Default 0."},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "member_company_code"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_trading_member_instant_volume(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_trading_member_instant_volume(
        stk_cd=params["stock_code"],
        mmcm_cd=params["member_company_code"],
        mrkt_tp=params.get("market_type", "0"),
        qty_tp=params.get("qty_tp", "0"),
        pric_tp=params.get("pric_tp", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Volatility Control Event (VI)
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.volatility_control_event",
    description="Get volatility interruption (VI) triggered stocks list.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)"},
            "bf_mkrt_tp": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Session (0:all, 1:regular, 2:after-hours single price)",
            },
            "motn_tp": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "VI type (0:all, 1:static, 2:dynamic, 3:dynamic+static)",
            },
            "skip_stk": {
                "type": "string",
                "description": "Stock exclusion mask (9-digit, e.g. 000000000 for all)",
            },
            "trde_qty_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Volume filter toggle (0:off, 1:on). Default 0.",
            },
            "trde_prica_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Trade amount filter toggle (0:off, 1:on). Default 0.",
            },
            "motn_drc": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Direction (0:all, 1:up, 2:down). Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "min_trde_qty": {"type": "string", "description": "Min volume (when trde_qty_tp=1). Default empty."},
            "max_trde_qty": {"type": "string", "description": "Max volume (when trde_qty_tp=1). Default empty."},
            "min_trde_prica": {
                "type": "string",
                "description": "Min trade amount in million KRW (when trde_prica_tp=1). Default empty.",
            },
            "max_trde_prica": {
                "type": "string",
                "description": "Max trade amount in million KRW (when trde_prica_tp=1). Default empty.",
            },
            "stock_code": {
                "type": "string",
                "description": "Stock code to filter (empty for all stocks). Default empty.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "bf_mkrt_tp", "motn_tp", "skip_stk"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_volatility_control_event(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_volatility_control_event(
        mrkt_tp=params["market_type"],
        bf_mkrt_tp=params["bf_mkrt_tp"],
        motn_tp=params["motn_tp"],
        skip_stk=params["skip_stk"],
        trde_qty_tp=params.get("trde_qty_tp", "0"),
        trde_prica_tp=params.get("trde_prica_tp", "0"),
        motn_drc=params.get("motn_drc", "0"),
        stex_tp=params.get("exchange_type", "1"),
        min_trde_qty=params.get("min_trde_qty", ""),
        max_trde_qty=params.get("max_trde_qty", ""),
        min_trde_prica=params.get("min_trde_prica", ""),
        max_trde_prica=params.get("max_trde_prica", ""),
        stk_cd=params.get("stock_code", ""),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Previous Day Execution Volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.prev_day_execution_volume",
    description="Get daily/previous day execution volume data for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "tdy_pred": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Day type (1:today, 2:prev day)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "tdy_pred"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_prev_day_execution_volume(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_daily_previous_day_execution_volume(
        stk_cd=params["stock_code"],
        tdy_pred=params["tdy_pred"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Trading Items by Investor
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.daily_trading_by_investor",
    description="Get daily trading items ranked by investor type.",
    parameters={
        "type": "object",
        "properties": {
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:net sell, 2:net buy)",
            },
            "market_type": {
                "type": "string",
                "enum": ["001", "101"],
                "description": "Market (001:KOSPI, 101:KOSDAQ)",
            },
            "invsr_tp": {
                "type": "string",
                "enum": [
                    "8000",
                    "9000",
                    "1000",
                    "3000",
                    "5000",
                    "4000",
                    "2000",
                    "6000",
                    "7000",
                    "7100",
                    "9999",
                ],
                "description": "Investor type (8000:individual, 9000:foreigner, etc.)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["start_date", "end_date", "trde_tp", "market_type", "invsr_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_daily_trading_by_investor(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_daily_trading_items_by_investor(
        strt_dt=params["start_date"],
        end_dt=params["end_date"],
        trde_tp=params["trde_tp"],
        mrkt_tp=params["market_type"],
        invsr_tp=params["invsr_tp"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Institutional Investor by Stock
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.institutional_by_stock",
    description="Get institutional investor data by stock (daily breakdown).",
    parameters={
        "type": "object",
        "properties": {
            "dt": {"type": "string", "description": "Date (YYYYMMDD)"},
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Type (1:amount, 2:quantity)",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Trade type (0:net buy, 1:buy, 2:sell)",
            },
            "unit_tp": {
                "type": "string",
                "enum": ["1000", "1"],
                "description": "Unit (1000:thousand, 1:share). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["dt", "stock_code", "amount_qty_type", "trde_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_institutional_by_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_institutional_investor_by_stock(
        dt=params["dt"],
        stk_cd=params["stock_code"],
        amt_qty_tp=params["amount_qty_type"],
        trde_tp=params["trde_tp"],
        unit_tp=params.get("unit_tp", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Total Institutional Investor by Stock
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.total_institutional_by_stock",
    description="Get total institutional investor data by stock (period aggregate).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Type (1:amount, 2:quantity)",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Trade type (0:net buy, 1:buy, 2:sell)",
            },
            "unit_tp": {
                "type": "string",
                "enum": ["1000", "1"],
                "description": "Unit (1000:thousand, 1:share). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "start_date", "end_date", "amount_qty_type", "trde_tp"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_total_institutional_by_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_total_institutional_investor_by_stock(
        stk_cd=params["stock_code"],
        strt_dt=params["start_date"],
        end_dt=params["end_date"],
        amt_qty_tp=params["amount_qty_type"],
        trde_tp=params["trde_tp"],
        unit_tp=params.get("unit_tp", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Previous Day Conclusion
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.prev_day_conclusion",
    description="Get daily/previous day conclusion data for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "tdy_pred": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Day type (1:today, 2:prev day)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "tdy_pred"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_prev_day_conclusion(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_daily_previous_day_conclusion(
        stk_cd=params["stock_code"],
        tdy_pred=params["tdy_pred"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Interest Stock Info
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.interest_stock",
    description="Get watchlist stock information (multiple codes separated by |).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock codes separated by | (e.g. 039490|005930)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_interest_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_interest_stock_info(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Info Summary (List)
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.summary",
    description="Get stock info summary list by market type.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "description": "Market (0:KOSPI, 10:KOSDAQ, 3:ELW, 8:ETF, 30:K-OTC, 50:KONEX, etc.)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_summary(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_stock_info_summary(
        mrkt_tp=params["market_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Info V1
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.basic_v1",
    description="Get stock information (v1 API).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_basic_v1(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_stock_info_v1(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Code List
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.industry_code",
    description="Get industry (sector) code list.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "description": "Market (0:KOSPI, 1:KOSDAQ, 2:KOSPI200, 4:KOSPI100, 7:KRX100)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_industry_code(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_industry_code(
        mrkt_tp=params["market_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Member Company List
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.member_company",
    description="Get member company (brokerage firm) list.",
    parameters={
        "type": "object",
        "properties": {
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": [],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_member_company(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_member_company(
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program Net Buy Top 50
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.program_net_buy_top50",
    description="Get top 50 stocks by program trading net buy/sell.",
    parameters={
        "type": "object",
        "properties": {
            "trde_upper_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Rank type (1:net sell top, 2:net buy top)",
            },
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Type (1:amount, 2:quantity)",
            },
            "market_type": {
                "type": "string",
                "description": "Market code (P00101:KOSPI, P10102:KOSDAQ)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["trde_upper_tp", "amount_qty_type", "market_type"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_program_net_buy_top50(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_top_50_program_net_buy(
        trde_upper_tp=params["trde_upper_tp"],
        amt_qty_tp=params["amount_qty_type"],
        mrkt_tp=params["market_type"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Program Trading Status by Stock
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.stock_info.program_trading_by_stock",
    description="Get program trading status for each stock.",
    parameters={
        "type": "object",
        "properties": {
            "dt": {"type": "string", "description": "Date (YYYYMMDD)"},
            "market_type": {
                "type": "string",
                "description": "Market code (P00101:KOSPI, P10102:KOSDAQ)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["dt", "market_type"],
    },
    returns={"type": "object"},
    category="kiwoom.stock_info",
    broker="kiwoom",
)
def handle_kiwoom_program_trading_by_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.stock_info.get_program_trading_status_by_stock(
        dt=params["dt"],
        mrkt_tp=params["market_type"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_stock_basic,
    handle_kiwoom_trading_member,
    handle_kiwoom_execution,
    handle_kiwoom_margin_trading_trend,
    handle_kiwoom_daily_trading_details,
    handle_kiwoom_new_high_low_price,
    handle_kiwoom_upper_lower_limit,
    handle_kiwoom_high_low_approach,
    handle_kiwoom_price_volatility,
    handle_kiwoom_volume_renewal,
    handle_kiwoom_supply_demand_concentration,
    handle_kiwoom_high_per,
    handle_kiwoom_change_rate_from_open,
    handle_kiwoom_trading_member_supply_demand,
    handle_kiwoom_trading_member_instant_volume,
    handle_kiwoom_volatility_control_event,
    handle_kiwoom_prev_day_execution_volume,
    handle_kiwoom_daily_trading_by_investor,
    handle_kiwoom_institutional_by_stock,
    handle_kiwoom_total_institutional_by_stock,
    handle_kiwoom_prev_day_conclusion,
    handle_kiwoom_interest_stock,
    handle_kiwoom_summary,
    handle_kiwoom_basic_v1,
    handle_kiwoom_industry_code,
    handle_kiwoom_member_company,
    handle_kiwoom_program_net_buy_top50,
    handle_kiwoom_program_trading_by_stock,
]


def register_kiwoom_stock_info_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
