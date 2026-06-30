from __future__ import annotations

import pytest
from _handler_fakes import FakeSession, assert_calls_client_once, assert_registers_all

from cluefin_openapi_cli.handlers import dart as handlers


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_dart_handlers() -> None:
    assert_registers_all(handlers.register_dart_handlers, handlers._ALL_HANDLERS, "dart")


def test_disclosure_search_forwards_only_provided_params() -> None:
    session = FakeSession()
    handlers.handle_disclosure_search({"corp_code": "00126380", "bgn_de": "20240101", "unknown": "x"}, session)
    _, method, _, kwargs = session.calls[0]
    assert method == "public_disclosure_search"
    assert kwargs == {"corp_code": "00126380", "bgn_de": "20240101"}


def test_corp_code_lookup_counts_returned_items() -> None:
    session = FakeSession()
    result = handlers.handle_corp_code_lookup({}, session)
    assert result["total"] == len(result["data"]) == 1


def test_corp_code_lookup_handles_empty_list() -> None:
    session = FakeSession(output_value=None)
    result = handlers.handle_corp_code_lookup({}, session)
    assert result == {"total": 0, "data": []}
