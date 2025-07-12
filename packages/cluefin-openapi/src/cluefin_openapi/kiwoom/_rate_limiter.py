"""Rate limiting implementation for Kiwoom API client."""

import threading
import time
from typing import Optional


class TokenBucket:
    """Token bucket rate limiter implementation."""

    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.

        Args:
            capacity: Maximum number of tokens in the bucket
            refill_rate: Rate at which tokens are added (tokens per second)
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens from the bucket.

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if not enough tokens available
        """
        with self._lock:
            self._refill()

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def wait_for_tokens(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """
        Wait until enough tokens are available.

        Args:
            tokens: Number of tokens needed
            timeout: Maximum time to wait in seconds

        Returns:
            True if tokens were acquired, False if timeout occurred
        """
        start_time = time.time()

        while True:
            if self.consume(tokens):
                return True

            if timeout and (time.time() - start_time) >= timeout:
                return False

            # Calculate how long to wait for next token
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    continue

                tokens_needed = tokens - self.tokens
                wait_time = tokens_needed / self.refill_rate

            # Sleep for a short period to avoid busy waiting
            time.sleep(min(wait_time, 0.1))

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    @property
    def available_tokens(self) -> float:
        """Get current number of available tokens."""
        with self._lock:
            self._refill()
            return self.tokens
