from __future__ import annotations

import pytest

from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers

from ._handler_fakes import (
    FakeSession,
    assert_calls_client_once,
    assert_registers_all,
    sample_params,
)

# valuation calls KIS and DART several times and computes; test_kis_opinion_valuation_unit.py covers it.
_PASS_THROUGH_HANDLERS = [h for h in handlers._ALL_HANDLERS if h is not handlers.handle_kis_stock_valuation]


@pytest.mark.parametrize("handler", _PASS_THROUGH_HANDLERS, ids=lambda h: h._rpc_schema.name)
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
    assert set(result) == {"summary", "data", "data_detail", "periods", "table", "note"}


def test_estimated_earnings_table_labels_rows_and_applies_scale() -> None:
    # 005930 as served on 2026-10-18: FY2023 column of the first data row and detail rows.
    periods = ["2023.12", "2024.12", "2025.12", "2026.12E", "2027.12E"]
    data = [
        {"data1": "2589355.0", "data2": "3008709.0", "data3": "3336059.0", "data4": "7109715.0", "data5": "9666551.0"},
        {"data1": "-143.0", "data2": "162.0", "data3": "109.0", "data4": "1131.0", "data5": "360.0"},
    ]
    detail = [
        {"data1": "452335.0", "data2": "", "data3": "905276.0", "data4": "4269289.0", "data5": "6449280.0"},
        {"data1": "21310.0", "data2": "49500.0", "data3": "66050.0", "data4": "462090.0", "data5": "672398.0"},
    ]

    table = handlers._estimate_table(data, handlers._ESTIMATE_ROWS, periods)
    assert [row["metric"] for row in table] == ["revenue", "revenue_growth_yoy"]
    assert table[0]["unit"] == "억원" and table[0]["values"]["2023.12"] == 2589355.0
    assert table[1]["unit"] == "%" and table[1]["values"]["2023.12"] == pytest.approx(-14.3)

    detail_table = handlers._estimate_table(detail, handlers._ESTIMATE_DETAIL_ROWS, periods)
    assert detail_table[0]["metric"] == "ebitda" and detail_table[0]["values"]["2024.12"] is None
    assert detail_table[1]["metric"] == "eps" and detail_table[1]["values"]["2023.12"] == 2131.0
    # Fewer response rows than the layout: only the rows that exist are labelled.
    assert len(detail_table) == 2


def test_sample_params_covers_required_fields() -> None:
    params = sample_params(handlers.handle_kis_investment_opinion)
    assert {"stock_code", "start_date", "end_date"} <= set(params)
