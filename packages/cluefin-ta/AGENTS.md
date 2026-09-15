# AGENTS.md — cluefin-ta

Pure-NumPy reimplementation of TA-Lib. Non-obvious constraints only; see the root
AGENTS.md for repo-wide rules.

## The contract: bit-for-bit TA-Lib parity

- The C-backed `ta-lib` package (dev dependency only) is the test oracle. New indicators
  must match it at `rtol=1e-10` **including the NaN warm-up prefix length** (ta-lib's
  lookback convention), not just post-warm-up values.
- The few looser tolerances (MACD, ADX, KAMA) are deliberate — ta-lib's internal
  "unstable period" handling diverges there. Don't loosen a tolerance to make a new
  implementation pass; reproduce ta-lib's algorithm quirks instead (see the comments in
  `overlap.py` DEMA, `momentum.py` STOCH, `volume.py` ADOSC for the pattern).

## Testing gotchas

- Parity test modules import `talib` at module level with no skip guard: without the
  TA-Lib **C library** installed, `pytest` fails at collection, not with clean skips.
  Only `test_pattern.py` / `test_portfolio.py` / `test_regime.py` run without it (no
  ta-lib counterpart).
- `hmmlearn` looks like the same kind of optional dep but *is* skip-guarded — don't
  copy the ta-lib import style for new optional deps.
