"""trend_setup groups, action order and price levels (factory `classify.mjs` tests plus boundaries)."""

from __future__ import annotations

from dataclasses import replace

import pytest

from cluefin_openapi_cli.trend_setup import (
    Pivot,
    PriceFeatures,
    Strength,
    classify,
    find_pivot,
    floor_to_tick,
    g2_score,
    levels,
    price_features,
    strength,
    tick_size,
)

from .test_trend_setup_unit import index_of, load, prices_of


def classify_fixture(name: str) -> dict:
    prices = prices_of(name)
    f, s = price_features(prices), strength(prices, index_of(load(name)["market"]))
    assert f is not None
    assert s is not None
    return classify(f, find_pivot(prices), s)


def failed(checks: list[dict]) -> list[str]:
    return [check["id"] for check in checks if not check["pass"]]


def test_close_on_the_pivot_is_an_alert() -> None:
    got = classify_fixture("stock-f")

    assert got["groups"] == {"g1": False, "g2": True, "g3": True}
    assert got["to_pivot_pct"] == 0
    assert got["action"] == "alert"


def test_seven_percent_below_pivot_is_an_alert() -> None:
    got = classify_fixture("stock-e")

    assert got["groups"]["g3"] is True
    assert (got["action"], got["status"]) == ("alert", "setup")


def test_weaker_than_index_is_excluded_even_with_contractions() -> None:
    got = classify_fixture("stock-a")

    assert failed(got["checks"]["g3"]) == ["g3.rel_band"]
    assert got["groups"] == {"g1": False, "g2": False, "g3": False}
    assert got["action"] == "exclude"
    assert got["levels"]["buy_stop"] == 179700


def test_slightly_weaker_than_index_is_excluded() -> None:
    assert classify_fixture("stock-c")["action"] == "exclude"


def test_group_1_is_overheated() -> None:
    got = classify_fixture("stock-d")

    assert got["groups"]["g1"] is True
    assert got["status"] == "overheated"


def test_thin_traded_value_is_illiquid() -> None:
    assert classify_fixture("stock-b")["status"] == "illiquid"


# A state that passes group 3: pivot 10,000, close −3%.
_F = PriceFeatures(
    date="20261006",
    close=9700,
    sma_50=9238,
    sma_150=9000,
    sma_200=8800,
    sma_200_rising=True,
    high_52w=10778,
    low_52w=5389,
    gap_to_high_pct=-10,
    from_low_pct=80,
    template=True,
    return_21d_pct=2,
    weighted_return=5.5,
    range_10d_pct=8,
    atr14_pct=3,
    volume_20_50=1,
    traded_value_20d_eok=50,
    dist_sma50_pct=5,
    depth_60d_pct=20,
)
_PV = Pivot(price=10000, date="20260930", age=4, last_contraction_pct=6, legs=(20, 12, 6))
_S = Strength(
    rel=1.1, excess_21d_pp=0, weighted_return=5.5, index_weighted_return=5, return_21d_pct=2, index_return_21d_pct=2
)


def run(*, f: dict | None = None, pv: dict | None = None, s: dict | None = None, no_pivot: bool = False) -> dict:
    pivot = None if no_pivot else replace(_PV, **(pv or {}))
    return classify(replace(_F, **(f or {})), pivot, replace(_S, **(s or {})))


def test_base_state_is_groups_2_and_3_and_an_alert() -> None:
    got = run()

    assert got["groups"] == {"g1": False, "g2": True, "g3": True}
    assert got["action"] == "alert"


@pytest.mark.parametrize(
    ("rel", "g2", "g3", "g1"),
    [
        (0.99, False, False, False),
        (1.0, False, False, False),
        (1.0001, True, True, False),
        (1.3199, True, True, False),
        (1.32, True, False, False),
    ],
)
def test_rel_band(rel: float, g2: bool, g3: bool, g1: bool) -> None:
    groups = run(s={"rel": rel})["groups"]

    assert (groups["g1"], groups["g2"], groups["g3"]) == (g1, g2, g3)


