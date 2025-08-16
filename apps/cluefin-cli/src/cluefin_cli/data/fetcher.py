import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pandas as pd
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from pydantic import SecretStr

from cluefin_cli.config.settings import settings


class DataFetcher:
    """Handles data fetching from Kiwoom Securities and KRX APIs."""

    def __init__(self):
        if not settings.kiwoom_app_key:
            raise ValueError("KIWOOM_APP_KEY environment variable is required")
        if not settings.kiwoom_secret_key:
            raise ValueError("KIWOOM_SECRET_KEY environment variable is required")

        auth = KiwoomAuth(
            app_key=settings.kiwoom_app_key,
            secret_key=SecretStr(settings.kiwoom_secret_key),
            env="dev",
        )
        token = auth.generate_token()
        self.kiwoom_client = KiwoomClient(
            token=token.get_token(),
            env="dev",
        )

    async def get_basic_data(self, stock_code: str):
        """
        Fetch basic data in company

        Args:
            stock_code: Korean stock code (e.g., "005930" for Samsung)

        Returns:
            DataFrame with basic data
        """
        stock_info = self.kiwoom_client.stock_info.get_stock_info(stock_code)
        stock_info_v1 = self.kiwoom_client.stock_info.get_stock_info_v1(stock_code)

        # Merge both stock info responses into a single dictionary
        merged_data = {}

        # Add fields from stock_info (DomesticStockInfoBasic)
        info_dict = stock_info.body
        merged_data.update(
            {
                "stock_code": info_dict.stk_cd,
                "stock_name": info_dict.stk_nm,
                "settlement_month": info_dict.setl_mm,
                "face_value": info_dict.fav,
                "capital": info_dict.cap,
                "floating_stock": info_dict.flo_stk,
                "distribution_stock": info_dict.dstr_stk,
                "distribution_ratio": info_dict.dstr_rt,
                "credit_ratio": info_dict.crd_rt,
                "market_cap": info_dict.mac,
                "market_cap_weight": info_dict.mac_wght,
                "foreign_exhaustion_rate": info_dict.for_exh_rt,
                "substitute_price": info_dict.repl_pric,
                "per": info_dict.per,
                "eps": info_dict.eps,
                "roe": info_dict.roe,
                "pbr": info_dict.pbr,
                "ev": info_dict.ev,
                "bps": info_dict.bps,
                "revenue": info_dict.sale_amt,
                "operating_profit": info_dict.open_pric,
                "net_profit": info_dict.cup_nga,
                "250_day_high": info_dict.hgst_250,
                "250hgst_pric_pre_rt": info_dict.hgst_prict_250pre_rt,
                "250_day_low": info_dict.lwst_250,
                "250lwst_pric_pre_rt": info_dict.lwst_prict_250pre_rt,
            }
        )

        # Add additional fields from stock_info_v1 (DomesticStockInfoBasicV1)
        info_v1_dict = stock_info_v1.body

        merged_data.update(
            {
                "list_count": info_v1_dict.listCount,
                "registration_day": info_v1_dict.regDay,
                "state": info_v1_dict.state,
                "market_name": info_v1_dict.marketName,
                "sector_name": info_v1_dict.upName,
                "order_warning": info_v1_dict.orderWarning,
                "nxt_enabled": info_v1_dict.nxtEnable,
            }
        )

        # Create DataFrame with a single row
        df = pd.DataFrame([merged_data])

        return df

    async def get_stock_data(self, stock_code: str, period: str = "3M") -> pd.DataFrame:
        """
        Fetch stock price data for the given period.

        Args:
            stock_code: Korean stock code (e.g., "005930" for Samsung)
            period: Data period (1M, 3M, 6M, 1Y)

        Returns:
            DataFrame with OHLCV data
        """
        # For now, always use mock data
        # TODO: Implement Kiwoom API integration when ready
        return self._generate_mock_data(stock_code, period)

    async def get_foreign_trading(self, stock_code: str) -> Dict[str, Any]:
        """
        Fetch foreign trading data for the stock.

        Args:
            stock_code: Korean stock code

        Returns:
            Dict with foreign buy/sell amounts
        """
        # For now, use mock data
        # TODO: Implement Kiwoom API integration
        # self.kiwoom_client.foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner()
        return self._generate_mock_foreign_data()

    async def get_kospi_data(self) -> Dict[str, Any]:
        """Fetch KOSPI index data."""
        # For now, return mock data since KRX client is not implemented yet
        import random

        base_value = 2500.0
        change = random.uniform(-1.5, 1.5)
        return {"value": base_value + (base_value * change / 100), "change": change}

    async def get_kosdaq_data(self) -> Dict[str, Any]:
        """Fetch KOSDAQ index data."""
        # For now, return mock data since KRX client is not implemented yet
        import random

        base_value = 850.0
        change = random.uniform(-2.0, 2.0)
        return {"value": base_value + (base_value * change / 100), "change": change}

    def _generate_mock_data(self, stock_code: str, period: str) -> pd.DataFrame:
        """Generate mock stock data for testing."""
        days_map = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365}
        days = days_map.get(period, 90)

        # Base price varies by stock code
        base_prices = {
            "005930": 70000,  # Samsung Electronics
            "000660": 50000,  # SK Hynix
            "035420": 300000,  # NAVER
            "051910": 900000,  # LG Chemical
        }
        base_price = base_prices.get(stock_code, 50000)

        dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq="D")

        # Generate realistic price movements
        import numpy as np

        np.random.seed(int(stock_code) if stock_code.isdigit() else 42)

        price_changes = np.random.normal(0, 0.02, len(dates))
        prices = [base_price]

        for change in price_changes[1:]:
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, base_price * 0.5))  # Prevent unrealistic drops

        data = []
        for i, date in enumerate(dates):
            price = prices[i]
            daily_volatility = np.random.normal(0, 0.01)

            high = price * (1 + abs(daily_volatility))
            low = price * (1 - abs(daily_volatility))
            open_price = price * (1 + np.random.normal(0, 0.005))

            data.append(
                {
                    "date": date,
                    "open": open_price,
                    "high": high,
                    "low": low,
                    "close": price,
                    "volume": np.random.randint(100000, 10000000),
                }
            )

        df = pd.DataFrame(data)
        df.set_index("date", inplace=True)
        return df

    def _generate_mock_foreign_data(self) -> Dict[str, Any]:
        """Generate mock foreign trading data."""
        import random

        buy_amount = random.randint(1000000000, 10000000000)  # 1B - 10B KRW
        sell_amount = random.randint(1000000000, 10000000000)

        return {"buy": buy_amount, "sell": sell_amount}
