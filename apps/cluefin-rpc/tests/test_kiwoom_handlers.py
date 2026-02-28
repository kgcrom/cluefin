"""Tests for Kiwoom RPC handler patterns using mock sessions."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from cluefin_rpc.handlers.kiwoom.domestic_chart import handle_kiwoom_stock_tick
from cluefin_rpc.handlers.kiwoom.domestic_foreign import (
    handle_kiwoom_consecutive_net_buy_sell,
    handle_kiwoom_foreign_investor_trading_trend,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class FakeModel:
    def __init__(self, data: dict):
        self._data = data

    def model_dump(self) -> dict:
        return self._data


def _mock_session():
    session = MagicMock()
    return session


# ---------------------------------------------------------------------------
# TestKiwoomChartHandlers
# ---------------------------------------------------------------------------


class TestKiwoomChartHandlers:
    def test_stock_tick_returns_body(self):
        session = _mock_session()
        body = FakeModel({"date": "20250228", "ticks": [{"price": 100}]})
        session.get_kiwoom().chart.get_stock_tick.return_value = SimpleNamespace(body=body)

        result = handle_kiwoom_stock_tick({"stock_code": "KRX:039490", "tic_scope": "1"}, session)
        assert result == {"date": "20250228", "ticks": [{"price": 100}]}

    def test_default_optional_params(self):
        session = _mock_session()
        body = FakeModel({})
        session.get_kiwoom().chart.get_stock_tick.return_value = SimpleNamespace(body=body)

        handle_kiwoom_stock_tick({"stock_code": "KRX:039490", "tic_scope": "5"}, session)
        session.get_kiwoom().chart.get_stock_tick.assert_called_with(
            stk_cd="KRX:039490",
            tic_scope="5",
            upd_stkpc_tp="0",
            cont_yn="N",
            next_key="",
        )

    def test_custom_params_forwarded(self):
        session = _mock_session()
        body = FakeModel({})
        session.get_kiwoom().chart.get_stock_tick.return_value = SimpleNamespace(body=body)

        handle_kiwoom_stock_tick(
            {
                "stock_code": "KRX:039490",
                "tic_scope": "10",
                "adj_price": "1",
                "cont_yn": "Y",
                "next_key": "abc123",
            },
            session,
        )
        session.get_kiwoom().chart.get_stock_tick.assert_called_with(
            stk_cd="KRX:039490",
            tic_scope="10",
            upd_stkpc_tp="1",
            cont_yn="Y",
            next_key="abc123",
        )


# ---------------------------------------------------------------------------
# TestKiwoomForeignHandlers
# ---------------------------------------------------------------------------


class TestKiwoomForeignHandlers:
    def test_simple_handler_required_params(self):
        session = _mock_session()
        body = FakeModel({"trend": [{"date": "20250228", "net_buy": 1000}]})
        session.get_kiwoom().foreign.get_foreign_investor_trading_trend_by_stock.return_value = SimpleNamespace(
            body=body
        )

        result = handle_kiwoom_foreign_investor_trading_trend({"stock_code": "KRX:039490"}, session)
        assert result == {"trend": [{"date": "20250228", "net_buy": 1000}]}
        session.get_kiwoom().foreign.get_foreign_investor_trading_trend_by_stock.assert_called_with(
            stk_cd="KRX:039490",
            cont_yn="N",
            next_key="",
        )

    def test_complex_handler_required_and_optional_params(self):
        session = _mock_session()
        body = FakeModel({"data": []})
        session.get_kiwoom().foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner.return_value = (
            SimpleNamespace(body=body)
        )

        result = handle_kiwoom_consecutive_net_buy_sell(
            {
                "period": "5",
                "market_type": "001",
                "stock_industry_type": "0",
                "amount_qty_type": "1",
                "exchange_type": "1",
            },
            session,
        )
        assert result == {"data": []}
        session.get_kiwoom().foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner.assert_called_with(
            dt="5",
            mrkt_tp="001",
            stk_inds_tp="0",
            amt_qty_tp="1",
            stex_tp="1",
            netslmt_tp="2",
            strt_dt="",
            end_dt="",
        )

    def test_complex_handler_custom_optional_params(self):
        session = _mock_session()
        body = FakeModel({"data": []})
        session.get_kiwoom().foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner.return_value = (
            SimpleNamespace(body=body)
        )

        handle_kiwoom_consecutive_net_buy_sell(
            {
                "period": "0",
                "market_type": "101",
                "stock_industry_type": "1",
                "amount_qty_type": "0",
                "exchange_type": "3",
                "net_sell_buy_type": "2",
                "start_date": "20250101",
                "end_date": "20250228",
            },
            session,
        )
        session.get_kiwoom().foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner.assert_called_with(
            dt="0",
            mrkt_tp="101",
            stk_inds_tp="1",
            amt_qty_tp="0",
            stex_tp="3",
            netslmt_tp="2",
            strt_dt="20250101",
            end_dt="20250228",
        )


# ---------------------------------------------------------------------------
# Edge case: body without model_dump
# ---------------------------------------------------------------------------


class TestKiwoomEdgeCase:
    def test_body_without_model_dump(self):
        session = _mock_session()
        raw_body = {"raw": True}  # plain dict, no model_dump
        session.get_kiwoom().chart.get_stock_tick.return_value = SimpleNamespace(body=raw_body)

        result = handle_kiwoom_stock_tick({"stock_code": "KRX:039490", "tic_scope": "1"}, session)
        assert result == {}
