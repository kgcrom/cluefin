from __future__ import annotations

from cluefin_ta_cli.metadata import missing_taxonomy_names
from cluefin_ta_cli.registry import Registry, build_registry


def test_registry_contains_all_expected_commands() -> None:
    registry = Registry()

    commands = registry.list_commands(category="ta")

    assert len(commands) == 11
    assert [command.name for command in commands] == [
        "adx",
        "atr",
        "bbands",
        "ema",
        "macd",
        "mdd",
        "obv",
        "rsi",
        "sharpe",
        "sma",
        "stoch",
    ]


def test_command_spec_qualified_name() -> None:
    registry = Registry()

    spec = registry.resolve_command(("ta", "sma"))

    assert spec is not None
    assert spec.path == ("ta", "sma")
    assert spec.qualified_name == "ta.sma"
    assert spec.description == "Simple Moving Average."


def test_command_spec_exposes_agent_metadata() -> None:
    registry = Registry()

    spec = registry.resolve_command(("ta", "sma"))

    assert spec is not None
    assert spec.domains == ("technical-indicator",)
    assert spec.tags == ("moving-average", "trend")
    assert spec.use_cases
    assert spec.examples
    assert spec.agent_notes


def test_all_commands_have_agent_metadata() -> None:
    registry = Registry()

    commands = registry.list_commands(category="ta")

    assert all(command.domains for command in commands)
    assert all(command.tags for command in commands)
    assert all(command.use_cases for command in commands)
    assert all(command.examples for command in commands)
    assert all(command.agent_notes for command in commands)


def test_ta_taxonomy_catalog_covers_all_real_domains_and_tags() -> None:
    registry = Registry()

    commands = registry.list_commands(category="ta")
    domains = {domain for command in commands for domain in command.domains}
    tags = {tag for command in commands for tag in command.tags}

    assert missing_taxonomy_names(kind="domains", names=domains) == set()
    assert missing_taxonomy_names(kind="tags", names=tags) == set()


def test_registry_filters_by_domain_and_tag() -> None:
    registry = Registry()

    assert [command.name for command in registry.list_commands(category="ta", domain="risk-metric")] == ["mdd"]
    assert {command.name for command in registry.list_commands(category="ta", tag="moving-average")} == {
        "bbands",
        "ema",
        "macd",
        "sma",
    }


def test_representative_ta_tags() -> None:
    registry = Registry()

    assert {"moving-average", "trend"}.issubset(registry.resolve_command(("ta", "sma")).tags)
    assert {"moving-average", "trend"}.issubset(registry.resolve_command(("ta", "ema")).tags)
    assert "momentum" in registry.resolve_command(("ta", "rsi")).tags
    assert "momentum" in registry.resolve_command(("ta", "macd")).tags
    assert "momentum" in registry.resolve_command(("ta", "stoch")).tags
    assert "trend" in registry.resolve_command(("ta", "adx")).tags
    assert "portfolio-risk" in registry.resolve_command(("ta", "mdd")).tags
    assert "portfolio-risk" in registry.resolve_command(("ta", "sharpe")).tags


def test_registry_paths_are_unique() -> None:
    registry = build_registry()

    assert len(registry) == len(set(registry))


def test_registry_command_names_are_category_prefixed() -> None:
    registry = Registry()

    assert {command.qualified_name for command in registry.list_commands(category="ta")} == {
        f"ta.{command.name}" for command in registry.list_commands(category="ta")
    }
