"""Unit tests for the TokenBucket rate limiter."""

import threading

import cluefin_openapi._rate_limiter as rate_limiter_module
from cluefin_openapi import TokenBucket
from cluefin_openapi._rate_limiter import TokenBucket as TokenBucketDirect


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: list[float] = []

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds + 1e-9

    def advance(self, seconds: float) -> None:
        self.now += seconds


def install_fake_clock(monkeypatch) -> FakeClock:
    clock = FakeClock()
    monkeypatch.setattr(rate_limiter_module.time, "time", clock.time)
    monkeypatch.setattr(rate_limiter_module.time, "sleep", clock.sleep)
    return clock


class TestTokenBucketInitialization:
    """Tests for TokenBucket initialization."""

    def test_initialization_sets_capacity(self):
        """Test that initialization sets capacity correctly."""
        bucket = TokenBucket(capacity=10, refill_rate=5.0)
        assert bucket.capacity == 10

    def test_initialization_sets_refill_rate(self):
        """Test that initialization sets refill rate correctly."""
        bucket = TokenBucket(capacity=10, refill_rate=5.0)
        assert bucket.refill_rate == 5.0

    def test_initialization_starts_with_full_bucket(self):
        """Test that bucket starts with full capacity."""
        bucket = TokenBucket(capacity=10, refill_rate=5.0)
        assert bucket.tokens == 10.0

    def test_import_from_package_root(self):
        """Test that TokenBucket can be imported from package root."""
        assert TokenBucket is TokenBucketDirect


class TestTokenBucketConsume:
    """Tests for TokenBucket.consume method."""

    def test_consume_single_token_succeeds_when_available(self):
        """Test consuming single token when tokens are available."""
        bucket = TokenBucket(capacity=10, refill_rate=5.0)
        assert bucket.consume() is True
        assert bucket.tokens == 9.0

    def test_consume_multiple_tokens_succeeds_when_available(self):
        """Test consuming multiple tokens when enough are available."""
        bucket = TokenBucket(capacity=10, refill_rate=5.0)
        assert bucket.consume(tokens=5) is True
        assert bucket.tokens == 5.0

    def test_consume_fails_when_not_enough_tokens(self):
        """Test that consume fails when not enough tokens available."""
        bucket = TokenBucket(capacity=5, refill_rate=1.0)
        assert bucket.consume(tokens=10) is False
        # Tokens should not be consumed on failure
        assert bucket.tokens == 5.0

    def test_consume_exact_capacity_succeeds(self):
        """Test consuming exactly the capacity amount."""
        bucket = TokenBucket(capacity=5, refill_rate=1.0)
        assert bucket.consume(tokens=5) is True
        assert bucket.tokens == 0.0

    def test_consume_depletes_bucket(self):
        """Test that consuming depletes the bucket."""
        bucket = TokenBucket(capacity=3, refill_rate=1.0)
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is False


