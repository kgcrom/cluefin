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


def _blocks_in_window(blocks, start: int, end: int):
    """Blocks whose text starts in ``[start, end)`` of the blocks' joined text.

    Offsets follow ``SecDocument.text``: non-empty block texts joined by a blank line.
    """
    from cluefin_sec_notes import block_text

    position = None
    for block in blocks:
        text = block_text(block)
        if not text:
            continue
        position = 0 if position is None else position + 2
        if start <= position < end:
            yield block
        position += len(text)


def _table_grids(blocks, start: int, end: int) -> list[list[list[str]]]:
    """Grids of the tables whose text starts in ``[start, end)`` of the blocks' joined text."""
    from cluefin_sec_notes import Table

    return [
        [list(row) for row in block.grid()]
        for block in _blocks_in_window(blocks, start, end)
        if isinstance(block, Table)
    ]


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
# Notes to the financial statements (cluefin-sec-notes split_notes)
# ---------------------------------------------------------------------------

# The financial statements Item per form: 10-K Item 8, 10-Q Part I Item 1.
_STATEMENT_ITEMS = {"10-K": (None, "8"), "10-Q": ("I", "1")}


def _statement_item(result, catalog, accession_number: str):
    """The financial statements Item, or a CliError saying why it cannot be split."""
    part, number = _STATEMENT_ITEMS[catalog.name]
    item = result.item(number, part, strict=False)
    if item is None:
        raise CliError(
            f"The financial statements Item ({_item_label(part, number)}) was not found in this filing",
            exit_code=EXIT_BROKER,
            error_type="ResponseParseError",
            data={"accession_number": accession_number, "warnings": _findings(result.warnings)},
            hint="Run sec filing-items without --items to see what was found.",
        )
    return item


def _item_label(part: str | None, number: str) -> str:
    return f"Part {part} Item {number}" if part else f"Item {number}"


def _statements_catalog(detail):
    catalog = _extractable_form(detail)
    if catalog.name not in _STATEMENT_ITEMS:
        raise CliError(
            f"Notes are read from 10-K and 10-Q only, not {detail.form}",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"form": detail.form, "supported": sorted(_STATEMENT_ITEMS)},
            hint="An 8-K has no notes; its earnings tables are in sec filing-exhibit.",
        )
    return catalog


def _note_matcher(value: str | None):
    """``"6,income tax,lease"`` → a predicate: a number (or letter) matches the note's label, a word its title."""
    tokens = [token.strip() for token in (value or "").split(",") if token.strip()]
    if not tokens:
        return None
    labels = {token.upper() for token in tokens if token.isdigit() or (len(token) == 1 and token.isalpha())}
    words = [token.lower() for token in tokens if token.upper() not in labels]

    def matches(note) -> bool:
        if note.label is not None and note.label.upper() in labels:
            return True
        return any(word in note.title.lower() for word in words)

    return matches


def _note_summary(note) -> dict:
    units = sorted({table.unit for table in note.tables if table.unit})
    return {
        "number": note.number,
        "label": note.label,
        "title": note.title,
        "chars": len(note.text),
        "tables": len(note.tables),
        "units": units,
    }


def _note_tables(blocks, start: int, end: int) -> list[dict]:
    """Tables whose text starts in ``[start, end)``: the filed unit and the column-aligned grid (unit not applied)."""
    from cluefin_sec_notes import Table

    return [
        {"unit": block.unit, "grid": [list(row) for row in block.grid()]}
        for block in _blocks_in_window(blocks, start, end)
        if isinstance(block, Table)
    ]


