from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from cluefin_openapi.krx._client import Client as KrxClient
from loguru import logger
from pydantic import SecretStr

from cluefin_cli.config.settings import settings


class DomesticDataFetcher:
    """Handles domestic stock data fetching from Kiwoom Securities and KRX APIs."""

    @staticmethod
    def _safe_float(value: str) -> float:
        """Safely convert string to float, returning 0 if value is '-' or invalid."""
        if value == "-" or not value or value.strip() == "":
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def __init__(self):
        if not settings.kiwoom_app_key:
            raise ValueError("KIWOOM_APP_KEY environment variable is required")
        if not settings.kiwoom_secret_key:
            raise ValueError("KIWOOM_SECRET_KEY environment variable is required")
        if not settings.kiwoom_env:
            raise ValueError("KIWOOM_ENV environment variable is required")

        auth = KiwoomAuth(
            app_key=settings.kiwoom_app_key,
            secret_key=SecretStr(settings.kiwoom_secret_key),
            env=settings.kiwoom_env,
        )
        token = auth.generate_token()
        self.kiwoom_client = KiwoomClient(
            token=token.get_token(),
            env=settings.kiwoom_env,
        )
        self.krx_client = KrxClient(
            auth_key=settings.krx_auth_key or "",
        )
        self._krx_index_base_date = None

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
                "250hgst_pric_pre_rt": info_dict.hgst_pric_pre_rt_250,
                "250_day_low": info_dict.lwst_250,
                "250lwst_pric_pre_rt": info_dict.lwst_pric_pre_rt_250,
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

    async def get_stock_data(self, stock_code: str, period: str) -> pd.DataFrame:
        """
        Fetch stock price data for the given period.

        Args:
            stock_code: Korean stock code (e.g., "005930" for Samsung)
            period: Data period (1D, 1W)

        Returns:
            DataFrame with OHLCV data
        """
        # return self._generate_mock_data(stock_code, period)
        # TODO: 주봉, 월봉도 같은 함수에서 리턴가능하도록. 타입먼저 처리해야한다.
        parsed_date = datetime.now().strftime("%Y%m%d")
        max_pages = 3  # Fetch ~300 trading days via continuation
        cont_yn = "N"
        next_key = ""
        rows: List[Dict[str, Any]] = []

        for _ in range(max_pages):
            response = self.kiwoom_client.chart.get_stock_daily(
                stk_cd=stock_code,
                base_dt=parsed_date,
                upd_stkpc_tp="1",
                cont_yn=cont_yn,
                next_key=next_key,
            )

            items = response.body.stk_dt_pole_chart_qry
            if not items:
                break

            rows.extend(
                {
                    "date": pd.to_datetime(item.dt),
                    "open": self._safe_float(item.open_pric),
                    "high": self._safe_float(item.high_pric),
                    "low": self._safe_float(item.low_pric),
                    "close": self._safe_float(item.cur_prc),
                    "volume": self._safe_float(item.trde_qty),
                }
                for item in items
            )

            cont_yn = response.headers.cont_yn
            next_key = response.headers.next_key
            if cont_yn != "Y" or not next_key:
                break

        if rows:
            df = pd.DataFrame(rows)
            df.set_index("date", inplace=True)
            df.sort_index(inplace=True)
            df = df[~df.index.duplicated(keep="last")]
        else:
            # Fallback to empty DataFrame if no data available
            df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume", "timeframe"])

        return df

    def _get_latest_krx_index_base_date(self) -> str:
        """Find the latest KRX index trading date by probing recent business days."""
        if self._krx_index_base_date:
            return self._krx_index_base_date

        today = datetime.now().date()
        for offset in range(0, 31):
            candidate = today - timedelta(days=offset)
            if candidate.weekday() >= 5:
                continue

            candidate_str = candidate.strftime("%Y%m%d")
            try:
                response = self.krx_client.index.get_kospi(base_date=candidate_str)
            except Exception as e:
                logger.error(f"KRX API failed for date {candidate_str}: {e}")
                continue

            if response and response.body and response.body.data:
                self._krx_index_base_date = candidate_str
                return candidate_str

        self._krx_index_base_date = today.strftime("%Y%m%d")
        return self._krx_index_base_date

    async def get_kospi_index_series(self) -> List[Dict[str, Any]]:
        """Return KOSPI index series with name, close_price, fluctuation_rate, trading_value, and transaction_amount."""

        try:
            base_date = self._get_latest_krx_index_base_date()
            response = self.krx_client.index.get_kospi(base_date=base_date)

            # Filter for specific KOSPI indices
            target_indices = ["코스피", "코스피 200", "코스피 200 중소형주", "코스피 200제외 코스피지수"]
            filtered_data = filter(lambda item: item.index_name in target_indices, response.body.data)

            # Extract data from response using map with lambda
            index_data = list(
                map(
                    lambda item: {
                        "name": item.index_name,
                        "close_price": self._safe_float(item.close_price_index),
                        "fluctuation_rate": self._safe_float(item.fluctuation_rate),
                        "trading_value": self._safe_float(item.accumulated_trading_value),
                        "transaction_amount": self._safe_float(item.accumulated_trading_volume),
                    },
                    filtered_data,
                )
            )

            return index_data
        except Exception:
            # Fallback to mock data if API call fails
            return [
                {
                    "name": "KOSPI",
                    "close_price": 2500.0,
                    "fluctuation_rate": 1.5,
                    "trading_value": 15000000000.0,
                    "transaction_amount": 500000000.0,
                }
            ]

    async def get_kosdaq_index_series(self) -> List[Dict[str, Any]]:
        """Fetch KOSDAQ index data."""

        try:
            # KRX 데이터 집계는 익일 오전 8시에 업데이트
            # TODO 실시간으로 조회 가능한 방법 찾아서 교체하기
            base_date = self._get_latest_krx_index_base_date()
            response = self.krx_client.index.get_kosdaq(base_date=base_date)

            # Filter for specific KOSDAQ indices
            target_indices = ["코스닥", "코스닥 150"]
            filtered_data = filter(lambda item: item.index_name in target_indices, response.body.data)

            # Extract data from response using map with lambda
            index_data = list(
                map(
                    lambda item: {
                        "name": item.index_name,
                        "close_price": self._safe_float(item.close_price_index),
                        "fluctuation_rate": self._safe_float(item.fluctuation_rate),
                        "trading_value": self._safe_float(item.accumulated_trading_value),
                        "transaction_amount": self._safe_float(item.accumulated_trading_volume),
                    },
                    filtered_data,
                )
            )

            return index_data
        except Exception:
            # Fallback to mock data if API call fails
            return [
                {
                    "name": "KOSPI",
                    "close_price": 2500.0,
                    "fluctuation_rate": 1.5,
                    "trading_value": 15000000000.0,
                    "transaction_amount": 500000000.0,
                }
            ]

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

    async def get_trading_trend(self, stock_code: str) -> Dict[str, str]:
        """
        Fetch trading trend data for the given stock.

        Args:
            stock_code: Korean stock code (e.g., "005930" for Samsung)

        Returns:
            Trading trend data
        """

        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
        end_date = datetime.now().strftime("%Y%m%d")

        response = self.kiwoom_client.stock_info.get_total_institutional_investor_by_stock(
            stk_cd=stock_code,
            strt_dt=start_date,
            end_dt=end_date,
            amt_qty_tp="1",
            trde_tp="0",
            unit_tp="1",
        )

        if len(response.body.stk_invsr_orgn_tot) == 0:
            raise ValueError(f"No trading trend data available for stock code {stock_code}")

        item = response.body.stk_invsr_orgn_tot[0]
        return {
            "개인투자자": item.ind_invsr[1:] if item.ind_invsr.startswith("--") else item.ind_invsr,
            "외국인투자자": item.frgnr_invsr[1:] if item.frgnr_invsr.startswith("--") else item.frgnr_invsr,
            "기관계": item.orgn[1:] if item.orgn.startswith("--") else item.orgn,
            "금융투자": item.fnnc_invt[1:] if item.fnnc_invt.startswith("--") else item.fnnc_invt,
            "투신": item.invtrt[1:] if item.invtrt.startswith("--") else item.invtrt,
            "연기금": item.penfnd_etc[1:] if item.penfnd_etc.startswith("--") else item.penfnd_etc,
        }
