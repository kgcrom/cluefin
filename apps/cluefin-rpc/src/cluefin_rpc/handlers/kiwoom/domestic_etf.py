"""RPC handlers for Kiwoom DomesticETF API (9 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# ETF Return Rate
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.return_rate",
    description="Get ETF return rate from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code (e.g. KRX:069500)"},
            "index_code": {"type": "string", "description": "ETF target index code (e.g. 001)"},
            "period": {
                "type": "integer",
                "enum": [0, 1, 2, 3],
                "description": "Period (0:1week, 1:1month, 2:6months, 3:1year)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "index_code", "period"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_return_rate(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_return_rate(
        stk_cd=params["stock_code"],
        etfobjt_idex_cd=params["index_code"],
        dt=params["period"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Item Info
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.item_info",
    description="Get ETF item information from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code (e.g. KRX:069500)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_item_info(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_item_info(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Daily Trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.daily_trend",
    description="Get ETF daily trend from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code (e.g. KRX:069500)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_daily_trend(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_daily_trend(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Full Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.full_price",
    description="Get ETF full price list from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "tax_type": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "5"],
                "description": "Tax type (0:all, 1:tax-free, 2:holding-period, 3:corporate, 4:foreign, 5:tax-free-overseas)",
            },
            "nav_premium": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "NAV premium (0:all, 1:NAV>prev close, 2:NAV<prev close)",
            },
            "management_company": {
                "type": "string",
                "enum": ["0000", "3020", "3027", "3191", "3228", "3023", "3022", "9999"],
                "description": "Management company (0000:all, 3020:KODEX, 3027:KOSEF, 3191:TIGER, 3228:KINDEX, 3023:KStar, 3022:Arirang, 9999:others)",
            },
            "tax_yn": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Taxable status (0:all, 1:taxable, 2:tax-free)",
            },
            "trace_index": {"type": "string", "enum": ["0"], "description": "Tracking index (0:all)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["tax_type", "nav_premium", "management_company", "tax_yn", "trace_index", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_full_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_full_price(
        txon_type=params["tax_type"],
        navpre=params["nav_premium"],
        mngmcomp=params["management_company"],
        txon_yn=params["tax_yn"],
        trace_idex=params["trace_index"],
        stex_tp=params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Hourly Trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.hourly_trend",
    description="Get ETF hourly trend from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_hourly_trend(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_hourly_trend(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Hourly Execution
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.hourly_execution",
    description="Get ETF hourly execution data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_hourly_execution(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_hourly_execution(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Daily Execution
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.daily_execution",
    description="Get ETF daily execution data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_daily_execution(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_daily_execution(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Hourly Execution V2
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.hourly_execution_v2",
    description="Get ETF hourly execution data (v2) from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_hourly_execution_v2(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_hourly_execution_v2(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# ETF Hourly Trend V2
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.etf.hourly_trend_v2",
    description="Get ETF hourly trend data (v2) from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_hourly_trend_v2(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_hourly_trend_v2(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_etf_return_rate,
    handle_kiwoom_etf_item_info,
    handle_kiwoom_etf_daily_trend,
    handle_kiwoom_etf_full_price,
    handle_kiwoom_etf_hourly_trend,
    handle_kiwoom_etf_hourly_execution,
    handle_kiwoom_etf_daily_execution,
    handle_kiwoom_etf_hourly_execution_v2,
    handle_kiwoom_etf_hourly_trend_v2,
]


def register_kiwoom_etf_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