@rpc_method(
    name="sec.filing_notes",
    description=(
        "Read the notes to the financial statements of a 10-K (Item 8) or 10-Q (Part I Item 1), split into "
        "numbered notes: revenue disaggregation, segments, income taxes, leases, debt, stock compensation, "
        "commitments and contingencies and so on. Without `notes` it returns the list only: per note number, "
        "label, title, chars, tables and the units their tables state (e.g. 'in millions'); the part before the "
        "first note (auditor's report and the statements) is number null, title 'statements'. With `notes` "
        "(comma-separated note numbers or title words, e.g. 6,lease) it returns each matching note's text, cut at "
        "max_chars (default 40000) with next_offset to continue, and its tables as column-aligned grids of cell "
        "strings with the unit as filed (amounts are not scaled). `findings` (a skipped note number, a heading "
        "without body) and the Item's own warnings are always returned. Note numbers change from year to year; "
        "for several years of one note use sec note-series. Nothing is written to disk."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cik": _CIK_PARAM,
            "accession_number": _ACCESSION_PARAM,
            "notes": {
                "type": "string",
                "description": "Comma-separated note numbers (or letters) and/or title words, e.g. 6 or "
                "income tax,lease. Omit for the list of notes.",
            },
            "max_chars": _MAX_CHARS_PARAM,
            "offset_chars": {
                **_OFFSET_CHARS_PARAM,
                "description": _OFFSET_CHARS_PARAM["description"] + " Needs exactly one matching note.",
            },
            "include_tables": {
                "type": "boolean",
                "default": True,
                "description": "Return each table starting inside the returned text as {unit, grid}. Default true.",
            },
        },
        "required": ["cik", "accession_number"],
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_filing_notes(params: dict, session) -> dict:
    from cluefin_sec_notes import extract_items, split_notes

    cik, accession_number = params["cik"], params["accession_number"]
    matches = _note_matcher(params.get("notes"))
    sec = session.get_sec()
    detail = _checked_detail(sec, cik, accession_number)
    catalog = _statements_catalog(detail)
    document = _main_document(detail)
    parsed = _load_document(sec, cik, accession_number, document, form=detail.form)
    item = _statement_item(extract_items(parsed), catalog, accession_number)
    split = split_notes(item)

    payload = {
        **_filing_header(detail, cik),
        "document": document.name,
        "item": _item_summary(item, catalog),
        "findings": _findings(split.findings),
    }
    if matches is None:
        payload["notes"] = [_note_summary(note) for note in split]
        if len(split) == 1:
            payload["hint"] = (
                "No numbered note heading was found; the whole Item is under 'statements'. Read it with sec "
                "filing-items --items " + _item_key(item.key, catalog) + "."
            )
        return payload

    selected = [note for note in split if matches(note)]
    if int(params.get("offset_chars", 0)) and len(selected) != 1:
        raise CliError(
            "offset_chars needs exactly one matching note",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"notes": params.get("notes"), "matched": [note.title for note in selected]},
            hint="Continue one truncated note at a time: --notes <number> --offset-chars <next_offset>.",
        )
    notes = []
    for note in selected:
        page = _text_page(note.text, note.blocks, {**params, "include_tables": False})
        if params.get("include_tables", True):
            start = page["offset_chars"]
            page["tables"] = _note_tables(note.blocks, start, start + page["chars_returned"])
        notes.append({**_note_summary(note), **page})
    payload["notes"] = notes
    if not notes:
        payload["hint"] = "No note matched. Run without --notes for the list of numbers and titles."
    elif any(note["truncated"] for note in notes):
        payload["hint"] = (
            "Text was cut at max_chars. Continue with --notes <number> --offset-chars <next_offset>, or raise "
            "--max-chars (0 = no cap)."
        )
    return payload


# ---------------------------------------------------------------------------
# Note series: one note's tables across several 10-Ks (note_series.py)
# ---------------------------------------------------------------------------

_DEFAULT_SERIES_YEARS = 5
_MAX_SERIES_YEARS = 10


def _annual_reports(sec, cik: str, years: int) -> list:
    """The latest ``years`` original 10-Ks (amendments excluded), newest first. Older history pages only if needed."""
    entries = sec.submissions.filings(cik, forms=["10-K"], include_amendments=False)
    if len(entries) < years:
        entries = sec.submissions.filings(cik, forms=["10-K"], include_amendments=False, include_older=True)
    return sorted(entries, key=lambda entry: entry.filing_date, reverse=True)[:years]


