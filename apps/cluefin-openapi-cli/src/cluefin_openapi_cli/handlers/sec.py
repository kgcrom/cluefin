"""SEC EDGAR handlers (US filings: 10-K, 10-Q, 8-K)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_USAGE, CliError
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
# Filing text (cluefin-sec-notes): download one document, parse, return text
# ---------------------------------------------------------------------------

_ACCESSION_PARAM = {
    "type": "string",
    "pattern": r"^\d{10}-?\d{2}-?\d{6}$",
    "description": "Accession number from sec filings, e.g. 0000320193-23-000106 (dashes optional)",
}
_DEFAULT_MAX_CHARS = 40000
_MAX_CHARS_PARAM = {
    "type": "integer",
    "minimum": 0,
    "default": _DEFAULT_MAX_CHARS,
    "description": "Max characters of text returned per item, cut at a blank line (else a line end). Default "
    "40000, 0 = no cap. Named max_chars because --limit is a global CLI option and never reaches handlers.",
}
_OFFSET_CHARS_PARAM = {
    "type": "integer",
    "minimum": 0,
    "default": 0,
    "description": "Start reading at this character of the text; pass the previous response's next_offset to "
    "continue a truncated text. Default 0.",
}
_INCLUDE_TABLES_PARAM = {
    "type": "boolean",
    "default": False,
    "description": "Also return each table that starts inside the returned text as a column-aligned grid of cell "
    "strings (unit not applied). Tables are always in `text` too, one row per line with tab-separated cells. "
    "Default false.",
}
_HTML_SUFFIXES = (".htm", ".html")


def _checked_detail(sec, cik: str, accession_number: str):
    """The filing's detail page, refused unless ``cik`` is one of its parties.

    SEC serves a filing folder under any CIK path (another company's CIK with a valid accession
    number is a 200), so the path proves nothing; the page's filer/issuer list does.
    """
    detail = sec.archives.filing_detail(cik, accession_number)
    parties = detail.parties or []
    if int(cik) not in {party.cik for party in parties}:
        raise CliError(
            "The filing does not belong to this cik (wrong accession_number?)",
            exit_code=EXIT_BROKER,
            error_type="ResponseParseError",
            data={"cik": int(cik), "accession_number": accession_number, "parties": [p.cik for p in parties]},
            hint="Take accession_number from `sec filings --cik <cik>`.",
        )
    return detail


def _filing_header(detail, cik: str) -> dict:
    company = next((party.name for party in detail.parties if party.cik == int(cik)), None)
    return {
        "cik": int(cik),
        "company": company,
        "accession_number": detail.accession_number,
        "form": detail.form,
        "filing_date": detail.filing_date.isoformat() if detail.filing_date else None,
        "period_of_report": detail.period_of_report.isoformat() if detail.period_of_report else None,
    }


def _load_document(sec, cik: str, accession_number: str, document, *, form: str | None):
    """Download one HTML document of the filing into a temp directory and parse it with cluefin-sec-notes.

    The parsed document holds everything in memory, so the directory is gone before the caller reads it.
    """
    # Imported here so other commands do not pay for the parser at startup.
    from cluefin_sec_notes import load_filing

    if not document.name.lower().endswith(_HTML_SUFFIXES):
        raise CliError(
            f"Only HTML documents are parsed; this one is {document.name}",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"document": document.name, "type": document.type},
            hint="Filings before about 2001 are plain text and are out of scope.",
        )
    with tempfile.TemporaryDirectory(prefix="cluefin-sec-filing-") as tmp:
        sec.archives.download_filing_document(cik, accession_number, document.name, destination=tmp)
        path = Path(tmp) / document.name
        if not path.is_file():
            raise CliError(
                "SEC returned no document",
                exit_code=EXIT_BROKER,
                error_type="ResponseParseError",
                data={"accession_number": accession_number, "document": document.name},
            )
        return load_filing(path, form=form)


def _window(text: str, offset: int, max_chars: int) -> tuple[int, int]:
    """``[offset, end)`` of at most ``max_chars`` (0 = rest), ending at a blank line, else a line end.

    A single paragraph or table row longer than the cap is cut where the cap falls.
    """
    if max_chars == 0 or offset + max_chars >= len(text):
        return offset, len(text)
    end = offset + max_chars
    for separator in ("\n\n", "\n"):
        cut = text.rfind(separator, offset + 1, end)
        if cut > offset:
            return offset, cut
    return offset, end


def _next_offset(text: str, end: int) -> int:
    """Where the next window starts: past the line breaks that separated the two."""
    while end < len(text) and text[end] == "\n":
        end += 1
    return end


def _table_grids(blocks, start: int, end: int) -> list[list[list[str]]]:
    """Grids of the tables whose text starts in ``[start, end)`` of the blocks' joined text.

    Offsets follow ``SecDocument.text``: non-empty block texts joined by a blank line.
    """
    from cluefin_sec_notes import Table, block_text

    grids = []
    position = None
    for block in blocks:
        text = block_text(block)
        if not text:
            continue
        position = 0 if position is None else position + 2
        if isinstance(block, Table) and start <= position < end:
            grids.append([list(row) for row in block.grid()])
        position += len(text)
    return grids


def _text_page(text: str, blocks, params: dict) -> dict:
    """The requested window of ``text`` with the truncation fields every text command returns."""
    offset = min(int(params.get("offset_chars", 0)), len(text))
    start, end = _window(text, offset, int(params.get("max_chars", _DEFAULT_MAX_CHARS)))
    page = {
        "chars_total": len(text),
        "offset_chars": start,
        "chars_returned": end - start,
        "truncated": end < len(text),
        "next_offset": _next_offset(text, end) if end < len(text) else None,
        "text": text[start:end],
    }
    if params.get("include_tables", False):
        page["tables"] = _table_grids(blocks, start, end)
    return page


def _item_key(key, catalog) -> str:
    """``1A``/``2.02``, or ``II:1A`` where item numbers restart per part (10-Q)."""
    return f"{key.part}:{key.number}" if catalog.part_scoped else key.number


def _requested_keys(params: dict) -> list[tuple[str | None, str]]:
    """``"1A,II:1A"`` → ``[(None, "1A"), ("II", "1A")]``."""
    keys = []
    for token in _split(params.get("items") or ""):
        part, _, number = token.rpartition(":")
        keys.append((part or None, number))
    return keys


def _key_matches(key, part: str | None, number: str) -> bool:
    return key.number == number and (part is None or key.part == part)


def _findings(findings) -> list[dict]:
    return [{"code": finding.code, "message": finding.message} for finding in findings]


def _item_summary(item, catalog) -> dict:
    from cluefin_sec_notes import UNCERTAIN_CODES

    return {
        "key": _item_key(item.key, catalog),
        "part": item.key.part,
        "number": item.key.number,
        "title": item.title,
        "heading": item.heading,
        "method": item.method,
        "confidence": item.confidence,
        "uncertain": any(finding.code in UNCERTAIN_CODES for finding in item.warnings),
        "warnings": _findings(item.warnings),
        "incorporated_by_reference": item.incorporated_by_reference,
        "shared_with": [_item_key(key, catalog) for key in item.shared_with],
    }


def _absent_item(result, catalog, part: str | None, number: str) -> dict:
    """Why a requested item has no text: the filing omitted it, detection missed it, or it is no such item."""
    from cluefin_sec_notes import MISSING_ITEM

    entry: dict = {"key": f"{part}:{number}" if part else number, "text": None}
    missed = [f for f in result.warnings if f.code == MISSING_ITEM and f.key and _key_matches(f.key, part, number)]
    if missed:
        return {**entry, "status": "missing", "warnings": _findings(missed)}
    if any(_key_matches(key, part, number) for key in result.omitted):
        return {**entry, "status": "omitted"}
    spec = catalog.resolve(part, number)
    return {**entry, "status": "not_in_filing" if spec else "not_in_catalog"}


def _check_items_request(params: dict) -> list[tuple[str | None, str]]:
    keys = _requested_keys(params)
    if int(params.get("offset_chars", 0)) and len(keys) != 1:
        raise CliError(
            "offset_chars needs exactly one item",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"items": params.get("items")},
            hint="Continue one truncated item at a time: --items <key> --offset-chars <next_offset>.",
        )
    return keys


def _extractable_form(detail):
    from cluefin_sec_notes import catalog_for

    catalog = catalog_for(detail.form)
    if catalog is None:
        raise CliError(
            f"Item extraction does not support form {detail.form}",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"form": detail.form, "supported": ["10-K", "10-Q", "8-K"]},
            hint="Items are read from 10-K, 10-Q and 8-K (and their amendments). 20-F/40-F/6-K (foreign private "
            "issuers, most Korean ADRs) are out of scope. For an 8-K exhibit such as the earnings release use "
            "sec filing-exhibit.",
        )
    return catalog


def _main_document(detail):
    document = next((doc for doc in detail.documents if doc.sequence == 1 and not doc.data_file), None)
    if document is None:
        raise CliError(
            "The filing lists no main document",
            exit_code=EXIT_BROKER,
            error_type="ResponseParseError",
            data={"accession_number": detail.accession_number},
        )
    return document


@rpc_method(
    name="sec.filing_items",
    description=(
        "Read Items of a 10-K, 10-Q or 8-K (and amendments) as text, e.g. 10-K 1A risk factors, 7 MD&A, 1 business "
        "(customers, suppliers); 10-Q II:1A and I:2 (MD&A); 8-K 2.02. Without `items` it returns the table of "
        "contents only: per Item key, title, heading, detection method and confidence, size in chars and tables, "
        "warnings and `uncertain` (the boundary may be wrong: read the warnings before trusting the text). With "
        "`items` (comma-separated; 10-Q keys are PART:NUMBER like II:1A, a bare number matches every part) it "
        "returns each Item's text, cut at max_chars (default 40000) with chars_total / truncated / next_offset to "
        "continue. Omitted, missing and unknown Items come back with `status` and no text instead of an error. "
        "Large 10-K Items run 20k-120k characters (1A, 7), bank 10-Ks far more. The 8-K body rarely holds the "
        "numbers: the earnings release is exhibit EX-99.1 (sec filing-exhibit). Nothing is written to disk."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cik": _CIK_PARAM,
            "accession_number": _ACCESSION_PARAM,
            "items": {
                "type": "string",
                "pattern": r"^[0-9A-Za-z.:,]+$",
                "description": "Comma-separated Item keys, e.g. 1A,7 (10-K), II:1A,I:2 (10-Q), 2.02 (8-K). "
                "Omit for the table of contents.",
            },
            "max_chars": _MAX_CHARS_PARAM,
            "offset_chars": {
                **_OFFSET_CHARS_PARAM,
                "description": _OFFSET_CHARS_PARAM["description"] + " Needs exactly one item.",
            },
            "include_tables": _INCLUDE_TABLES_PARAM,
        },
        "required": ["cik", "accession_number"],
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_filing_items(params: dict, session) -> dict:
    from cluefin_sec_notes import extract_items

    cik, accession_number = params["cik"], params["accession_number"]
    requested = _check_items_request(params)
    sec = session.get_sec()
    detail = _checked_detail(sec, cik, accession_number)
    catalog = _extractable_form(detail)
    document = _main_document(detail)
    parsed = _load_document(sec, cik, accession_number, document, form=detail.form)
    try:
        result = extract_items(parsed)
    except ValueError as exc:
        raise CliError(
            f"Item extraction failed: {exc}",
            exit_code=EXIT_BROKER,
            error_type="ResponseParseError",
            data={"accession_number": accession_number, "form": detail.form},
        ) from exc

    payload = {**_filing_header(detail, cik), "document": document.name, "catalog": catalog.name}
    if not requested:
        payload["items"] = [
            {**_item_summary(item, catalog), "chars": len(item.text), "tables": len(item.tables)} for item in result
        ]
        payload["missing"] = [_item_key(key, catalog) for key in result.missing if key not in result.omitted]
        payload["omitted"] = [_item_key(key, catalog) for key in result.omitted]
        payload["findings"] = [
            {"code": f.code, "severity": f.severity, "message": f.message} for f in result.findings if f.key is None
        ]
        return payload

    items = []
    for part, number in requested:
        found = [item for item in result if _key_matches(item.key, part, number)]
        if not found:
            items.append(_absent_item(result, catalog, part, number))
        for item in found:
            page = _text_page(item.text, item.blocks, params)
            items.append({**_item_summary(item, catalog), "status": "found", **page})
    payload["items"] = items
    truncated = [item["key"] for item in items if item.get("truncated")]
    if truncated:
        payload["hint"] = (
            f"Text was cut at max_chars for {', '.join(truncated)}. Continue with --items <key> --offset-chars "
            "<next_offset>, or raise --max-chars (0 = no cap)."
        )
    return payload


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_company_lookup,
    handle_filings,
    handle_filing_items,
]


def register_sec_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
