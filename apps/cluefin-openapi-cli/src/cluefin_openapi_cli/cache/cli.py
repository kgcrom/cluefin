"""`cache <sub>` meta command. `load` writes from brokers; every other subcommand only reads the file."""

from __future__ import annotations

import sys
from datetime import date, datetime, time, timedelta
from typing import Any, Callable
from zoneinfo import ZoneInfo

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.load import PARTS, Sources, run_load
from cluefin_openapi_cli.cache.perf import read_perf
from cluefin_openapi_cli.cache.read import read_company, read_ohlcv
from cluefin_openapi_cli.cliargs import _parse_fields, _parse_limit, _parse_named_options, _str_option
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError, classify_exception
from cluefin_openapi_cli.output import attach_truncation, limit_rows, render_output, select_fields

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
    sys.stderr.write(f"[cache load] {datetime.now():%H:%M:%S} {message}\n")
    sys.stderr.flush()


def _run_load(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache load` does not accept positional arguments.", exit_code=EXIT_USAGE)
    parts = _parse_parts(_str_option(options, "only"))
    since = _parse_day(_str_option(options, "since") or _DEFAULT_SINCE, "since")
    now = datetime.now(ZoneInfo("Asia/Seoul")).replace(tzinfo=None)
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
    until = _parse_day(until_raw, "until") if until_raw else date.today()
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


def _parse_rate(raw: str | None) -> float:
    if raw is None:
        return 0.0
    try:
        rate = float(raw)
    except ValueError:
        raise CliError(f"`--risk-free` must be a number, got `{raw}`.", exit_code=EXIT_USAGE) from None
    # 3.5 for 3.5% would subtract 350% a year; ECOS and KIS quote rates in percent.
    if not 0 <= rate < 1:
        raise CliError(f"`--risk-free` is an annual decimal (0.035 for 3.5%), got `{raw}`.", exit_code=EXIT_USAGE)
    return rate


def _run_perf(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    code = _str_option(options, "code")
    if positional or not code:
        raise CliError(
            "Usage: cache perf --code <code> [--bench U0001] [--since YYYYMMDD] [--until YYYYMMDD] "
            "[--risk-free 0.035].",
            exit_code=EXIT_USAGE,
        )
    until_raw = _str_option(options, "until")
    until = _parse_day(until_raw, "until") if until_raw else date.today()
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


SUBCOMMANDS: dict[str, Callable[[list[str]], None]] = {
    "status": _run_status,
    "load": _run_load,
    "ohlcv": _run_ohlcv,
    "company": _run_company,
    "perf": _run_perf,
}


def run_cache(argv: list[str]) -> None:
    if not argv or argv[0] not in SUBCOMMANDS:
        raise CliError(
            "Usage: cache <" + "|".join(SUBCOMMANDS) + "> [options].",
            exit_code=EXIT_USAGE,
            data={"subcommands": list(SUBCOMMANDS)},
        )
    SUBCOMMANDS[argv[0]](argv[1:])
