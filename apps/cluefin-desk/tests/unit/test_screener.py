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


def _make_foreigner_response(items_data):
    """Build mock response for get_top_foreigner_period_trading."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.trde_qty = d.get("trde_qty", "0")
        item.netprps_qty = d.get("netprps_qty", "0")
        items.append(item)
    response.body.for_dt_trde_upper = items
    return response


def _make_new_high_response(items_data):
    """Build mock response for get_new_high_low_price."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.flu_rt = d["flu_rt"]
        item.trde_qty = d.get("trde_qty", "0")
        item.pred_pre_sig = d.get("pred_pre_sig", "2")
        items.append(item)
    response.body.ntl_pric = items
    return response


def _make_volatility_response(items_data):
    """Build mock response for get_price_volatility."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.flu_rt = d["flu_rt"]
        item.trde_qty = d.get("trde_qty", "0")
        item.pred_pre_sig = d.get("pred_pre_sig", "2")
        item.jmp_rt = d.get("jmp_rt", "0")
        items.append(item)
    response.body.pric_jmpflu = items
    return response


def _make_margin_response(items_data):
    """Build mock response for get_top_margin_ratio."""
    response = MagicMock()
    items = []
    for d in items_data:
        item = MagicMock()
        item.stk_cd = d["stk_cd"]
        item.stk_nm = d["stk_nm"]
        item.cur_prc = d["cur_prc"]
        item.flu_rt = d["flu_rt"]
        item.now_trde_qty = d.get("now_trde_qty", "0")
        item.pred_pre_sig = d.get("pred_pre_sig", "2")
        item.crd_rt = d.get("crd_rt", "0")
        items.append(item)
    response.body.crd_rt_upper = items
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
        "netprps_qty": "5000000",
        "jmp_rt": "5.0",
        "crd_rt": "1.2",
    },
    {
        "stk_cd": "000660",
        "stk_nm": "SK하이닉스",
        "cur_prc": "185000",
        "flu_rt": "2.10",
        "now_trde_qty": "8000000",
        "trde_qty": "8000000",
        "pred_pre_sig": "2",
        "netprps_qty": "3000000",
        "jmp_rt": "3.0",
        "crd_rt": "0.8",
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


class TestStockScreenerGetTopLosers:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_percentage_change.return_value = _make_pct_change_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_top_losers()

        assert len(result) == 2
        assert result[0].stock_code == "005930"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_percentage_change.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_top_losers()

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


class TestStockScreenerGetTopForeignerNetBuy:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_foreigner_period_trading.return_value = _make_foreigner_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_top_foreigner_net_buy()

        assert len(result) == 2
        assert result[0].stock_code == "005930"
        assert result[0].extra == "5000000"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_foreigner_period_trading.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_top_foreigner_net_buy()

        assert result == []


class TestStockScreenerGetNewHighPrice:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_new_high_low_price.return_value = _make_new_high_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_new_high_price()

        assert len(result) == 2
        assert result[0].stock_code == "005930"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_new_high_low_price.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_new_high_price()

        assert result == []


class TestStockScreenerGetPriceVolatility:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_price_volatility.return_value = _make_volatility_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_price_volatility()

        assert len(result) == 2
        assert result[0].extra == "5.0"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_price_volatility.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_price_volatility()

        assert result == []


class TestStockScreenerGetTopMarginRatio:
    def test_returns_screening_items(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_margin_ratio.return_value = _make_margin_response(SAMPLE_ITEMS)

        screener = StockScreener(fetcher)
        result = screener.get_top_margin_ratio()

        assert len(result) == 2
        assert result[0].extra == "1.2"

    def test_returns_empty_on_error(self):
        fetcher = _make_mock_fetcher()
        fetcher.get_top_margin_ratio.side_effect = Exception("API error")

        screener = StockScreener(fetcher)
        result = screener.get_top_margin_ratio()

        assert result == []
