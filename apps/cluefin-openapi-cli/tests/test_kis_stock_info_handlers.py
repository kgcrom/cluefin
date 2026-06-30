from __future__ import annotations

import pytest
from _handler_fakes import (
    FakeSession,
    assert_calls_client_once,
    assert_registers_all,
    sample_params,
)

from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_kis_stock_info_handlers() -> None:
    assert_registers_all(handlers.register_kis_stock_info_handlers, handlers._ALL_HANDLERS, "kis")


def test_product_basic_info_reports_missing_output() -> None:
    session = FakeSession(output_value=None)
    result = handlers.handle_kis_product_basic_info({"pdno": "005930", "prdt_type_cd": "300"}, session)
    assert result == {"error": "No data returned"}


def test_stock_basic_info_reports_missing_output() -> None:
    session = FakeSession(output_value=None)
    result = handlers.handle_kis_stock_basic_info({"pdno": "005930"}, session)
    assert result == {"error": "No data returned"}


def test_stock_basic_info_defaults_product_type() -> None:
    session = FakeSession()
    handlers.handle_kis_stock_basic_info({"pdno": "005930"}, session)
    _, method, args, _ = session.calls[0]
    assert method == "get_stock_basic_info"
    assert args[0] == "300"


def test_estimated_earnings_collects_all_outputs() -> None:
    session = FakeSession()
    result = handlers.handle_kis_estimated_earnings({"stock_code": "005930"}, session)
    assert set(result) == {"summary", "data", "data_detail", "periods"}


def test_sample_params_covers_required_fields() -> None:
    params = sample_params(handlers.handle_kis_investment_opinion)
    assert {"stock_code", "start_date", "end_date"} <= set(params)
