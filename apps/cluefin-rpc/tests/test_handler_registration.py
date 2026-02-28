"""Tests for KIS/Kiwoom handler registration correctness."""

from __future__ import annotations

from cluefin_rpc.dispatcher import Dispatcher
from cluefin_rpc.handlers.kis import register_kis_handlers
from cluefin_rpc.handlers.kis.domestic_basic_quote import (
    _ALL_HANDLERS as KIS_BASIC_QUOTE,
)
from cluefin_rpc.handlers.kis.domestic_issue_other import (
    _ALL_HANDLERS as KIS_ISSUE_OTHER,
)
from cluefin_rpc.handlers.kis.domestic_market_analysis import (
    _ALL_HANDLERS as KIS_MARKET_ANALYSIS,
)
from cluefin_rpc.handlers.kis.domestic_ranking_analysis import (
    _ALL_HANDLERS as KIS_RANKING,
)
from cluefin_rpc.handlers.kis.domestic_stock_info import (
    _ALL_HANDLERS as KIS_STOCK_INFO,
)
from cluefin_rpc.handlers.kiwoom import register_kiwoom_handlers
from cluefin_rpc.handlers.kiwoom.domestic_chart import (
    _ALL_HANDLERS as KW_CHART,
)
from cluefin_rpc.handlers.kiwoom.domestic_etf import (
    _ALL_HANDLERS as KW_ETF,
)
from cluefin_rpc.handlers.kiwoom.domestic_foreign import (
    _ALL_HANDLERS as KW_FOREIGN,
)
from cluefin_rpc.handlers.kiwoom.domestic_market_condition import (
    _ALL_HANDLERS as KW_MARKET_COND,
)
from cluefin_rpc.handlers.kiwoom.domestic_rank_info import (
    _ALL_HANDLERS as KW_RANK_INFO,
)
from cluefin_rpc.handlers.kiwoom.domestic_sector import (
    _ALL_HANDLERS as KW_SECTOR,
)
from cluefin_rpc.handlers.kiwoom.domestic_stock_info import (
    _ALL_HANDLERS as KW_STOCK_INFO,
)
from cluefin_rpc.handlers.kiwoom.domestic_theme import (
    _ALL_HANDLERS as KW_THEME,
)
from cluefin_rpc.server import _build_dispatcher

# ---------------------------------------------------------------------------
# KIS per-module counts
# ---------------------------------------------------------------------------


class TestKisModuleCounts:
    def test_basic_quote_count(self):
        assert len(KIS_BASIC_QUOTE) == 21

    def test_issue_other_count(self):
        assert len(KIS_ISSUE_OTHER) == 14

    def test_market_analysis_count(self):
        assert len(KIS_MARKET_ANALYSIS) == 29

    def test_ranking_analysis_count(self):
        assert len(KIS_RANKING) == 22

    def test_stock_info_count(self):
        assert len(KIS_STOCK_INFO) == 26


class TestKisRegistration:
    def test_total_kis_methods(self):
        d = Dispatcher()
        register_kis_handlers(d)
        methods = d.list_methods(broker="kis")
        assert len(methods) == 112

    def test_all_methods_have_kis_prefix(self):
        d = Dispatcher()
        register_kis_handlers(d)
        for m in d.list_methods(broker="kis"):
            assert m["name"].startswith("kis."), f"{m['name']} missing kis. prefix"

    def test_all_handlers_broker_is_kis(self):
        d = Dispatcher()
        register_kis_handlers(d)
        for m in d.list_methods(broker="kis"):
            assert m["broker"] == "kis"

    def test_all_handlers_require_session(self):
        d = Dispatcher()
        register_kis_handlers(d)
        for m in d.list_methods(broker="kis"):
            assert m["requires_session"] is True

    def test_no_duplicate_method_names(self):
        d = Dispatcher()
        register_kis_handlers(d)
        names = [m["name"] for m in d.list_methods(broker="kis")]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# Kiwoom per-module counts
# ---------------------------------------------------------------------------


class TestKiwoomModuleCounts:
    def test_chart_count(self):
        assert len(KW_CHART) == 14

    def test_etf_count(self):
        assert len(KW_ETF) == 9

    def test_foreign_count(self):
        assert len(KW_FOREIGN) == 3

    def test_market_condition_count(self):
        assert len(KW_MARKET_COND) == 20

    def test_rank_info_count(self):
        assert len(KW_RANK_INFO) == 23

    def test_sector_count(self):
        assert len(KW_SECTOR) == 6

    def test_stock_info_count(self):
        assert len(KW_STOCK_INFO) == 28

    def test_theme_count(self):
        assert len(KW_THEME) == 2


class TestKiwoomRegistration:
    def test_total_kiwoom_methods(self):
        d = Dispatcher()
        register_kiwoom_handlers(d)
        methods = d.list_methods(broker="kiwoom")
        assert len(methods) == 105

    def test_all_methods_have_kiwoom_prefix(self):
        d = Dispatcher()
        register_kiwoom_handlers(d)
        for m in d.list_methods(broker="kiwoom"):
            assert m["name"].startswith("kiwoom."), f"{m['name']} missing kiwoom. prefix"

    def test_all_handlers_broker_is_kiwoom(self):
        d = Dispatcher()
        register_kiwoom_handlers(d)
        for m in d.list_methods(broker="kiwoom"):
            assert m["broker"] == "kiwoom"

    def test_no_duplicate_method_names(self):
        d = Dispatcher()
        register_kiwoom_handlers(d)
        names = [m["name"] for m in d.list_methods(broker="kiwoom")]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# Combined registration
# ---------------------------------------------------------------------------


class TestCombinedRegistration:
    def test_no_name_collision_between_brokers(self):
        d = Dispatcher()
        register_kis_handlers(d)
        register_kiwoom_handlers(d)
        kis_names = {m["name"] for m in d.list_methods(broker="kis")}
        kw_names = {m["name"] for m in d.list_methods(broker="kiwoom")}
        assert kis_names.isdisjoint(kw_names)

    def test_build_dispatcher_total_methods(self):
        d = _build_dispatcher()
        all_methods = d.list_methods()
        assert len(all_methods) >= 217