def test_rel_at_ceiling_is_group_1_when_overheated() -> None:
    assert run(s={"rel": 1.32}, f={"range_10d_pct": 15.01})["groups"]["g1"] is True
    assert run(s={"rel": 1.32}, f={"range_10d_pct": 15})["groups"]["g1"] is False


def test_last_contraction_and_contraction_count() -> None:
    assert run(pv={"last_contraction_pct": 10})["groups"]["g3"] is True
    assert run(pv={"last_contraction_pct": 10.01})["groups"]["g3"] is False
    assert run(pv={"legs": (20, 6)})["groups"]["g3"] is False


def test_range_and_gap_limits() -> None:
    assert run(f={"range_10d_pct": 12})["groups"]["g3"] is True
    assert run(f={"range_10d_pct": 12.01})["groups"]["g3"] is False
    assert run(f={"gap_to_high_pct": -20})["groups"]["g3"] is True
    assert run(f={"gap_to_high_pct": -20.01})["groups"]["g3"] is False


@pytest.mark.parametrize(
    ("close", "status"),
    [
        (9200, "setup"),  # −8%
        (9199, "far_below_pivot"),
        (10000, "setup"),  # on the pivot: not broken out yet
        (10001, "breaking_out"),
        (10499, "breaking_out"),
        (10500, "extended"),  # +5%
    ],
)
def test_distance_to_pivot_decides_the_status(close: float, status: str) -> None:
    got = run(f={"close": close})

    assert got["status"] == status
    assert got["action"] == ("alert" if status == "setup" else "watch")


def test_illiquid_comes_before_everything() -> None:
    got = run(f={"traded_value_20d_eok": 9.99}, s={"rel": 1.5}, pv={})

    assert (got["action"], got["status"]) == ("exclude", "illiquid")


def test_group_1_excludes_even_when_group_2_also_holds() -> None:
    got = run(s={"rel": 1.5}, f={"dist_sma50_pct": 30})

    assert got["groups"]["g1"] is True
    assert got["groups"]["g2"] is True
    assert (got["action"], got["status"]) == ("exclude", "overheated")


def test_no_pivot_means_no_group_3_and_no_levels() -> None:
    got = run(no_pivot=True)

    assert got["groups"]["g3"] is False
    assert got["to_pivot_pct"] is None
    assert got["levels"] is None
    assert got["status"] == "g3_candidate"


def test_group_2_only_splits_by_score() -> None:
    assert run(pv={"legs": (20, 6)})["status"] == "g3_candidate"
    low = run(pv={"legs": (20, 6)}, f={"range_10d_pct": 13, "atr14_pct": 5, "depth_60d_pct": 31})
    assert low["status"] == "g2"


def test_nothing_is_no_group() -> None:
    got = run(f={"template": False}, s={"rel": 0.9})

    assert (got["action"], got["status"]) == ("exclude", "no_group")


def test_g2_score_counts_passed_items() -> None:
    assert g2_score(_F, _S)["score"] == 7
    got = g2_score(replace(_F, range_10d_pct=13, from_low_pct=101), replace(_S, excess_21d_pp=5.6))
    assert (got["score"], got["candidate"]) == (4, False)
    assert g2_score(replace(_F, range_10d_pct=13), _S)["candidate"] is True  # 6 of 7


@pytest.mark.parametrize(
    ("price", "tick"),
    [
        (1999, 1),
        (2000, 5),
        (4999, 5),
        (5000, 10),
        (19999, 10),
        (20000, 50),
        (49999, 50),
        (50000, 100),
        (199999, 100),
        (200000, 500),
        (499999, 500),
        (500000, 1000),
    ],
)
def test_tick_size_bounds(price: float, tick: int) -> None:
    assert tick_size(price) == tick


def test_levels_on_valid_ticks() -> None:
    assert floor_to_tick(174309) == 174300
    assert levels(179700) == {
        "alert": 174300,
        "buy_stop": 179700,
        "chase_limit": 188600,
        "stop_loss": 165300,
        "take_profit": 222500,
    }


def test_checks_carry_an_id_and_a_rule() -> None:
    check = run()["checks"]["g3"][2]

    assert check == {"id": "g3.last_contraction", "rule": "마지막 수축 ≤ 10%", "value": 6, "pass": True}
