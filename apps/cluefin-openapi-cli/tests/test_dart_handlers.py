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


def test_corp_code_lookup_reads_items_from_the_result_envelope() -> None:
    session = FakeSession()
    result = handlers.handle_corp_code_lookup({}, session)
    assert result["total"] == result["returned"] == len(result["data"]) == 2
    assert result["truncated"] is False


def test_corp_code_lookup_handles_empty_list() -> None:
    session = FakeSession(output_value=None)
    result = handlers.handle_corp_code_lookup({}, session)
    assert result == {"total": 0, "returned": 0, "truncated": False, "data": []}


def test_corp_code_lookup_filters_drop_non_matching_rows() -> None:
    session = FakeSession()
    # Faked rows answer "1" to every field, so any other value must filter them out.
    assert handlers.handle_corp_code_lookup({"stock_code": "020000"}, session)["total"] == 0
    assert handlers.handle_corp_code_lookup({"corp_code": "00188089"}, session)["total"] == 0
    assert handlers.handle_corp_code_lookup({"corp_name": "한섬"}, session)["total"] == 0
    assert handlers.handle_corp_code_lookup({"stock_code": "1"}, session)["total"] == 2


def test_corp_code_lookup_limit_caps_rows_and_flags_truncation() -> None:
    session = FakeSession()
    capped = handlers.handle_corp_code_lookup({"max_rows": 1}, session)
    assert capped["total"] == 2 and capped["returned"] == 1 and capped["truncated"] is True

    uncapped = handlers.handle_corp_code_lookup({"max_rows": 0}, session)
    assert uncapped["returned"] == 2 and uncapped["truncated"] is False
