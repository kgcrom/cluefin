"""trend_setup.history: runs, previous state past flickers, g3 exits, recent g1 (plan 4-9)."""

from __future__ import annotations

import numpy as np
import pytest
from test_trend_setup import index_of, load, prices_of

from cluefin_openapi_cli import trend_setup
from cluefin_openapi_cli.trend_setup import IndexCloses, Pivot, PriceArrays, history

_PIVOT = Pivot(price=100.0, date="20260101", age=5, last_contraction_pct=5, legs=(10, 8, 5))


def _prices(n: int, last_close: float = 95.0) -> PriceArrays:
    closes = np.full(n, 95.0)
    closes[-1] = last_close
    return PriceArrays.from_rows([(f"D{i:04d}", c, c, c, c, 1, 1) for i, c in enumerate(closes)])


def _script(monkeypatch, states: list[str | None], *, g1_ends: tuple[int, ...] = (), n: int = 300) -> None:
    """``states`` are the last ``len(states)`` days, oldest first; g1 is true on the given bar ends."""

    first = n - len(states) + 1

    def judge(prices, index, end):
        state = states[end - first] if end >= first else None
        return (state, _PIVOT) if state else None

    monkeypatch.setattr(trend_setup, "_judge", judge)
    monkeypatch.setattr(trend_setup, "_was_g1", lambda prices, index, end: end in g1_ends)


_INDEX = IndexCloses(dates=(), closes=np.array([]))


def _history(monkeypatch, states, *, close: float = 95.0, g1_ends: tuple[int, ...] = ()) -> dict:
    _script(monkeypatch, states, g1_ends=g1_ends)
    return history(_prices(300, close), _INDEX, days=len(states))


def test_status_days_and_previous_state(monkeypatch) -> None:
    got = _history(monkeypatch, ["g2"] * 5 + ["g3"] * 4)

    assert (got["state"], got["status_days"], got["status_days_capped"]) == ("g3", 4, False)
    assert (got["prev_status"], got["prev_status_date"]) == ("g2", "D0295")


def test_flickers_and_runs_of_the_same_state_are_skipped(monkeypatch) -> None:
    # g1 for 4 days, none for 2 (flicker), g3 for 1, none 1 (flicker), g3 today.
    got = _history(monkeypatch, ["g1"] * 4 + ["none"] * 2 + ["g3", "none", "g3"])

    assert (got["status_days"], got["prev_status"]) == (1, "g1")


def test_status_days_cap_at_the_window(monkeypatch) -> None:
    got = _history(monkeypatch, ["g3"] * 20)

    assert (got["status_days"], got["status_days_capped"], got["prev_status"]) == (20, True, None)


def test_short_run_at_the_window_start_is_unknown_not_a_flicker(monkeypatch) -> None:
    got = _history(monkeypatch, ["g2", "g2"] + ["g3"] * 5)

    assert got["prev_status"] is None


@pytest.mark.parametrize(
    ("close", "kind"),
    [(100.0, "breakout"), (101.0, "breakout"), (91.99, "breakdown"), (92.0, "faded"), (99.0, "faded")],
)
def test_exit_from_group_3_against_yesterdays_pivot(monkeypatch, close: float, kind: str) -> None:
    assert _history(monkeypatch, ["g3", "g3", "g2"], close=close)["exit"] == kind


def test_no_exit_unless_yesterday_was_group_3(monkeypatch) -> None:
    assert _history(monkeypatch, ["g2", "g2", "none"])["exit"] is None
    assert _history(monkeypatch, ["g3", "g3", "g3"])["exit"] is None


@pytest.mark.parametrize(("g1_end", "within"), [(299, True), (240, True), (239, False), (300, False)])
def test_g1_within_60_sessions_before_today(monkeypatch, g1_end: int, within: bool) -> None:
    # Bar ends: 300 is today, 299 yesterday, 240 sixty sessions back, 239 sixty-one.
    got = _history(monkeypatch, ["g3"] * 3, g1_ends=(g1_end,))

    assert got["g1_within_60d"] is within
    assert got["last_g1_date"] == (f"D{g1_end - 1:04d}" if within else None)


def test_history_state_matches_todays_judgement_on_real_bars() -> None:
    prices = prices_of("stock-e")
    index = index_of(load("stock-e")["market"])

    got = history(prices, index)

    assert got["state"] == "g3"  # analyze: alert/setup
    assert 1 <= got["status_days"] <= 20
