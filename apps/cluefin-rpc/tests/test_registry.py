from __future__ import annotations

from cluefin_rpc.registry import build_cli_registry, list_cli_commands
from cluefin_rpc.server import _build_dispatcher


def test_cli_registry_matches_broker_rpc_surface():
    dispatcher = _build_dispatcher()
    broker_methods = {
        (item["broker"], item["name"])
        for item in dispatcher.list_methods()
        if item["broker"] in {"kis", "kiwoom", "dart"}
    }
    cli_registry = build_cli_registry()

    cli_methods = {(item.broker, item.method_name) for item in cli_registry.values()}
    assert cli_methods == broker_methods
    assert len(cli_registry) == 183


def test_cli_registry_has_unique_broker_first_paths():
    cli_registry = build_cli_registry()
    paths = list(cli_registry)
    assert len(paths) == len(set(paths))
    assert ("kis", "stock", "current-price") in cli_registry
    assert ("kiwoom", "chart", "tick") in cli_registry
    assert ("dart", "company-overview") in cli_registry


def test_list_cli_commands_filters_broker_methods_only():
    commands = list_cli_commands()
    assert commands
    assert all(command.broker in {"kis", "kiwoom", "dart"} for command in commands)
    assert all(command.category not in {"rpc", "session"} for command in commands)


def test_list_cli_commands_filtering():
    kis_stock_commands = list_cli_commands(broker="kis", category="stock")
    assert kis_stock_commands
    assert all(command.broker == "kis" for command in kis_stock_commands)
    assert all(command.category == "stock" for command in kis_stock_commands)
