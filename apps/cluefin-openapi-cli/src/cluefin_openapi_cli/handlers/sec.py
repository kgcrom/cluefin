"""SEC EDGAR handlers (US filings: 10-K, 10-Q, 8-K)."""

from __future__ import annotations

from cluefin_openapi_cli.handlers._base import DispatcherProtocol, dump_model, rpc_method

_CIK_PARAM = {
    "type": "string",
    "pattern": r"^\d{1,10}$",
    "description": "SEC Central Index Key, digits only (leading zeros optional). Get it from sec company-lookup.",
}

_DEFAULT_LOOKUP_ROWS = 20


def _cap(rows: list, params: dict, default: int) -> dict:
    """Cap rows like dart corp-code-lookup: ``total``/``returned``/``truncated`` + ``data``; 0 = no cap."""
    max_rows = int(params.get("max_rows", default))
    page = rows if max_rows == 0 else rows[:max_rows]
    return {"total": len(rows), "returned": len(page), "truncated": len(page) < len(rows), "data": page}


def _ticker_key(value: str) -> str:
    """SEC writes class shares with a hyphen (BRK-B); accept BRK.B and any case."""
    return value.strip().upper().replace(".", "-")


@rpc_method(
    name="sec.company_lookup",
    description=(
        "Resolve a US-listed company to its SEC CIK (Central Index Key), the id every other sec command takes. "
        "Filter by exact ticker (BRK.B or BRK-B, any case), name substring, or cik. The full SEC list (~10k rows) "
        "is downloaded on every call and filtered locally; output is capped at max_rows (default 20). Rows: cik, "
        "name, ticker, exchange. A company with several share classes has one row per ticker."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker": {"type": "string", "description": "Exact ticker, e.g. MU, AMAT, BRK.B"},
            "name": {"type": "string", "description": "Company name, case-insensitive substring match"},
            "cik": _CIK_PARAM,
            "max_rows": {
                "type": "integer",
                "minimum": 0,
                "default": _DEFAULT_LOOKUP_ROWS,
                "description": "Max rows returned. Default 20, 0 = no cap. "
                "Named max_rows because --limit is a global CLI option and never reaches handlers.",
            },
        },
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_company_lookup(params: dict, session) -> dict:
    sec = session.get_sec()
    rows = sec.reference.company_tickers_exchange()
    ticker = _ticker_key(params.get("ticker") or "")
    name = (params.get("name") or "").strip().lower()
    cik = int(params["cik"]) if params.get("cik") else None
    matched = [
        dump_model(row)
        for row in rows
        if (not ticker or _ticker_key(row.ticker) == ticker)
        and (not name or name in row.name.lower())
        and (cik is None or row.cik == cik)
    ]
    return _cap(matched, params, _DEFAULT_LOOKUP_ROWS)


_DEFAULT_FORMS = "10-K,10-Q,8-K"
_DEFAULT_FILING_ROWS = 20


def _split(value: str) -> list[str]:
    return [part.strip().upper() for part in value.split(",") if part.strip()]


def _filing_row(entry) -> dict:
    return {
        "accession_number": entry.accession_number,
        "form": entry.form,
        "filing_date": entry.filing_date.isoformat(),
        "report_date": entry.report_date.isoformat() if entry.report_date else None,
        "items": _split(entry.items or ""),
        "primary_document": entry.primary_document,
        "size": entry.size,
    }


def _wanted_forms(params: dict) -> set[str]:
    forms = set(_split(params.get("forms") or _DEFAULT_FORMS))
    if params.get("include_amendments", True):
        forms |= {f"{form}/A" for form in forms}
    return forms


@rpc_method(
    name="sec.filings",
    description=(
        "List a company's recent SEC filings, newest first: accession_number (input to sec filing-items and sec "
        "filing-exhibit), form, filing_date, report_date, 8-K item numbers (2.02 results, 1.01 material agreement, "
        "2.05/2.06 restructuring/impairment, 5.02 officers), primary_document, size. Also returns the company's "
        "name, tickers, SIC industry and fiscal year end. Covers SEC's recent list (at least one year or the last "
        "1,000 filings). Filter by forms (default 10-K,10-Q,8-K; amendments like 10-K/A included unless "
        "include_amendments is false) and, for 8-K, by item numbers. Foreign private issuers (most Korean ADRs) "
        "file 20-F/6-K instead, which sec filing-items does not read."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cik": _CIK_PARAM,
            "forms": {
                "type": "string",
                "default": _DEFAULT_FORMS,
                "description": "Comma-separated forms to keep, e.g. 10-K or 8-K or 4,13F-HR. Default 10-K,10-Q,8-K.",
            },
            "include_amendments": {
                "type": "boolean",
                "default": True,
                "description": "Also keep amendments (10-K/A ...) of the given forms. Default true.",
            },
            "items": {
                "type": "string",
                "description": "8-K only: keep filings reporting any of these comma-separated items, e.g. 2.02. "
                "Filings without item numbers are dropped when this is given.",
            },
            "max_rows": {
                "type": "integer",
                "minimum": 0,
                "default": _DEFAULT_FILING_ROWS,
                "description": "Max rows returned. Default 20, 0 = no cap.",
            },
        },
        "required": ["cik"],
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_filings(params: dict, session) -> dict:
    sec = session.get_sec()
    company = sec.submissions.submissions(params["cik"])
    forms = _wanted_forms(params)
    items = set(_split(params.get("items") or ""))
    entries = company.filings or []
    rows = [
        _filing_row(entry)
        for entry in entries
        if entry.form.upper() in forms and (not items or items & set(_split(entry.items or "")))
    ]
    result = {
        "cik": int(company.cik) if company.cik else None,
        "name": company.name,
        "tickers": company.tickers,
        "exchanges": company.exchanges,
        "sic_description": company.sic_description,
        "fiscal_year_end": company.fiscal_year_end,
        "forms": sorted(forms),
        **_cap(rows, params, _DEFAULT_FILING_ROWS),
    }
    if not rows:
        filed = sorted({entry.form for entry in entries})
        result["hint"] = (
            f"No matching filing among the recent ones. Forms this company filed recently: {', '.join(filed) or 'none'}."
            " 20-F/6-K mean a foreign private issuer, whose filings sec filing-items does not read."
        )
    return result


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_company_lookup,
    handle_filings,
]


def register_sec_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