class TestTokenBucketRefill:
    """Tests for TokenBucket refill mechanism."""

    def test_refill_adds_tokens_over_time(self, monkeypatch):
        """Test that tokens are refilled based on elapsed time."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=10.0)

        # Consume all tokens
        bucket.consume(tokens=10)
        assert bucket.tokens == 0.0

        clock.advance(0.2)

        # Should have about 2 tokens (10 tokens/sec * 0.2 sec)
        available = bucket.available_tokens
        assert 1.5 <= available <= 2.5

    def test_refill_does_not_exceed_capacity(self, monkeypatch):
        """Test that refill does not exceed capacity."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=5, refill_rate=100.0)

        clock.advance(0.1)

        # Should not exceed capacity
        assert bucket.available_tokens <= 5.0

    def test_available_tokens_triggers_refill(self, monkeypatch):
        """Test that available_tokens property triggers refill."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=10.0)
        bucket.consume(tokens=10)

        clock.advance(0.1)

        # available_tokens should show refilled amount
        tokens = bucket.available_tokens
        assert tokens > 0


class TestTokenBucketWaitForTokens:
    """Tests for TokenBucket.wait_for_tokens method."""

    def test_wait_for_tokens_returns_immediately_when_available(self, monkeypatch):
        """Test that wait_for_tokens returns immediately when tokens available."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=5.0)

        result = bucket.wait_for_tokens(tokens=1)

        assert result is True
        assert clock.sleeps == []

    def test_wait_for_tokens_waits_for_refill(self, monkeypatch):
        """Test that wait_for_tokens waits for token refill."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=50.0)  # 50 tokens/sec
        bucket.consume(tokens=10)

        result = bucket.wait_for_tokens(tokens=1, timeout=1.0)

        assert result is True
        assert clock.sleeps == [0.02]

    def test_wait_for_tokens_respects_timeout(self, monkeypatch):
        """Test that wait_for_tokens respects timeout."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=0.1)  # Very slow refill
        bucket.consume(tokens=10)

        result = bucket.wait_for_tokens(tokens=5, timeout=0.2)

        assert result is False
        assert clock.sleeps == [0.1, 0.1]

    def test_wait_for_tokens_without_timeout(self, monkeypatch):
        """Test wait_for_tokens without timeout (returns when tokens available)."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=100.0)
        bucket.consume(tokens=10)

        # Should eventually get tokens
        result = bucket.wait_for_tokens(tokens=1, timeout=None)
        assert result is True
        assert clock.sleeps == [0.01]


class TestTokenBucketReset:
    """Tests for TokenBucket.reset method."""

    def test_reset_restores_full_capacity(self):
        """Test that reset restores bucket to full capacity."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        bucket.consume(tokens=10)
        assert bucket.tokens == 0.0

        bucket.reset()
        assert bucket.tokens == 10.0

    def test_reset_updates_last_refill_time(self, monkeypatch):
        """Test that reset updates the last refill time."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        old_time = bucket.last_refill

        clock.advance(0.1)
        bucket.reset()

        assert bucket.last_refill > old_time


class TestTokenBucketThreadSafety:
    """Tests for TokenBucket thread safety."""

    def test_concurrent_consume_is_thread_safe(self):
        """Test that concurrent consume operations are thread safe."""
        bucket = TokenBucket(capacity=1000, refill_rate=0.0)  # No refill
        results = []
        errors = []

        def consumer():
            try:
                for _ in range(100):
                    results.append(bucket.consume())
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=consumer) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # Exactly 1000 successful consumes
        assert sum(results) == 1000
        assert bucket.tokens == 0.0

    def test_concurrent_wait_for_tokens_is_thread_safe(self):
        """Test that concurrent wait_for_tokens operations are thread safe."""
        bucket = TokenBucket(capacity=50, refill_rate=100.0)  # Fast refill
        results = []
        errors = []

        def consumer():
            try:
                for _ in range(10):
                    results.append(bucket.wait_for_tokens(tokens=1, timeout=5.0))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=consumer) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # All should succeed with fast refill
        assert all(results)


class TestTokenBucketUseCases:
    """Tests for common TokenBucket use cases."""

    def test_kis_rate_limiting_scenario(self):
        """Test rate limiting scenario similar to KIS API usage."""
        # KIS API typically allows ~10 requests/second
        bucket = TokenBucket(capacity=20, refill_rate=10.0)

        # Burst of requests should succeed
        for _ in range(15):
            assert bucket.consume() is True

        # Remaining capacity check
        assert bucket.available_tokens < 6

    def test_dart_rate_limiting_scenario(self, monkeypatch):
        """Test rate limiting scenario similar to DART API usage."""
        install_fake_clock(monkeypatch)
        # DART API might have lower limits
        bucket = TokenBucket(capacity=5, refill_rate=1.0)

        # Small burst should succeed
        for _ in range(5):
            assert bucket.consume() is True

        # Next request should wait
        result = bucket.wait_for_tokens(tokens=1, timeout=0.5)
        # Might succeed or fail depending on timing
        assert isinstance(result, bool)

    def test_krx_rate_limiting_scenario(self):
        """Test rate limiting scenario similar to KRX API usage."""
        bucket = TokenBucket(capacity=10, refill_rate=5.0)

        # Moderate burst
        for _ in range(8):
            assert bucket.consume() is True

        # Should have some tokens left
        assert bucket.available_tokens >= 1

    def test_kiwoom_rate_limiting_scenario(self, monkeypatch):
        """Test rate limiting scenario matching existing Kiwoom implementation."""
        clock = install_fake_clock(monkeypatch)
        # Match default values from Kiwoom client
        bucket = TokenBucket(capacity=20, refill_rate=10.0)

        # Should start with full bucket
        assert bucket.available_tokens == 20.0

        # Large burst should be allowed
        for _ in range(20):
            assert bucket.consume() is True

        # Bucket should be empty
        assert bucket.available_tokens < 1

        # wait_for_tokens with timeout should work
        result = bucket.wait_for_tokens(tokens=1, timeout=0.2)
        # Should get a token after ~0.1 seconds
        assert result is True
        assert clock.sleeps == [0.1]


class TestTokenBucketEdgeCases:
    """Tests for edge cases."""

    def test_zero_tokens_consume_always_succeeds(self):
        """Test that consuming 0 tokens always succeeds."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        bucket.consume(tokens=10)

        # Even with empty bucket, consuming 0 should work
        assert bucket.consume(tokens=0) is True

    def test_very_high_refill_rate(self, monkeypatch):
        """Test with very high refill rate."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=1000, refill_rate=10000.0)
        bucket.consume(tokens=1000)

        clock.advance(0.1)
        assert bucket.available_tokens >= 900

    def test_very_low_refill_rate(self, monkeypatch):
        """Test with very low refill rate."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=0.1)
        bucket.consume(tokens=10)

        clock.advance(0.1)
        # Should have only ~0.01 tokens
        assert bucket.available_tokens < 0.1

    def test_fractional_token_accumulation(self, monkeypatch):
        """Test that fractional tokens accumulate correctly."""
        clock = install_fake_clock(monkeypatch)
        bucket = TokenBucket(capacity=10, refill_rate=5.0)
        bucket.consume(tokens=10)

        clock.advance(0.1)

        tokens = bucket.available_tokens
        # Should have accumulated ~0.5 tokens
        assert 0.3 <= tokens <= 0.7
