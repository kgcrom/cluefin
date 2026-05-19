"""Kiwoom provider adapter."""

from __future__ import annotations

from datetime import date
from typing import Any

from cluefin_cli.domains.models import OhlcvPoint, OhlcvSeries, TradingFlowSnapshot
from cluefin_cli.domains.providers.base import BrokerProvider


class KiwoomProvider(BrokerProvider):
    broker = "kiwoom"

    def fetch_ohlcv(self, *, stock_code: str, interval: str = "daily", days: int = 300) -> OhlcvSeries:
        chart = self.client.chart
        if interval == "minute":
            response = chart.get_stock_minute(stk_cd=stock_code, tic_scope="1", upd_stkpc_tp="1")
            items = getattr(response.body, "stk_min_pole_chart_qry", [])
            points = [self._ohlcv_from_minute(item) for item in items]
        else:
            response = chart.get_stock_daily(
                stk_cd=stock_code,
                base_dt=date.today().strftime("%Y%m%d"),
                upd_stkpc_tp="1",
            )
            items = getattr(response.body, "stk_dt_pole_chart_qry", [])
            points = [self._ohlcv_from_daily(item) for item in items]

        points = sorted(points, key=lambda item: item.timestamp)[-days:]
        return OhlcvSeries(stock_code=stock_code.zfill(6), source="kiwoom", interval=interval, points=points)

    def fetch_trading_flow(self, *, stock_code: str, start_date: str, end_date: str) -> TradingFlowSnapshot:
        response = self.client.chart.get_individual_stock_institutional_chart(
            dt=end_date,
            stk_cd=stock_code,
            amt_qty_tp="2",
            trde_tp="0",
            unit_tp="1",
        )
        rows: list[dict[str, Any]] = []
        for item in getattr(response.body, "stk_invsr_orgn_chart", []):
            row_date = getattr(item, "dt", "")
            if row_date and row_date < start_date:
                continue
            rows.append(
                {
                    "date": row_date,
                    "individual": self._to_float(getattr(item, "ind_invsr", None)),
                    "foreign": self._to_float(getattr(item, "frgnr_invsr", None)),
                    "institution": self._to_float(getattr(item, "orgn", None)),
                    "financial_investment": self._to_float(getattr(item, "fnnc_invt", None)),
                    "insurance": self._to_float(getattr(item, "insrnc", None)),
                    "investment_trust": self._to_float(getattr(item, "invtrt", None)),
                    "bank": self._to_float(getattr(item, "bank", None)),
                    "pension_fund": self._to_float(getattr(item, "penfnd_etc", None)),
                    "other_corporation": self._to_float(getattr(item, "etc_corp", None)),
                }
            )
        rows = sorted(rows, key=lambda item: item["date"])
        return TradingFlowSnapshot(
            stock_code=stock_code.zfill(6),
            source="kiwoom",
            start_date=start_date,
            end_date=end_date,
            rows=rows,
            totals=self._totals(rows),
        )

    @classmethod
    def _ohlcv_from_daily(cls, item: Any) -> OhlcvPoint:
        return OhlcvPoint(
            timestamp=getattr(item, "dt", ""),
            open=cls._to_float(getattr(item, "open_pric", None), absolute=True),
            high=cls._to_float(getattr(item, "high_pric", None), absolute=True),
            low=cls._to_float(getattr(item, "low_pric", None), absolute=True),
            close=cls._to_float(getattr(item, "cur_prc", None), absolute=True),
            volume=cls._to_float(getattr(item, "trde_qty", None)),
        )

    @classmethod
    def _ohlcv_from_minute(cls, item: Any) -> OhlcvPoint:
        return OhlcvPoint(
            timestamp=getattr(item, "cntr_tm", ""),
            open=cls._to_float(getattr(item, "open_pric", None), absolute=True),
            high=cls._to_float(getattr(item, "high_pric", None), absolute=True),
            low=cls._to_float(getattr(item, "low_pric", None), absolute=True),
            close=cls._to_float(getattr(item, "cur_prc", None), absolute=True),
            volume=cls._to_float(getattr(item, "trde_qty", None)),
        )

    @staticmethod
    def _to_float(value: Any, *, absolute: bool = False) -> float | None:
        if value in {None, ""}:
            return None
        try:
            parsed = float(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return None
        return abs(parsed) if absolute else parsed

    @staticmethod
    def _totals(rows: list[dict[str, Any]]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for row in rows:
            for key, value in row.items():
                if key == "date" or value is None:
                    continue
                totals[key] = totals.get(key, 0.0) + float(value)
        return totals
