"""Tests for KIS RPC handler patterns using mock sessions."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from cluefin_rpc.handlers.kis.domestic_basic_quote import (
    handle_kis_stock_asking_expected,
    handle_kis_stock_conclusion,
    handle_kis_stock_current_price,
    handle_kis_stock_current_price_2,
    handle_kis_stock_daily,
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
    """Return a session mock where session.get_kis() returns a MagicMock."""
    session = MagicMock()
    return session


def _make_item(**kwargs):
    """Create a SimpleNamespace with given attributes (simulates a KIS output item)."""
    return SimpleNamespace(**kwargs)


# ---------------------------------------------------------------------------
# Pattern 1: Direct field access (handle_kis_stock_current_price)
# ---------------------------------------------------------------------------


class TestKisStockCurrentPrice:
    def test_success(self):
        session = _mock_session()
        item = _make_item(
            stck_prpr="65000",
            prdy_ctrt="1.23",
            prdy_vrss="800",
            prdy_vrss_sign="2",
            acml_vol="12345678",
            acml_tr_pbmn="98765432100",
            stck_oprc="64000",
            stck_hgpr="66000",
            stck_lwpr="63500",
            stck_mxpr="83000",
            stck_llam="45000",
            stck_sdpr="64200",
            hts_avls="400000000",
            per="12.5",
            pbr="1.8",
            eps="5200",
            bps="36000",
            w52_hgpr="70000",
            w52_lwpr="50000",
            hts_frgn_ehrt="35.5",
            frgn_ntby_qty="100000",
            bstp_kor_isnm="전기전자",
        )
        body = SimpleNamespace(output=item)
        session.get_kis().domestic_basic_quote.get_stock_current_price.return_value = SimpleNamespace(body=body)

        result = handle_kis_stock_current_price({"stock_code": "005930"}, session)

        assert result["stock_code"] == "005930"
        assert result["current_price"] == 65000
        assert result["change_rate"] == 1.23
        assert result["volume"] == 12345678
        assert result["per"] == 12.5
        assert result["sector_name"] == "전기전자"

    def test_none_output(self):
        session = _mock_session()
        body = SimpleNamespace(output=None)
        session.get_kis().domestic_basic_quote.get_stock_current_price.return_value = SimpleNamespace(body=body)

        result = handle_kis_stock_current_price({"stock_code": "005930"}, session)
        assert result == {"stock_code": "005930", "error": "No data returned"}

    def test_default_market(self):
        session = _mock_session()
        body = SimpleNamespace(output=None)
        session.get_kis().domestic_basic_quote.get_stock_current_price.return_value = SimpleNamespace(body=body)

        handle_kis_stock_current_price({"stock_code": "005930"}, session)
        session.get_kis().domestic_basic_quote.get_stock_current_price.assert_called_with("J", "005930")


# ---------------------------------------------------------------------------
# Pattern 2: extract_output single model (handle_kis_stock_current_price_2)
# ---------------------------------------------------------------------------


class TestKisStockCurrentPrice2:
    def test_success(self):
        session = _mock_session()
        model = FakeModel({"warning": "N", "vi_status": "normal"})
        body = SimpleNamespace(output=model)
        session.get_kis().domestic_basic_quote.get_stock_current_price_2.return_value = SimpleNamespace(body=body)

        result = handle_kis_stock_current_price_2({"stock_code": "005930"}, session)
        assert result["stock_code"] == "005930"
        assert result["warning"] == "N"
        assert result["vi_status"] == "normal"

    def test_none_output(self):
        session = _mock_session()
        body = SimpleNamespace(output=None)
        session.get_kis().domestic_basic_quote.get_stock_current_price_2.return_value = SimpleNamespace(body=body)

        result = handle_kis_stock_current_price_2({"stock_code": "005930"}, session)
        assert result == {"stock_code": "005930", "error": "No data returned"}


# ---------------------------------------------------------------------------
# Pattern 3: extract_output list (handle_kis_stock_conclusion)
# ---------------------------------------------------------------------------


class TestKisStockConclusion:
    def test_list_data(self):
        session = _mock_session()
        models = [FakeModel({"time": "100000", "price": 65000}), FakeModel({"time": "100001", "price": 65100})]
        body = SimpleNamespace(output=models)
        session.get_kis().domestic_basic_quote.get_stock_current_price_conclusion.return_value = SimpleNamespace(
            body=body
        )

        result = handle_kis_stock_conclusion({"stock_code": "005930"}, session)
        assert result["stock_code"] == "005930"
        assert len(result["data"]) == 2
        assert result["data"][0] == {"time": "100000", "price": 65000}

    def test_none_output_returns_none_data(self):
        session = _mock_session()
        body = SimpleNamespace(output=None)
        session.get_kis().domestic_basic_quote.get_stock_current_price_conclusion.return_value = SimpleNamespace(
            body=body
        )

        result = handle_kis_stock_conclusion({"stock_code": "005930"}, session)
        assert result["data"] is None


# ---------------------------------------------------------------------------
# Pattern 4: dual output (handle_kis_stock_asking_expected)
# ---------------------------------------------------------------------------


class TestKisStockAskingExpected:
    def test_summary_and_data(self):
        session = _mock_session()
        summary = FakeModel({"expected_price": 65500})
        data = [FakeModel({"ask": 65600, "bid": 65400})]
        body = SimpleNamespace(output1=summary, output2=data)
        session.get_kis().domestic_basic_quote.get_stock_current_price_asking_expected_conclusion.return_value = (
            SimpleNamespace(body=body)
        )

        result = handle_kis_stock_asking_expected({"stock_code": "005930"}, session)
        assert result["stock_code"] == "005930"
        assert result["summary"] == {"expected_price": 65500}
        assert result["data"] == [{"ask": 65600, "bid": 65400}]


# ---------------------------------------------------------------------------
# Pattern 5: Direct list iteration (handle_kis_stock_daily)
# ---------------------------------------------------------------------------


class TestKisStockDaily:
    def test_ohlcv_list(self):
        session = _mock_session()
        items = [
            _make_item(
                stck_bsop_date="20250101",
                stck_oprc="64000",
                stck_hgpr="66000",
                stck_lwpr="63500",
                stck_clpr="65000",
                acml_vol="10000000",
                prdy_ctrt="1.5",
                hts_frgn_ehrt="35.0",
            ),
            _make_item(
                stck_bsop_date="20250102",
                stck_oprc="65000",
                stck_hgpr="67000",
                stck_lwpr="64500",
                stck_clpr="66000",
                acml_vol="12000000",
                prdy_ctrt="1.54",
                hts_frgn_ehrt="35.2",
            ),
        ]
        body = SimpleNamespace(output=items)
        session.get_kis().domestic_basic_quote.get_stock_current_price_daily.return_value = SimpleNamespace(body=body)

        result = handle_kis_stock_daily({"stock_code": "005930"}, session)
        assert result["stock_code"] == "005930"
        assert len(result["data"]) == 2
        assert result["data"][0]["date"] == "20250101"
        assert result["data"][0]["open"] == 64000
        assert result["data"][0]["close"] == 65000
        assert result["data"][0]["volume"] == 10000000

    def test_empty_data(self):
        session = _mock_session()
        body = SimpleNamespace(output=None)
        session.get_kis().domestic_basic_quote.get_stock_current_price_daily.return_value = SimpleNamespace(body=body)

        result = handle_kis_stock_daily({"stock_code": "005930"}, session)
        assert result == {"stock_code": "005930", "data": []}

    def test_custom_period_and_adj(self):
        session = _mock_session()
        body = SimpleNamespace(output=[])
        session.get_kis().domestic_basic_quote.get_stock_current_price_daily.return_value = SimpleNamespace(body=body)

        handle_kis_stock_daily({"stock_code": "005930", "period": "W", "adj_price": "0"}, session)
        session.get_kis().domestic_basic_quote.get_stock_current_price_daily.assert_called_with("J", "005930", "W", "0")
