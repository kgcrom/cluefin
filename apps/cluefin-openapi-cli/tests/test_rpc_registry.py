from __future__ import annotations

from cluefin_openapi_cli.registry import RpcRegistry, build_cli_registry


class _FakeDartResult:
    def __init__(self, corp_code: str) -> None:
        self.corp_code = corp_code

    def model_dump(self):
        return {"corp_code": self.corp_code}


class _FakeDartPublicDisclosure:
    def company_overview(self, corp_code: str):
        return _FakeDartResult(corp_code)


class _FakeDartClient:
    def __init__(self) -> None:
        self.public_disclosure = _FakeDartPublicDisclosure()


class _FakeFactory:
    def create(self, broker: str):
        assert broker == "dart"
        return _FakeDartClient()


def test_rpc_registry_lists_real_commands() -> None:
    registry = RpcRegistry(client_factory=_FakeFactory())
    commands = registry.list_commands(broker="dart")

    assert commands
    assert any(command.path_segments == ("dart", "company-overview") for command in commands)


def test_cli_registry_keeps_existing_command_surface() -> None:
    registry = build_cli_registry()

    assert len(registry) == 183
    assert ("kis", "stock", "current-price") in registry
    assert ("kiwoom", "chart", "tick") in registry
    assert ("dart", "company-overview") in registry
    assert len(registry) == len(set(registry))


def test_cli_registry_commands_expose_agent_metadata() -> None:
    registry = build_cli_registry()
    command = registry[("kis", "stock", "current-price")]

    assert command.domains
    assert command.tags
    assert command.use_cases == ()
    assert command.examples == ()
    assert command.agent_notes is None
    assert command.required_credentials == ("KIS_APP_KEY", "KIS_SECRET_KEY")
    assert command.side_effect == "read"


def test_cli_registry_all_commands_have_domain_tag_and_credentials() -> None:
    registry = build_cli_registry()

    assert all(command.domains for command in registry.values())
    assert all(command.tags for command in registry.values())
    assert all(command.required_credentials for command in registry.values())
    assert {command.side_effect for command in registry.values()} == {"read"}


def test_cli_registry_maps_representative_domains_and_tags() -> None:
    registry = build_cli_registry()

    assert "chart" in registry[("kis", "chart", "period")].domains
    assert {"news", "market"}.issubset(registry[("kis", "market", "announcement")].domains)
    assert "corporate-actions" in registry[("kis", "schedule", "dividend")].domains
    assert {"theme", "market"}.issubset(registry[("kiwoom", "theme", "group")].domains)
    assert {"news", "statements"}.issubset(registry[("dart", "disclosure-search")].domains)

    assert "ohlcv" in registry[("kis", "chart", "period")].tags
    assert "announcement" in registry[("kis", "market", "announcement")].tags
    assert "theme-group" in registry[("kiwoom", "theme", "group")].tags


def test_rpc_registry_resolves_real_command_path() -> None:
    registry = RpcRegistry(client_factory=_FakeFactory())
    command = registry.resolve_command(("dart", "company-overview"))

    assert command is not None
    assert command.broker == "dart"
    assert command.executor is not None


def test_rpc_registry_invokes_real_executor_with_fake_client() -> None:
    registry = RpcRegistry(client_factory=_FakeFactory())
    command = registry.resolve_command(("dart", "company-overview"))

    assert command is not None
    result = registry.invoke_command(command, {"corp_code": "00126380"})

    assert result == {"corp_code": "00126380"}
