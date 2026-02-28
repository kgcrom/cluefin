"""RPC handlers for Kiwoom DomesticChart API (14 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Stock Tick Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.stock_tick",
    description="Get stock tick chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "tic_scope": {
                "type": "string",
                "description": "Tick scope (1:1tick, 3:3tick, 5:5tick, 10:10tick, 30:30tick)",
            },
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price type. Default 0.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "tic_scope"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_stock_tick(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_stock_tick(
        stk_cd=params["stock_code"],
        tic_scope=params["tic_scope"],
        upd_stkpc_tp=params.get("adj_price", "0"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Minute Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.stock_minute",
    description="Get stock minute chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "tic_scope": {
                "type": "string",
                "description": "Minute scope (1:1min, 3:3min, 5:5min, 10:10min, 15:15min, 30:30min, 45:45min, 60:60min)",
            },
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price type. Default 0.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "tic_scope"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_stock_minute(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_stock_minute(
        stk_cd=params["stock_code"],
        tic_scope=params["tic_scope"],
        upd_stkpc_tp=params.get("adj_price", "0"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Daily Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.stock_daily",
    description="Get stock daily chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:unadjusted, 1:adjusted). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_stock_daily(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_stock_daily(
        stk_cd=params["stock_code"],
        base_dt=params["base_date"],
        upd_stkpc_tp=params.get("adj_price", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Weekly Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.stock_weekly",
    description="Get stock weekly chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:unadjusted, 1:adjusted). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_stock_weekly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_stock_weekly(
        stk_cd=params["stock_code"],
        base_dt=params["base_date"],
        upd_stkpc_tp=params.get("adj_price", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Monthly Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.stock_monthly",
    description="Get stock monthly chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:unadjusted, 1:adjusted). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_stock_monthly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_stock_monthly(
        stk_cd=params["stock_code"],
        base_dt=params["base_date"],
        upd_stkpc_tp=params.get("adj_price", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Yearly Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.stock_yearly",
    description="Get stock yearly chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:unadjusted, 1:adjusted). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_stock_yearly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_stock_yearly(
        stk_cd=params["stock_code"],
        base_dt=params["base_date"],
        upd_stkpc_tp=params.get("adj_price", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Tick Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.industry_tick",
    description="Get industry tick chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 002:Large, 003:Mid, 004:Small, 101:KOSDAQ, 201:KOSPI200, 302:KOSTAR, 701:KRX100)",
            },
            "tic_scope": {
                "type": "string",
                "description": "Tick scope (1:1tick, 3:3tick, 5:5tick, 10:10tick, 30:30tick)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["industry_code", "tic_scope"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_industry_tick(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_industry_tick(
        inds_cd=params["industry_code"],
        tic_scope=params["tic_scope"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Minute Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.industry_minute",
    description="Get industry minute chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 002:Large, 003:Mid, 004:Small, 101:KOSDAQ, 201:KOSPI200, 302:KOSTAR, 701:KRX100)",
            },
            "tic_scope": {
                "type": "string",
                "description": "Tick scope (1:1tick, 3:3tick, 5:5tick, 10:10tick, 30:30tick)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["industry_code", "tic_scope"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_industry_minute(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_industry_minute(
        inds_cd=params["industry_code"],
        tic_scope=params["tic_scope"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Daily Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.industry_daily",
    description="Get industry daily chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 002:Large, 003:Mid, 004:Small, 101:KOSDAQ, 201:KOSPI200, 302:KOSTAR, 701:KRX100)",
            },
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["industry_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_industry_daily(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_industry_daily(
        inds_cd=params["industry_code"],
        base_dt=params["base_date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Weekly Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.industry_weekly",
    description="Get industry weekly chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 002:Large, 003:Mid, 004:Small, 101:KOSDAQ, 201:KOSPI200, 302:KOSTAR, 701:KRX100)",
            },
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["industry_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_industry_weekly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_industry_weekly(
        inds_cd=params["industry_code"],
        base_dt=params["base_date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Monthly Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.industry_monthly",
    description="Get industry monthly chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 002:Large, 003:Mid, 004:Small, 101:KOSDAQ, 201:KOSPI200, 302:KOSTAR, 701:KRX100)",
            },
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["industry_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_industry_monthly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_industry_monthly(
        inds_cd=params["industry_code"],
        base_dt=params["base_date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Yearly Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.industry_yearly",
    description="Get industry yearly chart data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 002:Large, 003:Mid, 004:Small, 101:KOSDAQ, 201:KOSPI200, 302:KOSTAR, 701:KRX100)",
            },
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["industry_code", "base_date"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_industry_yearly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_industry_yearly(
        inds_cd=params["industry_code"],
        base_dt=params["base_date"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Institutional By Stock Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.institutional_by_stock",
    description="Get institutional investor chart by stock from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Date (YYYYMMDD)"},
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity)",
            },
            "trade_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Trade type (0:net buy, 1:buy, 2:sell)",
            },
            "unit_type": {
                "type": "string",
                "enum": ["1000", "1"],
                "description": "Unit type (1000:thousands, 1:single)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["date", "stock_code", "amount_qty_type", "trade_type", "unit_type"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_institutional_by_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_individual_stock_institutional_chart(
        dt=params["date"],
        stk_cd=params["stock_code"],
        amt_qty_tp=params["amount_qty_type"],
        trde_tp=params["trade_type"],
        unit_tp=params["unit_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Intraday Investor Trading Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.chart.intraday_investor_trading",
    description="Get intraday investor trading chart from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market type (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "amount_qty_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Amount/quantity type (1:amount, 2:quantity)",
            },
            "trade_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Trade type (0:net buy, 1:buy, 2:sell)",
            },
            "stock_code": {"type": "string", "description": "Stock code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "amount_qty_type", "trade_type", "stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.chart",
    broker="kiwoom",
)
def handle_kiwoom_intraday_investor_trading(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.chart.get_intraday_investor_trading(
        mrkt_tp=params["market_type"],
        amt_qty_tp=params["amount_qty_type"],
        trde_tp=params["trade_type"],
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_stock_tick,
    handle_kiwoom_stock_minute,
    handle_kiwoom_stock_daily,
    handle_kiwoom_stock_weekly,
    handle_kiwoom_stock_monthly,
    handle_kiwoom_stock_yearly,
    handle_kiwoom_industry_tick,
    handle_kiwoom_industry_minute,
    handle_kiwoom_industry_daily,
    handle_kiwoom_industry_weekly,
    handle_kiwoom_industry_monthly,
    handle_kiwoom_industry_yearly,
    handle_kiwoom_institutional_by_stock,
    handle_kiwoom_intraday_investor_trading,
]


def register_kiwoom_chart_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
