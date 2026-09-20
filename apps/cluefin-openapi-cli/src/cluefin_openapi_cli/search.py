"""Ranked natural-language lookup over the command catalog.

`list --query` is a literal substring filter; this module is the other primitive — a
BM25F ranker that turns a task description ("외국인 순매수 상위 종목") into a short,
ordered shortlist. Pure stdlib: the CLI depends only on cluefin-openapi and pydantic.

Korean never enters the index — every command description is English — so Korean
queries reach the corpus through `metadata.QUERY_ALIASES` expansion instead.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from cluefin_openapi_cli.metadata import broker_rank
from cluefin_openapi_cli.query_terms import expand_query, tokenize
from cluefin_openapi_cli.registry import CommandSpec, RegistryProtocol
from cluefin_openapi_cli.search_fallback import build_fallback

__all__ = [
    "SearchHit",
    "SearchResult",
    "expand_query",
    "search_commands",
    "tokenize",
]

# Field weights. `params` is ~8x longer than every other field, so BM25F's per-field
# length normalization (not flat BM25) is what keeps parameter prose from drowning names.
_FIELD_WEIGHTS: dict[str, float] = {
    "name": 3.0,
    "tags": 2.2,
    "domains": 1.6,
    "description": 1.0,
    "params": 0.5,
}
_K1 = 1.2
_B = 0.75

#: Relative-score floor. A long tail of near-zero hits is worse for an agent than none.
_RELATIVE_FLOOR = 0.30
_DEFAULT_LIMIT = 8
_MAX_LIMIT = 50

#: Instrument-class qualifiers. A command carrying one of these in its path is a narrowing
#: of the general case, so it should not outrank the general command when the query never
#: mentioned it ("current price" means the stock quote, not the ETF quote).
_NARROWING_TOKENS = frozenset({"etf", "etn", "elw", "overseas", "bond", "future", "option"})
_NARROWING_PENALTY = 0.85


@dataclass(frozen=True, slots=True)
class SearchHit:
    command: CommandSpec
    score: float
    relative: float
    matched: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SearchResult:
    hits: tuple[SearchHit, ...]
    confidence: str
    expanded: tuple[str, ...]
    unmatched_terms: tuple[str, ...]
    fallback: dict[str, Any] | None = None
    per_term: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class _Index:
    docs: dict[str, dict[str, list[str]]]
    commands: dict[str, CommandSpec]
    doc_freq: dict[str, int]
    avg_len: dict[str, float]
    total: int

    @property
    def vocabulary(self) -> Iterable[str]:
        return self.doc_freq.keys()


def _doc_fields(command: CommandSpec) -> dict[str, list[str]]:
    params = command.parameters.get("properties", {}) if isinstance(command.parameters, dict) else {}
    param_text: list[str] = []
    for name, schema in params.items():
        param_text.extend(tokenize(name))
        if isinstance(schema, dict):
            param_text.extend(tokenize(str(schema.get("description", ""))))
    return {
        "name": tokenize(command.qualified_name),
        "tags": [token for tag in command.tags for token in tokenize(tag)],
        "domains": [token for domain in command.domains for token in tokenize(domain)],
        "description": tokenize(command.description),
        "params": param_text,
    }


def _build_index(registry: RegistryProtocol) -> _Index:
    docs: dict[str, dict[str, list[str]]] = {}
    commands: dict[str, CommandSpec] = {}
    for command in registry.list_commands():
        docs[command.qualified_name] = _doc_fields(command)
        commands[command.qualified_name] = command

    doc_freq: dict[str, int] = {}
    for fields in docs.values():
        seen = {token for tokens in fields.values() for token in tokens}
        for token in seen:
            doc_freq[token] = doc_freq.get(token, 0) + 1

    avg_len: dict[str, float] = {}
    for name in _FIELD_WEIGHTS:
        lengths = [len(fields[name]) for fields in docs.values()]
        avg_len[name] = (sum(lengths) / len(lengths)) if lengths else 1.0
        if avg_len[name] <= 0:
            avg_len[name] = 1.0

    return _Index(docs=docs, commands=commands, doc_freq=doc_freq, avg_len=avg_len, total=len(docs))


# Keyed on the registry *object* — `set_registry_provider` swaps registries between tests,
# and an unkeyed cache would silently serve a stale index across that swap.
_INDEX_CACHE: tuple[RegistryProtocol, _Index] | None = None


def _get_index(registry: RegistryProtocol) -> _Index:
    global _INDEX_CACHE
    if _INDEX_CACHE is None or _INDEX_CACHE[0] is not registry:
        _INDEX_CACHE = (registry, _build_index(registry))
    return _INDEX_CACHE[1]


def _score_doc(
    index: _Index, qualified_name: str, terms: Sequence[tuple[str, float]]
) -> tuple[float, list[str], dict[str, float]]:
    fields = index.docs[qualified_name]
    total = 0.0
    matched: list[str] = []
    per_term: dict[str, float] = {}

    for term, query_weight in terms:
        df = index.doc_freq.get(term, 0)
        if df == 0:
            continue
        idf = math.log(1 + (index.total - df + 0.5) / (df + 0.5))
        weighted_tf = 0.0
        for field_name, field_weight in _FIELD_WEIGHTS.items():
            tokens = fields[field_name]
            tf = tokens.count(term)
            if not tf:
                continue
            norm = 1 - _B + _B * (len(tokens) / index.avg_len[field_name])
            weighted_tf += field_weight * tf / norm
        if weighted_tf <= 0:
            continue
        contribution = query_weight * idf * weighted_tf / (_K1 + weighted_tf)
        total += contribution
        per_term[term] = round(contribution, 4)
        matched.append(term)

    return total, matched, per_term


def _apply_boosts(score: float, command: CommandSpec, index: _Index, terms: Sequence[tuple[str, float]]) -> float:
    if score <= 0:
        return score
    asked = {term for term, _ in terms}
    unasked = _NARROWING_TOKENS.intersection(index.docs[command.qualified_name]["name"]) - asked
    if unasked:
        score *= _NARROWING_PENALTY ** len(unasked)
    typed = [term for term, weight in terms if weight >= 1.0]
    if len(typed) >= 2:
        phrase = "-".join(typed)
        if phrase in command.qualified_name:
            score *= 1.4
        description = index.docs[command.qualified_name]["description"]
        for first, second in zip(typed, typed[1:], strict=False):
            for position in range(len(description) - 1):
                if description[position] == first and description[position + 1] == second:
                    score *= 1.15
                    break
            else:
                continue
            break
    return score


def search_commands(
    registry: RegistryProtocol,
    query: str,
    *,
    limit: int = _DEFAULT_LIMIT,
    broker: str | None = None,
    domain: str | None = None,
    tag: str | None = None,
    category: str | None = None,
    explain: bool = False,
) -> SearchResult:
    """Rank commands against a natural-language query.

    IDF always comes from the whole catalog, so scores stay comparable whether or not
    the caller narrowed the candidate set with filters.
    """

    index = _get_index(registry)
    terms, unmatched = expand_query(query)

    candidates = registry.list_commands(broker=broker, category=category, domain=domain, tag=tag)
    candidate_names = [command.qualified_name for command in candidates if command.qualified_name in index.docs]

    scored: list[tuple[float, str, list[str], dict[str, float]]] = []
    for qualified_name in candidate_names:
        raw, matched, per_term = _score_doc(index, qualified_name, terms)
        if raw <= 0:
            continue
        boosted = _apply_boosts(raw, index.commands[qualified_name], index, terms)
        scored.append((boosted, qualified_name, matched, per_term))

    scored.sort(
        key=lambda row: (
            -round(row[0], 3),
            broker_rank(index.commands[row[1]].broker),
            row[1],
        )
    )

    hits: tuple[SearchHit, ...] = ()
    confidence = "none"
    per_term_detail: dict[str, Any] = {}

    if scored:
        top = scored[0][0]
        kept = [row for row in scored if top <= 0 or row[0] / top >= _RELATIVE_FLOOR][: max(1, limit)]
        hits = tuple(
            SearchHit(
                command=index.commands[qualified_name],
                score=round(raw, 3),
                relative=round(raw / top, 3) if top else 0.0,
                matched=tuple(matched),
            )
            for raw, qualified_name, matched, _ in kept
        )
        distinct = {term for term, _ in terms if index.doc_freq.get(term, 0) > 0}
        matched_ratio = (len(set(kept[0][2])) / len(distinct)) if distinct else 0.0
        confidence = "high" if matched_ratio >= 0.5 else "low"
        if explain:
            per_term_detail = {row[1]: row[3] for row in kept}

    fallback = None
    if not hits or confidence == "low":
        fallback = build_fallback(
            index=index,
            scored=scored,
            terms=terms,
            unmatched=unmatched,
            filtered=any((broker, domain, tag, category)),
            candidate_count=len(candidate_names),
        )

    return SearchResult(
        hits=hits,
        confidence=confidence,
        expanded=tuple(term for term, _ in terms),
        unmatched_terms=tuple(unmatched),
        fallback=fallback,
        per_term=per_term_detail,
    )
