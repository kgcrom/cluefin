"""DART disclosure handlers."""

from __future__ import annotations

import contextlib
import itertools
import sys
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.errors import (
    DART_REQUEST_LIMIT_STATUS,
    EXIT_BROKER,
    EXIT_USAGE,
    CliError,
    DartQuotaExceededAPIError,
)
from cluefin_openapi_cli.handlers._base import DispatcherProtocol, dump_model, rpc_method


@rpc_method(
    name="dart.disclosure_search",
    description="Search DART disclosures. Supports filtering by corp code, date range, type.",
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
            "bgn_de": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_de": {"type": "string", "description": "End date (YYYYMMDD)"},
            "last_reprt_at": {"type": "string", "enum": ["Y", "N"], "description": "Last report only. Default N."},
            "pblntf_ty": {
                "type": "string",
                "enum": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "description": "Disclosure type (A:periodic, B:major-report, C:issuance, D:ownership, "
                "E:other, F:external-audit, G:fund, H:asset-securitization, I:exchange, J:fair-trade)",
            },
            "pblntf_detail_ty": {
                "type": "string",
                "description": "Disclosure detail type code (per DART docs). Ignored when pblntf_ty is A.",
            },
            "corp_cls": {
                "type": "string",
                "enum": ["Y", "K", "N", "E"],
                "description": "Corp class (Y:KOSPI, K:KOSDAQ, N:KONEX, E:other)",
            },
            "sort": {
                "type": "string",
                "enum": ["date", "crp", "rpt"],
                "description": "Sort key (date:received-date, crp:company-name, rpt:report-name)",
            },
            "sort_mth": {
                "type": "string",
                "enum": ["asc", "desc"],
                "description": "Sort order (asc, desc)",
            },
            "page_no": {"type": "integer", "description": "Page number"},
            "page_count": {"type": "integer", "description": "Items per page (1-100)"},
        },
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_disclosure_search(params: dict, session) -> dict:
    dart = session.get_dart()
    kwargs = {}
    for key in [
        "corp_code",
        "bgn_de",
        "end_de",
        "last_reprt_at",
        "pblntf_ty",
        "pblntf_detail_ty",
        "corp_cls",
        "sort",
        "sort_mth",
        "page_no",
        "page_count",
    ]:
        if key in params:
            kwargs[key] = params[key]
    result = dart.public_disclosure.public_disclosure_search(**kwargs)
    return dump_model(_checked(result))


