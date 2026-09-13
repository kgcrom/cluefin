"""Ranked natural-language lookup over the command catalog.

`list --query` is a literal substring filter; this module is the other primitive — a
BM25F ranker that turns a task description ("외국인 순매수 상위 종목") into a short,
ordered shortlist. Pure stdlib: the CLI depends only on cluefin-openapi and pydantic.

Korean never enters the index — every command description is English — so Korean
queries reach the corpus through `metadata.QUERY_ALIASES` expansion instead.
"""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from cluefin_openapi_cli.metadata import QUERY_ALIASES, broker_rank
from cluefin_openapi_cli.registry import CommandSpec, RegistryProtocol

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
#: Expanded terms score slightly below literally typed ones, so a literal match always wins.
_EXPANSION_WEIGHT = 0.85

_STOPWORDS = frozenset(
    {"get", "from", "the", "a", "an", "of", "by", "for", "data", "and", "or", "with", "to", "in", "on"}
)
_IRREGULAR_PLURALS = {"indices": "index", "indexes": "index", "ratios": "ratio"}

#: Instrument-class qualifiers. A command carrying one of these in its path is a narrowing
#: of the general case, so it should not outrank the general command when the query never
#: mentioned it ("current price" means the stock quote, not the ETF quote).
_NARROWING_TOKENS = frozenset({"etf", "etn", "elw", "overseas", "bond", "future", "option"})
_NARROWING_PENALTY = 0.85

_HANGUL = r"가-힣ᄀ-ᇿ㄰-㆏"
_HANGUL_RUN = re.compile(f"[{_HANGUL}]+")
_ASCII_SPLIT = re.compile(r"[^a-z0-9]+")

_ALIAS_TABLE: tuple[tuple[str, tuple[str, ...]], ...] = tuple(
    sorted(QUERY_ALIASES, key=lambda pair: len(pair[0]), reverse=True)
)


def _singular(token: str) -> str:
    if token in _IRREGULAR_PLURALS:
        return _IRREGULAR_PLURALS[token]
    if len(token) <= 3 or not token.endswith("s"):
        return token
    stem = token[:-1]
    if token.endswith("es") and stem[:-1].endswith(("s", "x", "ch", "sh")):
        return stem[:-1]
    if stem.endswith("s"):
        return token
    return stem


def tokenize(text: str) -> list[str]:
    """Normalize and split text the same way for documents and queries."""

    normalized = unicodedata.normalize("NFKC", text).casefold()
    tokens: list[str] = []
    for raw in _ASCII_SPLIT.split(_HANGUL_RUN.sub(" ", normalized)):
        if not raw or raw in _STOPWORDS:
            continue
        token = _singular(raw)
        if token and token not in _STOPWORDS:
            tokens.append(token)
    return tokens


def expand_query(text: str) -> tuple[list[tuple[str, float]], list[str]]:
    """Expand a raw query into weighted terms plus any Hangul left unexplained.

    Aliases are matched longest-first over the whole query and over each Hangul run, and
    a matched span is consumed so `순매수` fires instead of `매수`.
    """

    normalized = unicodedata.normalize("NFKC", text).casefold()
    weights: dict[str, float] = {}

    for token in tokenize(text):
        weights[token] = max(weights.get(token, 0.0), 1.0)

    covered: list[tuple[int, int]] = []

    def overlaps(start: int, end: int) -> bool:
        return any(start < c_end and c_start < end for c_start, c_end in covered)

    for key, expansions in _ALIAS_TABLE:
        start = normalized.find(key)
        while start != -1:
            end = start + len(key)
            if not overlaps(start, end):
                covered.append((start, end))
                # Expansions go through the same tokenizer as documents, or a plural like
                # "securities" would never match the indexed stem.
                for expansion in expansions:
                    for token in tokenize(expansion) or [expansion]:
                        weights[token] = max(weights.get(token, 0.0), _EXPANSION_WEIGHT)
            start = normalized.find(key, start + 1)

    unmatched: list[str] = []
    for match in _HANGUL_RUN.finditer(normalized):
        if not overlaps(match.start(), match.end()):
            unmatched.append(match.group())

    terms = sorted(weights.items(), key=lambda pair: (-pair[1], pair[0]))
    return terms, unmatched


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
        fallback = _build_fallback(
            index=index,
            scored=scored,
            terms=terms,
            unmatched=unmatched,
            filtered=bool(broker or domain or tag or category),
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


def _build_fallback(
    *,
    index: _Index,
    scored: Sequence[tuple[float, str, list[str], dict[str, float]]],
    terms: Sequence[tuple[str, float]],
    unmatched: Sequence[str],
    filtered: bool,
    candidate_count: int,
) -> dict[str, Any]:
    from cluefin_openapi_cli.metadata import build_taxonomy_entry
    from cluefin_openapi_cli.recipes import recipe_summaries

    app_name = "cluefin-openapi-cli"

    domain_scores: dict[str, float] = {}
    tag_scores: dict[str, float] = {}
    for raw, qualified_name, _, _ in scored[:25]:
        command = index.commands[qualified_name]
        for name in command.domains:
            domain_scores[name] = domain_scores.get(name, 0.0) + raw
        for name in command.tags:
            tag_scores[name] = tag_scores.get(name, 0.0) + raw

    def taxonomy_rows(kind: str, scores: dict[str, float]) -> list[dict[str, Any]]:
        rows = []
        for name, _ in sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:3]:
            count = sum(1 for command in index.commands.values() if name in getattr(command, kind))
            entry = build_taxonomy_entry(kind=kind, name=name, command_count=count, app_name=app_name)
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

    if not domain_scores:
        for command in index.commands.values():
            for name in command.domains:
                domain_scores[name] = domain_scores.get(name, 0.0) + 1.0
    if not tag_scores:
        for command in index.commands.values():
            for name in command.tags:
                tag_scores[name] = tag_scores.get(name, 0.0) + 1.0

    nearest_domains = taxonomy_rows("domains", domain_scores)
    nearest_tags = taxonomy_rows("tags", tag_scores)

    unknown = [term for term, _ in terms if index.doc_freq.get(term, 0) == 0]
    alias_keys = [key for key, _ in _ALIAS_TABLE]
    suggestions = _did_you_mean(index, unknown, alias_keys)
    for run in unmatched:
        run_grams = {run[i : i + 2] for i in range(max(1, len(run) - 1))}
        best = sorted(
            (
                (len(run_grams & {key[i : i + 2] for i in range(max(1, len(key) - 1))}) / len(run_grams or {""}), key)
                for key, _ in _ALIAS_TABLE
                if _HANGUL_RUN.fullmatch(key)
            ),
            key=lambda pair: (-pair[0], pair[1]),
        )
        if best and best[0][0] > 0 and best[0][1] not in suggestions:
            suggestions.append(best[0][1])

    domain_names = {row["name"] for row in nearest_domains}
    tag_names = {row["name"] for row in nearest_tags}
    recipes = [
        {
            "name": summary["name"],
            "title": summary["title"],
            "next": f"uv run {app_name} recipe {summary['name']} --json",
        }
        for summary in recipe_summaries()
        if domain_names & set(summary.get("domains", ())) or tag_names & set(summary.get("tags", ()))
    ][:2]
    if not recipes:
        recipes = [
            {"name": s["name"], "title": s["title"], "next": f"uv run {app_name} recipe {s['name']} --json"}
            for s in recipe_summaries()[:2]
        ]

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
            f"uv run {app_name} domains --json",
            f"uv run {app_name} tags --json",
        ],
    }
