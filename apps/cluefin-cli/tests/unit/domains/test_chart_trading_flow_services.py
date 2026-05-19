from datetime import date, timedelta

import pytest

from cluefin_cli.domains.chart import ChartService, calculate_indicators
from cluefin_cli.domains.models import OhlcvPoint, OhlcvSeries, TradingFlowSnapshot
from cluefin_cli.domains.trading_flow import TradingFlowService, resolve_dates


class FailingChartProvider:
    def fetch_ohlcv(self, **_: object) -> OhlcvSeries:
        raise ValueError("missing credentials")


class FakeChartProvider:
    def __init__(self, source: str):
        self.source = source

    def fetch_ohlcv(self, *, stock_code: str, interval: str, days: int) -> OhlcvSeries:
        return OhlcvSeries(
            stock_code=stock_code,
            source=self.source,
            interval=interval,
            points=[
                OhlcvPoint(timestamp=f"202501{i:02d}", open=float(i), high=float(i), low=float(i), close=float(i))
                for i in range(1, min(days, 60) + 1)
            ],
        )


class FakeFlowProvider:
    def __init__(self, source: str):
        self.source = source

    def fetch_trading_flow(self, *, stock_code: str, start_date: str, end_date: str) -> TradingFlowSnapshot:
        return TradingFlowSnapshot(
            stock_code=stock_code,
            source=self.source,
            start_date=start_date,
            end_date=end_date,
            rows=[{"date": end_date, "foreign": 1.0}],
            totals={"foreign": 1.0},
        )


def test_chart_service_falls_back_to_kis_and_adds_indicators() -> None:
    service = ChartService(kiwoom_provider=FailingChartProvider(), kis_provider=FakeChartProvider("kis"))

    series = service.fetch(stock_code="005930", source="auto", indicators=True)

    assert series.source == "kis"
    assert {item.name for item in series.indicators} >= {"sma_20", "rsi_14", "macd"}


def test_calculate_indicators_returns_json_safe_none_for_nan() -> None:
    series = OhlcvSeries(
        stock_code="005930",
        source="kiwoom",
        interval="daily",
        points=[OhlcvPoint(timestamp=f"202501{i:02d}", close=float(i)) for i in range(1, 31)],
    )

    indicators = calculate_indicators(series)

    sma_20 = next(item for item in indicators if item.name == "sma_20")
    assert sma_20.values[0] is None
    assert sma_20.latest is not None


def test_resolve_dates_defaults_to_recent_year() -> None:
    start, end = resolve_dates(start_date=None, end_date=None)

    expected_end = date.today()
    expected_start = expected_end - timedelta(days=365)
    assert end == expected_end.strftime("%Y%m%d")
    assert start == expected_start.strftime("%Y%m%d")


def test_resolve_dates_rejects_invalid_format() -> None:
    with pytest.raises(ValueError, match="YYYYMMDD"):
        resolve_dates(start_date="2025-01-01", end_date=None)


def test_trading_flow_service_all_sources() -> None:
    service = TradingFlowService(kiwoom_provider=FakeFlowProvider("kiwoom"), kis_provider=FakeFlowProvider("kis"))

    snapshots = service.fetch(stock_code="005930", source="all", start_date="20240101", end_date="20241231")

    assert [item.source for item in snapshots] == ["kiwoom", "kis"]
