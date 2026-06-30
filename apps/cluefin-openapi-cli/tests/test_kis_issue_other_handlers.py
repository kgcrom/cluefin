from __future__ import annotations

import pytest
from _handler_fakes import assert_calls_client_once, assert_registers_all

from cluefin_openapi_cli.handlers.kis import domestic_issue_other as handlers


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_kis_issue_other_handlers() -> None:
    assert_registers_all(handlers.register_kis_issue_other_handlers, handlers._ALL_HANDLERS, "kis")
