from __future__ import annotations

from cluefin_openapi_cli.handlers.kiwoom.domestic_chart import _ALL_HANDLERS as CHART_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_etf import _ALL_HANDLERS as ETF_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_foreign import _ALL_HANDLERS as FOREIGN_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_market_condition import _ALL_HANDLERS as MARKET_CONDITION_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_rank_info import _ALL_HANDLERS as RANK_INFO_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_sector import _ALL_HANDLERS as SECTOR_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_stock_info import _ALL_HANDLERS as STOCK_INFO_HANDLERS
from cluefin_openapi_cli.handlers.kiwoom.domestic_theme import _ALL_HANDLERS as THEME_HANDLERS


def get_kiwoom_handlers():
    return [
        *CHART_HANDLERS,
        *ETF_HANDLERS,
        *FOREIGN_HANDLERS,
        *MARKET_CONDITION_HANDLERS,
        *RANK_INFO_HANDLERS,
        *SECTOR_HANDLERS,
        *STOCK_INFO_HANDLERS,
        *THEME_HANDLERS,
    ]
