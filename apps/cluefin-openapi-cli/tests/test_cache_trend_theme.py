"""`cache trend-setup` theme block: hot themes on adjusted median returns, leaders that are not just big."""

from __future__ import annotations

import json
from datetime import date

from test_cache_trend import _AS_OF, cache, cache_dir  # noqa: F401 - pytest fixtures

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.trend import _Judged, _theme_tags
from cluefin_openapi_cli.main import run_cli


def _judged(code: str, *, ret: float, rel: float, value: float) -> _Judged:
    reading = {"strength": {"rel": rel}, "volume": {"traded_value_20d_eok": value}}
    return _Judged({"code": code}, reading, ret)


def _five_themes() -> tuple[list[tuple], list[tuple], dict[str, _Judged]]:
    """Themes T1…T5 with five stocks each; T1's stocks rose most, T5's least."""

    themes, members, judged = [], [], {}
    for t in range(1, 6):
        themes.append((f"T{t}", f"테마{t}", ""))
        for k in range(5):
            code = f"{t}{k:05d}"
            members.append((f"T{t}", code, f"종목{code}"))
            judged[code] = _judged(code, ret=50 - 10 * t + k, rel=1.0 + k / 10, value=100 - k * 10)
    return themes, members, judged


def test_top_fifth_of_themes_by_median_return_is_hot() -> None:
    blocks = _theme_tags(*_five_themes())

    t1, t2 = blocks["100000"]["themes"][0], blocks["200000"]["themes"][0]
    assert (t1["rank_pct"], t1["hot"], t1["return_20d_median_pct"]) == (20.0, True, 42.0)
    assert (t2["rank_pct"], t2["hot"]) == (40.0, False)


def test_themes_under_five_stocks_are_not_ranked() -> None:
    themes, members, judged = _five_themes()
    themes.append(("T6", "작은테마", ""))
    for code in ("600000", "600001"):
        members.append(("T6", code, code))
        judged[code] = _judged(code, ret=500, rel=2, value=1)

    small = _theme_tags(themes, members, judged)["600000"]["themes"][0]

    assert (small["rank_pct"], small["hot"]) == (None, False)


def test_leader_is_top_traded_value_or_main_stock_and_at_least_median_rel() -> None:
    themes, members, judged = _five_themes()
    # In T1: 100000 has the most traded value but the weakest rel (big but weak).
    themes[0] = ("T1", "테마1", "종목100004")
    blocks = _theme_tags(themes, members, judged)

    def t1(code: str) -> dict:
        return blocks[code]["themes"][0]

    assert t1("100000")["leader_by"] == ["traded_value_top3"] and t1("100000")["leader"] is False
    assert t1("100002")["leader"] is True  # top 3 by value, rel = median
    assert (t1("100004")["leader_by"], t1("100004")["leader"]) == (["main_stock"], True)
    assert blocks["100002"]["pass"] is True
    assert blocks["200002"]["pass"] is False  # leader, but T2 is not hot


def _add_snapshot(cache_dir) -> None:  # noqa: F811
    conn = store.open_store(cache_dir / "market.duckdb")
    day = date(2026, 10, 6)
    conn.execute("DELETE FROM theme")
    conn.execute("DELETE FROM theme_member")
    conn.execute("INSERT INTO theme (as_of, theme_code, name, main_stocks) VALUES (?, 'T1', '테스트', '알파')", [day])
    conn.executemany(
        "INSERT INTO theme_member (as_of, theme_code, code, name) VALUES (?, 'T1', ?, ?)",
        [(day, code, name) for code, name in (("000010", "알파"), ("000020", "베타"), ("000030", "감마"))],
    )
    conn.close()


def _scan(*extra: str) -> dict:
    return json.loads(run_cli(["cache", "trend-setup", "--as-of", _AS_OF, *extra, "--json"]).stdout)


def test_without_a_snapshot_theme_is_null_with_a_note(cache) -> None:  # noqa: F811
    conn = store.open_store(cache / "market.duckdb")
    conn.execute("DELETE FROM theme")
    conn.close()

    payload = _scan()

    assert all(row["theme"] is None for row in payload["rows"])
    assert any("테마 스냅샷 없음" in note for note in payload["notes"])
    assert "theme_pass" not in payload["summary"]


def test_snapshot_adds_theme_blocks_and_does_not_change_actions(cache) -> None:  # noqa: F811
    before = {row["code"]: (row["action"], row["status"]) for row in _scan()["rows"]}
    _add_snapshot(cache)

    payload = _scan()
    rows = {row["code"]: row for row in payload["rows"]}

    assert {code: (row["action"], row["status"]) for code, row in rows.items()} == before
    assert rows["000010"]["theme"]["themes"][0]["name"] == "테스트"
    assert rows["000040"]["theme"] == {"hot": False, "leader": False, "pass": False, "themes": []}
    assert payload["summary"]["theme_pass"] == 0  # 3 stocks: too few to rank, so never hot
    assert _scan("--theme-filter", "true")["rows"] == []
