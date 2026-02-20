from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from cluefin_openapi.krx._client import Client as KrxClient
from loguru import logger
from pydantic import SecretStr

from cluefin_desk.config.settings import settings


class DomesticDataFetcher:
    """Handles domestic stock data fetching from Kiwoom Securities and KRX APIs."""

    @staticmethod
    def _safe_float(value: str) -> float:
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

    async def get_basic_data(self, stock_code: str) -> pd.DataFrame:
        stock_info = self.kiwoom_client.stock_info.get_stock_info(stock_code)
        stock_info_v1 = self.kiwoom_client.stock_info.get_stock_info_v1(stock_code)

        info = stock_info.body
        info_v1 = stock_info_v1.body

        merged_data = {
            "stock_code": info.stk_cd,
            "stock_name": info.stk_nm,
            "market_cap": info.mac,
            "per": info.per,
            "eps": info.eps,
            "roe": info.roe,
            "pbr": info.pbr,
            "bps": info.bps,
            "sector_name": info_v1.upName,
            "market_name": info_v1.marketName,
        }
        return pd.DataFrame([merged_data])

    async def get_stock_data(self, stock_code: str) -> pd.DataFrame:
        parsed_date = datetime.now().strftime("%Y%m%d")
        max_pages = 3
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
            df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])

        return df

    def _get_latest_krx_index_base_date(self) -> str:
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
        try:
            base_date = self._get_latest_krx_index_base_date()
            response = self.krx_client.index.get_kospi(base_date=base_date)

            target_indices = ["코스피", "코스피 200"]
            filtered_data = filter(lambda item: item.index_name in target_indices, response.body.data)

            return list(
                map(
                    lambda item: {
                        "name": item.index_name,
                        "close_price": self._safe_float(item.close_price_index),
                        "fluctuation_rate": self._safe_float(item.fluctuation_rate),
                    },
                    filtered_data,
                )
            )
        except Exception:
            return [{"name": "코스피", "close_price": 0.0, "fluctuation_rate": 0.0}]

    async def get_kosdaq_index_series(self) -> List[Dict[str, Any]]:
        try:
            base_date = self._get_latest_krx_index_base_date()
            response = self.krx_client.index.get_kosdaq(base_date=base_date)

            target_indices = ["코스닥", "코스닥 150"]
            filtered_data = filter(lambda item: item.index_name in target_indices, response.body.data)

            return list(
                map(
                    lambda item: {
                        "name": item.index_name,
                        "close_price": self._safe_float(item.close_price_index),
                        "fluctuation_rate": self._safe_float(item.fluctuation_rate),
                    },
                    filtered_data,
                )
            )
        except Exception:
            return [{"name": "코스닥", "close_price": 0.0, "fluctuation_rate": 0.0}]

    def get_top_percentage_change(self):
        return self.kiwoom_client.rank_info.get_top_percentage_change_from_previous_day(
            mrkt_tp="000",
            sort_tp="1",
            trde_qty_cnd="0000",
            stk_cnd="4",
            crd_cnd="0",
            updown_incls="0",
            pric_cnd="8",
            trde_prica_cnd="10",
            stex_tp="1",
        )

    def get_top_trading_volume(self):
        return self.kiwoom_client.rank_info.get_top_current_day_trading_volume(
            mrkt_tp="000",
            sort_tp="1",
            mang_stk_incls="4",
            crd_tp="0",
            trde_qty_tp="0",
            pric_tp="2",
            trde_prica_tp="10",
            mrkt_open_tp="0",
            stex_tp="1",
        )

    def get_top_transaction_value(self):
        return self.kiwoom_client.rank_info.get_top_transaction_value(
            mrkt_tp="000",
            mang_stk_incls="0",
            stex_tp="1",
        )
