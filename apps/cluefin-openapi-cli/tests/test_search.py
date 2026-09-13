"""`search` contract: recall on real task descriptions, ranking, fallback, alias sync."""

from __future__ import annotations

import json

import pytest

from cluefin_openapi_cli import search as search_module
from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.metadata import QUERY_ALIASES
from cluefin_openapi_cli.registry import RpcRegistry
from cluefin_openapi_cli.search import expand_query, search_commands, tokenize


def _json(argv: list[str]) -> tuple[int, dict]:
    result = run_cli([*argv, "--json"])
    return result.exit_code, json.loads(result.stdout)


# Every row here returned 0 results from `list --query` before `search` existed.
RECALL_CASES = [
    ("외국인 순매수 상위 종목", "foreign"),
    ("재무제표", "kis.financial.balance-sheet"),
    ("moving average", "chart"),
    ("rsi", "chart"),
    ("foreign net buying", "foreign"),
    ("dividend schedule", "kis.schedule.dividend"),
    ("배당", "dividend"),
    ("테마", "kiwoom.theme.group"),
    ("공시", "dart.disclosure-search"),
    ("업종 지수", "sector"),
    ("조건검색", "kis.analysis.condition-search-list"),
    ("공매도", "short-selling"),
    ("체결강도", "execution-intensity"),
    ("etf 구성종목", "kis.etf.component-stocks"),
]


@pytest.mark.parametrize(("query", "expected"), RECALL_CASES, ids=[case[0] for case in RECALL_CASES])
def test_search_finds_expected_command_in_top_three(query: str, expected: str) -> None:
    code, payload = _json(["search", *query.split(), "--limit", "3"])

    assert code == 0
    assert payload["count"] > 0, payload
    top = [row["qualified_name"] for row in payload["commands"]]
    assert any(expected in name for name in top), (query, top)


def test_search_payload_is_cheap_enough_to_be_the_first_call() -> None:
    result = run_cli(["search", "차트", "--compact", "--json"])

    assert result.exit_code == 0
    assert len(result.stdout) < 5000


def test_path_phrase_boost_ranks_the_literal_command_first() -> None:
    _, payload = _json(["search", "current", "price", "--limit", "3"])

    assert payload["commands"][0]["qualified_name"] == "kis.stock.current-price"


def test_narrowing_qualifier_does_not_outrank_the_general_command() -> None:
    _, payload = _json(["search", "current", "price", "--limit", "5"])
    names = [row["qualified_name"] for row in payload["commands"]]

    assert names.index("kis.stock.current-price") < names.index("kis.etf.current-price")


def test_filters_restrict_candidates() -> None:
    _, payload = _json(["search", "차트", "--broker", "kiwoom"])
    assert payload["count"] > 0
    assert all(row["broker"] == "kiwoom" for row in payload["commands"])

    _, payload = _json(["search", "차트", "--domain", "chart"])
    assert all("chart" in row["domains"] for row in payload["commands"])


def test_unknown_broker_is_a_usage_error() -> None:
    code, _ = _json(["search", "차트", "--broker", "nhplug"])
    assert code == 2


def test_miss_returns_exit_zero_with_a_runnable_fallback() -> None:
    code, payload = _json(["search", "zzzz", "qqqq"])

    assert code == 0
    assert payload["count"] == 0
    fallback = payload["fallback"]
    assert fallback["reason"] == "no_command_scored_above_threshold"
    assert fallback["next"]
    # Every suggested filter must actually run.
    for row in [*fallback["nearest_domains"], *fallback["nearest_tags"]]:
        argv = row["example_filter"].split()[3:]
        assert run_cli(argv).exit_code == 0, row
    assert fallback["recipes"]


def test_empty_query_is_a_usage_error() -> None:
    code, _ = _json(["search"])
    assert code == 2


def test_limit_is_clamped_and_validated() -> None:
    _, payload = _json(["search", "차트", "--limit", "999"])
    assert payload["limit"] == 50

    code, _ = _json(["search", "차트", "--limit", "abc"])
    assert code == 2


def test_rows_carry_the_next_schema_call() -> None:
    _, payload = _json(["search", "재무제표", "--limit", "1"])
    row = payload["commands"][0]

    assert row["next"].endswith("--json")
    argv = row["next"].split()[3:]
    assert run_cli(argv).exit_code == 0


def test_results_are_deterministic() -> None:
    first = run_cli(["search", "외국인", "수급", "--json"])
    second = run_cli(["search", "외국인", "수급", "--json"])

    assert first.stdout == second.stdout


def test_tokenizer_splits_paths_and_normalizes_plurals() -> None:
    assert tokenize("kis.stock.current-price") == ["kis", "stock", "current", "price"]
    assert tokenize("stocks foreigners indices") == ["stock", "foreigner", "index"]
    # Hangul never reaches the index; it is handled by alias expansion instead.
    assert tokenize("외국인") == []


def test_expansion_prefers_the_longer_alias() -> None:
    terms, unmatched = expand_query("순매수")
    weights = dict(terms)

    assert "buy" in weights and "net" in weights
    assert not unmatched


def test_typed_terms_outweigh_expanded_terms() -> None:
    terms, _ = expand_query("foreign 외국인")
    weights = dict(terms)

    assert weights["foreign"] == 1.0
    assert weights["foreigner"] < 1.0


def test_unmatched_hangul_is_reported() -> None:
    _, unmatched = expand_query("꿈나라")
    assert unmatched == ["꿈나라"]


def test_every_alias_expansion_exists_in_the_corpus() -> None:
    """A renamed command must not silently orphan an alias."""

    registry = RpcRegistry()
    index = search_module._build_index(registry)
    dead = {
        f"{key} -> {expansion}"
        for key, expansions in QUERY_ALIASES
        for expansion in expansions
        # Check the normalized form the engine actually scores with.
        if all(index.doc_freq.get(token, 0) == 0 for token in (tokenize(expansion) or [expansion]))
    }
    assert dead == set()


def test_no_alias_key_shadows_another() -> None:
    keys = [key for key, _ in QUERY_ALIASES]
    assert len(keys) == len(set(keys))


def test_index_is_cached_per_registry_object(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = RpcRegistry()
    search_module._INDEX_CACHE = None
    builds = {"count": 0}
    real = search_module._build_index

    def counting(reg):
        builds["count"] += 1
        return real(reg)

    monkeypatch.setattr(search_module, "_build_index", counting)
    search_commands(registry, "차트")
    search_commands(registry, "배당")
    assert builds["count"] == 1

    search_commands(RpcRegistry(), "차트")
    assert builds["count"] == 2
    search_module._INDEX_CACHE = None
