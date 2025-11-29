"""
Performance benchmark tests for NumPy vs Numba implementations.

These tests measure and compare the performance of NumPy and Numba
implementations for various technical analysis functions.
"""

import time

import numpy as np
import pytest

from cluefin_ta._core import HAS_NUMBA, numpy_impl

if HAS_NUMBA:
    from cluefin_ta._core import numba_impl


def benchmark_function(func, *args, warmup_runs: int = 3, benchmark_runs: int = 10):
    """
    Benchmark a function and return average execution time.

    Args:
        func: Function to benchmark
        *args: Arguments to pass to the function
        warmup_runs: Number of warmup runs (for JIT compilation)
        benchmark_runs: Number of benchmark runs

    Returns:
        Tuple of (mean_time, std_time) in milliseconds
    """
    # Warmup (important for Numba JIT compilation)
    for _ in range(warmup_runs):
        func(*args)

    # Benchmark
    times = []
    for _ in range(benchmark_runs):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms

    return np.mean(times), np.std(times)


@pytest.fixture
def large_close():
    """Large closing price array for benchmarking."""
    np.random.seed(42)
    n = 10000
    base_price = 100.0
    returns = np.random.randn(n) * 0.02
    prices = base_price * np.cumprod(1 + returns)
    return prices.astype(np.float64)


