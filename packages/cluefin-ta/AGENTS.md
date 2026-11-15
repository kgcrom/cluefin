# AGENTS.md — cluefin-ta

Pure-NumPy indicators with ta-lib's results, plus portfolio metrics and regime detection that ta-lib lacks.
Non-obvious constraints only; repo-wide rules are in the root AGENTS.md and `packages/AGENTS.md`. What a caller
trips on (`risk_free` per period, NaN vs 0.0, `years=`, `matype`) is in README "걸리는 곳" and not repeated here.

## Why the package stays

- Decided 2026-10-11: keep it instead of depending on C ta-lib. Regime and portfolio functions have no ta-lib
  counterpart, so that code stays either way, and moving it into the apps would copy it into both consumers
  (`cluefin-openapi-cli`: `indicators.py`, `cache/perf.py`; `cluefin-desk`: ML features, chart widgets).
  C `ta-lib` is a dev dependency used only as the test oracle.
- The CLI's `trend_setup.py` deliberately does **not** import this package: it ports backtest formulas (plain
  14-day ATR, not Wilder's) whose thresholds are void under ta-lib's definitions. Do not "unify" them.
- Only indicators belong here. BUY/SELL scoring, and why CLI numbers differ from desk's, are in
  `apps/cluefin-openapi-cli/AGENTS.md` (the `kis chart technical` notes).

## The contract: ta-lib parity, checked two ways

- Per-module tests compare at `rtol=1e-10` on one 100-bar fixture. That fixture **hid** NaN-prefix and algorithm
  differences (STOCH's %K started before %D; MACD's seeding), so `test_parity_sweep_unit.py` runs every ta-lib-backed
  indicator on 800-bar series, continuous and tick-rounded: NaN mask **exactly** equal, values within
  `rtol=1e-9, atol=1e-9 * max|expected|`. The absolute term is there because a relative tolerance means nothing where
  ta-lib's value is ~0 (CCI, MFI, MACD histogram). A new indicator goes into that file's `INDICATORS` list.
- Never widen a tolerance per indicator. MACD and ADX tests once ran at `rtol` 0.05/0.06, blamed on ta-lib's
  "unstable period"; the real causes there and in KAMA were algorithm details (MACD was off by up to 35%, and the
  histogram's sign could flip). When a new indicator won't match, read the ta-lib C source and reproduce it.
- These match ta-lib and look like bugs. Leave them:
  - EMA updates as `prev + (x - prev) * k`; ADOSC alone uses `k * x + (1 - k) * prev` seeded with the first value.
    The two forms round differently, so the helpers must not be merged.
  - MACD seeds the fast EMA at the slow EMA's first bar, emits all outputs from the signal's first bar, and swaps
    the periods when `slowperiod < fastperiod`. STOCH/STOCHF emit %K only from %D's first bar.
  - RSI is 0 (not 100) when there is no movement at all; MFI is 0 when the total money flow is below 1; ADX skips
    a DX whose sums are within 1e-8 (`TA_IS_ZERO`); BBANDS uses the population standard deviation.
- An unimplemented ta-lib option must raise, never be accepted and ignored (`_require_sma`).
- `pattern.py` is under the same contract with **exact** equality. Its thresholds are ta-lib "candle settings"
  (average of a range over the previous N bars), and the sum must be a running total (add new, drop trailing) like
  ta-lib's: a fresh `sum()` rounds differently and flips ties, which tick-rounded KRX prices hit often. A new
  pattern needs the tick-rounded parity cases in `test_pattern_unit.py` too.

## Regime and portfolio functions have no oracle

- `regime.py`'s invariant is that bar `t` uses bars `<= t` only (desk feeds these into ML training). Thresholds are
  expanding, and the HMM is refitted on an expanding window and read with forward filtering, never
  `predict()`/Viterbi over the whole series. Only `REGIME_VOLATILITY` and `REGIME_HMM` — the two that used to look
  ahead — have a "prefix result == truncated full result" test. Add one for any new or changed regime function.
- Portfolio metrics are tested against series built from the formulas. `SORTINO` divides the downside deviation by
  all N periods; dividing by the losing periods only was 1.41x off at the median over 3,128 cached stocks.

## Testing traps

- Parity test modules `import talib` at module level on purpose: the `ta-lib>=0.6` wheel bundles the C library, so
  the oracle always comes with the dev group, and a skip guard would let CI pass with the parity checks gone.
  `hmmlearn` *is* skip-guarded (`pytest.importorskip` inside each test) because it is an optional extra.
- Do not add oracle calls on zero-length arrays. C `TA_OBV` reads and writes before its buffer on length 0 and
  corrupts the heap; the symptom was an unrelated cluefin-desk ML test dying later with a `free()` abort (exit 134),
  intermittently. The OBV empty-array test asserts only our output for that reason; the SMA/RSI/ATR and pattern
  ones still call the oracle on length 0 and have not shown it.
- `examples/ta_quickstart.ipynb` loads `.env.test`, whose KIS side is the real server.
