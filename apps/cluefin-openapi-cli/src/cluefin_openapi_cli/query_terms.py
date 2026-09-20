"""Query and document term normalization: tokenizer, stemmer and alias expansion.

Shared by the ranker (`search`) and the miss handler (`search_fallback`), which both need
the same view of what a term is. Korean never enters the index — every command description
is English — so Korean queries reach the corpus through `metadata.QUERY_ALIASES` instead.
"""

from __future__ import annotations

import re
import unicodedata

from cluefin_openapi_cli.metadata import QUERY_ALIASES

#: Expanded terms score slightly below literally typed ones, so a literal match always wins.
_EXPANSION_WEIGHT = 0.85

_STOPWORDS = frozenset(
    {"get", "from", "the", "a", "an", "of", "by", "for", "data", "and", "or", "with", "to", "in", "on"}
)
_IRREGULAR_PLURALS = {"indices": "index", "indexes": "index", "ratios": "ratio"}

_HANGUL = r"가-힣ᄀ-ᇿ㄰-㆏"
HANGUL_RUN = re.compile(f"[{_HANGUL}]+")
_ASCII_SPLIT = re.compile(r"[^a-z0-9]+")

ALIAS_TABLE: tuple[tuple[str, tuple[str, ...]], ...] = tuple(
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
    for raw in _ASCII_SPLIT.split(HANGUL_RUN.sub(" ", normalized)):
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

    for key, expansions in ALIAS_TABLE:
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
    for match in HANGUL_RUN.finditer(normalized):
        if not overlaps(match.start(), match.end()):
            unmatched.append(match.group())

    terms = sorted(weights.items(), key=lambda pair: (-pair[1], pair[0]))
    return terms, unmatched
