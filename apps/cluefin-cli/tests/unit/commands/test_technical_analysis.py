from __future__ import annotations

import pandas as pd

from cluefin_cli.commands.technical_analysis import (
    _display_company_info,
    _display_stock_info,
    _display_technical_indicators,
    _display_trading_trend,
)

# ---------------------------------------------------------------------------
# _display_company_info
# ---------------------------------------------------------------------------


def test_display_company_info_empty() -> None:
    _display_company_info("005930", pd.DataFrame())


def test_display_company_info_full() -> None:
    data = pd.DataFrame(
        [
            {
                "stock_name": "삼성전자",
                "settlement_month": "12",
                "industry_name": "반도체",
                "registration_day": "19750611",
                "sector_name": "전기전자",
                "distribution_stock": "100000",
                "distribution_ratio": "10.5",
                "floating_stock": "900000",
                "company_size": "대형주",
                "market_cap": "4000000",
                "per": "15.2",
                "eps": "5000",
                "pbr": "1.5",
                "roe": "12.3",
                "bps": "45000",
                "revenue": "3000000",
                "operating_profit": "500000",
                "net_profit": "400000",
                "250_day_high": "80000",
                "250hgst_pric_pre_rt": "-5.2",
                "250_day_low": "60000",
                "250lwst_pric_pre_rt": "10.1",
                "foreign_exhaustion_rate": "45.0",
                "order_warning": "3",
            }
        ]
    )
    _display_company_info("005930", data)


# ---------------------------------------------------------------------------
# _display_stock_info
# ---------------------------------------------------------------------------


def test_display_stock_info_empty() -> None:
    _display_stock_info("005930", pd.DataFrame())


def test_display_stock_info_single_row() -> None:
    data = pd.DataFrame({"close": [70000.0], "volume": [1000.0]})
    _display_stock_info("005930", data)


def test_display_stock_info_multi_row_negative_change() -> None:
    data = pd.DataFrame({"close": [71000.0, 70000.0], "volume": [1000.0, 1200.0]})
    _display_stock_info("005930", data)


# ---------------------------------------------------------------------------
# _display_trading_trend
# ---------------------------------------------------------------------------


def test_display_trading_trend_empty() -> None:
    _display_trading_trend(None)
    _display_trading_trend({})


def test_display_trading_trend_with_data() -> None:
    _display_trading_trend({"개인": "-1000", "외국인": "1500", "기관": "N/A"})


# ---------------------------------------------------------------------------
# _display_technical_indicators
# ---------------------------------------------------------------------------


def test_display_technical_indicators_full() -> None:
    indicators = pd.DataFrame(
        {
            "close": [70000.0],
            "rsi": [75.0],
            "macd": [1.5],
            "macd_signal": [1.0],
            "sma_20": [69000.0],
            "sma_50": [68000.0],
            "sma_120": [67000.0],
            "sma_240": [66000.0],
        }
    )
    _display_technical_indicators(indicators)
