"""`kis chart technical` — the one command that computes instead of passing through.

The shared handler fakes assert a 1:1 client passthrough, which this command is not, so
it carries its own fake: one that hands back a realistic candle page.
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers.kis.domestic_basic_quote import handle_kis_chart_technical
from cluefin_openapi_cli.indicators import MIN_CANDLES


def _rows(count: int, *, start_day: int = 1) -> list[dict[str, str]]:
    """A compounding rise, newest-first the way KIS actually answers."""

    rows = []
    for index in range(count):
        close = 1000.0 * (1.01**index)
        day = start_day + index
        rows.append(
            {
                "stck_bsop_date": f"2026{(day // 28) + 1:02d}{(day % 28) + 1:02d}",
                "stck_oprc": f"{close:.0f}",
                "stck_hgpr": f"{close * 1.01:.0f}",
                "stck_lwpr": f"{close * 0.99:.0f}",
                "stck_clpr": f"{close:.0f}",
                "acml_vol": "1000",
            }
        )
    return list(reversed(rows))


class _FakeQuote:
    def __init__(self, pages: list[list[dict[str, str]]]) -> None:
        self._pages = pages
        self.calls: list[tuple] = []

    def get_stock_period_quote(self, market, code, start, end, period, adj):  # noqa: PLR0913
        self.calls.append((market, code, start, end, period, adj))
        rows = self._pages.pop(0) if self._pages else []
        return type("Response", (), {"body": type("Body", (), {"output2": rows})()})()


class _FakeSession:
    def __init__(self, pages: list[list[dict[str, str]]]) -> None:
        self.quote = _FakeQuote(pages)

    def get_kis(self):
        return type("Client", (), {"domestic_basic_quote": self.quote})()


def test_returns_indicator_readings_not_the_candle_series() -> None:
    """Returning the candles would defeat the entire purpose of the command."""

    session = _FakeSession([_rows(120)])

    result = handle_kis_chart_technical({"stock_code": "005930"}, session)

    assert "candles" not in result
    assert set(result) == {
        "stock_code",
        "source",
        "as_of",
        "candle_count",
        "missing_candles",
        "close",
        "indicators",
        "signal",
    }
    assert result["stock_code"] == "005930"
    assert result["signal"]["trend"]["label"] == "BULLISH"


def test_payload_stays_small_enough_to_be_worth_it() -> None:
    import json

    session = _FakeSession([_rows(600)])

    result = handle_kis_chart_technical({"stock_code": "005930", "count": 600}, session)

    assert len(json.dumps(result, allow_nan=False)) < 2000


def test_defaults_to_120_candles() -> None:
    session = _FakeSession([_rows(200)])

    result = handle_kis_chart_technical({"stock_code": "005930"}, session)

    assert result["candle_count"] == 120


def test_count_is_honored() -> None:
    session = _FakeSession([_rows(200)])

    result = handle_kis_chart_technical({"stock_code": "005930", "count": 80}, session)

    assert result["candle_count"] == 80


def test_adjusted_flag_maps_to_this_endpoints_polarity() -> None:
    """chart.period reads 0 as adjusted — the opposite of chart.daily."""

    session = _FakeSession([_rows(120)])
    handle_kis_chart_technical({"stock_code": "005930", "adjusted": True}, session)
    assert session.quote.calls[0][5] == "0"

    session = _FakeSession([_rows(120)])
    handle_kis_chart_technical({"stock_code": "005930", "adjusted": False}, session)
    assert session.quote.calls[0][5] == "1"


def test_market_and_end_date_reach_the_client() -> None:
    session = _FakeSession([_rows(120)])

    handle_kis_chart_technical({"stock_code": "005930", "market": "NX", "end_date": "20260301"}, session)

    market, code, _start, end, period, _adj = session.quote.calls[0]
    assert (market, code, end, period) == ("NX", "005930", "20260301", "D")


def test_short_history_fails_with_a_broker_exit_code_not_a_crash() -> None:
    session = _FakeSession([_rows(10), []])

    with pytest.raises(CliError) as excinfo:
        handle_kis_chart_technical({"stock_code": "005930"}, session)

    error = excinfo.value
    assert error.exit_code == EXIT_BROKER
    assert error.error_type == "InsufficientHistory"
    assert error.data == {"stock_code": "005930", "candles": 10, "required": MIN_CANDLES}
    assert error.hint


def test_empty_response_is_reported_as_insufficient_history() -> None:
    session = _FakeSession([[]])

    with pytest.raises(CliError, match="Only 0 daily candles"):
        handle_kis_chart_technical({"stock_code": "005930"}, session)


def test_pages_until_the_requested_count_is_reached() -> None:
    session = _FakeSession([_rows(70, start_day=70), _rows(70)])

    result = handle_kis_chart_technical({"stock_code": "005930", "count": 120}, session)

    assert len(session.quote.calls) == 2
    assert result["candle_count"] == 120