def _filing_notes(sec, cik: str, entry):
    """Download one 10-K and split its Item 8 into notes: (FilingNotes or None, problem dict or None)."""
    from types import SimpleNamespace

    from cluefin_sec_notes import extract_items, split_notes

    from cluefin_openapi_cli.note_series import FilingNotes, NoteInput, TableInput

    document = SimpleNamespace(name=entry.primary_document or "", type="10-K")
    parsed = _load_document(sec, cik, entry.accession_number, document, form="10-K")
    try:
        item = extract_items(parsed).item("8", strict=False)
    except ValueError as exc:  # filing-items 와 같다: 한 편이 안 읽혀도 나머지 해는 낸다
        return None, {"accession_number": entry.accession_number, "problem": f"Item extraction failed: {exc}"}
    if item is None:
        return None, {"accession_number": entry.accession_number, "problem": "Item 8 not found"}
    split = split_notes(item)
    fy = _fiscal_year(parsed, entry)
    statement_units = [table.unit for table in split.notes[0].tables if table.unit]
    filing = FilingNotes(
        fy=fy,
        period_end=parsed.period_end or entry.report_date,
        accession_number=entry.accession_number,
        notes=tuple(
            NoteInput(note.number, note.title, tuple(TableInput(table.grid(), table.unit) for table in note.tables))
            for note in split
        ),
        statements_unit=statement_units[0] if statement_units else None,
    )
    warnings = [finding.code for finding in (*item.warnings, *split.findings)]
    problem = {"fy": fy, "accession_number": entry.accession_number, "warnings": warnings} if warnings else None
    return filing, problem


def _fiscal_year(parsed, entry) -> int:
    """dei:DocumentFiscalYearFocus, else the period end's year (a January-March year end belongs to the year before)."""
    focus = (parsed.dei.get("DocumentFiscalYearFocus") or "").strip()
    if focus.isdigit():
        return int(focus)
    period = parsed.period_end or entry.report_date or entry.filing_date
    return period.year - 1 if period.month <= 3 else period.year


def _series_selector(value: str | None):
    tokens = [token.strip() for token in (value or "").split(",") if token.strip()]
    if not tokens:
        return None
    numbers = {int(token) for token in tokens if token.isdigit()}
    words = [token.lower() for token in tokens if not token.isdigit()]

    def selected(title: str, number: int | None) -> bool:
        return (number is not None and number in numbers) or any(word in title.lower() for word in words)

    return selected


def _series_summary(note: dict) -> dict:
    return {
        "title": note["title"],
        "numbers_by_fy": note["numbers_by_fy"],
        "tables": len(note["tables"]),
        "rows": sum(len(table["rows"]) for table in note["tables"]),
    }


@rpc_method(
    name="sec.note_series",
    description=(
        "Join one company's 10-K notes across years (default the last 5 annual reports): the same note is matched "
        "by title even when its number changes, each note table is matched to the newer year's by its row labels, "
        "and each row becomes a series of the current-year column of each 10-K. Amounts are converted to USD "
        "millions (unit_filed keeps what each year stated, e.g. 'in thousands'); percentages and per-share values "
        "are left as filed. Rows whose label changed are not merged: the new row carries label_changed with the "
        "old label(s) as candidates. When the next 10-K's comparative column differs from what was filed "
        "(beyond rounding), the row carries restated: [{fy, filed_value, later_value}]; values are never "
        "corrected. Without `notes` it returns the list of note series (title, number per fiscal year, tables, "
        "rows); with `notes` (comma-separated latest note numbers or title words, e.g. income tax,lease) the full "
        "tables. Downloads one document per year (about 1 second each). Original 10-Ks only (10-K/A skipped)."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cik": _CIK_PARAM,
            "years": {
                "type": "integer",
                "minimum": 1,
                "maximum": _MAX_SERIES_YEARS,
                "default": _DEFAULT_SERIES_YEARS,
                "description": "How many of the latest 10-Ks to join. Default 5, max 10.",
            },
            "notes": {
                "type": "string",
                "description": "Comma-separated note numbers (as numbered in the latest 10-K) and/or title words, "
                "e.g. 6 or income tax,lease. Omit for the list of note series.",
            },
            "include_xbrl": {
                "type": "boolean",
                "default": True,
                "description": "With `notes`: add to each amount row the us-gaap concept whose 10-K annual value "
                "equals it (SEC companyfacts, one more request) and that concept's values per fiscal year, latest "
                "filed (first_filed_by_fy where the first filing differed). Segment and geographic rows have no "
                "concept there. Default true.",
            },
        },
        "required": ["cik"],
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_note_series(params: dict, session) -> dict:
    from cluefin_openapi_cli.note_series import build_series

    cik = params["cik"]
    years = int(params.get("years", _DEFAULT_SERIES_YEARS))
    selector = _series_selector(params.get("notes"))
    sec = session.get_sec()
    entries = _annual_reports(sec, cik, years)
    if not entries:
        raise CliError(
            "This company has no 10-K",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"cik": int(cik)},
            hint="Check the forms with sec filings --cik <cik> --forms 10-K. Foreign private issuers file 20-F.",
        )
    filings, problems = [], []
    for entry in entries:
        filing, problem = _filing_notes(sec, cik, entry)
        if filing is not None and any(kept.fy == filing.fy for kept in filings):
            # 회계연도를 바꾼 해 등. 같은 해 두 편을 섞지 않고 최근 공시만 쓴다.
            problems.append(
                {"accession_number": entry.accession_number, "problem": f"duplicate fiscal year {filing.fy}"}
            )
            continue
        if filing is not None:
            filings.append(filing)
        if problem is not None:
            problems.append(problem)
    series = build_series(filings, selector)
    payload = {
        "cik": int(cik),
        "unit": "USD millions (percent and per-share values as filed)",
        "filings": [
            {"fy": filing.fy, "accession_number": filing.accession_number, "period_end": str(filing.period_end)}
            for filing in sorted(filings, key=lambda filing: filing.fy, reverse=True)
        ],
        "problems": problems,
    }
    if selector is None:
        payload["notes"] = [_series_summary(note) for note in series]
        return payload
    payload["notes"] = series
    if not series:
        payload["hint"] = "No note matched. Run without --notes for the list of note titles."
    elif params.get("include_xbrl", True):
        payload["xbrl"] = _attach_company_facts(sec, cik, series, filings)
    return payload


