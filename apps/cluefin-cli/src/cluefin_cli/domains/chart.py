"""Domain service for normalized OHLCV chart data."""

from __future__ import annotations

import math
from typing import Sequence

import cluefin_ta
import numpy as np

from cluefin_cli.domains.models import IndicatorSnapshot, OhlcvSeries
from cluefin_cli.domains.providers.kis import KisProvider
from cluefin_cli.domains.providers.kiwoom import KiwoomProvider


class ChartService:
    def __init__(self, *, kiwoom_provider: KiwoomProvider | None = None, kis_provider: KisProvider | None = None):
        self.kiwoom_provider = kiwoom_provider or KiwoomProvider()
        self.kis_provider = kis_provider or KisProvider()

    def fetch(
        self,
        *,
        stock_code: str,
        source: str = "auto",
        interval: str = "daily",
        days: int = 300,
        indicators: bool = False,
    ) -> OhlcvSeries:
        if source == "kiwoom":
            series = self.kiwoom_provider.fetch_ohlcv(stock_code=stock_code, interval=interval, days=days)
        elif source == "kis":
            series = self.kis_provider.fetch_ohlcv(stock_code=stock_code, interval=interval, days=days)
        else:
            series = self._fetch_auto(stock_code=stock_code, interval=interval, days=days)

        if indicators:
            series.indicators = calculate_indicators(series)
        return series

    def _fetch_auto(self, *, stock_code: str, interval: str, days: int) -> OhlcvSeries:
        try:
            return self.kiwoom_provider.fetch_ohlcv(stock_code=stock_code, interval=interval, days=days)
        except Exception:
            return self.kis_provider.fetch_ohlcv(stock_code=stock_code, interval=interval, days=days)


def calculate_indicators(series: OhlcvSeries) -> list[IndicatorSnapshot]:
    close = np.array([point.close if point.close is not None else np.nan for point in series.points], dtype=np.float64)
    if close.size == 0:
        return []

    macd, macd_signal, macd_histogram = cluefin_ta.MACD(close)
    indicators = [
        IndicatorSnapshot(
            name="sma_20", values=_json_values(cluefin_ta.SMA(close, timeperiod=20)), params={"period": 20}
        ),
        IndicatorSnapshot(
            name="sma_50", values=_json_values(cluefin_ta.SMA(close, timeperiod=50)), params={"period": 50}
        ),
        IndicatorSnapshot(
            name="rsi_14", values=_json_values(cluefin_ta.RSI(close, timeperiod=14)), params={"period": 14}
        ),
        IndicatorSnapshot(name="macd", values=_json_values(macd), params={"fast": 12, "slow": 26, "signal": 9}),
        IndicatorSnapshot(
            name="macd_signal", values=_json_values(macd_signal), params={"fast": 12, "slow": 26, "signal": 9}
        ),
        IndicatorSnapshot(
            name="macd_histogram",
            values=_json_values(macd_histogram),
            params={"fast": 12, "slow": 26, "signal": 9},
        ),
    ]
    for item in indicators:
        item.latest = _latest(item.values)
    return indicators


def _json_values(values: Sequence[float]) -> list[float | None]:
    result: list[float | None] = []
    for value in values:
        parsed = float(value)
        result.append(None if math.isnan(parsed) or math.isinf(parsed) else parsed)
    return result


def _latest(values: Sequence[float | None]) -> float | None:
    for value in reversed(values):
        if value is not None:
            return value
    return None
