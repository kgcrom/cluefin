"""DART disclosure handlers."""

from __future__ import annotations

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
    return dump_model(result)


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
    return dump_model(result)


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
    items = getattr(getattr(result, "result", None), "list", None) or []
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
    rows = getattr(getattr(result, "result", None), "list", None) or []
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
    return dump_model(result)


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
    return dump_model(result)


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
    return dump_model(result)


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
    return dump_model(result)


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
    handle_financial_major_accounts,
    handle_financial_full_statements,
    handle_financial_major_indicators,
]


def register_dart_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
