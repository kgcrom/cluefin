"""`cache screen --rank`: pick by the sum of several factor ranks (decided 2026-11-22).

`--rank roa_ttm:desc,per_ttm:asc` ranks the rows left after `--where` and the exclusions on each factor
(1 = best in the given direction, ties share the best rank) and sorts by the sum — the 아이투자
"마법공식" style. A row whose value for a rank factor is `null` cannot be ranked and is dropped, counted
in `dropped_null` like a `--where` null. Each row gets `rank_sum` and `ranks` (per factor).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["RankKey", "apply_rank", "parse_rank"]


@dataclass(frozen=True, slots=True)
class RankKey:
    factor: str
    descending: bool

    def label(self) -> str:
        return f"{self.factor}:{'desc' if self.descending else 'asc'}"


def parse_rank(raw: str, factor_names: Iterable[str]) -> list[RankKey]:
    """``f1:desc,f2:asc`` → keys. Direction is required; an unknown factor or direction is exit 2."""

    known = set(factor_names)
    keys: list[RankKey] = []
    issues: list[str] = []
    for item in (part.strip() for part in raw.split(",")):
        if not item:
            continue
        factor, _, direction = item.partition(":")
        if factor not in known:
            issues.append(f"unknown factor `{factor}`")
        elif direction not in ("asc", "desc"):
            issues.append(f"`{item}` needs :asc or :desc")
        else:
            keys.append(RankKey(factor, direction == "desc"))
    if issues or not keys:
        raise CliError(
            "`--rank` takes factor:asc|desc pairs, e.g. roa_ttm:desc,per_ttm:asc.",
            exit_code=EXIT_USAGE,
            data={"issues": issues or ["no factor given"]},
            hint="Run `cache screen --factors true` for the factor list.",
        )
    return keys


def _competition_ranks(rows: list[dict[str, Any]], key: RankKey) -> dict[str, int]:
    ordered = sorted(rows, key=lambda row: -row[key.factor] if key.descending else row[key.factor])
    ranks: dict[str, int] = {}
    previous: float | None = None
    rank = 0
    for index, row in enumerate(ordered, 1):
        if row[key.factor] != previous:
            rank, previous = index, row[key.factor]
        ranks[row["code"]] = rank
    return ranks


def apply_rank(rows: list[dict[str, Any]], keys: list[RankKey]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Rows with every rank factor present, sorted by `rank_sum` (then code), and the null drop counts."""

    dropped: dict[str, int] = {}
    kept: list[dict[str, Any]] = []
    for row in rows:
        missing = [key.factor for key in keys if row.get(key.factor) is None]
        for factor in missing:
            dropped[factor] = dropped.get(factor, 0) + 1
        if not missing:
            kept.append(row)
    per_key = {key.factor: _competition_ranks(kept, key) for key in keys}
    for row in kept:
        row["ranks"] = {factor: ranks[row["code"]] for factor, ranks in per_key.items()}
        row["rank_sum"] = sum(row["ranks"].values())
    kept.sort(key=lambda row: (row["rank_sum"], row["code"]))
    return kept, dropped
