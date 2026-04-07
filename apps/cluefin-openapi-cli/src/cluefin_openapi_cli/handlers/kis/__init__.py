from __future__ import annotations

from cluefin_openapi_cli.handlers.kis.domestic_basic_quote import _ALL_HANDLERS as BASIC_QUOTE_HANDLERS
from cluefin_openapi_cli.handlers.kis.domestic_issue_other import _ALL_HANDLERS as ISSUE_OTHER_HANDLERS
from cluefin_openapi_cli.handlers.kis.domestic_market_analysis import _ALL_HANDLERS as MARKET_ANALYSIS_HANDLERS
from cluefin_openapi_cli.handlers.kis.domestic_ranking_analysis import _ALL_HANDLERS as RANKING_HANDLERS
from cluefin_openapi_cli.handlers.kis.domestic_stock_info import _ALL_HANDLERS as STOCK_INFO_HANDLERS


def get_kis_handlers():
    return [
        *BASIC_QUOTE_HANDLERS,
        *ISSUE_OTHER_HANDLERS,
        *STOCK_INFO_HANDLERS,
        *MARKET_ANALYSIS_HANDLERS,
        *RANKING_HANDLERS,
    ]
