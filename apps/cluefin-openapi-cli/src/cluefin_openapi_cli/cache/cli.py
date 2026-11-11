"""`cache <sub>` meta command. `load` writes from brokers; every other subcommand only reads the file."""

from __future__ import annotations

import sys
import tomllib
from collections.abc import Callable
from datetime import date, datetime, time, timedelta
from typing import Any

from cluefin_openapi_cli.cache import baserate, breadth, magic, store
from cluefin_openapi_cli.cache import peers as cache_peers
from cluefin_openapi_cli.cache import screen as cache_screen
from cluefin_openapi_cli.cache.load import PARTS, Sources, run_load
from cluefin_openapi_cli.cache.macro_beta import DEFAULT_SINCE_DAYS, read_macro_beta
from cluefin_openapi_cli.cache.perf import read_perf
from cluefin_openapi_cli.cache.rates import RATE_SERIES
from cluefin_openapi_cli.cache.read import read_company, read_financials, read_ohlcv
from cluefin_openapi_cli.cache.trend import latest_index_date, scan
from cluefin_openapi_cli.cliargs import _parse_fields, _parse_limit, _parse_named_options, _str_option
from cluefin_openapi_cli.clock import now_kst, today_kst
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError, classify_exception
from cluefin_openapi_cli.output import attach_truncation, limit_rows, render_output, select_fields
from cluefin_openapi_cli.review.paths import research_root

__all__ = ["SUBCOMMANDS", "run_cache"]


def _run_status(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache status` does not accept positional arguments.", exit_code=EXIT_USAGE)
    path = store.cache_path()
    conn = store.open_store(path, read_only=True)
    try:
        payload = {"path": str(path), "size_bytes": path.stat().st_size, **store.status(conn)}
    finally:
        conn.close()
    render_output(payload, force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False)))


_DEFAULT_SINCE = "20160101"
# KRX closes at 15:30 (closing auction until then); a bar fetched earlier would be a partial day.
_SESSION_FINAL = time(16, 0)


def _last_closed_day(now: datetime) -> date:
    return now.date() if now.time() >= _SESSION_FINAL else now.date() - timedelta(days=1)


def _client_factory() -> Any:
    # Imported here so offline subcommands never load client code; tests replace this function.
    from cluefin_openapi.client_factory import BrokerClientFactory

    return BrokerClientFactory()


def _parse_day(raw: str, option: str) -> date:
    try:
        return datetime.strptime(raw, "%Y%m%d").date()
    except ValueError:
        raise CliError(f"`--{option}` must be YYYYMMDD, got `{raw}`.", exit_code=EXIT_USAGE) from None


def _parse_parts(raw: str | None) -> tuple[str, ...]:
    if raw is None or raw == "all":
        return PARTS
    parts = tuple(part.strip() for part in raw.split(",") if part.strip())
    unknown = [part for part in parts if part not in PARTS]
    if unknown or not parts:
        raise CliError(
            f"`--only` takes {', '.join(PARTS)} or all; got `{raw}`.",
            exit_code=EXIT_USAGE,
            data={"parts": list(PARTS)},
        )
    return tuple(part for part in PARTS if part in parts)


def _progress(message: str) -> None:
    sys.stderr.write(f"[cache load] {now_kst():%H:%M:%S} {message}\n")
    sys.stderr.flush()


def _run_load(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache load` does not accept positional arguments.", exit_code=EXIT_USAGE)
    parts = _parse_parts(_str_option(options, "only"))
    since = _parse_day(_str_option(options, "since") or _DEFAULT_SINCE, "since")
    now = now_kst()
    path = store.cache_path()
    conn = store.open_store(path)
    try:
        result = run_load(
            conn,
            Sources(factory=_client_factory()),
            parts=parts,
            since=since,
            today=now.date(),
            last_day=_last_closed_day(now),
            progress=_progress,
        )
    except CliError:
        raise
    except Exception as exc:
        raise classify_exception(exc, command="cache.load", broker="cache") from exc
    finally:
        conn.close()
    render_output(
        {"path": str(path), "since": since.isoformat(), "parts": result},
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


_DEFAULT_OHLCV_DAYS = 365
_DEFAULT_COMPANY_LIMIT = 100


def _parse_bool(options: dict[str, str | bool], key: str) -> bool:
    raw = _str_option(options, key)
    if raw is None:
        return False
    if raw.lower() in {"true", "1", "yes"}:
        return True
    if raw.lower() in {"false", "0", "no"}:
        return False
    raise CliError(f"`--{key.replace('_', '-')}` takes true or false, got `{raw}`.", exit_code=EXIT_USAGE)


def _render_read(payload: dict[str, Any], options: dict[str, str | bool], *, default_limit: int | None) -> None:
    fields = _parse_fields(options.get("fields"))
    limit = _parse_limit(options.get("limit"))
    if limit is None:
        limit = default_limit
    data: Any = payload
    if fields:
        data = select_fields(data, fields)
    if limit is not None:
        data, notes = limit_rows(data, limit)
        data = attach_truncation(data, limit, notes)
    render_output(data, force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False)))


