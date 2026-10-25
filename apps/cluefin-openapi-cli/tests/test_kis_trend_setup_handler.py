"""`kis chart trend-setup`: golden fixtures served as KIS pages survive the handler end to end."""

from __future__ import annotations

import json
from datetime import datetime
from types import SimpleNamespace

import pytest
from test_trend_setup import load

from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_USAGE, CliError
from cluefin_openapi_cli.handlers.kis import domestic_basic_quote
from cluefin_openapi_cli.handlers.kis.domestic_basic_quote import handle_kis_chart_trend_setup


def _response(rows: list) -> SimpleNamespace:
    return SimpleNamespace(body=SimpleNamespace(output2=rows))


def _in_window(rows: list[dict], start: str, end: str, cap: int) -> list[dict]:
    """Newest ``cap`` rows of the window, newest first — how chart.period answers."""

    return sorted((row for row in rows if start <= row["date"] <= end), key=lambda row: row["date"], reverse=True)[:cap]


class FakeKis:
    def __init__(self, stock: str = "stock-e", *, market: str = "STK", index_cut: int = 0) -> None:
        data = load(stock)
        self.candles = data["candles"]
        index = load("index-0001" if data["market"] == "KOSPI" else "index-1001")["closes"]
        self.index = index[: len(index) - index_cut]
        self.basic = SimpleNamespace(mket_id_cd=market, scty_grp_id_cd="ST")
        self.calls: list[str] = []
        self.sectors: list[str] = []
        self.domestic_basic_quote = self
        self.domestic_issue_other = self
        self.domestic_stock_info = self

    def get_stock_period_quote(self, market, code, start, end, period, adj):  # noqa: PLR0913
        self.calls.append("period")
        assert adj == "0"  # chart.period: 0 = adjusted
        rows = [
            {
                "stck_bsop_date": c["date"],
                "stck_oprc": str(c["open"]),
                "stck_hgpr": str(c["high"]),
                "stck_lwpr": str(c["low"]),
                "stck_clpr": str(c["close"]),
                "acml_vol": str(c["volume"]),
                "acml_tr_pbmn": str(c["value"]),
            }
            for c in _in_window(self.candles, start, end, 100)
        ]
        return _response(rows)

    def get_sector_period_quote(self, market, sector, start, end, period):  # noqa: PLR0913
        self.calls.append("sector")
        self.sectors.append(sector)
        rows = [
            SimpleNamespace(
                stck_bsop_date=r["date"],
                bstp_nmix_oprc=str(r["close"]),
                bstp_nmix_hgpr=str(r["close"]),
                bstp_nmix_lwpr=str(r["close"]),
                bstp_nmix_prpr=str(r["close"]),
                acml_vol="0",
                acml_tr_pbmn="0",
            )
            for r in _in_window(self.index, start, end, 50)
        ]
        return _response(rows)

    def get_stock_basic_info(self, product, code):
        self.calls.append("basic")
        return SimpleNamespace(body=SimpleNamespace(output=self.basic))


class FakeSession:
    def __init__(self, kis: FakeKis) -> None:
        self.kis = kis

    def get_kis(self) -> FakeKis:
        return self.kis


@pytest.fixture(autouse=True)
def after_close(monkeypatch):
    monkeypatch.setattr(domestic_basic_quote, "_now", lambda: datetime(2026, 10, 6, 16, 0))


def _run(kis: FakeKis, **params) -> dict:
    return handle_kis_chart_trend_setup({"stock_code": "000010", **params}, FakeSession(kis))


def test_golden_values_survive_the_handler() -> None:
    expected = load("stock-e")["expected"]

    got = _run(FakeKis())

    assert (got["as_of"], got["benchmark"], got["market"], got["candle_count"]) == ("20261006", "0001", "KOSPI", 260)
    assert got["pivot"]["price"] == expected["pivot"]
    assert got["strength"]["rel"] == pytest.approx(expected["rel"], abs=1e-4)
    assert got["range_52w"]["gap_to_high_pct"] == pytest.approx(expected["gap52h"], abs=1e-4)
    assert (got["setup"]["action"], got["setup"]["status"]) == ("alert", "setup")
    assert got["levels"]["buy_stop"] == expected["pivot"]


def test_returns_readings_not_candles_and_stays_small() -> None:
    got = _run(FakeKis())

    assert "candles" not in got
    assert len(json.dumps(got, ensure_ascii=False).encode()) < 8000


def test_auto_benchmark_follows_basic_info() -> None:
    kis = FakeKis("stock-d", market="KSQ")

    got = _run(kis)

    assert set(kis.sectors) == {"1001"} and got["market"] == "KOSDAQ"


def test_explicit_benchmark_skips_basic_info() -> None:
    kis = FakeKis()

    _run(kis, benchmark="0001")

    assert "basic" not in kis.calls


def test_unknown_market_is_a_usage_error() -> None:
    with pytest.raises(CliError) as excinfo:
        _run(FakeKis(market="KNX"))

    assert excinfo.value.exit_code == EXIT_USAGE


def test_intraday_bar_is_dropped_before_the_close(monkeypatch) -> None:
    monkeypatch.setattr(domestic_basic_quote, "_now", lambda: datetime(2026, 10, 6, 14, 0))

    got = _run(FakeKis())

    assert got["dropped_intraday_candle"] == "20261006" and got["as_of"] == "20261002"


def test_include_today_keeps_the_intraday_bar_with_a_caveat(monkeypatch) -> None:
    monkeypatch.setattr(domestic_basic_quote, "_now", lambda: datetime(2026, 10, 6, 14, 0))

    got = _run(FakeKis(), include_today=True)

    assert got["dropped_intraday_candle"] is None and got["as_of"] == "20261006"
    assert any("장중" in caveat for caveat in got["caveats"])


def test_end_date_never_drops(monkeypatch) -> None:
    monkeypatch.setattr(domestic_basic_quote, "_now", lambda: datetime(2026, 10, 6, 14, 0))

    assert _run(FakeKis(), end_date="20261006")["as_of"] == "20261006"


def test_missing_index_date_is_exit_4() -> None:
    with pytest.raises(CliError) as excinfo:
        _run(FakeKis(index_cut=1))

    assert (excinfo.value.exit_code, excinfo.value.error_type) == (EXIT_BROKER, "IndexDateMismatch")


def test_short_history_is_exit_4() -> None:
    kis = FakeKis()
    kis.candles = kis.candles[-250:]

    with pytest.raises(CliError) as excinfo:
        _run(kis)

    assert (excinfo.value.exit_code, excinfo.value.error_type) == (EXIT_BROKER, "InsufficientHistory")


def test_preferred_share_code_gets_a_caveat() -> None:
    got = handle_kis_chart_trend_setup({"stock_code": "000015"}, FakeSession(FakeKis()))

    assert any("우선주" in caveat for caveat in got["caveats"])
