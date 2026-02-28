"""RPC handlers for Kiwoom DomesticSector API (6 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Industry Program
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.sector.program",
    description="Get industry program trading data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Industry code"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.sector",
    broker="kiwoom",
)
def handle_kiwoom_sector_program(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.sector.get_industry_program(
        params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Investor Net Buy
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.sector.investor_net_buy",
    description="Get industry investor net buy data by sector.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Market type (0:KOSPI, 1:KOSDAQ).",
            },
            "amount_qty_type": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Amount/quantity type (0:amount, 1:quantity).",
            },
            "base_date": {"type": "string", "description": "Base date (YYYYMMDD)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["market_type", "amount_qty_type", "base_date", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.sector",
    broker="kiwoom",
)
def handle_kiwoom_sector_investor_net_buy(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.sector.get_industry_investor_net_buy(
        params["market_type"],
        params["amount_qty_type"],
        params["base_date"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Current Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.sector.current_price",
    description="Get current price for an industry sector.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Market type (0:KOSPI, 1:KOSDAQ, 2:KOSPI200).",
            },
            "industry_code": {"type": "string", "description": "Industry code (e.g. 001:KOSPI composite)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["market_type", "industry_code"],
    },
    returns={"type": "object"},
    category="kiwoom.sector",
    broker="kiwoom",
)
def handle_kiwoom_sector_current_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.sector.get_industry_current_price(
        params["market_type"],
        params["industry_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Industry Price by Sector
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.sector.price_by_sector",
    description="Get stock prices grouped by industry sector.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Market type (0:KOSPI, 1:KOSDAQ, 2:KOSPI200).",
            },
            "industry_code": {"type": "string", "description": "Industry code (e.g. 001:KOSPI composite)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined).",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["market_type", "industry_code", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.sector",
    broker="kiwoom",
)
def handle_kiwoom_sector_price_by_sector(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.sector.get_industry_price_by_sector(
        params["market_type"],
        params["industry_code"],
        params["exchange_type"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# All Industry Index
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.sector.all_index",
    description="Get all industry index data.",
    parameters={
        "type": "object",
        "properties": {
            "industry_code": {
                "type": "string",
                "description": "Industry code (001:KOSPI, 101:KOSDAQ, 201:KOSPI200, etc.)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["industry_code"],
    },
    returns={"type": "object"},
    category="kiwoom.sector",
    broker="kiwoom",
)
def handle_kiwoom_sector_all_index(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.sector.get_all_industry_index(
        params["industry_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Daily Industry Current Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.sector.daily_current_price",
    description="Get daily current price for an industry sector.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Market type (0:KOSPI, 1:KOSDAQ, 2:KOSPI200).",
            },
            "industry_code": {"type": "string", "description": "Industry code (e.g. 001:KOSPI composite)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Pagination key. Default empty."},
        },
        "required": ["market_type", "industry_code"],
    },
    returns={"type": "object"},
    category="kiwoom.sector",
    broker="kiwoom",
)
def handle_kiwoom_sector_daily_current_price(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.sector.get_daily_industry_current_price(
        params["market_type"],
        params["industry_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_sector_program,
    handle_kiwoom_sector_investor_net_buy,
    handle_kiwoom_sector_current_price,
    handle_kiwoom_sector_price_by_sector,
    handle_kiwoom_sector_all_index,
    handle_kiwoom_sector_daily_current_price,
]


def register_kiwoom_sector_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
