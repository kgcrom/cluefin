"""`cache screen --rank` rank-sum selection (cache/screen_rank.py) and its CLI options."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.cache.screen_rank import apply_rank, parse_rank
from cluefin_openapi_cli.errors import CliError


def test_parse_rank_requires_known_factor_and_direction() -> None:
    keys = parse_rank("roa_ttm:desc, per_ttm:asc", ["roa_ttm", "per_ttm"])
    assert [key.label() for key in keys] == ["roa_ttm:desc", "per_ttm:asc"]

    with pytest.raises(CliError) as excinfo:
        parse_rank("roa_ttm,nope:asc", ["roa_ttm"])
    assert excinfo.value.exit_code == 2
    assert len(excinfo.value.data["issues"]) == 2


def test_rank_sum_orders_rows_and_drops_nulls() -> None:
    rows = [
        {"code": "A", "roa_ttm": 30.0, "per_ttm": 10.0},
        {"code": "B", "roa_ttm": 25.0, "per_ttm": 5.0},
        {"code": "C", "roa_ttm": 10.0, "per_ttm": 4.0},
        {"code": "D", "roa_ttm": 20.0, "per_ttm": None},
    ]
    keys = parse_rank("roa_ttm:desc,per_ttm:asc", ["roa_ttm", "per_ttm"])

    ranked, dropped = apply_rank(rows, keys)

    # A 1+3=4, B 2+2=4, C 3+1=4 → all tied, code breaks the tie; then make B win outright.
    assert [row["code"] for row in ranked] == ["A", "B", "C"]
    assert ranked[1]["ranks"] == {"roa_ttm": 2, "per_ttm": 2}
    rows[1]["per_ttm"] = 3.0
    ranked, _ = apply_rank(rows, keys)
    assert [row["code"] for row in ranked][0] == "B"
    assert dropped == {"per_ttm": 1}


def test_ties_share_the_best_rank() -> None:
    rows = [{"code": "A", "x": 1.0}, {"code": "B", "x": 1.0}, {"code": "C", "x": 2.0}]
    ranked, _ = apply_rank(rows, parse_rank("x:asc", ["x"]))
    assert [row["rank_sum"] for row in ranked] == [1, 1, 3]
