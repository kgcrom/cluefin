"""Vendor chart responses normalized into one OHLCV series.

`cluefin-openapi` has no typed candle abstraction and no pagination helper, so every
chart endpoint hands back its own field names, its own ordering, and its own idea of
what "adjusted price" means. Indicators need one shape: float arrays, oldest first.

Three vendor quirks are handled here rather than at the call site, because each one
fails silently if you skip it:

- **Missing values become NaN, never 0.0.** A zero-priced candle is not a gap to an
  indicator — it is a crash to zero, and it poisons RSI/MACD/Bollinger for the whole
  warm-up window that follows.
- **Kiwoom prices carry a direction sign** on at least some responses (`cur_prc` comes
  back as `"-270406"` on down days in the shipped fixtures). Prices cannot be negative,
  so magnitude is taken unconditionally: correct whether or not a given endpoint signs
  its values, with no live call needed to find out which do.
- **`adj_price` polarity is inverted between endpoints.** `chart.daily` reads
  `0:unadjusted, 1:adjusted`; `chart.period` reads `0:adjusted, 1:original`. Callers ask
  for `adjusted=True/False` and `adj_price_flag` picks the right literal, so the two
  endpoints can never silently return different price bases.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Iterable, Literal, Sequence

import numpy as np

__all__ = [
    "Candle",
    "CandleSeries",
    "adj_price_flag",
    "from_kis_daily",
    "from_kis_minute",
    "from_kis_period",
    "from_kiwoom_daily",
    "from_kiwoom_minute",
    "fetch_kis_daily_series",
]


# ---------------------------------------------------------------------------
# Value parsing
# ---------------------------------------------------------------------------


def _to_float(raw: Any, *, magnitude: bool = False) -> float:
    """Parse one vendor numeric string; unparseable or blank becomes NaN.

    ``magnitude`` takes the absolute value — used for prices and volumes, which cannot
    be negative but arrive signed from some Kiwoom endpoints.
    """

    if raw is None:
        return math.nan
    if isinstance(raw, (int, float)):
        value = float(raw)
    else:
        text = str(raw).strip().replace(",", "")
        if not text:
            return math.nan
        try:
            value = float(text)
        except ValueError:
            return math.nan
    if math.isnan(value) or math.isinf(value):
        return math.nan
    return abs(value) if magnitude else value


def _field(item: Any, name: str) -> Any:
    """Read one field from a pydantic model or a plain dict."""

    if isinstance(item, dict):
        return item.get(name)
    return getattr(item, name, None)


# ---------------------------------------------------------------------------
# Series types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Candle:
    """One normalized bar. ``timestamp`` is ``YYYYMMDD`` or ``YYYYMMDDHHMMSS``."""

    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def complete(self) -> bool:
        return not any(math.isnan(value) for value in (self.open, self.high, self.low, self.close, self.volume))


@dataclass(frozen=True, slots=True)
class CandleSeries:
    """Candles for one instrument, always ascending by timestamp (oldest first)."""

    stock_code: str
    source: str
    candles: tuple[Candle, ...]

    def __len__(self) -> int:
        return len(self.candles)

    @property
    def timestamps(self) -> tuple[str, ...]:
        return tuple(candle.timestamp for candle in self.candles)

    @property
    def missing_count(self) -> int:
        return sum(1 for candle in self.candles if not candle.complete)

    def arrays(self) -> dict[str, np.ndarray]:
        """Return float64 arrays keyed ``open``/``high``/``low``/``close``/``volume``.

        `cluefin-ta` takes `np.ndarray` directly, so this is the handoff point; nothing
        downstream needs pandas.
        """

        return {
            name: np.array([getattr(candle, name) for candle in self.candles], dtype=np.float64)
            for name in ("open", "high", "low", "close", "volume")
        }

    def tail(self, count: int) -> CandleSeries:
        if count <= 0 or count >= len(self.candles):
            return self
        return CandleSeries(stock_code=self.stock_code, source=self.source, candles=self.candles[-count:])


def _build_series(stock_code: str, source: str, candles: Iterable[Candle]) -> CandleSeries:
    """Sort ascending and drop duplicate timestamps, keeping the last seen.

    Vendors disagree on ordering (KIS chart responses are newest-first) and overlapping
    pagination windows repeat dates, so neither is assumed. Within a single endpoint the
    stamps are zero-padded and equal-width, which makes a lexicographic sort the same as
    a chronological one; series from different endpoints are never merged.
    """

    by_timestamp: dict[str, Candle] = {}
    for candle in candles:
        if not candle.timestamp:
            continue
        by_timestamp[candle.timestamp] = candle
    ordered = tuple(by_timestamp[key] for key in sorted(by_timestamp))
    return CandleSeries(stock_code=stock_code, source=source, candles=ordered)


# ---------------------------------------------------------------------------
# adj_price polarity
# ---------------------------------------------------------------------------

_ADJ_POLARITY: dict[str, tuple[str, str]] = {
    # endpoint -> (literal meaning "adjusted", literal meaning "unadjusted")
    "chart.daily": ("1", "0"),  # 0:수정주가미반영, 1:수정주가반영
    "chart.period": ("0", "1"),  # 0:수정주가, 1:원주가
    "kiwoom.daily": ("1", "0"),  # 0:수정주가적용안함, 1:수정주가
}


def adj_price_flag(endpoint: str, *, adjusted: bool = True) -> str:
    """Return the vendor literal that means ``adjusted`` for this endpoint.

    The two KIS chart endpoints use opposite polarity for the same parameter, so
    passing a raw "0"/"1" through mixes adjusted and original price bases without
    any error surfacing.
    """

    try:
        adjusted_flag, original_flag = _ADJ_POLARITY[endpoint]
    except KeyError:
        raise ValueError(f"Unknown chart endpoint `{endpoint}`; known: {sorted(_ADJ_POLARITY)}") from None
    return adjusted_flag if adjusted else original_flag


# ---------------------------------------------------------------------------
# Vendor normalizers
# ---------------------------------------------------------------------------


def _kis_candle(item: Any, *, close_field: str, volume_field: str, timestamp: str) -> Candle:
    return Candle(
        timestamp=timestamp,
        open=_to_float(_field(item, "stck_oprc"), magnitude=True),
        high=_to_float(_field(item, "stck_hgpr"), magnitude=True),
        low=_to_float(_field(item, "stck_lwpr"), magnitude=True),
        close=_to_float(_field(item, close_field), magnitude=True),
        volume=_to_float(_field(item, volume_field), magnitude=True),
    )


def from_kis_daily(items: Sequence[Any], *, stock_code: str) -> CandleSeries:
    """Normalize `chart.daily` (`body.output`) rows."""

    return _build_series(
        stock_code,
        "kis.chart.daily",
        (
            _kis_candle(
                item,
                close_field="stck_clpr",
                volume_field="acml_vol",
                timestamp=str(_field(item, "stck_bsop_date") or "").strip(),
            )
            for item in items
        ),
    )


def from_kis_period(items: Sequence[Any], *, stock_code: str) -> CandleSeries:
    """Normalize `chart.period` (`body.output2`) rows."""

    return _build_series(
        stock_code,
        "kis.chart.period",
        (
            _kis_candle(
                item,
                close_field="stck_clpr",
                volume_field="acml_vol",
                timestamp=str(_field(item, "stck_bsop_date") or "").strip(),
            )
            for item in items
        ),
    )


def from_kis_minute(items: Sequence[Any], *, stock_code: str) -> CandleSeries:
    """Normalize `chart.minute` / `chart.daily-minute` (`body.output2`) rows.

    Minute bars carry neither `stck_clpr` nor a per-bar `acml_vol`: the close is
    `stck_prpr` and the bar volume is `cntg_vol`. `acml_vol` exists only on `output1`
    as the running day total, so using it per bar would feed OBV a monotonic ramp.
    """

    candles = []
    for item in items:
        day = str(_field(item, "stck_bsop_date") or "").strip()
        hour = str(_field(item, "stck_cntg_hour") or "").strip()
        candles.append(
            _kis_candle(item, close_field="stck_prpr", volume_field="cntg_vol", timestamp=f"{day}{hour}" if day else "")
        )
    return _build_series(stock_code, "kis.chart.minute", candles)


def _kiwoom_candle(item: Any, *, timestamp: str) -> Candle:
    return Candle(
        timestamp=timestamp,
        open=_to_float(_field(item, "open_pric"), magnitude=True),
        high=_to_float(_field(item, "high_pric"), magnitude=True),
        low=_to_float(_field(item, "low_pric"), magnitude=True),
        close=_to_float(_field(item, "cur_prc"), magnitude=True),
        volume=_to_float(_field(item, "trde_qty"), magnitude=True),
    )


def from_kiwoom_daily(items: Sequence[Any], *, stock_code: str) -> CandleSeries:
    """Normalize `stk_dt_pole_chart_qry` rows (Kiwoom ka10081 daily chart)."""

    return _build_series(
        stock_code,
        "kiwoom.chart.daily",
        (_kiwoom_candle(item, timestamp=str(_field(item, "dt") or "").strip()) for item in items),
    )


def from_kiwoom_minute(items: Sequence[Any], *, stock_code: str) -> CandleSeries:
    """Normalize `stk_min_pole_chart_qry` rows (Kiwoom minute chart).

    Kiwoom packs date and time into one `cntr_tm` field, unlike KIS which splits them
    across `stck_bsop_date` + `stck_cntg_hour`. Its width varies by endpoint (minute
    bars come back as `YYYYMMDDHHMM`, tick bars as `YYYYMMDDHHMMSS`), which is harmless
    because ordering only ever compares stamps from the same endpoint.
    """

    return _build_series(
        stock_code,
        "kiwoom.chart.minute",
        (_kiwoom_candle(item, timestamp=str(_field(item, "cntr_tm") or "").strip()) for item in items),
    )


# ---------------------------------------------------------------------------
# KIS daily pagination
# ---------------------------------------------------------------------------

# chart.period answers with at most ~100 rows per call and exposes no cursor — only a
# date window — so more history means walking the window backwards. 140 calendar days
# is a little under 100 trading days after weekends and holidays, which keeps each call
# close to full without overshooting the cap.
_WINDOW_DAYS = 140
_MAX_REQUESTS = 12


def _parse_yyyymmdd(value: str) -> date:
    return datetime.strptime(value, "%Y%m%d").date()


def fetch_kis_daily_series(
    kis: Any,
    stock_code: str,
    *,
    count: int,
    market: Literal["J", "NX", "UN"] = "J",
    end_date: str | None = None,
    adjusted: bool = True,
    period: Literal["D", "W", "M", "Y"] = "D",
) -> CandleSeries:
    """Fetch at least ``count`` daily candles by walking `chart.period` backwards.

    KIS chart endpoints have no continuation cursor (unlike Kiwoom's `cont_yn`/`next_key`
    headers), so pagination is date-window arithmetic. Stops as soon as ``count`` candles
    are in hand, a window comes back empty, or ``_MAX_REQUESTS`` windows have been tried —
    the last guard keeps a delisted or thinly traded code from looping to the epoch.
    """

    if count <= 0:
        raise ValueError("count must be positive")

    window_end = _parse_yyyymmdd(end_date) if end_date else date.today()
    adj = adj_price_flag("chart.period", adjusted=adjusted)
    collected: list[Candle] = []
    seen: set[str] = set()

    for _ in range(_MAX_REQUESTS):
        window_start = window_end - timedelta(days=_WINDOW_DAYS)
        response = kis.domestic_basic_quote.get_stock_period_quote(
            market,
            stock_code,
            window_start.strftime("%Y%m%d"),
            window_end.strftime("%Y%m%d"),
            period,
            adj,
        )
        items = getattr(response.body, "output2", None) or []
        page = from_kis_period(items, stock_code=stock_code)
        if not page.candles:
            break

        for candle in page.candles:
            if candle.timestamp not in seen:
                seen.add(candle.timestamp)
                collected.append(candle)

        if len(collected) >= count:
            break

        # Step the window to the day before the oldest row actually returned, rather than
        # a fixed stride, so a window that hit the row cap does not skip the remainder.
        oldest = _parse_yyyymmdd(page.candles[0].timestamp[:8])
        window_end = oldest - timedelta(days=1)

    series = _build_series(stock_code, "kis.chart.period", collected)
    return series.tail(count)
