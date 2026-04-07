from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Protocol

from cluefin_openapi import BrokerClientFactory

from cluefin_openapi_cli.handlers.dart import _ALL_HANDLERS as DART_HANDLERS
from cluefin_openapi_cli.handlers.kis import get_kis_handlers
from cluefin_openapi_cli.handlers.kiwoom import get_kiwoom_handlers


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Metadata and executor wiring for one CLI command."""

    broker: str
    category: str
    name: str
    description: str
    path_segments: tuple[str, ...]
    parameters: dict[str, Any] = field(default_factory=dict)
    returns: dict[str, Any] = field(default_factory=dict)
    executor: Callable[[dict[str, Any], Any], Any] | None = None

    @property
    def path(self) -> tuple[str, ...]:
        return self.path_segments

    @property
    def qualified_name(self) -> str:
        return ".".join(self.path_segments)


class RegistryProtocol(Protocol):
    def list_commands(
        self,
        *,
        broker: str | None = None,
        category: str | None = None,
    ) -> list[CommandSpec]:
        """Return commands filtered by broker and category."""

    def get_command(self, broker: str, category: str, name: str) -> CommandSpec | None:
        """Return one command definition when available."""

    def resolve_command(self, path_segments: tuple[str, ...]) -> CommandSpec | None:
        """Return one command using broker-first CLI path segments."""

    def iter_brokers(self) -> Iterable[str]:
        """Return known brokers."""

    def invoke_command(self, command: CommandSpec, params: dict[str, Any]) -> Any:
        """Execute one command."""


class EmptyRegistry:
    """Default registry used until the command registry is wired in."""

    def list_commands(
        self,
        *,
        broker: str | None = None,
        category: str | None = None,
    ) -> list[CommandSpec]:
        return []

    def get_command(self, broker: str, category: str, name: str) -> CommandSpec | None:
        return None

    def resolve_command(self, path_segments: tuple[str, ...]) -> CommandSpec | None:
        return None

    def iter_brokers(self) -> Iterable[str]:
        return ()

    def invoke_command(self, command: CommandSpec, params: dict[str, Any]) -> Any:
        raise RuntimeError("No registry is configured.")


class _BrokerSession:
    def __init__(self, broker: str, client_factory: BrokerClientFactory | None = None) -> None:
        self._broker = broker
        self._client_factory = client_factory or BrokerClientFactory()
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = self._client_factory.create(self._broker)
        return self._client

    def get_kis(self):
        if self._broker != "kis":
            raise RuntimeError("KIS client requested from non-KIS session.")
        return self._get_client()

    def get_kiwoom(self):
        if self._broker != "kiwoom":
            raise RuntimeError("Kiwoom client requested from non-Kiwoom session.")
        return self._get_client()

    def get_dart(self):
        if self._broker != "dart":
            raise RuntimeError("DART client requested from non-DART session.")
        return self._get_client()


def _kebab_case(value: str) -> str:
    return value.replace("_", "-").replace(".", "-")


def _iter_broker_handlers() -> Iterable[Callable[..., Any]]:
    yield from get_kis_handlers()
    yield from get_kiwoom_handlers()
    yield from DART_HANDLERS


def build_cli_registry() -> dict[tuple[str, ...], CommandSpec]:
    registry: dict[tuple[str, ...], CommandSpec] = {}

    for handler in _iter_broker_handlers():
        schema = handler._rpc_schema
        method_name = schema.name

        if schema.broker == "dart":
            _, leaf_name = method_name.split(".", 1)
            category = "dart"
            path_segments = ("dart", _kebab_case(leaf_name))
            command_name = _kebab_case(leaf_name)
        else:
            category, leaf_name = method_name.split(".", 1)
            path_segments = (schema.broker, _kebab_case(category), _kebab_case(leaf_name))
            command_name = _kebab_case(leaf_name)

        if path_segments in registry:
            raise ValueError(f"Duplicate CLI path detected: {' '.join(path_segments)}")

        registry[path_segments] = CommandSpec(
            broker=schema.broker,
            category=category,
            name=command_name,
            description=schema.description,
            path_segments=path_segments,
            parameters=schema.parameters,
            returns=schema.returns,
            executor=handler,
        )

    return registry


class RpcRegistry:
    """CLI command registry with broker metadata and executors."""

    def __init__(self, client_factory: BrokerClientFactory | None = None) -> None:
        self._client_factory = client_factory or BrokerClientFactory()
        self._commands = build_cli_registry()

    def list_commands(self, *, broker: str | None = None, category: str | None = None) -> list[CommandSpec]:
        commands = list(self._commands.values())
        if broker is not None:
            commands = [command for command in commands if command.broker == broker]
        if category is not None:
            commands = [command for command in commands if command.category == category]
        return sorted(commands, key=lambda command: command.path_segments)

    def get_command(self, broker: str, category: str, name: str) -> CommandSpec | None:
        return self.resolve_command((broker, category, name))

    def resolve_command(self, path_segments: tuple[str, ...]) -> CommandSpec | None:
        return self._commands.get(path_segments)

    def iter_brokers(self) -> Iterable[str]:
        return sorted({command.broker for command in self._commands.values()})

    def invoke_command(self, command: CommandSpec, params: dict[str, Any]) -> Any:
        if command.executor is None:
            raise RuntimeError(f"Command `{command.qualified_name}` has no executor.")

        session = _BrokerSession(command.broker, client_factory=self._client_factory)
        return command.executor(params, session)


_registry_provider: Callable[[], RegistryProtocol] = RpcRegistry


def set_registry_provider(provider: Callable[[], RegistryProtocol]) -> None:
    """Install a registry provider for runtime and tests."""

    global _registry_provider
    _registry_provider = provider


def get_registry() -> RegistryProtocol:
    """Return the active registry instance."""

    return _registry_provider()
