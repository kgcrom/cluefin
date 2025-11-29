"""Rate limiting implementation for API clients.

This module provides a thread-safe TokenBucket rate limiter that can be used
by kis, krx, dart, and kiwoom clients to control API request rates.
"""

import threading
import time
from typing import Optional


class TokenBucket:
    """Token bucket rate limiter implementation.

    A thread-safe rate limiter using the token bucket algorithm.
    Tokens are added to the bucket at a fixed rate, and requests
    consume tokens. If no tokens are available, requests can either
    fail immediately or wait for tokens to become available.

    Example:
        >>> # Create a rate limiter allowing 10 requests/second with burst of 20
        >>> limiter = TokenBucket(capacity=20, refill_rate=10.0)
        >>> if limiter.consume():
        ...     # Make API request
        ...     pass

        >>> # Or wait for tokens with timeout
        >>> if limiter.wait_for_tokens(timeout=5.0):
        ...     # Make API request
        ...     pass
    """

    def __init__(self, capacity: int, refill_rate: float):
        """Initialize token bucket.

        Args:
            capacity: Maximum number of tokens in the bucket (burst size)
            refill_rate: Rate at which tokens are added (tokens per second)
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from the bucket.

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
        """Wait until enough tokens are available.

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

            if timeout is not None and (time.time() - start_time) >= timeout:
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

    def _refill(self) -> None:
        """Refill tokens based on elapsed time.

        This method should only be called while holding the lock.
        """
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

    def reset(self) -> None:
        """Reset the bucket to full capacity."""
        with self._lock:
            self.tokens = float(self.capacity)
            self.last_refill = time.time()
