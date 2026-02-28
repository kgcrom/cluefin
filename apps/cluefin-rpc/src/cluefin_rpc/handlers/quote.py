"""Quote handlers for KIS and Kiwoom market data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# KIS Quote Handlers
# ---------------------------------------------------------------------------


@rpc_method(
    name="quote.kis.stock_current",
    description="Get current stock price from KIS. Returns price, volume, market cap, PER, PBR.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kis",
)
def handle_kis_stock_current(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price(market, params["stock_code"])
    item = response.body.output
    if item is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {
        "stock_code": params["stock_code"],
        "current_price": int(item.stck_prpr),
        "change_rate": float(item.prdy_ctrt),
        "change_amount": int(item.prdy_vrss),
        "change_sign": item.prdy_vrss_sign,
        "volume": int(item.acml_vol),
        "trade_amount": int(item.acml_tr_pbmn),
        "open_price": int(item.stck_oprc),
        "high_price": int(item.stck_hgpr),
        "low_price": int(item.stck_lwpr),
        "upper_limit": int(item.stck_mxpr),
        "lower_limit": int(item.stck_llam),
        "base_price": int(item.stck_sdpr),
        "market_cap": int(item.hts_avls),
        "per": float(item.per) if item.per else None,
        "pbr": float(item.pbr) if item.pbr else None,
        "eps": float(item.eps) if item.eps else None,
        "bps": float(item.bps) if item.bps else None,
        "w52_high": int(item.w52_hgpr),
        "w52_low": int(item.w52_lwpr),
        "foreign_ratio": float(item.hts_frgn_ehrt),
        "foreign_net_buy": int(item.frgn_ntby_qty),
        "sector_name": item.bstp_kor_isnm,
    }


@rpc_method(
    name="quote.kis.stock_daily",
    description="Get daily stock price history from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {"type": "string", "enum": ["J", "NX", "UN"], "description": "Market code. Default J."},
            "period": {
                "type": "string",
                "enum": ["D", "W", "M"],
                "description": "Period (D:daily, W:weekly, M:monthly). Default D.",
            },
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:unadjusted, 1:adjusted). Default 1.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kis",
)
def handle_kis_stock_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    period = params.get("period", "D")
    adj = params.get("adj_price", "1")
    response = kis.domestic_basic_quote.get_stock_current_price_daily(market, params["stock_code"], period, adj)
    items = response.body.output or []
    return {
        "stock_code": params["stock_code"],
        "data": [
            {
                "date": item.stck_bsop_date,
                "open": int(item.stck_oprc),
                "high": int(item.stck_hgpr),
                "low": int(item.stck_lwpr),
                "close": int(item.stck_clpr),
                "volume": int(item.acml_vol),
                "change_rate": float(item.prdy_ctrt),
                "foreign_ratio": float(item.hts_frgn_ehrt),
            }
            for item in items
        ],
    }


@rpc_method(
    name="quote.kis.stock_period",
    description="Get stock price for a specific date range from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "market": {"type": "string", "enum": ["J", "NX", "UN"], "description": "Market code. Default J."},
            "period": {"type": "string", "enum": ["D", "W", "M", "Y"], "description": "Period code. Default D."},
            "adj_price": {"type": "string", "enum": ["0", "1"], "description": "0:adjusted, 1:original. Default 0."},
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kis",
)
def handle_kis_stock_period(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    period = params.get("period", "D")
    adj = params.get("adj_price", "0")
    response = kis.domestic_basic_quote.get_stock_period_quote(
        market, params["stock_code"], params["start_date"], params["end_date"], period, adj
    )
    items = response.body.output2 if hasattr(response.body, "output2") else []
    data = []
    for item in items or []:
        entry = item.model_dump() if hasattr(item, "model_dump") else {}
        data.append(entry)
    return {"stock_code": params["stock_code"], "data": data}


@rpc_method(
    name="quote.kis.stock_investor",
    description="Get investor trading data for a stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {"type": "string", "enum": ["J", "NX", "UN"], "description": "Market code. Default J."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kis",
)
def handle_kis_stock_investor(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_investor(market, params["stock_code"])
    items = response.body.output if hasattr(response.body, "output") else []
    data = []
    for item in items or []:
        entry = item.model_dump() if hasattr(item, "model_dump") else {}
        data.append(entry)
    return {"stock_code": params["stock_code"], "data": data}


@rpc_method(
    name="quote.kis.etf_current",
    description="Get current ETF/ETN price from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF/ETN code"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kis",
)
def handle_kis_etf_current(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etfetn_current_price(params["stock_code"])
    output = response.body.output
    if output is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {"stock_code": params["stock_code"], **output.model_dump()}


@rpc_method(
    name="quote.kis.sector_index",
    description="Get current sector index from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "description": "Market code (e.g. U for sector)"},
            "sector_code": {
                "type": "string",
                "description": "Sector code (e.g. 0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200)",
            },
        },
        "required": ["market", "sector_code"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kis",
)
def handle_kis_sector_index(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_issue_other.get_sector_current_index(params["market"], params["sector_code"])
    output = response.body.output
    if output is None:
        return {"sector_code": params["sector_code"], "error": "No data returned"}
    return {"sector_code": params["sector_code"], **output.model_dump()}


# ---------------------------------------------------------------------------
# Kiwoom Quote Handlers
# ---------------------------------------------------------------------------


@rpc_method(
    name="quote.kiwoom.stock_daily",
    description="Get daily stock chart from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. 039490)"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:no, 1:yes). Default 1.",
            },
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kiwoom",
)
def handle_kiwoom_stock_daily(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    adj = params.get("adj_price", "1")
    response = kiwoom.chart.get_stock_daily(params["stock_code"], params["base_date"], adj)
    items = response.body.output if hasattr(response.body, "output") else []
    data = []
    for item in items or []:
        entry = item.model_dump() if hasattr(item, "model_dump") else {}
        data.append(entry)
    return {"stock_code": params["stock_code"], "data": data}


@rpc_method(
    name="quote.kiwoom.stock_minute",
    description="Get minute stock chart from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code"},
            "tic_scope": {"type": "string", "description": "Tick scope (1:1min, 3:3min, 5:5min, 10:10min, etc.)"},
            "adj_price": {"type": "string", "enum": ["0", "1"], "description": "Adjusted price. Default 0."},
        },
        "required": ["stock_code", "tic_scope"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kiwoom",
)
def handle_kiwoom_stock_minute(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    adj = params.get("adj_price", "0")
    response = kiwoom.chart.get_stock_minute(params["stock_code"], params["tic_scope"], adj)
    items = response.body.output if hasattr(response.body, "output") else []
    data = []
    for item in items or []:
        entry = item.model_dump() if hasattr(item, "model_dump") else {}
        data.append(entry)
    return {"stock_code": params["stock_code"], "data": data}


@rpc_method(
    name="quote.kiwoom.stock_weekly",
    description="Get weekly stock chart from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {"type": "string", "enum": ["0", "1"], "description": "Adjusted price. Default 1."},
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kiwoom",
)
def handle_kiwoom_stock_weekly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    adj = params.get("adj_price", "1")
    response = kiwoom.chart.get_stock_weekly(params["stock_code"], params["base_date"], adj)
    items = response.body.output if hasattr(response.body, "output") else []
    data = []
    for item in items or []:
        entry = item.model_dump() if hasattr(item, "model_dump") else {}
        data.append(entry)
    return {"stock_code": params["stock_code"], "data": data}


@rpc_method(
    name="quote.kiwoom.stock_monthly",
    description="Get monthly stock chart from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code"},
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "adj_price": {"type": "string", "enum": ["0", "1"], "description": "Adjusted price. Default 1."},
        },
        "required": ["stock_code", "base_date"],
    },
    returns={"type": "object"},
    category="quote",
    broker="kiwoom",
)
def handle_kiwoom_stock_monthly(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    adj = params.get("adj_price", "1")
    response = kiwoom.chart.get_stock_monthly(params["stock_code"], params["base_date"], adj)
    items = response.body.output if hasattr(response.body, "output") else []
    data = []
    for item in items or []:
        entry = item.model_dump() if hasattr(item, "model_dump") else {}
        data.append(entry)
    return {"stock_code": params["stock_code"], "data": data}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kis_stock_current,
    handle_kis_stock_daily,
    handle_kis_stock_period,
    handle_kis_stock_investor,
    handle_kis_etf_current,
    handle_kis_sector_index,
    handle_kiwoom_stock_daily,
    handle_kiwoom_stock_minute,
    handle_kiwoom_stock_weekly,
    handle_kiwoom_stock_monthly,
]


def register_quote_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