def _attach_company_facts(sec, cik: str, series: list[dict], filings: list) -> dict:
    """Add an ``xbrl`` block to each amount row that a us-gaap concept matches; a company without XBRL is not an error."""
    from cluefin_openapi.sec import SecNotFoundError

    from cluefin_openapi_cli.note_xbrl import attach_xbrl, fact_index

    try:
        facts = sec.xbrl.company_facts(cik)
    except SecNotFoundError:
        return {"source": "companyfacts", "error": "SEC has no XBRL company facts for this cik"}
    period_ends = {filing.fy: filing.period_end for filing in filings if filing.period_end is not None}
    matched, total = attach_xbrl(series, fact_index(facts), period_ends)
    return {"source": "companyfacts", "taxonomy": "us-gaap", "unit": "USD millions", "rows": total, "matched": matched}


_DEFAULT_SUMMARY_YEARS = 3
_MAX_SUMMARY_YEARS = 10


@rpc_method(
    name="sec.financial_summary",
    description=(
        "One company's standard annual accounts from SEC XBRL companyfacts (10-K, fiscal-year figures), newest first: "
        "revenue, cost of sales, gross profit, SG&A, R&D, operating income, interest expense, pretax income, tax, net "
        "income (incl. and excl. noncontrolling interests), assets, current/noncurrent assets and liabilities, cash, "
        "receivables, inventories, long-term debt, equity, retained earnings, operating/investing/financing cash "
        "flow, capex, dividends, D&A, buybacks, share issuance, interest and taxes paid. Account keys match dart "
        "financial-summary where the meaning is the same. Each account takes the first of several us-gaap concepts "
        "the filer used (e.g. Revenues or RevenueFromContractWithCustomerExcludingAssessedTax); `account_match` names "
        "the concept per account for the latest year, null when none was filed. Banks, insurers and brokers also get "
        "deposits, loans, interest/noninterest income and expense, credit loss, premiums, policyholder benefits, "
        "brokerage and investment-banking revenue — only when one of those bank/insurer/broker-only concepts has a "
        "value. Values are USD millions as filed (sign included); a period filed again later (comparative column, "
        "10-K/A) takes the latest filed value, so restatements replace originals. 2 SEC requests (companyfacts, "
        "submissions for the SIC code). No ratios are computed."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cik": _CIK_PARAM,
            "years": {
                "type": "integer",
                "minimum": 1,
                "maximum": _MAX_SUMMARY_YEARS,
                "default": _DEFAULT_SUMMARY_YEARS,
                "description": "How many of the latest fiscal years to return. Default 3, max 10.",
            },
        },
        "required": ["cik"],
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_financial_summary(params: dict, session) -> dict:
    from cluefin_openapi.sec import SecNotFoundError

    from cluefin_openapi_cli.sec_summary import summarize

    cik = params["cik"]
    sec = session.get_sec()
    try:
        facts = sec.xbrl.company_facts(cik)
    except SecNotFoundError as exc:
        raise CliError(
            "SEC has no XBRL company facts for this cik",
            exit_code=EXIT_BROKER,
            error_type="NotFound",
            data={"cik": int(cik)},
            hint="Check the cik with sec company-lookup. Foreign private issuers (20-F) have no us-gaap 10-K facts.",
        ) from exc
    summary = summarize(facts, int(params.get("years", _DEFAULT_SUMMARY_YEARS)))
    if summary is None:
        raise CliError(
            "No 10-K fiscal-year figures in this company's XBRL facts",
            exit_code=EXIT_BROKER,
            error_type="NotFound",
            data={"cik": int(cik), "entity_name": facts.entity_name},
            hint=(
                "A ticker can point at a new holding company that has filed only 10-Qs so far; its predecessor's cik "
                "(sec company-lookup by name) carries the 10-K history. 20-F filers have no 10-K."
            ),
        )
    submissions = sec.submissions.submissions(cik)
    return {
        "cik": int(cik),
        "entity_name": facts.entity_name,
        "sic": submissions.sic,
        "sic_description": submissions.sic_description,
        "unit": "USD millions",
        **summary,
    }


_DEFAULT_EXHIBIT = "EX-99.1"


def _document_row(document) -> dict:
    return {
        "sequence": document.sequence,
        "type": document.type,
        "name": document.name,
        "description": document.description,
        "size": document.size,
    }


@rpc_method(
    name="sec.filing_exhibit",
    description=(
        "Read one exhibit of a filing as text, by exhibit type (default EX-99.1). An 8-K's results live there, not "
        "in the 8-K body: EX-99.1 is usually the earnings press release (revenue, margins, guidance tables), EX-99.2 "
        "often the slides or CFO commentary. Also lists the filing's HTML documents (type, name, description, "
        "size) so other exhibits can be picked. The exhibit is returned as plain text (tables one row per line, "
        "tab-separated), cut at max_chars (default 40000) with chars_total / truncated / next_offset; "
        "include_tables adds column-aligned grids. Amounts stay strings as filed; units are not applied. "
        "Press releases measured 2-30k characters. Nothing is written to disk."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cik": _CIK_PARAM,
            "accession_number": _ACCESSION_PARAM,
            "exhibit": {
                "type": "string",
                "default": _DEFAULT_EXHIBIT,
                "pattern": r"^[A-Za-z0-9.-]+$",
                "description": "Exhibit type as listed by SEC, e.g. EX-99.1, EX-99.2, EX-10.1. Default EX-99.1.",
            },
            "max_chars": _MAX_CHARS_PARAM,
            "offset_chars": _OFFSET_CHARS_PARAM,
            "include_tables": _INCLUDE_TABLES_PARAM,
        },
        "required": ["cik", "accession_number"],
    },
    returns={"type": "object"},
    category="sec",
    broker="sec",
)
def handle_filing_exhibit(params: dict, session) -> dict:
    cik, accession_number = params["cik"], params["accession_number"]
    exhibit = (params.get("exhibit") or _DEFAULT_EXHIBIT).strip().upper()
    sec = session.get_sec()
    detail = _checked_detail(sec, cik, accession_number)
    # Images, XBRL and the full submission text are not readable exhibits; old .txt documents are out of scope.
    documents = [
        document
        for document in detail.documents
        if document.type and not document.data_file and document.name.lower().endswith(_HTML_SUFFIXES)
    ]
    payload = {
        **_filing_header(detail, cik),
        "exhibit": exhibit,
        "documents": [_document_row(document) for document in documents],
    }
    document = next((document for document in documents if document.type.upper() == exhibit), None)
    if document is None:
        listed = sorted({document.type for document in documents})
        return {
            **payload,
            "document": None,
            "text": None,
            "hint": f"This filing has no {exhibit}. Its documents are: {', '.join(listed) or 'none'}. "
            "Pass one of them as --exhibit.",
        }

    parsed = _load_document(sec, cik, accession_number, document, form=exhibit)
    payload["document"] = _document_row(document)
    payload.update(_text_page(parsed.text(), parsed.blocks, params))
    if payload["truncated"]:
        payload["hint"] = "Text was cut at max_chars. Continue with --offset-chars <next_offset>, or raise --max-chars."
    return payload


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_company_lookup,
    handle_filings,
    handle_filing_items,
    handle_filing_notes,
    handle_note_series,
    handle_financial_summary,
    handle_filing_exhibit,
]


def register_sec_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
