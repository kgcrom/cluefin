# AGENTS.md — cluefin-ta

Pure-NumPy reimplementation of TA-Lib. Non-obvious constraints only; see the root
AGENTS.md for repo-wide rules.

## The contract: bit-for-bit TA-Lib parity

- The C-backed `ta-lib` package (dev dependency only) is the test oracle. New indicators
  must match it at `rtol=1e-10` **including the NaN warm-up prefix length** (ta-lib's
  lookback convention), not just post-warm-up values.
- There are no looser tolerances: MACD, ADX and KAMA used to differ (MACD by up to 35%)
  and were blamed on ta-lib's "unstable period", but the real causes were algorithm
  details — MACD seeds the fast EMA at the slow EMA's first bar, ADX starts its Wilder
  sums from `period - 1` bars and skips near-zero (`TA_IS_ZERO`, 1e-8) DX, KAMA's first
  value is at index `period`. When a new indicator won't match, read the ta-lib C source
  and reproduce it; don't loosen the tolerance (see `_core.py` and DEMA, STOCH, ADOSC).

## Regime functions never look ahead

- `regime.py` has no ta-lib oracle; its invariant instead is that bar `t` is computed
  from bars `<= t` only (desk feeds these straight into ML training). Thresholds are
  expanding (`REGIME_VOLATILITY`), the HMM is refitted on an expanding window and read
  with forward filtering, never `predict()`/Viterbi over the whole series. Each function
  has a "prefix result == truncated full result" test; keep one for any new function.

## Candlestick patterns are under the same contract

- `pattern.py` reproduces ta-lib's C functions, compared with **exact** equality. The
  thresholds are ta-lib "candle settings" (average of a range over the previous N bars),
  and the average's sum must be a running total (add new, drop trailing) like ta-lib's:
  a fresh `sum()` rounds differently and flips ties, which tick-rounded KRX prices hit
  often. A new pattern needs the tick-rounded parity cases in `test_pattern_unit.py` too.

## Testing gotchas

- Parity test modules `import talib` at module level on purpose: the `ta-lib>=0.6`
  wheel bundles the C library, so the oracle is always installed with the dev group, and
  a skip guard would only let CI pass with the parity checks silently gone.
- `hmmlearn` *is* skip-guarded (`pytest.importorskip`) because it is an optional extra
  of the package itself, not a test oracle.