def _read_conn():
    return store.open_store(store.cache_path(), read_only=True)


def _run_ohlcv(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError(
            "Usage: cache ohlcv --code <code> [--since YYYYMMDD] [--until YYYYMMDD] [--adjusted true].",
            exit_code=EXIT_USAGE,
        )
    until_raw = _str_option(options, "until")
    until = _parse_day(until_raw, "until") if until_raw else today_kst()
    since_raw = _str_option(options, "since")
    since = _parse_day(since_raw, "since") if since_raw else until - timedelta(days=_DEFAULT_OHLCV_DAYS)
    if since > until:
        raise CliError("`--since` is after `--until`.", exit_code=EXIT_USAGE)
    adjusted = _parse_bool(options, "adjusted")
    conn = _read_conn()
    try:
        payload = read_ohlcv(conn, code.strip().upper(), since=since, until=until, adjusted=adjusted)
    finally:
        conn.close()
    if not payload["bars"]:
        payload["hint"] = (
            "No bars in range. Check the code with `cache company --code` and the span with `cache status`."
        )
    _render_read(payload, options, default_limit=None)


def _run_company(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache company` does not accept positional arguments.", exit_code=EXIT_USAGE)
    code = _str_option(options, "code")
    market = _str_option(options, "market")
    if market is not None and market.upper() not in {"KOSPI", "KOSDAQ"}:
        raise CliError("`--market` takes KOSPI or KOSDAQ.", exit_code=EXIT_USAGE)
    as_of_raw = _str_option(options, "as_of")
    conn = _read_conn()
    try:
        payload = read_company(
            conn,
            code=code.strip().upper() if code else None,
            as_of=_parse_day(as_of_raw, "as-of") if as_of_raw else None,
            include_delisted=_parse_bool(options, "include_delisted"),
            market=market.upper() if market else None,
        )
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None if code else _DEFAULT_COMPANY_LIMIT)


_DEFAULT_BENCHMARK = "U0001"


def _parse_rate(raw: str | None) -> float | str:
    if raw is None:
        return 0.0
    if raw.lower() in RATE_SERIES:
        return raw.lower()
    try:
        rate = float(raw)
    except ValueError:
        raise CliError(
            f"`--risk-free` takes an annual decimal or one of {', '.join(RATE_SERIES)}, got `{raw}`.",
            exit_code=EXIT_USAGE,
        ) from None
    # 3.5 for 3.5% would subtract 350% a year; ECOS and KIS quote rates in percent.
    if not 0 <= rate < 1:
        raise CliError(f"`--risk-free` is an annual decimal (0.035 for 3.5%), got `{raw}`.", exit_code=EXIT_USAGE)
    return rate


def _run_financials(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError(
            "Usage: cache financials --code <code> [--since-year YYYY] [--until-year YYYY].", exit_code=EXIT_USAGE
        )
    conn = _read_conn()
    try:
        payload = read_financials(
            conn,
            code.strip().upper(),
            since_year=_str_option(options, "since_year"),
            until_year=_str_option(options, "until_year"),
        )
    finally:
        conn.close()
    if not payload["years"]:
        payload["hint"] = (
            "No cached financials. Check the code with `cache company --code` and run `cache load --only "
            "financials` if the cache predates it."
        )
    _render_read(payload, options, default_limit=None)


def _run_perf(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError(
            "Usage: cache perf --code <code> [--bench U0001] [--since YYYYMMDD] [--until YYYYMMDD] "
            "[--risk-free 0.035|ktb3y].",
            exit_code=EXIT_USAGE,
        )
    until_raw = _str_option(options, "until")
    until = _parse_day(until_raw, "until") if until_raw else today_kst()
    since_raw = _str_option(options, "since")
    since = _parse_day(since_raw, "since") if since_raw else until - timedelta(days=_DEFAULT_OHLCV_DAYS)
    if since > until:
        raise CliError("`--since` is after `--until`.", exit_code=EXIT_USAGE)
    benchmark = (_str_option(options, "bench") or _DEFAULT_BENCHMARK).strip().upper()
    risk_free = _parse_rate(_str_option(options, "risk_free"))
    conn = _read_conn()
    try:
        payload = read_perf(
            conn, code.strip().upper(), benchmark=benchmark, since=since, until=until, risk_free=risk_free
        )
    finally:
        conn.close()
    if payload["performance"] is None:
        payload["hint"] = (
            "Fewer than 2 days with bars for both codes. Check them with `cache ohlcv --code` "
            "and the span with `cache status`."
        )
    _render_read(payload, options, default_limit=None)


def _list_option(options: dict[str, str | bool], key: str) -> list[str] | None:
    raw = _str_option(options, key)
    items = [item.strip() for item in raw.split(",") if item.strip()] if raw else []
    return items or None


def _trend_as_of(conn, raw: str | None) -> date:
    """`--as-of`, defaulting to the last KOSPI bar; a day without an index bar is a usage error."""

    latest = latest_index_date(conn)
    if latest is None:
        raise CliError("The cache has no index bars.", exit_code=EXIT_USAGE, hint="Run `cache load` first.")
    if raw is None:
        return latest
    as_of = _parse_day(raw, "as-of")
    row = conn.execute("SELECT max(date) FROM ohlcv WHERE code = 'U0001' AND date <= ?", [as_of]).fetchone()
    previous = row[0] if row else None
    if previous != as_of:
        hint = f"The previous trading day in the cache is {previous:%Y%m%d}." if previous else "Pick a later day."
        raise CliError(
            f"No KOSPI bar on {as_of:%Y%m%d} in the cache (holiday, or not loaded yet).",
            exit_code=EXIT_USAGE,
            hint=hint,
            data={"as_of": as_of.isoformat(), "latest": latest.isoformat()},
        )
    return as_of


def _history_filter(options: dict[str, str | bool]) -> bool:
    raw = _str_option(options, "history_filter")
    if raw is None:
        return False
    if raw != "fresh_g3":
        raise CliError(
            f"`--history-filter` takes fresh_g3, got `{raw}`.",
            exit_code=EXIT_USAGE,
            hint="Only filters that passed the out-of-sample test exist (README trend-setup §9).",
        )
    return True


def _run_trend_setup(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache trend-setup` does not accept positional arguments.", exit_code=EXIT_USAGE)
    market = _str_option(options, "market")
    if market is not None and market.upper() not in {"KOSPI", "KOSDAQ"}:
        raise CliError("`--market` takes KOSPI or KOSDAQ.", exit_code=EXIT_USAGE)
    codes = _list_option(options, "code")
    include_excluded = _parse_bool(options, "include_excluded")
    conn = _read_conn()
    try:
        as_of = _trend_as_of(conn, _str_option(options, "as_of"))
        payload = scan(
            conn,
            as_of,
            market=market.upper() if market else None,
            codes=[code.upper() for code in codes] if codes else None,
            statuses=_list_option(options, "status"),
            include_excluded=include_excluded,
            theme_filter=_parse_bool(options, "theme_filter"),
            with_history=_parse_bool(options, "history"),
            fresh_g3=_history_filter(options),
        )
    finally:
        conn.close()
    _render_read(payload, options, default_limit=_DEFAULT_COMPANY_LIMIT if include_excluded else None)


def _parse_int_list(raw: str | None, *, option: str) -> list[int] | None:
    if raw is None:
        return None
    items = [item.strip() for item in raw.split(",") if item.strip()]
    try:
        values = [int(item) for item in items]
    except ValueError:
        raise CliError(f"`--{option}` takes comma-separated integers, got `{raw}`.", exit_code=EXIT_USAGE) from None
    if not values or any(value <= 0 for value in values):
        raise CliError(f"`--{option}` takes positive integers, got `{raw}`.", exit_code=EXIT_USAGE)
    return values


def _parse_float(raw: str | None, *, option: str) -> float | None:
    if raw is None:
        return None
    try:
        value = float(raw)
    except ValueError:
        raise CliError(f"`--{option}` takes a number, got `{raw}`.", exit_code=EXIT_USAGE) from None
    if value <= 0:
        raise CliError(f"`--{option}` must be positive, got `{raw}`.", exit_code=EXIT_USAGE)
    return value


def _run_base_rate_build(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache base-rate-build` does not accept positional arguments.", exit_code=EXIT_USAGE)
    until_raw = _str_option(options, "until")
    until = _parse_day(until_raw, "until") if until_raw else None
    stride_raw = _str_option(options, "stride")
    stride = int(stride_raw) if stride_raw else baserate.SAMPLE_STRIDE
    if stride <= 0:
        raise CliError(f"`--stride` must be positive, got `{stride_raw}`.", exit_code=EXIT_USAGE)
    path = store.cache_path()
    conn = store.open_store(path)
    try:
        result = baserate.build(conn, stride=stride, until=until)
    finally:
        conn.close()
    render_output(
        {"path": str(path), **result},
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_base_rate(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError(
            "Usage: cache base-rate --code <code> [--as-of YYYYMMDD] [--horizons 20,40,60] "
            "[--target-pct P --stop-pct P].",
            exit_code=EXIT_USAGE,
        )
    as_of_raw = _str_option(options, "as_of")
    horizons = _parse_int_list(_str_option(options, "horizons"), option="horizons") or list(baserate.DEFAULT_HORIZONS)
    target_pct = _parse_float(_str_option(options, "target_pct"), option="target-pct")
    stop_pct = _parse_float(_str_option(options, "stop_pct"), option="stop-pct")
    if (target_pct is None) != (stop_pct is None):
        raise CliError("`--target-pct` and `--stop-pct` must be given together.", exit_code=EXIT_USAGE)
    conn = _read_conn()
    try:
        payload = baserate.query(
            conn,
            code.strip().upper(),
            as_of=_parse_day(as_of_raw, "as-of") if as_of_raw else None,
            horizons=tuple(horizons),
            target_pct=target_pct,
            stop_pct=stop_pct,
        )
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None)


def _run_rs(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache rs` does not accept positional arguments.", exit_code=EXIT_USAGE)
    market = _str_option(options, "market")
    if market is not None and market.upper() not in {"KOSPI", "KOSDAQ"}:
        raise CliError("`--market` takes KOSPI or KOSDAQ.", exit_code=EXIT_USAGE)
    codes = _list_option(options, "code")
    group_by = _str_option(options, "by") or "sector"
    if group_by not in {"sector", "industry"}:
        raise CliError("`--by` takes sector or industry.", exit_code=EXIT_USAGE)
    conn = _read_conn()
    try:
        as_of = _trend_as_of(conn, _str_option(options, "as_of"))
        payload = breadth.rs(
            conn,
            as_of,
            market=market.upper() if market else None,
            codes=[code.upper() for code in codes] if codes else None,
            group_by=group_by,
        )
    finally:
        conn.close()
    _render_read(payload, options, default_limit=_DEFAULT_COMPANY_LIMIT)


def _run_macro_beta(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError(
            "Usage: cache macro-beta --code <code> [--since YYYYMMDD] [--until YYYYMMDD] [--json].",
            exit_code=EXIT_USAGE,
        )
    until_raw = _str_option(options, "until")
    until = _parse_day(until_raw, "until") if until_raw else today_kst()
    since_raw = _str_option(options, "since")
    since = _parse_day(since_raw, "since") if since_raw else until - timedelta(days=DEFAULT_SINCE_DAYS)
    conn = _read_conn()
    try:
        payload = read_macro_beta(conn, code.strip().upper(), since=since, until=until)
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None)


def _run_breadth(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache breadth` does not accept positional arguments.", exit_code=EXIT_USAGE)
    market = _str_option(options, "market")
    if market is not None and market.upper() not in {"KOSPI", "KOSDAQ"}:
        raise CliError("`--market` takes KOSPI or KOSDAQ.", exit_code=EXIT_USAGE)
    conn = _read_conn()
    try:
        as_of = _trend_as_of(conn, _str_option(options, "as_of"))
        payload = breadth.breadth(conn, as_of, market=market.upper() if market else None)
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None)


def _parse_top(raw: str | None, *, default: int = magic.DEFAULT_TOP) -> int:
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise CliError(f"`--top` takes a positive integer, got `{raw}`.", exit_code=EXIT_USAGE) from None
    if value <= 0:
        raise CliError(f"`--top` must be positive, got `{raw}`.", exit_code=EXIT_USAGE)
    return value


def _run_magic_formula(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache magic-formula` does not accept positional arguments.", exit_code=EXIT_USAGE)
    top = _parse_top(_str_option(options, "top"))
    conn = _read_conn()
    try:
        as_of = _trend_as_of(conn, _str_option(options, "as_of"))
        payload = magic.screen(conn, as_of, top=top)
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None)


_SCREENS_TOML = "screens.toml"


def _load_preset(name: str) -> dict[str, Any]:
    """`[name]` of research/screens.toml: `where`, and optionally `sort`, `order`, `top`."""

    path = research_root() / _SCREENS_TOML
    if not path.is_file():
        raise CliError(
            f"No {path} — `--preset` needs a file there first.",
            exit_code=EXIT_USAGE,
            hint='Example:\n[my-quality]\nwhere = "per<10,roe>=15,rs_1m>=70"\nsort = "roe"',
        )
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise CliError(f"{path} is not valid TOML: {exc}.", exit_code=EXIT_USAGE) from exc
    preset = data.get(name)
    if not isinstance(preset, dict):
        raise CliError(f"No preset `{name}` in {path}.", exit_code=EXIT_USAGE, data={"presets": sorted(data)})
    issues = [f"`{key}` must be a string" for key in ("where", "sort", "order") if not _is_str_or_none(preset.get(key))]
    top = preset.get("top")
    if top is not None and (not isinstance(top, int) or isinstance(top, bool) or top <= 0):
        issues.append("`top` must be a positive integer")
    if issues:
        raise CliError(f"Preset `{name}` in {path} is invalid.", exit_code=EXIT_USAGE, data={"issues": issues})
    return preset


def _is_str_or_none(value: Any) -> bool:
    return value is None or isinstance(value, str)


def _parse_order(raw: str | None) -> bool:
    """True for descending (the default)."""

    if raw is None or raw == "desc":
        return True
    if raw == "asc":
        return False
    raise CliError(f"`--order` takes asc or desc, got `{raw}`.", exit_code=EXIT_USAGE)


def _run_screen(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache screen` does not accept positional arguments.", exit_code=EXIT_USAGE)
    if _parse_bool(options, "factors"):
        render_output(
            cache_screen.factor_catalog(),
            force_json=bool(options.get("json", False)),
            compact=bool(options.get("compact", False)),
        )
        return
    where_raw = _str_option(options, "where")
    sort = _str_option(options, "sort")
    preset_name = _str_option(options, "preset")
    top_raw = _str_option(options, "top")
    order_raw = _str_option(options, "order")
    if preset_name is not None:
        if where_raw is not None or sort is not None or order_raw is not None:
            raise CliError("`--preset` cannot be combined with `--where`/`--sort`/`--order`.", exit_code=EXIT_USAGE)
        preset = _load_preset(preset_name)
        where_raw, sort, order_raw = preset.get("where"), preset.get("sort"), preset.get("order")
        if top_raw is None and preset.get("top") is not None:
            top_raw = str(preset["top"])
    descending = _parse_order(order_raw)
    if sort is not None and sort not in cache_screen.FACTOR_NAMES:
        raise CliError(
            f"`--sort` takes a factor name, got `{sort}`.",
            exit_code=EXIT_USAGE,
            hint="Run `cache screen --factors true` for the factor list.",
        )
    market = _str_option(options, "market")
    if market is not None and market.upper() not in {"KOSPI", "KOSDAQ"}:
        raise CliError("`--market` takes KOSPI or KOSDAQ.", exit_code=EXIT_USAGE)
    codes = _list_option(options, "code")
    conn = _read_conn()
    try:
        as_of = _trend_as_of(conn, _str_option(options, "as_of"))
        payload = cache_screen.screen(
            conn,
            as_of,
            market=market.upper() if market else None,
            sector=_str_option(options, "sector"),
            industry=_str_option(options, "industry"),
            codes=[code.upper() for code in codes] if codes else None,
            where=cache_screen.parse_where(where_raw) if where_raw else None,
            sort=sort,
            descending=descending,
            top=_parse_top(top_raw, default=cache_screen.DEFAULT_TOP) if top_raw is not None else None,
        )
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None)


def _run_peers(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError("Usage: cache peers --code <code> [--as-of YYYYMMDD] [--top 5] [--json].", exit_code=EXIT_USAGE)
    top = _parse_top(_str_option(options, "top"), default=cache_peers.DEFAULT_TOP)
    conn = _read_conn()
    try:
        as_of = _trend_as_of(conn, _str_option(options, "as_of"))
        payload = cache_peers.peers(conn, as_of, code, top=top)
    finally:
        conn.close()
    _render_read(payload, options, default_limit=None)


SUBCOMMANDS: dict[str, Callable[[list[str]], None]] = {
    "status": _run_status,
    "load": _run_load,
    "ohlcv": _run_ohlcv,
    "company": _run_company,
    "financials": _run_financials,
    "perf": _run_perf,
    "trend-setup": _run_trend_setup,
    "base-rate-build": _run_base_rate_build,
    "base-rate": _run_base_rate,
    "rs": _run_rs,
    "breadth": _run_breadth,
    "macro-beta": _run_macro_beta,
    "magic-formula": _run_magic_formula,
    "screen": _run_screen,
    "peers": _run_peers,
}


def run_cache(argv: list[str]) -> None:
    if not argv or argv[0] not in SUBCOMMANDS:
        raise CliError(
            "Usage: cache <" + "|".join(SUBCOMMANDS) + "> [options].",
            exit_code=EXIT_USAGE,
            data={"subcommands": list(SUBCOMMANDS)},
        )
    SUBCOMMANDS[argv[0]](argv[1:])
