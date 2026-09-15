from __future__ import annotations

import pytest
from _handler_fakes import assert_calls_client_once, assert_registers_all

from cluefin_openapi_cli.handlers.kis import domestic_basic_quote as handlers

# `chart.technical` is the one handler in this module that is not a 1:1 client
# passthrough: it pages the date window until it has enough candles, so the
# "exactly one client call" contract does not describe it. It has its own
# coverage in `test_kis_technical_handler.py`.
_PASSTHROUGH_HANDLERS = [
    handler for handler in handlers._ALL_HANDLERS if handler is not handlers.handle_kis_chart_technical
]


@pytest.mark.parametrize("handler", _PASSTHROUGH_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_kis_basic_quote_handlers() -> None:
    assert_registers_all(handlers.register_kis_basic_quote_handlers, handlers._ALL_HANDLERS, "kis")
