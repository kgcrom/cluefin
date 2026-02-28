"""RPC handlers for Kiwoom DomesticTheme API (2 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_body, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Theme Group
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.theme.group",
    description="Get theme group data from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "query_type": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Search type (0:all, 1:by theme name, 2:by stock code)",
            },
            "date_type": {
                "type": "string",
                "description": "Date type (n days ago, 1~99 days)",
            },
            "theme_name": {"type": "string", "description": "Theme name to search"},
            "fluctuation_type": {
                "type": "string",
                "enum": ["1", "2", "3", "4"],
                "description": "Fluctuation type (1:top period return, 2:bottom period return, 3:top change rate, 4:bottom change rate)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined)",
            },
            "stock_code": {"type": "string", "description": "Stock code to search. Default empty."},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["query_type", "date_type", "theme_name", "fluctuation_type", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.theme",
    broker="kiwoom",
)
def handle_kiwoom_theme_group(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.theme.get_theme_group(
        qry_tp=params["query_type"],
        date_tp=params["date_type"],
        thema_nm=params["theme_name"],
        flu_pl_amt_tp=params["fluctuation_type"],
        stex_tp=params["exchange_type"],
        stk_cd=params.get("stock_code", ""),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Theme Group Stocks
# ---------------------------------------------------------------------------


@rpc_method(
    name="kiwoom.theme.group_stocks",
    description="Get stocks belonging to a theme group from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "theme_group_code": {"type": "string", "description": "Theme group code"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange type (1:KRX, 2:NXT, 3:combined)",
            },
            "date_type": {"type": "string", "description": "Date type (n days ago, 1~99 days). Default empty."},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["theme_group_code", "exchange_type"],
    },
    returns={"type": "object"},
    category="kiwoom.theme",
    broker="kiwoom",
)
def handle_kiwoom_theme_group_stocks(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.theme.get_theme_group_stocks(
        thema_grp_cd=params["theme_group_code"],
        stex_tp=params["exchange_type"],
        date_tp=params.get("date_type", ""),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_theme_group,
    handle_kiwoom_theme_group_stocks,
]


def register_kiwoom_theme_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
