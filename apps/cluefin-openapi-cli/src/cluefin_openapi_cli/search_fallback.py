"""What `search` returns when the ranker finds nothing useful.

A miss must never be an empty result: an agent that gets `[]` has nowhere to go. This
builds the consolation payload — did-you-mean terms, the nearest domains and tags, and a
couple of runnable recipes — so every search ends with a next step.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Sequence

from cluefin_openapi_cli.metadata import build_taxonomy_entry
from cluefin_openapi_cli.query_terms import ALIAS_TABLE, HANGUL_RUN
from cluefin_openapi_cli.recipes import recipe_summaries

if TYPE_CHECKING:  # pragma: no cover - import cycle at runtime, annotations only
    from cluefin_openapi_cli.search import _Index

_APP_NAME = "cluefin-openapi-cli"


def _trigrams(text: str) -> set[str]:
    padded = f"  {text}  "
    return {padded[i : i + 3] for i in range(len(padded) - 2)}


def _did_you_mean(index: _Index, unknown: Sequence[str], extra: Iterable[str]) -> list[str]:
    candidates = set(index.vocabulary) | set(extra)
    scored: list[tuple[float, str]] = []
    for term in unknown:
        term_grams = _trigrams(term)
        for candidate in candidates:
            other = _trigrams(candidate)
            union = term_grams | other
            if not union:
                continue
            similarity = len(term_grams & other) / len(union)
            if similarity >= 0.4:
                scored.append((similarity, candidate))
    scored.sort(key=lambda pair: (-pair[0], pair[1]))
    seen: list[str] = []
    for _, candidate in scored:
        if candidate not in seen:
            seen.append(candidate)
        if len(seen) == 3:
            break
    return seen


def _taxonomy_scores(
    index: "_Index", scored: Sequence[tuple[float, str, list[str], dict[str, float]]], kind: str
) -> dict[str, float]:
    """Sum the top hits' scores per domain (or tag).

    With nothing scored there is nothing to rank, so every name gets a flat 1.0 and the
    caller still has a catalog-wide starting point to offer.
    """
    scores: dict[str, float] = {}
    for raw, qualified_name, _, _ in scored[:25]:
        for name in getattr(index.commands[qualified_name], kind):
            scores[name] = scores.get(name, 0.0) + raw
    if not scores:
        for command in index.commands.values():
            for name in getattr(command, kind):
                scores[name] = scores.get(name, 0.0) + 1.0
    return scores


def _taxonomy_rows(index: "_Index", kind: str, scores: dict[str, float]) -> list[dict[str, Any]]:
    rows = []
    for name, _ in sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:3]:
        count = sum(1 for command in index.commands.values() if name in getattr(command, kind))
        entry = build_taxonomy_entry(kind=kind, name=name, command_count=count, app_name=_APP_NAME)
        row = entry if isinstance(entry, dict) else entry.__dict__
        rows.append(
            {
                "name": name,
                "command_count": count,
                "when_to_use": row.get("when_to_use"),
                "example_filter": row.get("example_filter"),
            }
        )
    return rows


def _recipe_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": summary["name"],
        "title": summary["title"],
        "next": f"uv run {_APP_NAME} recipe {summary['name']} --json",
    }


def _nearest_alias_key(run: str) -> str | None:
    """Closest Hangul alias key to an unexplained Hangul run, by bigram overlap."""
    run_grams = {run[i : i + 2] for i in range(max(1, len(run) - 1))}
    best = sorted(
        (
            (len(run_grams & {key[i : i + 2] for i in range(max(1, len(key) - 1))}) / len(run_grams or {""}), key)
            for key, _ in ALIAS_TABLE
            if HANGUL_RUN.fullmatch(key)
        ),
        key=lambda pair: (-pair[0], pair[1]),
    )
    if best and best[0][0] > 0:
        return best[0][1]
    return None


def build_fallback(
    *,
    index: _Index,
    scored: Sequence[tuple[float, str, list[str], dict[str, float]]],
    terms: Sequence[tuple[str, float]],
    unmatched: Sequence[str],
    filtered: bool,
    candidate_count: int,
) -> dict[str, Any]:

    nearest_domains = _taxonomy_rows(index, "domains", _taxonomy_scores(index, scored, "domains"))
    nearest_tags = _taxonomy_rows(index, "tags", _taxonomy_scores(index, scored, "tags"))

    unknown = [term for term, _ in terms if index.doc_freq.get(term, 0) == 0]
    alias_keys = [key for key, _ in ALIAS_TABLE]
    suggestions = _did_you_mean(index, unknown, alias_keys)
    for run in unmatched:
        best = _nearest_alias_key(run)
        if best is not None and best not in suggestions:
            suggestions.append(best)

    domain_names = {row["name"] for row in nearest_domains}
    tag_names = {row["name"] for row in nearest_tags}
    related = [
        summary
        for summary in recipe_summaries()
        if domain_names & set(summary.get("domains", ())) or tag_names & set(summary.get("tags", ()))
    ]
    recipes = [_recipe_row(summary) for summary in (related or recipe_summaries())[:2]]

    if filtered and candidate_count == 0:
        reason = "filters_excluded_all_candidates"
    elif not scored:
        reason = "no_command_scored_above_threshold"
    else:
        reason = "low_term_coverage"

    return {
        "reason": reason,
        "did_you_mean": suggestions[:3],
        "nearest_domains": nearest_domains,
        "nearest_tags": nearest_tags,
        "recipes": recipes,
        "next": [
            f"uv run {_APP_NAME} domains --json",
            f"uv run {_APP_NAME} tags --json",
        ],
    }
