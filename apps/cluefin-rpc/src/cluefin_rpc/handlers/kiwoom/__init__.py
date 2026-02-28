from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


def register_kiwoom_handlers(dispatcher: Dispatcher) -> None:
    from cluefin_rpc.handlers.kiwoom.domestic_chart import register_kiwoom_chart_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_etf import register_kiwoom_etf_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_foreign import register_kiwoom_foreign_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_market_condition import register_kiwoom_market_condition_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_rank_info import register_kiwoom_rank_info_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_sector import register_kiwoom_sector_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_stock_info import register_kiwoom_stock_info_handlers
    from cluefin_rpc.handlers.kiwoom.domestic_theme import register_kiwoom_theme_handlers

    register_kiwoom_chart_handlers(dispatcher)
    register_kiwoom_etf_handlers(dispatcher)
    register_kiwoom_foreign_handlers(dispatcher)
    register_kiwoom_market_condition_handlers(dispatcher)
    register_kiwoom_rank_info_handlers(dispatcher)
    register_kiwoom_sector_handlers(dispatcher)
    register_kiwoom_stock_info_handlers(dispatcher)
    register_kiwoom_theme_handlers(dispatcher)
