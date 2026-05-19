"""Domain service for normalized investor trading flow data."""

from __future__ import annotations

from datetime import date, timedelta

from cluefin_cli.domains.models import TradingFlowSnapshot
from cluefin_cli.domains.providers.kis import KisProvider
from cluefin_cli.domains.providers.kiwoom import KiwoomProvider


class TradingFlowService:
    def __init__(self, *, kiwoom_provider: KiwoomProvider | None = None, kis_provider: KisProvider | None = None):
        self.kiwoom_provider = kiwoom_provider or KiwoomProvider()
        self.kis_provider = kis_provider or KisProvider()

    def fetch(
        self,
        *,
        stock_code: str,
        source: str = "auto",
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[TradingFlowSnapshot]:
        resolved_start, resolved_end = resolve_dates(start_date=start_date, end_date=end_date)
        if source == "kiwoom":
            return [
                self.kiwoom_provider.fetch_trading_flow(
                    stock_code=stock_code, start_date=resolved_start, end_date=resolved_end
                )
            ]
        if source == "kis":
            return [
                self.kis_provider.fetch_trading_flow(
                    stock_code=stock_code, start_date=resolved_start, end_date=resolved_end
                )
            ]
        if source == "all":
            snapshots: list[TradingFlowSnapshot] = []
            for provider in [self.kiwoom_provider, self.kis_provider]:
                snapshots.append(
                    provider.fetch_trading_flow(stock_code=stock_code, start_date=resolved_start, end_date=resolved_end)
                )
            return snapshots
        try:
            return [
                self.kiwoom_provider.fetch_trading_flow(
                    stock_code=stock_code, start_date=resolved_start, end_date=resolved_end
                )
            ]
        except Exception:
            return [
                self.kis_provider.fetch_trading_flow(
                    stock_code=stock_code, start_date=resolved_start, end_date=resolved_end
                )
            ]


def resolve_dates(*, start_date: str | None, end_date: str | None) -> tuple[str, str]:
    end = _parse_date(end_date) if end_date else date.today()
    start = _parse_date(start_date) if start_date else end - timedelta(days=365)
    return start.strftime("%Y%m%d"), end.strftime("%Y%m%d")


def _parse_date(value: str) -> date:
    if len(value) != 8 or not value.isdigit():
        raise ValueError("dates must use YYYYMMDD format")
    return date(int(value[:4]), int(value[4:6]), int(value[6:]))
