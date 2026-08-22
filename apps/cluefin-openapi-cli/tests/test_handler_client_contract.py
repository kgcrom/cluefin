"""핸들러 ↔ 실제 broker client 계약 검증.

`tests/_handler_fakes.py`의 페이크는 `__getattr__`로 어떤 메서드명이든 받아주므로,
존재하지 않는 client 메서드 호출이나 응답 모델에 없는 output 필드 접근이
단위 테스트를 통과해 버린다. 이 테스트는 모든 등록 핸들러를 실제 client
클래스·메서드 시그니처·응답 모델과 대조해 그 구멍을 막는다.
"""

from __future__ import annotations

import ast
import inspect
import typing
from functools import lru_cache

import pytest
from cluefin_openapi.dart._client import Client as DartClient
from cluefin_openapi.kis._http_client import HttpClient as KisClient
from cluefin_openapi.kiwoom._client import Client as KiwoomClient

from cluefin_openapi_cli.metadata import _sample_value
from cluefin_openapi_cli.registry import build_cli_registry


@lru_cache(maxsize=1)
def _real_clients() -> dict:
    return {
        "kis": KisClient(token="token", app_key="key", secret_key="secret", env="dev"),
        "kiwoom": KiwoomClient(token="token", env="dev"),
        "dart": DartClient(auth_key="key"),
    }


def _response_model(method) -> type | None:
    """반환 어노테이션에서 응답 body 모델을 추출한다.

    `KisHttpResponse[X]` / `KiwoomHttpResponse[X]` → X, DART처럼 모델을 직접
    반환하면 그 모델, 어노테이션이 없으면 None.
    """
    try:
        hints = typing.get_type_hints(method)
    except Exception:
        return None
    ret = hints.get("return")
    if ret is None:
        return None
    args = typing.get_args(ret)
    if args:
        return args[0]
    return ret if inspect.isclass(ret) else None


class _BodyProbe:
    """extract_output이 접근하는 body 필드명을 기록한다."""

    def __init__(self) -> None:
        object.__setattr__(self, "accessed", [])

    def model_dump(self) -> dict:
        return {}

    def __getattr__(self, field: str):
        self.accessed.append(field)
        return None


class _FakeResponse:
    def __init__(self, probe: _BodyProbe) -> None:
        self.body = probe

    def model_dump(self) -> dict:
        return {}


class _ContractMethod:
    def __init__(self, real_method, calls: list) -> None:
        self._real_method = real_method
        self._calls = calls

    def __call__(self, *args, **kwargs):
        inspect.signature(self._real_method).bind(*args, **kwargs)
        probe = _BodyProbe()
        self._calls.append((self._real_method, probe))
        return _FakeResponse(probe)


class _ContractSubClient:
    def __init__(self, real_sub, calls: list) -> None:
        self._real_sub = real_sub
        self._calls = calls

    def __getattr__(self, method_name: str) -> _ContractMethod:
        real_method = getattr(self._real_sub, method_name)  # 존재하지 않으면 AttributeError
        return _ContractMethod(real_method, self._calls)


class _ContractClient:
    def __init__(self, real_client, calls: list) -> None:
        self._real_client = real_client
        self._calls = calls

    def __getattr__(self, sub_name: str) -> _ContractSubClient:
        real_sub = getattr(self._real_client, sub_name)  # 존재하지 않으면 AttributeError
        return _ContractSubClient(real_sub, self._calls)


class _ContractSession:
    def __init__(self) -> None:
        self.calls: list = []

    def get_kis(self) -> _ContractClient:
        return _ContractClient(_real_clients()["kis"], self.calls)

    def get_kiwoom(self) -> _ContractClient:
        return _ContractClient(_real_clients()["kiwoom"], self.calls)

    def get_dart(self) -> _ContractClient:
        return _ContractClient(_real_clients()["dart"], self.calls)


def _build_params(parameters: dict) -> dict:
    properties = parameters.get("properties", {})
    return {field: _sample_value(field, schema) for field, schema in properties.items()}


_ALL_COMMANDS = sorted(build_cli_registry().values(), key=lambda spec: spec.qualified_name)


@pytest.mark.parametrize("spec", _ALL_COMMANDS, ids=lambda spec: spec.qualified_name)
def test_handler_matches_real_client_contract(spec):
    session = _ContractSession()
    params = _build_params(spec.parameters)

    spec.executor(params, session)

    assert session.calls, f"{spec.qualified_name}: 핸들러가 client 메서드를 호출하지 않았다"
    for real_method, probe in session.calls:
        model = _response_model(real_method)
        if model is None or not hasattr(model, "model_fields"):
            continue
        for field in probe.accessed:
            assert field in model.model_fields, (
                f"{spec.qualified_name}: {real_method.__qualname__} 응답 모델 "
                f"{model.__name__}에 없는 필드 `{field}`를 읽는다 "
                f"(실제 필드: {sorted(model.model_fields)})"
            )


def _params_keys_read(fn) -> set[str]:
    """핸들러 소스에서 params["x"] / params.get("x", …)로 읽는 키를 수집한다."""
    tree = ast.parse(inspect.getsource(fn))
    keys: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id == "params"
            and isinstance(node.slice, ast.Constant)
        ):
            keys.add(node.slice.value)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "params"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            keys.add(node.args[0].value)
    return keys


@pytest.mark.parametrize("spec", _ALL_COMMANDS, ids=lambda spec: spec.qualified_name)
def test_handler_reads_only_declared_params(spec):
    """핸들러가 읽는 params 키는 모두 스키마에 선언되어야 한다.

    스키마에 없는 키는 describe/--help에 노출되지 않아 agent가 존재 자체를
    알 수 없는 숨은 파라미터가 된다.
    """
    declared = set(spec.parameters.get("properties", {}))
    hidden = _params_keys_read(spec.executor) - declared
    assert not hidden, f"{spec.qualified_name}: 스키마에 선언되지 않은 params 키 {sorted(hidden)}"
