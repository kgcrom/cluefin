from __future__ import annotations

from cluefin_openapi_cli.registry import RpcRegistry


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
