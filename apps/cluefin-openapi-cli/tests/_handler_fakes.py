"""Shared fakes for RPC handler tests.

Handlers follow one of two response shapes:

- Kiwoom handlers call ``extract_body(response)`` → ``response.body.model_dump()``.
- KIS handlers call ``extract_output(response, "output*")`` → ``response.body.output*.model_dump()``.
- DART handlers use the client return value directly (``result.model_dump()`` /
  ``result.list``), without a ``.body`` wrapper.

``FakeSession`` records every client call and returns a flexible ``_Result`` that
satisfies all three shapes, so a single fake drives the parametrized tests for
every handler module.
"""

from __future__ import annotations

from typing import Any

_PRESENT = object()

_SAMPLE_VALUES = {
    "amount_qty_type": "0",
    "exchange_type": "1",
    "market_type": "001",
    "period": "1",
    "stock_code": "KRX:005930",
    "stock_industry_type": "0",
    "sector_code": "0001",
    "pdno": "005930",
    "prdt_type_cd": "300",
    "start_date": "20240101",
    "end_date": "20240131",
    "bsns_year": "2024",
    "reprt_code": "11011",
    "corp_code": "00126380",
    "hour": "1",
}


class _Record:
    """Stands in for a KIS ``output*`` sub-model.

    Any attribute resolves to ``"1"`` (convertible by ``int``/``float`` and
    truthy), so handlers that read fields directly and cast them — e.g.
    ``int(item.stck_prpr)`` — work without enumerating every model field. It
    also exposes ``model_dump()`` for pass-through handlers and is iterable /
    indexable for handlers that loop over list outputs.
    """

    def __getattr__(self, name: str) -> str:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return "1"

    def model_dump(self) -> dict[str, str]:
        return {"value": "1"}

    def __iter__(self):
        return iter([_Record(), _Record()])

    def __getitem__(self, index) -> "_Record":
        return _Record()

    def __len__(self) -> int:
        return 2


class _Body:
    def __init__(self, method: str, output_value: Any = _PRESENT) -> None:
        self.__dict__["_method"] = method
        self.__dict__["_output_value"] = output_value

    def model_dump(self) -> dict[str, str]:
        return {"method": self.__dict__["_method"]}

    def __getattr__(self, name: str):
        if name.startswith("output"):
            if self.__dict__["_output_value"] is None:
                return None
            return _Record()
        raise AttributeError(name)


class _Result:
    """Return value of a faked client method.

    Supports ``.body`` (KIS/Kiwoom), ``.model_dump()`` and ``.list`` (DART).
    """

    def __init__(self, method: str, output_value: Any = _PRESENT) -> None:
        self._method = method
        self._output_value = output_value
        self.body = _Body(method, output_value)

    def model_dump(self) -> dict[str, str]:
        return {"method": self._method}

    @property
    def list(self) -> list[_Body]:
        if self._output_value is None:
            return []
        return [_Body(self._method)]


class _MethodRecorder:
    def __init__(self, calls: list, sub: str, output_value: Any) -> None:
        self.__dict__["_calls"] = calls
        self.__dict__["_sub"] = sub
        self.__dict__["_output_value"] = output_value

    def __getattr__(self, method_name: str):
        def call(*args, **kwargs):
            self.__dict__["_calls"].append((self.__dict__["_sub"], method_name, args, kwargs))
            return _Result(method_name, self.__dict__["_output_value"])

        return call


class _Client:
    def __init__(self, calls: list, output_value: Any) -> None:
        self.__dict__["_calls"] = calls
        self.__dict__["_output_value"] = output_value

    def __getattr__(self, sub_client: str) -> _MethodRecorder:
        return _MethodRecorder(self.__dict__["_calls"], sub_client, self.__dict__["_output_value"])


class FakeSession:
    """Session whose broker accessors return call-recording fake clients."""

    def __init__(self, output_value: Any = _PRESENT) -> None:
        self.calls: list[tuple[str, str, tuple, dict]] = []
        self._output_value = output_value

    def _client(self) -> _Client:
        return _Client(self.calls, self._output_value)

    def get_kis(self) -> _Client:
        return self._client()

    def get_kiwoom(self) -> _Client:
        return self._client()

    def get_dart(self) -> _Client:
        return self._client()


class FakeDispatcher:
    def __init__(self) -> None:
        self.registrations: list[tuple[str, object, object]] = []

    def register(self, name, handler, schema) -> None:
        self.registrations.append((name, handler, schema))


def sample_params(handler) -> dict[str, str]:
    """Build a params dict covering a handler's required fields."""
    required = handler._rpc_schema.parameters.get("required", [])
    return {name: _SAMPLE_VALUES.get(name, f"value_{name}") for name in required}


def assert_calls_client_once(handler) -> dict:
    """Call a handler with a present-data fake session; assert one client call."""
    session = FakeSession()
    result = handler(sample_params(handler), session)
    assert len(session.calls) == 1, f"{handler.__name__} made {len(session.calls)} client calls"
    assert isinstance(result, dict)
    return result


def assert_registers_all(register_fn, all_handlers, broker: str) -> None:
    dispatcher = FakeDispatcher()
    register_fn(dispatcher)
    registered_names = [name for name, _, _ in dispatcher.registrations]
    assert registered_names == [h._rpc_schema.name for h in all_handlers]
    assert all(schema.broker == broker for _, _, schema in dispatcher.registrations)
