from unittest.mock import MagicMock

from cluefin_desk.data.screener import ScreeningItem, StockScreener


def _make_mock_fetcher():
    return MagicMock()


def _make_pct_change_response(items_data):
    """Build mock response for get_top_percentage_change."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.flu_rt = d["flu_rt"]
        item.now_trde_qty = d["now_trde_qty"]
        item.pred_pre_sig = d.get("pred_pre_sig", "2")
        items.append(item)
    response.body.pred_pre_flu_rt_upper = items
    return response


def _make_volume_response(items_data):
    """Build mock response for get_top_trading_volume."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.flu_rt = d["flu_rt"]
        item.trde_qty = d["trde_qty"]
        item.pred_pre_sig = d.get("pred_pre_sig", "2")
        items.append(item)
    response.body.tdy_trde_qty_upper = items
    return response


def _make_value_response(items_data):
    """Build mock response for get_top_transaction_value."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.flu_rt = d["flu_rt"]
        item.now_trde_qty = d["now_trde_qty"]
        item.pred_pre_sig = d.get("pred_pre_sig", "2")
        items.append(item)
    response.body.trde_prica_upper = items
    return response


SAMPLE_ITEMS = [
    {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "cur_prc": "72000",
        "flu_rt": "3.50",
        "now_trde_qty": "15000000",
        "trde_qty": "15000000",
        "pred_pre_sig": "2",
    },
    {
        "stk_cd": "000660",
        "stk_nm": "SK하이닉스",
        "cur_prc": "185000",
        "flu_rt": "2.10",
        "now_trde_qty": "8000000",
        "trde_qty": "8000000",
        "pred_pre_sig": "2",
    },
]


class TestStockScreenerGetTopGainers:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_percentage_change.return_value = _make_pct_change_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_top_gainers()

        assert len(result) == 2
        assert isinstance(result[0], ScreeningItem)
        assert result[0].stock_code == "005930"
        assert result[0].stock_name == "삼성전자"
        assert result[0].current_price == "72000"
        assert result[0].change_rate == "3.50"
        assert result[0].rank == 1
        assert result[1].rank == 2

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_percentage_change.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_top_gainers()

        assert result == []


class TestStockScreenerGetTopVolume:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_trading_volume.return_value = _make_volume_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_top_volume()

        assert len(result) == 2
        assert result[0].stock_code == "005930"
        assert result[0].volume == "15000000"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_trading_volume.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_top_volume()

        assert result == []


class TestStockScreenerGetTopValue:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_transaction_value.return_value = _make_value_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_top_value()

        assert len(result) == 2
        assert result[0].stock_code == "005930"
        assert result[0].volume == "15000000"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_transaction_value.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_top_value()

        assert result == []
