"""``_cache.SimpleCache``/``create_cache_key`` unit 테스트."""

import time

from cluefin_openapi.kiwoom._cache import SimpleCache, create_cache_key


class TestSimpleCacheGetSet:
    def test_set_then_get_returns_value(self):
        cache = SimpleCache()
        cache.set("k", {"a": 1})
        assert cache.get("k") == {"a": 1}

    def test_get_missing_key_returns_none(self):
        cache = SimpleCache()
        assert cache.get("missing") is None

    def test_set_overwrites_existing_value(self):
        cache = SimpleCache()
        cache.set("k", "first")
        cache.set("k", "second")
        assert cache.get("k") == "second"


class TestSimpleCacheDeleteClear:
    def test_delete_existing_key_returns_true_and_removes(self):
        cache = SimpleCache()
        cache.set("k", "v")
        assert cache.delete("k") is True
        assert cache.get("k") is None

    def test_delete_missing_key_returns_false(self):
        cache = SimpleCache()
        assert cache.delete("missing") is False

    def test_clear_removes_all_entries(self):
        cache = SimpleCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.get("a") is None
        assert cache.get("b") is None
        assert cache.cache_info()["total_entries"] == 0


class TestSimpleCacheTtlExpiry:
    def test_get_returns_none_after_ttl_expires(self, monkeypatch):
        cache = SimpleCache()
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("k", "v", ttl=10)
        current[0] += 11
        assert cache.get("k") is None

    def test_get_returns_value_before_ttl_expires(self, monkeypatch):
        cache = SimpleCache()
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("k", "v", ttl=10)
        current[0] += 5
        assert cache.get("k") == "v"

    def test_get_removes_expired_entry_from_internal_store(self, monkeypatch):
        cache = SimpleCache()
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("k", "v", ttl=10)
        current[0] += 11
        cache.get("k")
        assert "k" not in cache._cache

    def test_set_uses_default_ttl_when_ttl_is_none(self, monkeypatch):
        cache = SimpleCache(default_ttl=100)
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("k", "v")
        current[0] += 99
        assert cache.get("k") == "v"
        current[0] += 2
        assert cache.get("k") is None


class TestCleanupExpired:
    def test_cleanup_expired_removes_only_expired_entries(self, monkeypatch):
        cache = SimpleCache()
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("fresh", "v", ttl=100)
        cache.set("expired_1", "v", ttl=10)
        cache.set("expired_2", "v", ttl=10)
        current[0] += 11

        removed = cache.cleanup_expired()

        assert removed == 2
        assert cache.get("fresh") == "v"
        assert "expired_1" not in cache._cache
        assert "expired_2" not in cache._cache

    def test_cleanup_expired_returns_zero_when_nothing_expired(self, monkeypatch):
        cache = SimpleCache()
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("fresh", "v", ttl=100)
        assert cache.cleanup_expired() == 0
        assert cache.get("fresh") == "v"


class TestCacheInfo:
    def test_cache_info_on_empty_cache(self):
        cache = SimpleCache()
        assert cache.cache_info() == {"total_entries": 0, "valid_entries": 0, "expired_entries": 0}

    def test_cache_info_counts_valid_and_expired_separately(self, monkeypatch):
        cache = SimpleCache()
        current = [1000.0]
        monkeypatch.setattr(time, "time", lambda: current[0])

        cache.set("fresh", "v", ttl=100)
        cache.set("expired", "v", ttl=10)
        current[0] += 11

        # cache_info does not evict; it should just count.
        info = cache.cache_info()
        assert info == {"total_entries": 2, "valid_entries": 1, "expired_entries": 1}
        assert cache.cache_info()["total_entries"] == 2


class TestCreateCacheKey:
    def test_same_inputs_produce_same_key(self):
        key1 = create_cache_key("https://x/y", {"Accept": "application/json"}, {"a": 1})
        key2 = create_cache_key("https://x/y", {"Accept": "application/json"}, {"a": 1})
        assert key1 == key2

    def test_different_url_produces_different_key(self):
        key1 = create_cache_key("https://x/y", {}, {"a": 1})
        key2 = create_cache_key("https://x/z", {}, {"a": 1})
        assert key1 != key2

    def test_different_body_produces_different_key(self):
        key1 = create_cache_key("https://x/y", {}, {"a": 1})
        key2 = create_cache_key("https://x/y", {}, {"a": 2})
        assert key1 != key2

    def test_dynamic_headers_do_not_affect_key(self):
        key1 = create_cache_key("https://x/y", {"Authorization": "Bearer 1"}, {"a": 1})
        key2 = create_cache_key("https://x/y", {"Authorization": "Bearer 2"}, {"a": 1})
        assert key1 == key2

    def test_key_is_short_hex_string(self):
        key = create_cache_key("https://x/y", {}, {"a": 1})
        assert len(key) == 16
        int(key, 16)  # raises ValueError if not hex
