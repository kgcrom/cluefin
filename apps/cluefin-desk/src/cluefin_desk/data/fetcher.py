from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from pydantic import SecretStr

from cluefin_desk.config.settings import settings


class DomesticDataFetcher:
    """Handles domestic stock data fetching from Kiwoom Securities API."""

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

    # ──────────────────────────────────────
    # Basic stock data
    # ──────────────────────────────────────

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

    # ──────────────────────────────────────
    # Rankings (existing)
    # ──────────────────────────────────────

    def get_top_percentage_change(self, sort_tp: str = "1"):
        return self.kiwoom_client.rank_info.get_top_percentage_change_from_previous_day(
            mrkt_tp="000",
            sort_tp=sort_tp,
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

    # ──────────────────────────────────────
    # Rankings (new)
    # ──────────────────────────────────────

    def get_top_foreigner_period_trading(self, trde_tp: str = "1"):
        return self.kiwoom_client.rank_info.get_top_foreigner_period_trading(
            mrkt_tp="000",
            trde_tp=trde_tp,
            dt="1",
            stex_tp="1",
        )

    def get_new_high_low_price(self, ntl_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_new_high_low_price(
            mrkt_tp="000",
            ntl_tp=ntl_tp,
            high_low_close_tp="1",
            stk_cnd="4",
            trde_qty_tp="0",
            crd_cnd="0",
            updown_incls="0",
            dt="1",
            stex_tp="1",
        )

    def get_price_volatility(self, flu_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_price_volatility(
            mrkt_tp="000",
            flu_tp=flu_tp,
            tm_tp="1",
            tm="60",
            trde_qty_tp="00000",
            stk_cnd="1",
            crd_cnd="0",
            pric_cnd="8",
            updown_incls="0",
            stex_tp="1",
        )

    def get_top_margin_ratio(self):
        return self.kiwoom_client.rank_info.get_top_margin_ratio(
            mrkt_tp="000",
            trde_qty_tp="0",
            stk_cnd="4",
            updown_incls="0",
            crd_cnd="0",
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Sector / Industry
    # ──────────────────────────────────────

    def get_all_industry_index(self, inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_all_industry_index(inds_cd=inds_cd)

    def get_industry_current_price(self, mrkt_tp: str = "0001", inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_industry_current_price(
            mrkt_tp=mrkt_tp,
            inds_cd=inds_cd,
        )

    def get_industry_price_by_sector(self, mrkt_tp: str = "0001", inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_industry_price_by_sector(
            mrkt_tp=mrkt_tp,
            inds_cd=inds_cd,
            stex_tp="1",
        )

    def get_daily_industry_current_price(self, mrkt_tp: str = "0001", inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_daily_industry_current_price(
            mrkt_tp=mrkt_tp,
            inds_cd=inds_cd,
        )

    def get_industry_investor_net_buy(self, mrkt_tp: str = "0001", amt_qty_tp: str = "1"):
        return self.kiwoom_client.sector.get_industry_investor_net_buy(
            mrkt_tp=mrkt_tp,
            amt_qty_tp=amt_qty_tp,
            base_dt=datetime.now().strftime("%Y%m%d"),
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Theme
    # ──────────────────────────────────────

    def get_theme_group(self):
        return self.kiwoom_client.theme.get_theme_group(
            qry_tp="0",
            date_tp="1",
            thema_nm="",
            flu_pl_amt_tp="1",
            stex_tp="1",
        )

    def get_theme_group_stocks(self, thema_grp_cd: str):
        return self.kiwoom_client.theme.get_theme_group_stocks(
            thema_grp_cd=thema_grp_cd,
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # ETF
    # ──────────────────────────────────────

    def get_etf_full_price(self):
        return self.kiwoom_client.etf.get_etf_full_price(
            txon_type="0",
            navpre="0",
            mngmcomp="0",
            txon_yn="0",
            trace_idex="0",
            stex_tp="1",
        )

    def get_etf_return_rate(self, stk_cd: str, etfobjt_idex_cd: str = "0", dt: int = 0):
        return self.kiwoom_client.etf.get_etf_return_rate(
            stk_cd=stk_cd,
            etfobjt_idex_cd=etfobjt_idex_cd,
            dt=dt,
        )

    def get_etf_item_info(self, stk_cd: str):
        return self.kiwoom_client.etf.get_etf_item_info(stk_cd=stk_cd)

    def get_etf_daily_trend(self, stk_cd: str):
        return self.kiwoom_client.etf.get_etf_daily_trend(stk_cd=stk_cd)

    # ──────────────────────────────────────
    # Investor Flow
    # ──────────────────────────────────────

    def get_top_intraday_trading_by_investor(self, trde_tp: str = "1", orgn_tp: str = "1000"):
        return self.kiwoom_client.rank_info.get_top_intraday_trading_by_investor(
            trde_tp=trde_tp,
            mrkt_tp="000",
            orgn_tp=orgn_tp,
        )

    def get_top_50_program_net_buy(self, trde_upper_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_top_50_program_net_buy(
            trde_upper_tp=trde_upper_tp,
            amt_qty_tp="1",
            mrkt_tp="000",
            stex_tp="1",
        )

    def get_program_trading_status_by_stock(self):
        return self.kiwoom_client.stock_info.get_program_trading_status_by_stock(
            dt=datetime.now().strftime("%Y%m%d"),
            mrkt_tp="000",
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Stock Detail (extended)
    # ──────────────────────────────────────

    def get_institutional_investor_by_stock(self, stk_cd: str, amt_qty_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_institutional_investor_by_stock(
            dt=datetime.now().strftime("%Y%m%d"),
            stk_cd=stk_cd,
            amt_qty_tp=amt_qty_tp,
            trde_tp="0",
            unit_tp="1",
        )

    def get_stock_trading_member(self, stk_cd: str):
        return self.kiwoom_client.stock_info.get_stock_trading_member(stk_cd=stk_cd)

    def get_stock_specific_securities_firm_ranking(self, stk_cd: str):
        today = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
        return self.kiwoom_client.rank_info.get_stock_specific_securities_firm_ranking(
            stk_cd=stk_cd,
            strt_dt=start,
            end_dt=today,
            qry_tp="0",
        )

    def get_margin_trading_trend(self, stk_cd: str):
        return self.kiwoom_client.stock_info.get_margin_trading_trend(
            stk_cd=stk_cd,
            dt=datetime.now().strftime("%Y%m%d"),
            qry_tp="0",
        )

    def get_supply_demand_concentration(self):
        return self.kiwoom_client.stock_info.get_supply_demand_concentration(
            mrkt_tp="000",
            prps_cnctr_rt="5",
            cur_prc_entry="0",
            prpscnt="0",
            cycle_tp="0",
            stex_tp="1",
        )
