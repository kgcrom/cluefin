from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


def register_kis_handlers(dispatcher: Dispatcher) -> None:
    from cluefin_rpc.handlers.kis.domestic_basic_quote import register_kis_basic_quote_handlers
    from cluefin_rpc.handlers.kis.domestic_issue_other import register_kis_issue_other_handlers
    from cluefin_rpc.handlers.kis.domestic_market_analysis import register_kis_market_analysis_handlers
    from cluefin_rpc.handlers.kis.domestic_ranking_analysis import register_kis_ranking_handlers
    from cluefin_rpc.handlers.kis.domestic_stock_info import register_kis_stock_info_handlers

    register_kis_basic_quote_handlers(dispatcher)
    register_kis_issue_other_handlers(dispatcher)
    register_kis_stock_info_handlers(dispatcher)
    register_kis_market_analysis_handlers(dispatcher)
    register_kis_ranking_handlers(dispatcher)
