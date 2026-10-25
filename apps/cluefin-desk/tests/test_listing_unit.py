from types import SimpleNamespace

from cluefin_desk.data.listing import ListedStock, StockListing, is_stock_code, load_listing


def _stock(code, name, market="KOSPI", kind="거래소", sector=""):
    return ListedStock(code=code, name=name, market=market, kind=kind, sector=sector)


LISTING = StockListing(
    [
        _stock("100010", "가나전자", sector="전기전자"),
        _stock("100015", "가나전자우"),
        _stock("200020", "가나 바이오", market="KOSDAQ", kind="코스닥"),
        _stock("300030", "다라 가나전자 ETF", kind="ETF"),
        _stock("0001A0", "마바테크", market="KOSDAQ", kind="코스닥"),
        _stock("00088K", "사아홀딩스우"),
        _stock("400040", "ABC Global"),
    ]
)


class TestIsStockCode:
    def test_digits_and_letters(self):
        assert is_stock_code("100010")
        assert is_stock_code("0001A0")

    def test_rejects_other_shapes(self):
        assert not is_stock_code("10001")
        assert not is_stock_code("0001a0")
        assert not is_stock_code("가나전자")


class TestResolve:
    def test_code_exact(self):
        assert LISTING.resolve("100010").name == "가나전자"

    def test_alphanumeric_code_case_insensitive(self):
        assert LISTING.resolve("0001a0").name == "마바테크"
        assert LISTING.resolve(" 00088K ").name == "사아홀딩스우"

    def test_unknown_code_is_none(self):
        assert LISTING.resolve("999999") is None

    def test_exact_name_wins_over_partial(self):
        # "가나전자" is also inside "가나전자우" and the ETF name.
        assert LISTING.resolve("가나전자").code == "100010"

    def test_ignores_spaces_and_case(self):
        assert LISTING.resolve("가나바이오").code == "200020"
        assert LISTING.resolve("abc global").code == "400040"

    def test_unique_partial(self):
        assert LISTING.resolve("마바").code == "0001A0"

    def test_ambiguous_partial_is_none(self):
        assert LISTING.resolve("가나") is None

    def test_blank_is_none(self):
        assert LISTING.resolve("   ") is None


class TestSuggest:
    def test_blank_gives_nothing(self):
        assert LISTING.suggest("") == []

    def test_order_exact_prefix_partial_and_funds_last(self):
        codes = [row.code for row in LISTING.suggest("가나전자")]
        # exact, then prefix, then the ETF whose name merely contains it
        assert codes == ["100010", "100015", "300030"]

    def test_kospi_before_kosdaq_in_same_tier(self):
        codes = [row.code for row in LISTING.suggest("가나")]
        assert codes == ["100010", "100015", "200020", "300030"]

    def test_code_prefix(self):
        assert [row.code for row in LISTING.suggest("1000")] == ["100010", "100015"]
        assert [row.code for row in LISTING.suggest("0001a")] == ["0001A0"]

    def test_limit(self):
        assert len(LISTING.suggest("가나", limit=2)) == 2

    def test_no_match(self):
        assert LISTING.suggest("없는이름") == []


def _item(code, name, market_name="거래소", up_name=""):
    return SimpleNamespace(code=code, name=name, marketName=market_name, upName=up_name)


def _response(items, cont_yn="N", next_key=""):
    return SimpleNamespace(
        body=SimpleNamespace(list=items),
        headers=SimpleNamespace(cont_yn=cont_yn, next_key=next_key),
    )


class FakeStockInfo:
    def __init__(self, pages):
        self.pages = pages  # {(mrkt_tp, next_key): response}
        self.calls = []

    def get_stock_info_summary(self, mrkt_tp, cont_yn="N", next_key=""):
        self.calls.append((mrkt_tp, cont_yn, next_key))
        return self.pages[(mrkt_tp, next_key)]


class TestLoadListing:
    def test_merges_markets_and_follows_continuation(self):
        stock_info = FakeStockInfo(
            {
                ("0", ""): _response([_item("100010", "가나전자", up_name="전기전자")], cont_yn="Y", next_key="k1"),
                ("0", "k1"): _response([_item("300030", "다라 ETF", market_name="ETF")]),
                ("10", ""): _response([_item("0001A0", "마바테크", market_name="코스닥")]),
            }
        )
        listing = load_listing(SimpleNamespace(stock_info=stock_info))

        assert stock_info.calls == [("0", "N", ""), ("0", "Y", "k1"), ("10", "N", "")]
        assert len(listing) == 3
        assert listing.get("100010") == _stock("100010", "가나전자", sector="전기전자")
        assert listing.get("300030").kind == "ETF"
        assert listing.get("0001A0").market == "KOSDAQ"

    def test_skips_rows_without_code_or_name(self):
        stock_info = FakeStockInfo(
            {
                ("0", ""): _response([_item("", "이름만"), _item("100010", " "), _item("100020", "가나전자")]),
                ("10", ""): _response([]),
            }
        )
        listing = load_listing(SimpleNamespace(stock_info=stock_info))
        assert len(listing) == 1

    def test_continuation_without_key_stops(self):
        stock_info = FakeStockInfo(
            {
                ("0", ""): _response([_item("100010", "가나전자")], cont_yn="Y", next_key=""),
                ("10", ""): _response([]),
            }
        )
        load_listing(SimpleNamespace(stock_info=stock_info))
        assert stock_info.calls == [("0", "N", ""), ("10", "N", "")]
