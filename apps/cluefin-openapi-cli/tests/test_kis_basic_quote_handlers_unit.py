from __future__ import annotations

import pytest

from cluefin_openapi_cli.handlers.kis import domestic_basic_quote as handlers

from ._handler_fakes import FakeSession, assert_calls_client_once, assert_registers_all

# `chart.technical` and `chart.trend_setup` are not 1:1 client passthroughs: they page
# the date window until they have enough candles (trend-setup also reads basic-info and
# the index), so the "exactly one client call" contract does not describe them. They have
# their own coverage in `test_kis_technical_handler_unit.py` / `test_kis_trend_setup_handler_unit.py`.
_COMPUTING = (handlers.handle_kis_chart_technical, handlers.handle_kis_chart_trend_setup)
_PASSTHROUGH_HANDLERS = [handler for handler in handlers._ALL_HANDLERS if handler not in _COMPUTING]


@pytest.mark.parametrize("handler", _PASSTHROUGH_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_kis_basic_quote_handlers() -> None:
    assert_registers_all(handlers.register_kis_basic_quote_handlers, handlers._ALL_HANDLERS, "kis")


# ---------------------------------------------------------------------------
# current-price on a delisted code
# ---------------------------------------------------------------------------


class _FakeValidationError(Exception):
    """Stands in for KISValidationError: the body came back without the price fields."""


class _DelistedSession:
    def __init__(self, abol_dt: str, kosdaq_abol_dt: str = "") -> None:
        self.calls: list[str] = []
        info = type("Info", (), {"scts_mket_lstg_abol_dt": abol_dt, "kosdaq_mket_lstg_abol_dt": kosdaq_abol_dt})()
        self._info = type("Response", (), {"body": type("Body", (), {"output": info})()})()

    def get_kis(self):
        session = self

        class _Quote:
            def get_stock_current_price(self, market, code):
                session.calls.append("current-price")
                raise _FakeValidationError("DomesticStockCurrentPrice validation failed (8 error(s))")

        class _Info:
            def get_stock_basic_info(self, prdt_type_cd, pdno):
                session.calls.append("basic-info")
                return session._info

        return type("Client", (), {"domestic_basic_quote": _Quote(), "domestic_stock_info": _Info()})()


def test_current_price_on_a_delisted_code_is_exit_4_delisted_with_the_date() -> None:
    session = _DelistedSession("20170307")

    with pytest.raises(handlers.CliError) as info:
        handlers.handle_kis_stock_current_price({"stock_code": "117930"}, session)

    assert info.value.exit_code == handlers.EXIT_BROKER
    assert info.value.error_type == "Delisted"
    assert info.value.data == {"stock_code": "117930", "delisted_on": "20170307"}
    assert session.calls == ["current-price", "basic-info"]


def test_current_price_validation_failure_on_a_listed_code_re_raises_the_original() -> None:
    session = _DelistedSession("", "00000000")

    with pytest.raises(_FakeValidationError):
        handlers.handle_kis_stock_current_price({"stock_code": "005930"}, session)

    assert session.calls == ["current-price", "basic-info"]


# ---------------------------------------------------------------------------
# chart.daily / chart.period: `adjusted` echoes the input polarity
# ---------------------------------------------------------------------------


def test_chart_daily_reports_adjusted_true_for_the_adjusted_literal() -> None:
    result = handlers.handle_kis_stock_daily({"stock_code": "005930", "adj_price": "1"}, FakeSession())
    assert result["adjusted"] is True


def test_chart_daily_reports_adjusted_false_for_the_unadjusted_literal() -> None:
    result = handlers.handle_kis_stock_daily({"stock_code": "005930", "adj_price": "0"}, FakeSession())
    assert result["adjusted"] is False


def test_chart_daily_defaults_to_adjusted_true() -> None:
    result = handlers.handle_kis_stock_daily({"stock_code": "005930"}, FakeSession())
    assert result["adjusted"] is True


def test_chart_period_reports_adjusted_true_for_the_opposite_literal() -> None:
    """chart.period's polarity is inverted from chart.daily: "0" means adjusted here."""

    result = handlers.handle_kis_stock_period_quote(
        {"stock_code": "005930", "start_date": "20240101", "end_date": "20240131", "adj_price": "0"}, FakeSession()
    )
    assert result["adjusted"] is True


def test_chart_period_reports_adjusted_false_for_the_opposite_literal() -> None:
    result = handlers.handle_kis_stock_period_quote(
        {"stock_code": "005930", "start_date": "20240101", "end_date": "20240131", "adj_price": "1"}, FakeSession()
    )
    assert result["adjusted"] is False


def test_chart_period_defaults_to_adjusted_true() -> None:
    result = handlers.handle_kis_stock_period_quote(
        {"stock_code": "005930", "start_date": "20240101", "end_date": "20240131"}, FakeSession()
    )
    assert result["adjusted"] is True