@pytest.fixture
def large_ohlcv():
    """Large OHLCV data for benchmarking."""
    np.random.seed(42)
    n = 10000
    base_price = 100.0

    returns = np.random.randn(n) * 0.02
    close = base_price * np.cumprod(1 + returns)

    high = close * (1 + np.abs(np.random.randn(n) * 0.01))
    low = close * (1 - np.abs(np.random.randn(n) * 0.01))
    open_prices = low + (high - low) * np.random.rand(n)

    high = np.maximum(high, np.maximum(close, open_prices))
    low = np.minimum(low, np.minimum(close, open_prices))

    volume = np.random.randint(1000000, 10000000, n).astype(np.float64)

    return {
        "open": open_prices.astype(np.float64),
        "high": high.astype(np.float64),
        "low": low.astype(np.float64),
        "close": close.astype(np.float64),
        "volume": volume,
    }


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestEmaLoopBenchmark:
    """Benchmark EMA loop implementations."""

    def test_ema_loop_benchmark(self, large_close, capsys):
        """Compare EMA loop performance."""
        period = 20
        alpha = 2.0 / (period + 1)
        initial_sma = np.mean(large_close[:period])

        numpy_time, numpy_std = benchmark_function(
            numpy_impl.ema_loop, large_close, period, alpha, initial_sma
        )
        numba_time, numba_std = benchmark_function(
            numba_impl.ema_loop, large_close, period, alpha, initial_sma
        )

        speedup = numpy_time / numba_time

        with capsys.disabled():
            print(f"\n[EMA Loop] n={len(large_close)}, period={period}")
            print(f"  NumPy: {numpy_time:.3f} ms (+/- {numpy_std:.3f})")
            print(f"  Numba: {numba_time:.3f} ms (+/- {numba_std:.3f})")
            print(f"  Speedup: {speedup:.2f}x")

        # Numba should be faster (at least 1.5x for this operation)
        assert speedup > 1.0, f"Expected Numba to be faster, got {speedup:.2f}x"


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestRollingStdBenchmark:
    """Benchmark rolling std implementations."""

    def test_rolling_std_benchmark(self, large_close, capsys):
        """Compare rolling std performance."""
        period = 20

        numpy_time, numpy_std = benchmark_function(
            numpy_impl.rolling_std, large_close, period
        )
        numba_time, numba_std = benchmark_function(
            numba_impl.rolling_std, large_close, period
        )

        speedup = numpy_time / numba_time

        with capsys.disabled():
            print(f"\n[Rolling Std] n={len(large_close)}, period={period}")
            print(f"  NumPy: {numpy_time:.3f} ms (+/- {numpy_std:.3f})")
            print(f"  Numba: {numba_time:.3f} ms (+/- {numba_std:.3f})")
            print(f"  Speedup: {speedup:.2f}x")

        assert speedup > 1.0, f"Expected Numba to be faster, got {speedup:.2f}x"


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestRollingMinMaxBenchmark:
    """Benchmark rolling min/max implementations."""

    def test_rolling_minmax_benchmark(self, large_ohlcv, capsys):
        """Compare rolling min/max performance."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        period = 14

        numpy_time, numpy_std = benchmark_function(
            numpy_impl.rolling_minmax, high, low, period
        )
        numba_time, numba_std = benchmark_function(
            numba_impl.rolling_minmax, high, low, period
        )

        speedup = numpy_time / numba_time

        with capsys.disabled():
            print(f"\n[Rolling MinMax] n={len(high)}, period={period}")
            print(f"  NumPy: {numpy_time:.3f} ms (+/- {numpy_std:.3f})")
            print(f"  Numba: {numba_time:.3f} ms (+/- {numba_std:.3f})")
            print(f"  Speedup: {speedup:.2f}x")

        assert speedup > 1.0, f"Expected Numba to be faster, got {speedup:.2f}x"


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestTrueRangeBenchmark:
    """Benchmark True Range implementations."""

    def test_true_range_benchmark(self, large_ohlcv, capsys):
        """Compare True Range performance."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        close = large_ohlcv["close"]

        numpy_time, numpy_std = benchmark_function(
            numpy_impl.true_range_loop, high, low, close
        )
        numba_time, numba_std = benchmark_function(
            numba_impl.true_range_loop, high, low, close
        )

        speedup = numpy_time / numba_time

        with capsys.disabled():
            print(f"\n[True Range] n={len(close)}")
            print(f"  NumPy: {numpy_time:.3f} ms (+/- {numpy_std:.3f})")
            print(f"  Numba: {numba_time:.3f} ms (+/- {numba_std:.3f})")
            print(f"  Speedup: {speedup:.2f}x")

        assert speedup > 1.0, f"Expected Numba to be faster, got {speedup:.2f}x"


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestOBVBenchmark:
    """Benchmark OBV implementations."""

    def test_obv_benchmark(self, large_ohlcv, capsys):
        """Compare OBV performance."""
        close = large_ohlcv["close"]
        volume = large_ohlcv["volume"]

        numpy_time, numpy_std = benchmark_function(numpy_impl.obv_loop, close, volume)
        numba_time, numba_std = benchmark_function(numba_impl.obv_loop, close, volume)

        speedup = numpy_time / numba_time

        with capsys.disabled():
            print(f"\n[OBV] n={len(close)}")
            print(f"  NumPy: {numpy_time:.3f} ms (+/- {numpy_std:.3f})")
            print(f"  Numba: {numba_time:.3f} ms (+/- {numba_std:.3f})")
            print(f"  Speedup: {speedup:.2f}x")

        assert speedup > 1.0, f"Expected Numba to be faster, got {speedup:.2f}x"


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestADBenchmark:
    """Benchmark A/D implementations."""

    def test_ad_benchmark(self, large_ohlcv, capsys):
        """Compare A/D performance."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        close = large_ohlcv["close"]
        volume = large_ohlcv["volume"]

        numpy_time, numpy_std = benchmark_function(
            numpy_impl.ad_loop, high, low, close, volume
        )
        numba_time, numba_std = benchmark_function(
            numba_impl.ad_loop, high, low, close, volume
        )

        speedup = numpy_time / numba_time

        with capsys.disabled():
            print(f"\n[A/D] n={len(close)}")
            print(f"  NumPy: {numpy_time:.3f} ms (+/- {numpy_std:.3f})")
            print(f"  Numba: {numba_time:.3f} ms (+/- {numba_std:.3f})")
            print(f"  Speedup: {speedup:.2f}x")

        assert speedup > 1.0, f"Expected Numba to be faster, got {speedup:.2f}x"


class TestBenchmarkSummary:
    """Summary benchmark test."""

    @pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
    def test_all_functions_summary(self, large_ohlcv, capsys):
        """Print summary of all benchmark results."""
        close = large_ohlcv["close"]
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        volume = large_ohlcv["volume"]

        results = []

        # EMA
        period = 20
        alpha = 2.0 / (period + 1)
        initial_sma = np.mean(close[:period])
        numpy_t, _ = benchmark_function(
            numpy_impl.ema_loop, close, period, alpha, initial_sma
        )
        numba_t, _ = benchmark_function(
            numba_impl.ema_loop, close, period, alpha, initial_sma
        )
        results.append(("EMA Loop", numpy_t, numba_t))

        # Rolling Std
        numpy_t, _ = benchmark_function(numpy_impl.rolling_std, close, 20)
        numba_t, _ = benchmark_function(numba_impl.rolling_std, close, 20)
        results.append(("Rolling Std", numpy_t, numba_t))

        # Rolling MinMax
        numpy_t, _ = benchmark_function(numpy_impl.rolling_minmax, high, low, 14)
        numba_t, _ = benchmark_function(numba_impl.rolling_minmax, high, low, 14)
        results.append(("Rolling MinMax", numpy_t, numba_t))

        # True Range
        numpy_t, _ = benchmark_function(numpy_impl.true_range_loop, high, low, close)
        numba_t, _ = benchmark_function(numba_impl.true_range_loop, high, low, close)
        results.append(("True Range", numpy_t, numba_t))

        # OBV
        numpy_t, _ = benchmark_function(numpy_impl.obv_loop, close, volume)
        numba_t, _ = benchmark_function(numba_impl.obv_loop, close, volume)
        results.append(("OBV", numpy_t, numba_t))

        # A/D
        numpy_t, _ = benchmark_function(numpy_impl.ad_loop, high, low, close, volume)
        numba_t, _ = benchmark_function(numba_impl.ad_loop, high, low, close, volume)
        results.append(("A/D", numpy_t, numba_t))

        with capsys.disabled():
            print(f"\n{'='*60}")
            print(f"Benchmark Summary (n={len(close)})")
            print(f"{'='*60}")
            print(f"{'Function':<20} {'NumPy (ms)':<15} {'Numba (ms)':<15} {'Speedup':<10}")
            print(f"{'-'*60}")

            for name, numpy_time, numba_time in results:
                speedup = numpy_time / numba_time
                print(f"{name:<20} {numpy_time:<15.3f} {numba_time:<15.3f} {speedup:<10.2f}x")

            avg_speedup = np.mean([r[1] / r[2] for r in results])
            print(f"{'-'*60}")
            print(f"{'Average':<20} {'':<15} {'':<15} {avg_speedup:<10.2f}x")
            print(f"{'='*60}")
