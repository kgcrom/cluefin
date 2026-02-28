"""RPC handlers for Kiwoom DomesticForeign API (3 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Foreign Investor Trading Trend by Stock
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.foreign.investor_trading_trend",
    description="Get foreign investor trading trend by stock from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kiwoom.foreign",
    broker="kiwoom",
)
def handle_kiwoom_foreign_investor_trading_trend(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.foreign.get_foreign_investor_trading_trend_by_stock(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Institution
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.foreign.stock_institution",
    description="Get stock institution data from Kiwoom.",
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
    category="kiwoom.foreign",
    broker="kiwoom",
)
def handle_kiwoom_stock_institution(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.foreign.get_stock_institution(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Consecutive Net Buy/Sell Status by Institution/Foreigner
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.foreign.consecutive_net_buy_sell",
    description="Get consecutive net buy/sell status by institution and foreigner from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "period": {
                "type": "string",
                "enum": ["1", "3", "5", "10", "20", "120", "0"],
                "description": "Period (1/3/5/10/20/120 days, 0:custom range)",
            },
            "market_type": {
                "type": "string",
                "enum": ["001", "101"],
                "description": "Market type (001:KOSPI, 101:KOSDAQ)",
            },
            "stock_industry_type": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Stock/industry type (0:stock, 1:industry)",
            },
            "amount_qty_type": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Amount/quantity type (0:amount, 1:quantity)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined)",
            },
            "net_sell_buy_type": {
                "type": "string",
                "enum": ["2"],
                "description": "Net sell/buy type. Default 2.",
            },
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD). Default empty."},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD). Default empty."},
        },
        "required": ["period", "market_type", "stock_industry_type", "amount_qty_type", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.foreign",
    broker="kiwoom",
)
def handle_kiwoom_consecutive_net_buy_sell(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner(
        dt=params["period"],
        mrkt_tp=params["market_type"],
        stk_inds_tp=params["stock_industry_type"],
        amt_qty_tp=params["amount_qty_type"],
        stex_tp=params["exchange_type"],
        netslmt_tp=params.get("net_sell_buy_type", "2"),
        strt_dt=params.get("start_date", ""),
        end_dt=params.get("end_date", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_foreign_investor_trading_trend,
    handle_kiwoom_stock_institution,
    handle_kiwoom_consecutive_net_buy_sell,
]


def register_kiwoom_foreign_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
