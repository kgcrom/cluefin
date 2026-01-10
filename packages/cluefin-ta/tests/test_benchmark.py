"""
Performance benchmark tests: cluefin-ta vs TA-Lib.

These tests measure and compare the performance of cluefin-ta pure Python
implementations against TA-Lib (C-based library).

The goal is to ensure cluefin-ta performance remains within acceptable
bounds relative to TA-Lib, accepting that pure Python will be slower.
"""

import time

import numpy as np
import pytest
import talib

import cluefin_ta

# Maximum acceptable slowdown factor compared to TA-Lib
# Pure Python implementations are expected to be significantly slower than C-based TA-Lib.
# This threshold is set high to allow for expected performance differences while still
# catching major performance regressions.
MAX_SLOWDOWN_FACTOR = 2000.0


def benchmark_function(func, *args, warmup_runs: int = 3, benchmark_runs: int = 10):
    """
    Benchmark a function and return average execution time.

    Args:
        func: Function to benchmark
        *args: Arguments to pass to the function
        warmup_runs: Number of warmup runs
        benchmark_runs: Number of benchmark runs

    Returns:
        Tuple of (mean_time, std_time) in milliseconds
    """
    # Warmup
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


@pytest.mark.slow
class TestEMABenchmark:
    """Benchmark EMA implementations."""

    def test_ema_benchmark(self, large_close, capsys):
        """Compare EMA performance: cluefin-ta vs TA-Lib."""
        period = 20

        talib_time, talib_std = benchmark_function(talib.EMA, large_close, period)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.EMA, large_close, period)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[EMA] n={len(large_close)}, period={period}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta EMA is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestRSIBenchmark:
    """Benchmark RSI implementations."""

    def test_rsi_benchmark(self, large_close, capsys):
        """Compare RSI performance: cluefin-ta vs TA-Lib."""
        period = 14

        talib_time, talib_std = benchmark_function(talib.RSI, large_close, period)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.RSI, large_close, period)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[RSI] n={len(large_close)}, period={period}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta RSI is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestATRBenchmark:
    """Benchmark ATR implementations."""

    def test_atr_benchmark(self, large_ohlcv, capsys):
        """Compare ATR performance: cluefin-ta vs TA-Lib."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        close = large_ohlcv["close"]
        period = 14

        talib_time, talib_std = benchmark_function(talib.ATR, high, low, close, period)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.ATR, high, low, close, period)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[ATR] n={len(close)}, period={period}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta ATR is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestBBANDSBenchmark:
    """Benchmark Bollinger Bands implementations."""

    def test_bbands_benchmark(self, large_close, capsys):
        """Compare BBANDS performance: cluefin-ta vs TA-Lib."""
        period = 20

        talib_time, talib_std = benchmark_function(talib.BBANDS, large_close, period)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.BBANDS, large_close, period)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[BBANDS] n={len(large_close)}, period={period}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta BBANDS is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestSTOCHBenchmark:
    """Benchmark Stochastic implementations."""

    def test_stoch_benchmark(self, large_ohlcv, capsys):
        """Compare STOCH performance: cluefin-ta vs TA-Lib."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        close = large_ohlcv["close"]

        talib_time, talib_std = benchmark_function(talib.STOCH, high, low, close)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.STOCH, high, low, close)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[STOCH] n={len(close)}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta STOCH is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestADXBenchmark:
    """Benchmark ADX implementations."""

    def test_adx_benchmark(self, large_ohlcv, capsys):
        """Compare ADX performance: cluefin-ta vs TA-Lib."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        close = large_ohlcv["close"]
        period = 14

        talib_time, talib_std = benchmark_function(talib.ADX, high, low, close, period)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.ADX, high, low, close, period)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[ADX] n={len(close)}, period={period}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta ADX is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestOBVBenchmark:
    """Benchmark OBV implementations."""

    def test_obv_benchmark(self, large_ohlcv, capsys):
        """Compare OBV performance: cluefin-ta vs TA-Lib."""
        close = large_ohlcv["close"]
        volume = large_ohlcv["volume"]

        talib_time, talib_std = benchmark_function(talib.OBV, close, volume)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.OBV, close, volume)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[OBV] n={len(close)}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta OBV is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestADBenchmark:
    """Benchmark A/D implementations."""

    def test_ad_benchmark(self, large_ohlcv, capsys):
        """Compare AD performance: cluefin-ta vs TA-Lib."""
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        close = large_ohlcv["close"]
        volume = large_ohlcv["volume"]

        talib_time, talib_std = benchmark_function(talib.AD, high, low, close, volume)
        cluefin_time, cluefin_std = benchmark_function(cluefin_ta.AD, high, low, close, volume)

        slowdown = cluefin_time / talib_time

        with capsys.disabled():
            print(f"\n[AD] n={len(close)}")
            print(f"  TA-Lib:     {talib_time:.3f} ms (+/- {talib_std:.3f})")
            print(f"  cluefin-ta: {cluefin_time:.3f} ms (+/- {cluefin_std:.3f})")
            print(f"  Slowdown:   {slowdown:.2f}x")

        assert slowdown < MAX_SLOWDOWN_FACTOR, (
            f"cluefin-ta AD is {slowdown:.1f}x slower than TA-Lib (max allowed: {MAX_SLOWDOWN_FACTOR}x)"
        )


@pytest.mark.slow
class TestBenchmarkSummary:
    """Summary benchmark test."""

    def test_all_functions_summary(self, large_ohlcv, capsys):
        """Print summary of all benchmark results."""
        close = large_ohlcv["close"]
        high = large_ohlcv["high"]
        low = large_ohlcv["low"]
        volume = large_ohlcv["volume"]

        results = []

        # EMA
        talib_t, _ = benchmark_function(talib.EMA, close, 20)
        cluefin_t, _ = benchmark_function(cluefin_ta.EMA, close, 20)
        results.append(("EMA", talib_t, cluefin_t))

        # RSI
        talib_t, _ = benchmark_function(talib.RSI, close, 14)
        cluefin_t, _ = benchmark_function(cluefin_ta.RSI, close, 14)
        results.append(("RSI", talib_t, cluefin_t))

        # ATR
        talib_t, _ = benchmark_function(talib.ATR, high, low, close, 14)
        cluefin_t, _ = benchmark_function(cluefin_ta.ATR, high, low, close, 14)
        results.append(("ATR", talib_t, cluefin_t))

        # BBANDS
        talib_t, _ = benchmark_function(talib.BBANDS, close, 20)
        cluefin_t, _ = benchmark_function(cluefin_ta.BBANDS, close, 20)
        results.append(("BBANDS", talib_t, cluefin_t))

        # STOCH
        talib_t, _ = benchmark_function(talib.STOCH, high, low, close)
        cluefin_t, _ = benchmark_function(cluefin_ta.STOCH, high, low, close)
        results.append(("STOCH", talib_t, cluefin_t))

        # ADX
        talib_t, _ = benchmark_function(talib.ADX, high, low, close, 14)
        cluefin_t, _ = benchmark_function(cluefin_ta.ADX, high, low, close, 14)
        results.append(("ADX", talib_t, cluefin_t))

        # OBV
        talib_t, _ = benchmark_function(talib.OBV, close, volume)
        cluefin_t, _ = benchmark_function(cluefin_ta.OBV, close, volume)
        results.append(("OBV", talib_t, cluefin_t))

        # AD
        talib_t, _ = benchmark_function(talib.AD, high, low, close, volume)
        cluefin_t, _ = benchmark_function(cluefin_ta.AD, high, low, close, volume)
        results.append(("AD", talib_t, cluefin_t))

        with capsys.disabled():
            print(f"\n{'=' * 70}")
            print(f"Benchmark Summary: cluefin-ta vs TA-Lib (n={len(close)})")
            print(f"{'=' * 70}")
            print(f"{'Function':<15} {'TA-Lib (ms)':<15} {'cluefin-ta (ms)':<18} {'Slowdown':<12}")
            print(f"{'-' * 70}")

            for name, talib_time, cluefin_time in results:
                slowdown = cluefin_time / talib_time
                status = "✓" if slowdown < MAX_SLOWDOWN_FACTOR else "✗"
                print(f"{name:<15} {talib_time:<15.3f} {cluefin_time:<18.3f} {slowdown:<10.2f}x {status}")

            avg_slowdown = np.mean([r[2] / r[1] for r in results])
            print(f"{'-' * 70}")
            print(f"{'Average':<15} {'':<15} {'':<18} {avg_slowdown:<10.2f}x")
            print(f"{'=' * 70}")
            print(f"Max allowed slowdown: {MAX_SLOWDOWN_FACTOR}x")

        # Ensure average is within bounds
        assert avg_slowdown < MAX_SLOWDOWN_FACTOR, (
            f"Average slowdown ({avg_slowdown:.1f}x) exceeds max allowed ({MAX_SLOWDOWN_FACTOR}x)"
        )
