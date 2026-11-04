"""`data/trend_groups.py` — 캐시가 없거나 실패해도 조용히 빈 dict 로 돌아가는지, 그룹 라벨이
맞는지. KIS 도 실제 DuckDB 파일도 건드리지 않는다: `store`/`scan`/`latest_index_date` 를 모두
가짜로 바꾼다.
"""

from datetime import date

import cluefin_desk.data.trend_groups as trend_groups_module
from cluefin_desk.data.trend_groups import NO_GROUP, _label, lookup_trend_groups


class FakeConn:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class TestLabel:
    def test_single_group(self):
        assert _label({"g1": True, "g2": False, "g3": False}) == "1"

    def test_overlapping_groups_in_order(self):
        assert _label({"g1": False, "g2": True, "g3": True}) == "2,3"

    def test_no_group(self):
        assert _label({"g1": False, "g2": False, "g3": False}) == NO_GROUP


class TestLookupTrendGroups:
    def test_empty_codes_short_circuits(self, monkeypatch):
        monkeypatch.setattr(
            trend_groups_module.store,
            "open_store",
            lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not open")),
        )
        assert lookup_trend_groups([]) == {}

    def test_cache_missing_returns_empty(self, monkeypatch):
        def _raise(*args, **kwargs):
            raise RuntimeError("No cache at ...")

        monkeypatch.setattr(trend_groups_module.store, "open_store", _raise)
        assert lookup_trend_groups(["100010"]) == {}

    def test_no_index_date_returns_empty(self, monkeypatch):
        conn = FakeConn()
        monkeypatch.setattr(trend_groups_module.store, "open_store", lambda *a, **k: conn)
        monkeypatch.setattr(trend_groups_module, "latest_index_date", lambda c: None)
        assert lookup_trend_groups(["100010"]) == {}
        assert conn.closed  # 실패해도 연결은 닫는다

    def test_scan_failure_returns_empty(self, monkeypatch):
        conn = FakeConn()
        monkeypatch.setattr(trend_groups_module.store, "open_store", lambda *a, **k: conn)
        monkeypatch.setattr(trend_groups_module, "latest_index_date", lambda c: date(2026, 11, 4))

        def _raise_scan(*args, **kwargs):
            raise RuntimeError("boom")

        monkeypatch.setattr(trend_groups_module, "scan", _raise_scan)
        assert lookup_trend_groups(["100010"]) == {}
        assert conn.closed

    def test_maps_codes_to_group_labels(self, monkeypatch):
        conn = FakeConn()
        monkeypatch.setattr(trend_groups_module.store, "open_store", lambda *a, **k: conn)
        monkeypatch.setattr(trend_groups_module, "latest_index_date", lambda c: date(2026, 11, 4))

        def _scan(conn_, as_of, *, codes, include_excluded):
            assert codes == ["100010", "200020"]
            assert include_excluded is True
            return {
                "rows": [
                    {"code": "100010", "groups": {"g1": False, "g2": False, "g3": True}},
                    {"code": "200020", "groups": {"g1": False, "g2": False, "g3": False}},
                ]
            }

        monkeypatch.setattr(trend_groups_module, "scan", _scan)
        result = lookup_trend_groups(["100010", "200020"])
        assert result == {"100010": "3", "200020": NO_GROUP}
        assert conn.closed
