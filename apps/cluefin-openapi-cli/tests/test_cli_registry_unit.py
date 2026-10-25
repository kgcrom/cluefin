from __future__ import annotations

from cluefin_openapi_cli.registry import CommandSpec, EmptyRegistry, get_registry, set_registry_provider


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


def test_get_registry_reuses_provider_instance_until_provider_changes() -> None:
    calls = 0

    class CountingRegistry(EmptyRegistry):
        pass

    def provider() -> CountingRegistry:
        nonlocal calls
        calls += 1
        return CountingRegistry()

    try:
        set_registry_provider(provider)
        first = get_registry()
        second = get_registry()

        assert first is second
        assert calls == 1

        set_registry_provider(EmptyRegistry)
        assert get_registry() is not first
    finally:
        set_registry_provider(EmptyRegistry)
