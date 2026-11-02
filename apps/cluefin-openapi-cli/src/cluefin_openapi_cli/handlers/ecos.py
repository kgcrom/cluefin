"""Bank of Korea ECOS handlers (economic statistics)."""

from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from cluefin_openapi_cli import industry, macro
from cluefin_openapi_cli.clock import today_kst
from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_CREDENTIALS, EXIT_USAGE, CliError
from cluefin_openapi_cli.handlers._base import DispatcherProtocol, rpc_method

CYCLES = ("D", "M", "Q", "A", "S", "SM")

# ECOS period formats by cycle (검색시작일자 · 검색종료일자). The server answers a wrong one with ERROR-101.
_PERIOD_PATTERNS = {
    "A": (re.compile(r"^\d{4}$"), "2024"),
    "S": (re.compile(r"^\d{4}S[12]$"), "2024S1"),
    "Q": (re.compile(r"^\d{4}Q[1-4]$"), "2024Q1"),
    "M": (re.compile(r"^\d{4}(0[1-9]|1[0-2])$"), "202401"),
    "SM": (re.compile(r"^\d{4}(0[1-9]|1[0-2])S[12]$"), "202401S1"),
    "D": (re.compile(r"^\d{8}$"), "20240101"),
}

_STAT_CODE_PARAM = {
    "type": "string",
    "pattern": r"^[0-9A-Z]{7}$",
    "description": "ECOS table code (통계표코드), e.g. 817Y002 market rates (daily). Find it with ecos table-search.",
}

_CYCLE_DESCRIPTION = "Cycle (주기): D daily, M monthly, Q quarterly, A annual, S half-year, SM half-month."

_DEFAULT_TABLE_ROWS = 50
_DEFAULT_ITEM_ROWS = 200
_DEFAULT_SERIES_ROWS = 500


def _max_rows_param(default: int, what: str) -> dict:
    return {
        "type": "integer",
        "minimum": 0,
        "default": default,
        "description": f"Max {what} returned. Default {default}, 0 = no cap. "
        "Named max_rows because --limit is a global CLI option and never reaches handlers.",
    }


def _cap(rows: list, params: dict, default: int, *, keep_latest: bool = False) -> dict:
    """``total``/``returned``/``truncated`` + ``data`` like sec company-lookup; 0 = no cap."""
    max_rows = int(params.get("max_rows", default))
    if max_rows == 0 or len(rows) <= max_rows:
        page = rows
    else:
        page = rows[-max_rows:] if keep_latest else rows[:max_rows]
    return {"total": len(rows), "returned": len(page), "truncated": len(page) < len(rows), "data": page}


def _terms(value: str | None) -> list[str]:
    return [term.lower() for term in (value or "").split() if term]


def _matches(terms: list[str], *texts: str | None) -> bool:
    haystack = " ".join(text or "" for text in texts).lower()
    return all(term in haystack for term in terms)


def to_number(raw: str | None) -> float | None:
    """ECOS `DATA_VALUE` → float. Blank (holiday, not yet compiled) or non-numeric → None."""
    if raw is None or not str(raw).strip():
        return None
    try:
        return float(Decimal(str(raw).replace(",", "")))
    except InvalidOperation:
        return None


def check_period(cycle: str, value: str, field: str) -> None:
    pattern, example = _PERIOD_PATTERNS[cycle]
    valid = bool(pattern.match(value))
    if valid and cycle == "D":
        try:
            datetime.strptime(value, "%Y%m%d")
        except ValueError:
            valid = False
    if not valid:
        raise CliError(
            f"{field} {value!r} does not match cycle {cycle}.",
            exit_code=EXIT_USAGE,
            data={"field": field, "cycle": cycle, "value": value},
            error_type="InvalidPeriod",
            hint=f"Cycle {cycle} periods look like {example}. "
            "Formats: A 2024, S 2024S1, Q 2024Q1, M 202401, SM 202401S1, D 20240101.",
        )