@rpc_method(
    name="dart.company_overview",
    description="Get company overview from DART.",
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
        },
        "required": ["corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_company_overview(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.public_disclosure.company_overview(params["corp_code"])
    return dump_model(_checked(result))


def _checked(result):
    """Pass a client result through, raising if DART answered 200 with status 020 (quota).

    The client parses that body into a normal model. The status sits on the model itself or
    under its ``result`` envelope depending on the endpoint. Other statuses (e.g. 013, no
    data) are left alone on purpose.
    """
    for holder in (result, getattr(result, "result", None)):
        status = getattr(holder, "status", None)
        if status is None:
            continue
        if getattr(status, "value", status) == DART_REQUEST_LIMIT_STATUS:
            raise DartQuotaExceededAPIError(str(getattr(holder, "message", None) or "DART request limit exceeded"))
        break
    return result


_DEFAULT_MAX_ROWS = 100


def _clean(value) -> str:
    """Normalize an XML-sourced field; DART pads unlisted stock codes with spaces."""
    return str(value).strip() if value is not None else ""


def _max_rows(params: dict) -> int:
    """Row cap from params. Anything unusable falls back to the default; 0 means no cap."""
    try:
        max_rows = int(params.get("max_rows", _DEFAULT_MAX_ROWS))
    except (TypeError, ValueError):
        return _DEFAULT_MAX_ROWS
    return _DEFAULT_MAX_ROWS if max_rows < 0 else max_rows


def _paged_response(matched: list, params: dict) -> dict:
    """Cap ``matched`` and shape it like the ``list --full`` truncation contract.

    Callers that need a specific row order must sort before calling: the cap keeps the
    head of the list, so the ordering decides which rows survive.
    """
    max_rows = _max_rows(params)
    page = matched if max_rows == 0 else matched[:max_rows]
    data = [dump_model(row) for row in page]
    return {
        "total": len(matched),
        "returned": len(data),
        "truncated": len(data) < len(matched),
        "data": data,
    }


@rpc_method(
    name="dart.corp_code_lookup",
    description=(
        "Look up DART corporate codes. The full list is ~120k rows, so filter by corp_code, "
        "stock_code or corp_name; output is capped at 100 rows unless max_rows says otherwise."
    ),
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Exact corporate unique code (8 digits)"},
            "stock_code": {"type": "string", "description": "Exact listed stock code (6 digits), e.g. 020000"},
            "corp_name": {"type": "string", "description": "Company name, case-insensitive substring match"},
            "listed_only": {"type": "boolean", "description": "Keep only companies with a stock code. Default false."},
            "max_rows": {
                "type": "integer",
                "description": "Max rows returned. Default 100, 0 = no cap. "
                "Named max_rows because --limit is a global CLI option and never reaches handlers.",
            },
        },
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_corp_code_lookup(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.public_disclosure.corp_code()
    # Items live under the DART result envelope. UniqueNumber also declares a top-level
    # `list` field that parse() never fills, so reading that one yields zero rows.
    items = getattr(getattr(_checked(result), "result", None), "list", None) or []
    return _paged_response(_filter_corp_codes(items, params), params)


def _filter_corp_codes(items, params: dict) -> list:
    """Apply the corp-code-lookup filters. Pure: takes rows in, gives matching rows out.

    ``corp_code``/``stock_code`` match exactly after stripping the padding DART puts on
    unlisted stock codes; ``corp_name`` is a case-insensitive substring match.
    """
    corp_code = _clean(params.get("corp_code"))
    stock_code = _clean(params.get("stock_code"))
    corp_name = _clean(params.get("corp_name")).lower()
    listed_only = bool(params.get("listed_only", False))

    matched = []
    for item in items:
        item_stock_code = _clean(getattr(item, "stock_code", None))
        if corp_code and _clean(getattr(item, "corp_code", None)) != corp_code:
            continue
        if stock_code and item_stock_code != stock_code:
            continue
        if corp_name and corp_name not in _clean(getattr(item, "corp_name", None)).lower():
            continue
        if listed_only and not item_stock_code:
            continue
        matched.append(item)
    return matched


def _digits(value) -> str:
    """Keep only digits; DART returns rcept_dt as `2026-09-09` here but `20260909` elsewhere."""
    return "".join(ch for ch in _clean(value) if ch.isdigit())


def _collect_share_rows(result, params: dict) -> dict:
    """Filter, sort and cap a share-disclosure list into the standard response shape.

    Both share-disclosure endpoints take only ``corp_code`` and return the company's
    full reporting history, so date filtering and capping happen here. Rows come back
    newest first, which keeps ``max_rows`` from dropping the recent ones.
    """
    rows = getattr(getattr(_checked(result), "result", None), "list", None) or []
    return _paged_response(_filter_share_rows(rows, params), params)


def _filter_share_rows(rows, params: dict) -> list:
    """Apply the share-disclosure filters and sort newest first. Pure: rows in, rows out.

    ``since``/``until`` are inclusive and compared on digits only, so ``2026-09-09`` and
    ``20260909`` both work. Rows without a receipt date pass the date filters.
    """
    since = _digits(params.get("since"))
    until = _digits(params.get("until"))
    reporter = _clean(params.get("reporter")).lower()

    matched = []
    for row in rows:
        rcept_dt = _digits(getattr(row, "rcept_dt", None))
        if since and rcept_dt and rcept_dt < since:
            continue
        if until and rcept_dt and rcept_dt > until:
            continue
        if reporter and reporter not in _clean(getattr(row, "repror", None)).lower():
            continue
        matched.append(row)

    matched.sort(key=lambda row: _digits(getattr(row, "rcept_dt", None)), reverse=True)
    return matched


_SHARE_DISCLOSURE_FILTERS = {
    "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
    "since": {"type": "string", "description": "Keep reports filed on or after this date (YYYYMMDD)"},
    "until": {"type": "string", "description": "Keep reports filed on or before this date (YYYYMMDD)"},
    "reporter": {"type": "string", "description": "Reporter name, case-insensitive substring match"},
    "max_rows": {
        "type": "integer",
        "description": "Max rows returned, newest first. Default 100, 0 = no cap. "
        "Named max_rows because --limit is a global CLI option and never reaches handlers.",
    },
}


@rpc_method(
    name="dart.large_holding_report",
    description=(
        "Get 5%-rule large holding reports (주식등의 대량보유상황보고) for one company: who crossed "
        "or moved a 5%+ stake, by how much, and why. Returns the full history, newest first."
    ),
    parameters={
        "type": "object",
        "properties": dict(_SHARE_DISCLOSURE_FILTERS),
        "required": ["corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_large_holding_report(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.share_disclosure_comprehensive.large_holding_report(params["corp_code"])
    return _collect_share_rows(result, params)


@rpc_method(
    name="dart.executive_ownership_report",
    description=(
        "Get executive and major-shareholder ownership reports (임원·주요주주 특정증권등 소유상황보고) "
        "for one company, including share-count and stake changes. Returns the full history, newest first."
    ),
    parameters={
        "type": "object",
        "properties": dict(_SHARE_DISCLOSURE_FILTERS),
        "required": ["corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_executive_ownership_report(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.share_disclosure_comprehensive.executive_major_shareholder_ownership_report(params["corp_code"])
    return _collect_share_rows(result, params)


_PERIODIC_REPORT_KEY = {
    "corp_code": {"type": "string", "description": "Corporate unique code (8 digits, from dart corp-code-lookup)"},
    "bsns_year": {"type": "string", "description": "Business year (4 digits, e.g. 2025)"},
    "reprt_code": {
        "type": "string",
        "enum": ["11013", "11012", "11014", "11011"],
        "description": "Report code (11013:Q1, 11012:H1, 11014:Q3, 11011:Annual). "
        "In quarterly reports income-statement rows carry that single quarter in thstrm_amount and "
        "the year-to-date sum in thstrm_add_amount (equal for Q1); annual reports and balance-sheet "
        "rows fill only thstrm_amount. Use the *_add_amount fields to compare a half-year with prior years.",
    },
}


@rpc_method(
    name="dart.financial_major_accounts",
    description=(
        "Get the major accounts (revenue, operating income, net income, total assets/equity, ...) "
        "of one company's periodic report (단일회사 주요계정). Cheapest way to read the latest "
        "reported results, including half-year and quarterly reports KIS financial commands do not expose."
    ),
    parameters={
        "type": "object",
        "properties": dict(_PERIODIC_REPORT_KEY),
        "required": ["corp_code", "bsns_year", "reprt_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_financial_major_accounts(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.periodic_report_financial_statement.get_single_company_major_accounts(
        corp_code=params["corp_code"],
        bsns_year=params["bsns_year"],
        reprt_code=params["reprt_code"],
    )
    return dump_model(_checked(result))


@rpc_method(
    name="dart.financial_full_statements",
    description=(
        "Get every line item of one company's financial statements (단일회사 전체 재무제표): "
        "balance sheet, income statement, comprehensive income, cash flow and equity changes, "
        "with XBRL account ids. Large; prefer financial-major-accounts unless a specific line is needed."
    ),
    parameters={
        "type": "object",
        "properties": {
            **_PERIODIC_REPORT_KEY,
            "fs_div": {
                "type": "string",
                "enum": ["CFS", "OFS"],
                "description": "Statement basis (CFS:consolidated, OFS:separate). Default CFS.",
            },
        },
        "required": ["corp_code", "bsns_year", "reprt_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_financial_full_statements(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.periodic_report_financial_statement.get_single_company_full_statements(
        corp_code=params["corp_code"],
        bsns_year=params["bsns_year"],
        reprt_code=params["reprt_code"],
        fs_div=params.get("fs_div", "CFS"),
    )
    return dump_model(_checked(result))


@rpc_method(
    name="dart.financial_major_indicators",
    description=(
        "Get one company's major financial indicators (단일회사 주요 재무지표) for one indicator "
        "class: profitability, stability, growth or activity ratios as reported in the periodic report."
    ),
    parameters={
        "type": "object",
        "properties": {
            **_PERIODIC_REPORT_KEY,
            "idx_cl_code": {
                "type": "string",
                "enum": ["M210000", "M220000", "M230000", "M240000"],
                "description": "Indicator class (M210000:profitability, M220000:stability, "
                "M230000:growth, M240000:activity)",
            },
        },
        "required": ["corp_code", "bsns_year", "reprt_code", "idx_cl_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_financial_major_indicators(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.periodic_report_financial_statement.get_single_company_major_indicators(
        corp_code=params["corp_code"],
        bsns_year=params["bsns_year"],
        reprt_code=params["reprt_code"],
        idx_cl_code=params["idx_cl_code"],
    )
    return dump_model(_checked(result))


_AS_FILED_STATEMENTS = ("BS", "IS", "CIS", "CF", "SCE")
_AS_FILED_DEFAULT_STATEMENTS = "BS,IS,CIS,CF"
_AS_FILED_STATEMENTS_PATTERN = "^(BS|IS|CIS|CF|SCE)(,(BS|IS|CIS|CF|SCE))*$"
_AS_FILED_BASES = (("CFS", "consolidated"), ("OFS", "separate"))
_AS_FILED_COLD_CACHE_HINT = (
    "Arelle downloads base taxonomies on a cold cache (~/Library/Caches/Arelle); offline with a cold "
    "cache the parse fails or yields an empty document. Check network access and retry."
)


def _as_filed_statements(params: dict) -> list[str]:
    """Requested statement types in canonical order. The schema pattern already rejected bad input."""
    tokens = params.get("statements", _AS_FILED_DEFAULT_STATEMENTS).split(",")
    return [code for code in _AS_FILED_STATEMENTS if code in tokens]


def _as_filed_period_key(item) -> tuple:
    """Newest period first, then dimensions: orders the facts of one presentation node."""
    period = item.period
    end = (period.end_date or period.instant) if period is not None else None
    start = period.start_date if period is not None else None
    return (
        end is None,
        -(end.toordinal() if end else 0),
        start is None,
        -(start.toordinal() if start else 0),
        sorted(item.dimensions.items()),
    )


def _iso(value: date | None) -> str | None:
    return value.isoformat() if value is not None else None


def _as_filed_rows(statement) -> list[dict]:
    """Rows of one parsed statement. ``value`` stays an exact ``str(Decimal)`` (never float).

    Line items come in presentation (depth-first) order, which is kept: ``order`` is only
    relative to siblings, so sorting on it would interleave different parents' children.
    Only the facts of one node, whose order Arelle does not fix, are sorted.
    """
    rows = []
    shown = [i for i in statement.line_items if not i.is_abstract]
    ordered = []
    for _, node_items in itertools.groupby(shown, key=lambda i: i.concept_qname):
        ordered.extend(sorted(node_items, key=_as_filed_period_key))
    for item in ordered:
        period = item.period
        value: Decimal | None = item.value
        rows.append(
            {
                "concept_qname": item.concept_qname,
                "concept": item.concept_local_name,
                "label_ko": item.label_ko,
                "label_en": item.label_en,
                "value": str(value) if value is not None else None,
                "unit": item.unit,
                "period_type": period.period_type.value if period is not None else None,
                "instant": _iso(period.instant) if period is not None else None,
                "start_date": _iso(period.start_date) if period is not None else None,
                "end_date": _iso(period.end_date) if period is not None else None,
                "dimensions": dict(item.dimensions),
                "depth": item.depth,
                "order": item.order,
            }
        )
    return rows


@rpc_method(
    name="dart.financial_as_filed",
    description=(
        "Get one periodic report's financial statements as first filed, parsed from the report's XBRL "
        "attachment by receipt number (rcept_no, from dart disclosure-search). The JSON APIs "
        "(financial-major-accounts / financial-full-statements) return only the latest amended values; "
        "this returns the values of the given filing, so an original and its amendment can be compared. "
        "Nothing is written to disk. The first call on a cold Arelle taxonomy cache downloads base "
        "taxonomies and can take ~1 minute (later calls ~1-5s). Rows include prior-period comparative "
        "columns (period fields are kept); only the current-period column is the as-filed value for this "
        "report, comparatives are restated values. Some filers have no IS: their income statement lives "
        "only under CIS (do not expect IS); some have no consolidated statements. Requested statements "
        "that the filing lacks are listed in `missing` as `<TYPE>/<basis>`, e.g. `IS/consolidated`."
    ),
    parameters={
        "type": "object",
        "properties": {
            "rcept_no": {
                "type": "string",
                "pattern": r"^\d{14}$",
                "description": "Receipt number of the periodic report (14 digits), original or amendment",
            },
            "reprt_code": {
                **_PERIODIC_REPORT_KEY["reprt_code"],
                "description": "Report code (11013:Q1, 11012:H1, 11014:Q3, 11011:Annual). DART ignores it "
                "for this endpoint, but the client requires it; the filing is identified by rcept_no.",
            },
            "corp_code": {
                "type": "string",
                "pattern": r"^\d{8}$",
                "description": "Corporate unique code (8 digits). Required safety check: DART returns another "
                "company's file for a wrong rcept_no, so the parsed entity must equal this value.",
            },
            "statements": {
                "type": "string",
                "pattern": _AS_FILED_STATEMENTS_PATTERN,
                "default": _AS_FILED_DEFAULT_STATEMENTS,
                "description": "Comma-separated subset of BS,IS,CIS,CF,SCE (balance sheet, income statement, "
                "comprehensive income, cash flow, equity changes). Default BS,IS,CIS,CF.",
            },
            "fs_div": {
                "type": "string",
                "enum": ["CFS", "OFS", "both"],
                "default": "both",
                "description": "Statement basis (CFS:consolidated, OFS:separate, both). Default both.",
            },
        },
        "required": ["rcept_no", "reprt_code", "corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_financial_as_filed(params: dict, session) -> dict:
    requested = _as_filed_statements(params)
    fs_div = params.get("fs_div", "both")
    bases = [name for code, name in _AS_FILED_BASES if fs_div in (code, "both")]
    rcept_no = params["rcept_no"]
    corp_code = params["corp_code"]

    # Heavy (Arelle): imported here so other commands do not pay for it at startup.
    from cluefin_xbrl import XbrlParseError, extract_financial_statements, parse_xbrl_directory

    dart = session.get_dart()
    with tempfile.TemporaryDirectory(prefix="cluefin-as-filed-") as tmp:
        dart.periodic_report_financial_statement.download_financial_statement_xbrl(
            rcept_no, params["reprt_code"], destination=tmp
        )
        try:
            # Arelle logs "[info] loaded …" to stdout by default; stdout is the JSON channel.
            with contextlib.redirect_stdout(sys.stderr):
                doc = parse_xbrl_directory(tmp, include_taxonomy=True)
            if doc.reporting_period_end is None or len(doc.facts) == 0:
                raise CliError(
                    "XBRL parsed to an empty document (no facts or no reporting period)",
                    exit_code=EXIT_BROKER,
                    error_type="ResponseParseError",
                    data={"rcept_no": rcept_no, "facts": len(doc.facts)},
                    hint=_AS_FILED_COLD_CACHE_HINT,
                )
            entity_id = (doc.entity_id or "").strip()
            if entity_id != corp_code:
                raise CliError(
                    "XBRL belongs to a different company than corp_code (wrong rcept_no?)",
                    exit_code=EXIT_BROKER,
                    error_type="ResponseParseError",
                    data={"rcept_no": rcept_no, "expected": corp_code, "actual": doc.entity_id},
                )
            parsed = extract_financial_statements(doc)
        except (XbrlParseError, ValueError) as exc:
            raise CliError(
                f"Failed to parse XBRL: {exc}",
                exit_code=EXIT_BROKER,
                error_type="ResponseParseError",
                data={"rcept_no": rcept_no, "exception": type(exc).__name__},
                hint=_AS_FILED_COLD_CACHE_HINT,
            ) from exc

        statements: dict[str, dict[str, list[dict]]] = {}
        missing: list[str] = []
        by_basis = {"consolidated": parsed.statements, "separate": parsed.separate_statements}
        for code in requested:
            for basis in bases:
                statement = by_basis[basis].get(code)
                if statement is None:
                    missing.append(f"{code}/{basis}")
                    continue
                statements.setdefault(code, {})[basis] = _as_filed_rows(statement)
        reporting_period_end = doc.reporting_period_end.isoformat()

    return {
        "rcept_no": rcept_no,
        "corp_code": corp_code,
        "entity_id": entity_id,
        "reporting_period_end": reporting_period_end,
        "statements": statements,
        "missing": missing,
    }


@rpc_method(
    name="dart.major_shareholder",
    description="Get major shareholder status from periodic report.",
    parameters={
        "type": "object",
        "properties": {
            "corp_code": {"type": "string", "description": "Corporate unique code (8 digits)"},
            "bsns_year": {"type": "string", "description": "Business year (4 digits, e.g. 2024)"},
            "reprt_code": {
                "type": "string",
                "enum": ["11013", "11012", "11014", "11011"],
                "description": "Report code (11013:Q1, 11012:H1, 11014:Q3, 11011:Annual)",
            },
        },
        "required": ["corp_code", "bsns_year", "reprt_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_major_shareholder(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.periodic_report_key_information.get_major_shareholder_status(
        corp_code=params["corp_code"],
        bsns_year=params["bsns_year"],
        reprt_code=params["reprt_code"],
    )
    return dump_model(_checked(result))


@rpc_method(
    name="dart.share_count",
    description=(
        "Get the total number of shares (주식의 총수 현황) of one company's periodic report: issued, "
        "treasury and outstanding share counts split by `se` (common / preferred / total). "
        'Numbers arrive as comma strings such as "5,969,782,550" and missing values as "-". '
        "Data is available from bsns_year 2015. Each row's `rcept_no` is the latest amended report, not the "
        "original filing, so this cannot give the share count as first reported."
    ),
    parameters={
        "type": "object",
        "properties": dict(_PERIODIC_REPORT_KEY),
        "required": ["corp_code", "bsns_year", "reprt_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_share_count(params: dict, session) -> dict:
    dart = session.get_dart()
    result = dart.periodic_report_key_information.get_total_number_of_shares(
        corp_code=params["corp_code"],
        bsns_year=params["bsns_year"],
        reprt_code=params["reprt_code"],
    )
    return dump_model(_checked(result))


# ---------------------------------------------------------------------------
# Filing text (cluefin-dart-notes): download the original XML, parse, return blocks
# ---------------------------------------------------------------------------

# cluefin-dart-notes supports periodic and audit reports filed 2017 or later; older filings use
# another document layout. The year is the first four digits of the receipt number.
_DOCUMENT_MIN_YEAR = 2017

_DOCUMENT_PARAMS = {
    "rcept_no": {
        "type": "string",
        "pattern": r"^\d{14}$",
        "description": "Receipt number (14 digits, from dart disclosure-search) of a periodic report "
        "(사업·반기·분기보고서) or an audit report (감사보고서) filed 2017 or later",
    },
    "corp_code": {
        "type": "string",
        "pattern": r"^\d{8}$",
        "description": "Corporate unique code (8 digits). Required safety check: DART returns another "
        "company's file for a wrong rcept_no, so every parsed document must belong to this company.",
    },
}


def _check_document_year(rcept_no: str) -> None:
    if int(rcept_no[:4]) < _DOCUMENT_MIN_YEAR:
        raise CliError(
            f"Filings before {_DOCUMENT_MIN_YEAR} are not supported",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"rcept_no": rcept_no, "min_year": _DOCUMENT_MIN_YEAR},
            hint=f"Filings before {_DOCUMENT_MIN_YEAR} use an older document layout that the parser does not "
            "read. Pick a later rcept_no from dart disclosure-search.",
        )


def _load_filing(session, rcept_no: str, corp_code: str) -> list[tuple[str, Any]]:
    """Download every XML of one filing into a temp directory and parse it: ``[(file name, DartDocument)]``.

    The main document comes first, attached audit reports follow by name. A ZIP can hold only an
    audit report. Parsing reads each file into memory, so the documents (and their lazily
    computed blocks) outlive the temp directory. The directory is listed rather than trusting the
    client's return value.
    """
    # Imported here so other commands do not pay for the parser at startup.
    from cluefin_dart_notes import DartXmlRepairError, load_document

    dart = session.get_dart()
    with tempfile.TemporaryDirectory(prefix="cluefin-dart-document-") as tmp:
        dart.public_disclosure.disclosure_document_files(rcept_no, destination=tmp)
        main_name = f"{rcept_no}.xml"
        paths = sorted(Path(tmp).glob("*.xml"), key=lambda p: (p.name != main_name, p.name))
        if not paths:
            raise CliError(
                "DART returned no XML document for this rcept_no",
                exit_code=EXIT_BROKER,
                error_type="ResponseParseError",
                data={"rcept_no": rcept_no},
            )
        try:
            documents = [(path.name, load_document(path)) for path in paths]
        except DartXmlRepairError as exc:
            raise CliError(
                f"Failed to parse the filing XML: {exc}",
                exit_code=EXIT_BROKER,
                error_type="ResponseParseError",
                data={"rcept_no": rcept_no, "exception": type(exc).__name__},
            ) from exc

    actual = sorted({document.corp_code or "" for _, document in documents})
    if actual != [corp_code]:
        raise CliError(
            "The filing belongs to a different company than corp_code (wrong rcept_no?)",
            exit_code=EXIT_BROKER,
            error_type="ResponseParseError",
            data={"rcept_no": rcept_no, "expected": corp_code, "actual": actual},
        )
    return documents


def _block_chars(block) -> int:
    """Text size of one block; a table counts every grid cell (merged cells repeat)."""
    from cluefin_dart_notes import Table

    if isinstance(block, Table):
        return sum(len(text) for row in block.to_rows() for text in row)
    return len(block.text)


def _section_size(section, cache: dict) -> tuple[int, int]:
    """(chars, tables) of a section with its subsections, counting subsection titles as text.

    This is what ``document-section`` returns with ``include_children`` (the default), so the
    outline tells the caller how large a request will be before making it.
    """
    from cluefin_dart_notes import Table

    key = id(section)
    if key not in cache:
        chars = sum(_block_chars(block) for block in section.blocks)
        tables = sum(1 for block in section.blocks if isinstance(block, Table))
        for child in section.children:
            child_chars, child_tables = _section_size(child, cache)
            chars += len(child.title) + child_chars
            tables += child_tables
        cache[key] = (chars, tables)
    return cache[key]


def _repair_summary(document) -> dict:
    repair = document.repair
    if repair is None:
        return {"used_fallback": False, "rules": {}, "warnings": []}
    return {
        "used_fallback": repair.used_fallback,
        "rules": {report.rule: report.count for report in repair.reports},
        "warnings": list(repair.warnings),
    }


def _section_indexes(documents: list[tuple[str, Any]]) -> dict[int, int]:
    """``id(section)`` → number across the whole filing, in document order (main document first).

    ``document-outline`` shows these numbers and ``document-section --index`` takes them back.
    """
    sections = (section for _, document in documents for section in document.iter_sections())
    return {id(section): number for number, section in enumerate(sections)}


def _document_header(file: str, document) -> dict:
    return {
        "file": file,
        "document_name": document.document_name,
        "document_code": document.document_code,
        "company_name": document.company_name,
        "is_periodic_report": document.is_periodic_report,
        "is_audit_report": document.is_audit_report,
    }


@rpc_method(
    name="dart.document_outline",
    description=(
        "List the sections of one filing's original document (공시 원문): the periodic report body and its "
        "attached audit reports (a ZIP can also hold only an audit report). Use it before dart document-section "
        "or dart financial-notes to see what the filing contains and how large each part is. Sections are "
        "numbered by `index` across the whole filing in document order (main document first). `chars` and "
        "`tables` include subsections. `assoc_code` meanings differ by document kind: in a periodic report "
        "D-0-2-0-0 is II. 사업의 내용, in an audit report it is 외부감사 실시내용. Supported: periodic and audit "
        "reports filed 2017 or later. Nothing is written to disk."
    ),
    parameters={
        "type": "object",
        "properties": dict(_DOCUMENT_PARAMS),
        "required": ["rcept_no", "corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_document_outline(params: dict, session) -> dict:
    rcept_no = params["rcept_no"]
    corp_code = params["corp_code"]
    _check_document_year(rcept_no)
    documents = _load_filing(session, rcept_no, corp_code)

    indexes = _section_indexes(documents)
    payload = []
    for file, document in documents:
        cache: dict = {}
        sections = []
        for section in document.iter_sections():
            chars, tables = _section_size(section, cache)
            sections.append(
                {
                    "index": indexes[id(section)],
                    "level": section.level,
                    "title": section.title,
                    "assoc_code": section.assoc_code,
                    "is_correction": section.is_correction,
                    "chars": chars,
                    "tables": tables,
                }
            )
        payload.append(
            {
                **_document_header(file, document),
                "summary": dict(document.summary),
                "sections": sections,
                "repair": _repair_summary(document),
            }
        )
    return {"rcept_no": rcept_no, "corp_code": corp_code, "documents": payload}


_DEFAULT_MAX_CHARS = 20000
_SECTION_SELECTORS = ("section", "assoc_code", "title", "index")


def _max_chars(params: dict) -> int:
    """Text cap from params; 0 means no cap. The schema already rejected negatives."""
    return int(params.get("max_chars", _DEFAULT_MAX_CHARS))


def _block_payload(block) -> dict:
    """One block as JSON. Amounts stay strings as filed; `unit` is reported, never applied."""
    from cluefin_dart_notes import Heading, Table

    if isinstance(block, Table):
        return {"type": "table", "caption": block.caption, "unit": block.unit, "rows": block.to_rows()}
    kind = "heading" if isinstance(block, Heading) else "paragraph"
    return {"type": kind, "text": block.text}


def _section_blocks(section, *, include_children: bool) -> list[tuple[int, dict]]:
    """``(chars, block)`` of a section in document order.

    ``Section.blocks`` leaves subsections out, so with ``include_children`` each subsection is
    announced by a ``section`` marker (its title counts as text, as in the outline) and followed
    by its own blocks.
    """
    blocks = [(_block_chars(block), _block_payload(block)) for block in section.blocks]
    if include_children:
        for child in section.children:
            marker = {"type": "section", "level": child.level, "title": child.title, "assoc_code": child.assoc_code}
            blocks.append((len(child.title), marker))
            blocks.extend(_section_blocks(child, include_children=True))
    return blocks


class _CharBudget:
    """Cuts a response at block boundaries once ``max_chars`` would be exceeded (0 = no cap).

    The first block is always kept, even when it alone is over the cap, so a section that opens
    with a large table never comes back empty. After the first cut every later block is dropped,
    so what is returned is a prefix of the selection.
    """

    def __init__(self, max_chars: int) -> None:
        self.max_chars = max_chars
        self.total = 0
        self.returned = 0
        self.cut = False

    def take(self, sized_blocks: list[tuple[int, dict]]) -> list[dict]:
        kept = []
        for chars, block in sized_blocks:
            self.total += chars
            over = self.max_chars and self.returned + chars > self.max_chars and self.returned > 0
            if self.cut or over:
                self.cut = True
                continue
            self.returned += chars
            kept.append(block)
        return kept

    def summary(self) -> dict:
        return {"total_chars": self.total, "returned_chars": self.returned, "truncated": self.cut}


def _selector(params: dict) -> tuple[str, Any]:
    given = [name for name in _SECTION_SELECTORS if name in params]
    if len(given) != 1:
        raise CliError(
            "Give exactly one section selector",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"selectors": list(_SECTION_SELECTORS), "given": given},
            hint="Pass one of --section, --assoc-code, --title or --index. Run dart document-outline first to "
            "see the titles, codes and indexes of this filing.",
        )
    return given[0], params[given[0]]


def _named_sections(documents: list[tuple[str, Any]], name: str) -> list:
    from cluefin_dart_notes import business_description, business_overviews, company_overview

    periodic = [document for _, document in documents if document.is_periodic_report]
    if not periodic:
        raise CliError(
            f"--section {name} needs a periodic report, and this filing holds only audit reports",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"section": name, "documents": [document.document_code for _, document in documents]},
            hint="An audit report has no business description or company overview. Use dart financial-notes "
            "for its notes, or --assoc-code/--title/--index from dart document-outline.",
        )
    if name == "business-overview":
        return [section for document in periodic for section in business_overviews(document)]
    find = business_description if name == "business" else company_overview
    return [section for section in map(find, periodic) if section is not None]


def _matching_sections(documents: list[tuple[str, Any]], kind: str, value, indexes: dict[int, int]) -> list:
    from cluefin_dart_notes import find_sections

    if kind == "section":
        return _named_sections(documents, value)
    if kind == "index":
        return [s for _, document in documents for s in document.iter_sections() if indexes[id(s)] == value]
    return [section for _, document in documents for section in find_sections(document, **{kind: value})]


def _outermost(sections: list) -> list:
    """Drop sections nested in another selected one; their content already comes with the parent."""
    nested = {id(child) for section in sections for child in itertools.islice(section.iter(), 1, None)}
    return [section for section in sections if id(section) not in nested]


@rpc_method(
    name="dart.document_section",
    description=(
        "Read sections of one filing's original document (공시 원문) as blocks: paragraph, heading, table "
        "(caption, unit, rows of cell strings) and, with include_children, a `section` marker before each "
        "subsection. Choose exactly one selector: `section` (business = II. 사업의 내용, business-overview = "
        "사업의 개요 for every industry template, company-overview = I. 회사의 개요; periodic reports only), "
        "`assoc_code` (`*` wildcard allowed, e.g. L-0-2-*), `title` (leading number and spaces ignored) or "
        "`index` (from dart document-outline). Every matching section is returned with its file and index. "
        "Output stops at a block boundary after max_chars characters of text (default 20000, 0 = no cap; the "
        "first block is always returned) and reports total_chars / returned_chars / truncated. Amounts are "
        "returned as filed (strings, unit not applied). Run dart document-outline first: a large-cap "
        "business section is ~40k characters, a single subsection usually fits. Nothing is written to disk."
    ),
    parameters={
        "type": "object",
        "properties": {
            **_DOCUMENT_PARAMS,
            "section": {
                "type": "string",
                "enum": ["business", "business-overview", "company-overview"],
                "description": "Named section of a periodic report (II. 사업의 내용, 사업의 개요, I. 회사의 개요)",
            },
            "assoc_code": {
                "type": "string",
                "description": "Section code (AASSOCNOTE) from the outline, `*` wildcard allowed (`?` is not). "
                "Codes differ by document kind: D-0-2-0-0 is II. 사업의 내용 in a periodic report and "
                "외부감사 실시내용 in an audit report.",
            },
            "title": {
                "type": "string",
                "description": "Section title; the leading number and all spaces are ignored "
                "(`연결재무제표 주석` matches `3. 연결재무제표 주석`)",
            },
            "index": {"type": "integer", "minimum": 0, "description": "Section index from dart document-outline"},
            "include_children": {
                "type": "boolean",
                "default": True,
                "description": "Include subsections (default true). False returns the section's own text only.",
            },
            "max_chars": {
                "type": "integer",
                "minimum": 0,
                "default": _DEFAULT_MAX_CHARS,
                "description": "Max characters of text returned, cut at a block boundary. Default 20000, "
                "0 = no cap. Named max_chars because --limit is a global CLI option and never reaches handlers.",
            },
        },
        "required": ["rcept_no", "corp_code"],
    },
    returns={"type": "object"},
    category="dart",
    broker="dart",
)
def handle_document_section(params: dict, session) -> dict:
    rcept_no = params["rcept_no"]
    corp_code = params["corp_code"]
    kind, value = _selector(params)
    _check_document_year(rcept_no)
    documents = _load_filing(session, rcept_no, corp_code)

    indexes = _section_indexes(documents)
    files = {id(section): file for file, document in documents for section in document.iter_sections()}
    include_children = params.get("include_children", True)
    matched = _matching_sections(documents, kind, value, indexes)
    selected = _outermost(matched) if include_children else matched
    budget = _CharBudget(_max_chars(params))
    sections = [
        {
            "file": files[id(section)],
            "index": indexes[id(section)],
            "level": section.level,
            "title": section.title,
            "assoc_code": section.assoc_code,
            "blocks": budget.take(_section_blocks(section, include_children=include_children)),
        }
        for section in selected
    ]
    result = {
        "rcept_no": rcept_no,
        "corp_code": corp_code,
        "selector": {kind: value},
        "sections": sections,
        **budget.summary(),
    }
    if not sections:
        result["hint"] = "No section matched. Run dart document-outline to see this filing's titles, codes and indexes."
    elif budget.cut:
        result["hint"] = (
            "Output was cut at max_chars. Raise --max-chars (0 = no cap) or select a subsection by --index "
            "or --assoc-code from dart document-outline."
        )
    return result


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_disclosure_search,
    handle_company_overview,
    handle_corp_code_lookup,
    handle_large_holding_report,
    handle_executive_ownership_report,
    handle_major_shareholder,
    handle_share_count,
    handle_financial_major_accounts,
    handle_financial_full_statements,
    handle_financial_major_indicators,
    handle_financial_as_filed,
    handle_document_outline,
    handle_document_section,
]


def register_dart_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
