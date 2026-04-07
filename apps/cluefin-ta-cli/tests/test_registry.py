from __future__ import annotations

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


def test_registry_paths_are_unique() -> None:
    registry = build_registry()

    assert len(registry) == len(set(registry))


def test_registry_command_names_are_category_prefixed() -> None:
    registry = Registry()

    assert {command.qualified_name for command in registry.list_commands(category="ta")} == {
        f"ta.{command.name}" for command in registry.list_commands(category="ta")
    }
