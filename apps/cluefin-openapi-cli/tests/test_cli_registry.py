from __future__ import annotations

from cluefin_openapi_cli.registry import CommandSpec, EmptyRegistry


def test_command_spec_qualified_name() -> None:
    spec = CommandSpec(
        broker="kis",
        category="stock",
        name="current-price",
        description="Current price lookup",
        path_segments=("kis", "stock", "current-price"),
    )

    assert spec.path == ("kis", "stock", "current-price")
    assert spec.qualified_name == "kis.stock.current-price"


def test_empty_registry_is_safe() -> None:
    registry = EmptyRegistry()

    assert registry.list_commands() == []
    assert registry.get_command("kis", "stock", "current-price") is None
    assert registry.resolve_command(("kis", "stock", "current-price")) is None
    assert list(registry.iter_brokers()) == []