@rpc_method(
    name="ecos.table_search",
    description=(
        "Find Bank of Korea ECOS statistics tables (통계표) by name: base rate, market rates, exchange rates, CPI, "
        "GDP growth, composite leading index, business (BSI) and consumer sentiment, exports, money supply. Every "
        "space-separated term must appear in the table name or code. Rows: stat_code, stat_name (with its "
        "outline number), cycle, org_name. The full list (~840 rows) is downloaded on every call and filtered "
        "locally — with the public sample key that is ~85 calls. Next: ecos items --stat-code."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Name terms, e.g. 경기종합, 시장금리, 환율 (all must match)"},
            "cycle": {"type": "string", "enum": list(CYCLES), "description": _CYCLE_DESCRIPTION},
            "searchable_only": {
                "type": "boolean",
                "default": True,
                "description": "Only tables ecos series can read (SRCH_YN=Y); false also lists grouping rows.",
            },
            "max_rows": _max_rows_param(_DEFAULT_TABLE_ROWS, "tables"),
        },
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_table_search(params: dict, session) -> dict:
    ecos = session.get_ecos()
    page = ecos.statistic_catalog.table_list()
    terms = _terms(params.get("query"))
    cycle = params.get("cycle")
    searchable_only = params.get("searchable_only", True)
    rows = [
        {
            "stat_code": table.stat_code,
            "stat_name": table.stat_name,
            "cycle": table.cycle,
            "org_name": table.org_name,
            "parent_stat_code": table.parent_stat_code,
        }
        for table in page.rows or []
        if (not searchable_only or table.searchable == "Y")
        and (not cycle or table.cycle == cycle)
        and _matches(terms, table.stat_name, table.stat_code)
    ]
    return _cap(rows, params, _DEFAULT_TABLE_ROWS)


@rpc_method(
    name="ecos.items",
    description=(
        "List an ECOS table's item codes (통계항목코드) — what ecos series takes as item_codes. One row per item and "
        "cycle: group_code (Group1 → item_codes[0], Group2 → item_codes[1], …), item_code, item_name, cycle, "
        "start_time, end_time (latest period on file), unit_name. Filter by item name terms and cycle."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stat_code": _STAT_CODE_PARAM,
            "query": {"type": "string", "description": "Item name terms, e.g. 국고채 3년 (all must match)"},
            "cycle": {"type": "string", "enum": list(CYCLES), "description": _CYCLE_DESCRIPTION},
            "max_rows": _max_rows_param(_DEFAULT_ITEM_ROWS, "items"),
        },
        "required": ["stat_code"],
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_items(params: dict, session) -> dict:
    ecos = session.get_ecos()
    page = ecos.statistic_catalog.item_list(params["stat_code"])
    terms = _terms(params.get("query"))
    cycle = params.get("cycle")
    rows = [
        {
            "group_code": item.group_code,
            "group_name": item.group_name,
            "item_code": item.item_code,
            "item_name": item.item_name,
            "parent_item_code": item.parent_item_code,
            "cycle": item.cycle,
            "start_time": item.start_time,
            "end_time": item.end_time,
            "unit_name": item.unit_name,
        }
        for item in page.rows or []
        if (not cycle or item.cycle == cycle) and _matches(terms, item.item_name, item.item_code)
    ]
    payload = {"stat_code": params["stat_code"]}
    payload.update(_cap(rows, params, _DEFAULT_ITEM_ROWS))
    if not rows and not page.list_total_count:
        payload["hint"] = "No items. Check the table code with ecos table-search."
    return payload


def _split_codes(value: str | None) -> list[str]:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def _observation_row(row) -> dict[str, Any]:
    out: dict[str, Any] = {"time": row.time, "value": to_number(row.data_value)}
    for level in range(1, 5):
        code = getattr(row, f"item_code{level}")
        if code:
            out[f"item_code{level}"] = code
            out[f"item_name{level}"] = getattr(row, f"item_name{level}")
    return out


@rpc_method(
    name="ecos.series",
    description=(
        "Read an ECOS statistic's time series (StatisticSearch): one table, one cycle, a start/end period and up "
        "to four item codes (from ecos items; omitted = every item in the table). Rows: time, value (number; null "
        "for blank), item codes and names. Periods follow the cycle: D 20240101, M 202401, Q 2024Q1, A 2024, "
        "S 2024S1, SM 202401S1. Values are as published — rates in annual percent (3.5 = 3.5%), indices by their "
        "base year. max_rows keeps the most recent rows."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stat_code": _STAT_CODE_PARAM,
            "cycle": {"type": "string", "enum": list(CYCLES), "description": _CYCLE_DESCRIPTION},
            "start_date": {"type": "string", "description": "First period in the cycle's format (검색시작일자)"},
            "end_date": {"type": "string", "description": "Last period in the cycle's format (검색종료일자)"},
            "item_codes": {
                "type": "string",
                "description": "Comma-separated item codes in group order, up to 4 (e.g. 99988,BA for 512Y014)",
            },
            "max_rows": _max_rows_param(_DEFAULT_SERIES_ROWS, "observations (most recent kept)"),
        },
        "required": ["stat_code", "cycle", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_series(params: dict, session) -> dict:
    cycle = params["cycle"]
    start, end = params["start_date"], params["end_date"]
    check_period(cycle, start, "start_date")
    check_period(cycle, end, "end_date")
    if start > end:
        raise CliError(f"start_date {start} is after end_date {end}.", exit_code=EXIT_USAGE, error_type="InvalidPeriod")
    item_codes = _split_codes(params.get("item_codes"))
    if len(item_codes) > 4:
        raise CliError(
            f"ECOS takes up to 4 item codes, got {len(item_codes)}.",
            exit_code=EXIT_USAGE,
            error_type="TooManyItemCodes",
        )

    ecos = session.get_ecos()
    page = ecos.statistic_search.search(params["stat_code"], cycle, start, end, tuple(item_codes))
    observations = list(page.rows or [])
    first = observations[0] if observations else None
    units = sorted({row.unit_name for row in observations if row.unit_name})
    rows = [_observation_row(row) for row in observations]
    if len(units) > 1:
        for out, row in zip(rows, observations, strict=False):
            out["unit_name"] = row.unit_name
    # ECOS orders several items item by item; sort by period (stable) so max_rows keeps the latest periods of all.
    rows.sort(key=lambda out: out["time"])

    payload: dict[str, Any] = {
        "stat_code": params["stat_code"],
        "stat_name": first.stat_name if first else None,
        "cycle": cycle,
        "unit": units[0] if len(units) == 1 else units or None,
    }
    payload.update(_cap(rows, params, _DEFAULT_SERIES_ROWS, keep_latest=True))
    if not rows:
        payload["hint"] = (
            "No data (INFO-200). Check the table/item codes and cycle with ecos items — its end_time is the latest "
            "period on file, and monthly or quarterly statistics are published weeks after the period ends."
        )
    return payload


@rpc_method(
    name="ecos.key_stats",
    description=(
        "ECOS 100 key statistics (100대 통계지표): the latest value of each headline indicator — base rate, call and "
        "CD rates, treasury yields, KOSPI, exchange rates, money supply, GDP growth, CPI, unemployment, current "
        "account and more — each with its own as_of period. One call, no codes needed. Filter by name terms."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Indicator or group name terms, e.g. 금리, 환율"},
        },
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_key_stats(params: dict, session) -> dict:
    ecos = session.get_ecos()
    page = ecos.statistic_catalog.key_statistic_list()
    terms = _terms(params.get("query"))
    rows = [
        {
            "class_name": row.class_name,
            "name": row.keystat_name,
            "value": to_number(row.data_value),
            "as_of": row.cycle,
            "unit_name": row.unit_name,
        }
        for row in page.rows or []
        if _matches(terms, row.class_name, row.keystat_name)
    ]
    # The server's row order changes between calls; sort so two calls diff cleanly.
    rows.sort(key=lambda row: (row["class_name"] or "", row["name"] or ""))
    return {"total": len(rows), "data": rows}


@rpc_method(
    name="ecos.word",
    description=(
        "ECOS statistics glossary (통계용어사전): the definition of an economic term such as 경제심리지수, "
        "선행지수순환변동치, 기업경기실사지수. Rows: word, content."
    ),
    parameters={
        "type": "object",
        "properties": {"term": {"type": "string", "description": "Term to look up (Korean), e.g. 경제심리지수"}},
        "required": ["term"],
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_word(params: dict, session) -> dict:
    ecos = session.get_ecos()
    page = ecos.statistic_glossary.word(params["term"])
    rows = [{"word": row.word, "content": row.content} for row in page.rows or []]
    return {"term": params["term"], "total": len(rows), "data": rows}


def _today():
    """Injection point for tests."""
    return today_kst()


_MACRO_NOTES = [
    "Each indicator has its own as_of: monthly and quarterly statistics are published weeks after the period, so "
    "they are not aligned to one date. ECOS posts daily rates one business day late.",
    "change.1m/3m/1y (1q/1y for quarterly) is the latest value minus the last value on or before that many months "
    "earlier, in the indicator's unit (%p for rates, spreads and the yoy rows; points for indices).",
    "percentile is the share of the window's observations at or below the latest value (0-100); min/max are over "
    "the same window. Daily series have ~250 observations a year, monthly 12.",
    "Values are as published today. GDP and some indices are revised later, so a past percentile computed from "
    "this data is not what was known at the time.",
    "No regime label is given on purpose: read levels, direction and percentiles yourself and say which ones a "
    "call depends on.",
]


@rpc_method(
    name="ecos.macro_snapshot",
    description=(
        "Macro backdrop in one call: base rate, treasury 3y/10y, corporate bond AA-/BBB- yields, USD/KRW, CPI "
        "inflation (yoy), composite leading and coincident index cycles, economic sentiment (ESI), business "
        "outlook (BSI), consumer sentiment (CCSI), news sentiment, real GDP growth (qoq) and exports growth (yoy), "
        "plus term spread (10y-3y) and credit spreads (AA- minus treasury, BBB- minus AA-). Each row: value, "
        "as_of, change over 1m/3m/1y, percentile and min/max within the last window_years, source table and "
        "items. Numbers only, no regime label. About 15 ECOS series calls; needs ECOS_AUTH_KEY (the sample key "
        "would take hundreds of calls)."
    ),
    parameters={
        "type": "object",
        "properties": {
            "window_years": {
                "type": "integer",
                "minimum": 3,
                "maximum": 20,
                "default": 10,
                "description": "Years of history behind percentile/min/max. Default 10.",
            },
        },
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_macro_snapshot(params: dict, session) -> dict:
    window_years = int(params.get("window_years", 10))
    ecos = session.get_ecos()
    # `is True`: the client contract test hands in a proxy object, which must not read as the sample key.
    if ecos.is_sample is True:
        raise CliError(
            "ecos macro-snapshot needs ECOS_AUTH_KEY.",
            exit_code=EXIT_CREDENTIALS,
            error_type="CredentialsMissing",
            hint="Set ECOS_AUTH_KEY in .env. The public sample key pages 10 rows a call, so ten years of daily "
            "rates would take hundreds of calls. ecos series still works without a key for short ranges.",
        )
    today = _today()

    def fetch(series: macro.MacroSeries) -> list[macro.Point]:
        start, end = macro.fetch_window(series, today, window_years)
        page = ecos.statistic_search.search(series.stat_code, series.cycle, start, end, series.item_codes)
        points = [(row.time, to_number(row.data_value)) for row in page.rows or []]
        return sorted((time, value) for time, value in points if value is not None)

    result = macro.snapshot(fetch, window_years=window_years)
    if not result["indicators"]:
        raise CliError(
            "ECOS returned no data for any macro series.",
            exit_code=EXIT_BROKER,
            data={"missing": result["missing"]},
            error_type="BrokerApiError",
            retryable=True,
            hint="Retry once; if it persists, check one series with ecos series.",
        )
    return {"run_date": f"{today:%Y-%m-%d}", "window_years": window_years, **result, "notes": _MACRO_NOTES}


_INDUTY_CODE_PARAM = {
    "type": "string",
    "pattern": r"^[0-9]{2,5}$",
    "description": "Industry code as DART company-overview's induty_code (KSIC), 2-5 digits. Only the first two "
    "digits (the KSIC manufacturing division) are used, e.g. 26410 -> division 26.",
}

_INDUSTRY_NOTES = [
    "Industry-level: these are division averages, not one company. A diversified company (holding company, "
    "several business segments) should also check which product its own segments actually sell (recipe "
    "filing-text) rather than read the division number as that company's number.",
    "Each indicator has its own as_of (BSI, production/shipment/inventory and product prices are monthly but "
    "not published the same week). change.1m/3m/1y is the latest value minus the last value on or before that "
    "many months earlier. percentile is the share of the window's observations at or below the latest value.",
    "production/shipment/inventory and the inventory cycle use the raw (원지수) index, not seasonally adjusted, "
    "so the same basis underlies both the YoY rows and the inventory-cycle subtraction.",
    "inventory_cycle gives shipments_up/inventory_up (sign of each YoY) and their difference only — no phase "
    "name (회복/확장/하강/수축): that is a forecast rule and this repo only ships rules that passed an "
    "out-of-sample check (README §9).",
    "export_price_yoy is 원화기준 (KRW basis, 402Y014 item 'W'), matching the KRW basis of ppi_yoy and the "
    "production/shipment/inventory legs, not the dollar-basis alternative ECOS also publishes.",
    "missing lists the indicators this division has no mapped code for (e.g. no standalone commodity price for "
    "printing or for shipbuilding/기타운송장비 in these ECOS tables) rather than substituting a loosely related "
    "product. See industry.py for which division has which code and how it was checked.",
    "If industry.bsi_shared_with is non-empty, this division's bsi_outlook/bsi_actual come from a BSI survey "
    "industry code shared with another division (e.g. 12 담배 and 33 기타 제품 both read C3300) — the BSI value "
    "is not specific to this division alone.",
]


@rpc_method(
    name="ecos.industry_outlook",
    description=(
        "One KSIC manufacturing division's (C10-C33) leading indicators in one call: business survey index (BSI) "
        "outlook and actual, production/shipment/inventory indices (yoy, raw index), the inventory cycle "
        "(shipment yoy minus inventory yoy, signs only), and a representative product's export price, producer "
        "price (PPI) and export value index (yoy). Each row: value, as_of, change over 1m/3m/1y, percentile and "
        "min/max within the last window_years, source table and items. Numbers only, no phase/regime label. "
        "induty_code is the KSIC code as DART company-overview returns it (first two digits select the division); "
        "non-manufacturing or unknown divisions are exit 2. About 8-11 ECOS series calls; needs ECOS_AUTH_KEY."
    ),
    parameters={
        "type": "object",
        "properties": {
            "induty_code": _INDUTY_CODE_PARAM,
            "window_years": {
                "type": "integer",
                "minimum": 3,
                "maximum": 20,
                "default": 10,
                "description": "Years of history behind percentile/min/max. Default 10.",
            },
        },
        "required": ["induty_code"],
    },
    returns={"type": "object"},
    category="ecos",
    broker="ecos",
)
def handle_industry_outlook(params: dict, session) -> dict:
    division = industry.resolve_division(params["induty_code"])
    if division is None:
        raise CliError(
            f"induty_code {params['induty_code']!r} is not a KSIC manufacturing division (10-33).",
            exit_code=EXIT_USAGE,
            error_type="UnsupportedIndustry",
            hint="This command covers manufacturing divisions only (KSIC C10-C33, from DART company-overview "
            "induty_code). Non-manufacturing industries are out of scope.",
        )
    window_years = int(params.get("window_years", 10))
    ecos = session.get_ecos()
    if ecos.is_sample is True:
        raise CliError(
            "ecos industry-outlook needs ECOS_AUTH_KEY.",
            exit_code=EXIT_CREDENTIALS,
            error_type="CredentialsMissing",
            hint="Set ECOS_AUTH_KEY in .env. The public sample key pages 10 rows a call, so ten years of monthly "
            "series would take many calls. ecos series still works without a key for short ranges.",
        )
    today = _today()

    def fetch(series: macro.MacroSeries) -> list[macro.Point]:
        start, end = macro.fetch_window(series, today, window_years)
        page = ecos.statistic_search.search(series.stat_code, series.cycle, start, end, series.item_codes)
        points = [(row.time, to_number(row.data_value)) for row in page.rows or []]
        return sorted((time, value) for time, value in points if value is not None)

    result = industry.industry_outlook(division, fetch, window_years=window_years)
    if not result["indicators"]:
        raise CliError(
            "ECOS returned no data for any indicator of this division.",
            exit_code=EXIT_BROKER,
            data={"missing": result["missing"]},
            error_type="BrokerApiError",
            retryable=True,
            hint="Retry once; if it persists, check one series with ecos series.",
        )
    return {
        "run_date": f"{today:%Y-%m-%d}",
        "window_years": window_years,
        "industry": {
            "ksic": division.ksic,
            "name": division.name,
            "product": division.product_name,
            "codes": {
                "bsi": division.bsi_item,
                "production_shipment_inventory": division.production_item,
                "export_price": division.export_price_item,
                "ppi": division.ppi_item,
                "export_value": division.export_value_item,
            },
            "bsi_shared_with": [
                {"ksic": shared.ksic, "name": shared.name} for shared in industry.bsi_shared_with(division)
            ],
        },
        **result,
        "notes": _INDUSTRY_NOTES,
    }


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_table_search,
    handle_items,
    handle_series,
    handle_key_stats,
    handle_word,
    handle_macro_snapshot,
    handle_industry_outlook,
]


def register_ecos_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
