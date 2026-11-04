"""sec filing-items / filing-exhibit: download is faked with synthetic HTML, parsing is real cluefin-sec-notes.

Synthetic filings only: no real company, CIK or accession number (cluefin-sec-notes AGENTS.md). The layout follows
the package's own synthetic 10-K (Workiva-style TOC table linking to anchored Item headings).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest
from cluefin_openapi.sec import FilingDetail, FilingDocument, FilingParty

from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_USAGE, CliError
from cluefin_openapi_cli.handlers import sec as handlers

CIK = "1001"
ACCESSION = "0000001001-26-000008"

ITEMS = (
    ("I", "1", "Business"),
    ("I", "1A", "Risk Factors"),
    ("I", "1B", "Unresolved Staff Comments"),
    ("I", "1C", "Cybersecurity"),
    ("I", "2", "Properties"),
    ("I", "3", "Legal Proceedings"),
    ("I", "4", "Mine Safety Disclosures"),
    ("II", "5", "Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity"),
    ("II", "6", "[Reserved]"),
    ("II", "7", "Management’s Discussion and Analysis of Financial Condition and Results of Operations"),
    ("II", "7A", "Quantitative and Qualitative Disclosures About Market Risk"),
    ("II", "8", "Financial Statements and Supplementary Data"),
    ("II", "9", "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure"),
    ("II", "9A", "Controls and Procedures"),
    ("II", "9B", "Other Information"),
    ("II", "9C", "Disclosure Regarding Foreign Jurisdictions that Prevent Inspections"),
    ("III", "10", "Directors, Executive Officers and Corporate Governance"),
    ("III", "11", "Executive Compensation"),
    ("III", "12", "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters"),
    ("III", "13", "Certain Relationships and Related Transactions, and Director Independence"),
    ("III", "14", "Principal Accountant Fees and Services"),
    ("IV", "15", "Exhibits and Financial Statement Schedules"),
    ("IV", "16", "Form 10-K Summary"),
)
COVER = (
    '<div style="display:none"><ix:header><ix:hidden>'
    '<ix:nonNumeric name="dei:DocumentType">10-K</ix:nonNumeric>'
    '<ix:nonNumeric name="dei:DocumentPeriodEndDate">2025-12-31</ix:nonNumeric>'
    "</ix:hidden></ix:header></div><div>FORM 10-K</div>"
)
# Long bodies keep the length checks (implausible_length, statements_not_found) quiet, as in the package's fixture.
RISKS = "".join(f"<div>Risk factor {row}: demand for our products may decline.</div>" for row in range(40))
MDNA = "".join(f"<div>Results of operations paragraph {row}: revenue grew in the period.</div>" for row in range(60))
STATEMENTS = (
    "<table>"
    + "".join(f"<tr><td>Balance sheet line {row}</td><td>$</td><td>1,{row:03}</td></tr>" for row in range(200))
    + "</table>"
)
BODIES = {"1A": RISKS, "7": MDNA, "8": STATEMENTS}


def _ten_k(items=ITEMS, bodies=None) -> str:
    bodies = BODIES if bodies is None else bodies
    toc = "".join(
        f'<tr><td><a href="#i{n.lower()}">Item {n}.</a></td><td><a href="#i{n.lower()}">{t}</a></td></tr>'
        for _, n, t in items
    )
    body = "".join(
        f'<hr style="page-break-after:always"/><div id="i{n.lower()}"></div>'
        f'<div style="font-weight:700">Item {n}. {t}</div><div>Body of item {n}.</div>' + bodies.get(n, "")
        for _, n, t in items
    )
    return f"<html><body>{COVER}<table>{toc}</table>{body}<div>SIGNATURES</div></body></html>"


def _detail(form: str = "10-K", main: str = "alpha-10k.htm", cik: int = 1001) -> FilingDetail:
    return FilingDetail(
        accession_number=ACCESSION,
        form=form,
        filing_date=date(2026, 2, 20),
        period_of_report=date(2025, 12, 31),
        documents=[
            FilingDocument(sequence=1, description=form, name=main, type=form, size=1),
            FilingDocument(sequence=2, description="EX-99.1 PRESS RELEASE", name="ex991.htm", type="EX-99.1", size=1),
            FilingDocument(sequence=3, description="SCHEMA", name="alpha.xsd", type="EX-101.SCH", data_file=True),
            FilingDocument(description="Complete submission text file", name=f"{ACCESSION}.txt"),
        ],
        parties=[FilingParty(cik=cik, name="Alpha Memory Corp", role="Filer")],
    )


class _Session:
    """get_sec() → a client whose archives serve one detail page and a dict of documents."""

    def __init__(self, detail: FilingDetail, documents: dict[str, str]) -> None:
        self.downloads: list[str] = []

        def download(cik, accession_number, name, *, destination):
            self.downloads.append(name)
            path = Path(destination) / name
            path.write_text(documents[name], encoding="utf-8")
            return path

        archives = SimpleNamespace(
            filing_detail=lambda cik, accession_number: detail, download_filing_document=download
        )
        self._client = SimpleNamespace(archives=archives)

    def get_sec(self):
        return self._client


def _items(params: dict, html: str | None = None, detail: FilingDetail | None = None) -> dict:
    session = _Session(detail or _detail(), {"alpha-10k.htm": html or _ten_k()})
    return handlers.handle_filing_items({"cik": CIK, "accession_number": ACCESSION, **params}, session)


# --- filing-items ----------------------------------------------------------------------------------------------


def test_without_items_returns_the_table_of_contents_only() -> None:
    result = _items({})

    assert (result["cik"], result["company"], result["form"], result["catalog"]) == (
        1001,
        "Alpha Memory Corp",
        "10-K",
        "10-K",
    )
    assert result["document"] == "alpha-10k.htm"
    assert [item["key"] for item in result["items"]] == [number for _, number, _ in ITEMS]
    risk = next(item for item in result["items"] if item["key"] == "1A")
    assert risk["heading"] == "Item 1A. Risk Factors"
    assert (risk["method"], risk["uncertain"], risk["warnings"]) == ("toc_anchor", False, [])
    assert risk["chars"] > 2000
    assert next(item for item in result["items"] if item["key"] == "8")["tables"] == 1
    assert all("text" not in item for item in result["items"])
    assert result["missing"] == result["omitted"] == []


def test_items_return_text_with_truncation_fields() -> None:
    result = _items({"items": "1a,7", "max_chars": 500})

    risk, mdna = result["items"]
    assert (risk["key"], risk["status"]) == ("1A", "found")
    assert risk["text"].startswith("Item 1A. Risk Factors")
    assert risk["chars_returned"] <= 500
    assert risk["truncated"] is True
    # Cut at a block boundary: the next window starts on the following paragraph.
    assert risk["next_offset"] == risk["chars_returned"] + 2
    assert mdna["key"] == "7"
    assert "1A, 7" in result["hint"]


def test_offset_continues_where_the_previous_page_stopped() -> None:
    whole = _items({"items": "1A", "max_chars": 0})["items"][0]
    assert whole["truncated"] is False
    assert whole["next_offset"] is None

    pages, offset = [], 0
    while offset is not None:
        page = _items({"items": "1A", "max_chars": 700, "offset_chars": offset})["items"][0]
        pages.append(page["text"])
        offset = page["next_offset"]
    assert len(pages) > 2
    assert "\n\n".join(pages) == whole["text"]


def test_offset_needs_exactly_one_item() -> None:
    with pytest.raises(CliError) as error:
        _items({"items": "1A,7", "offset_chars": 10})
    assert error.value.exit_code == EXIT_USAGE


def test_include_tables_returns_grids_of_tables_in_the_window() -> None:
    statements = _items({"items": "8", "include_tables": True, "max_chars": 0})["items"][0]
    assert len(statements["tables"]) == 1
    assert statements["tables"][0][0] == ["Balance sheet line 0", "$1,000"]

    without = _items({"items": "8"})["items"][0]
    assert "tables" not in without


def test_absent_items_come_back_with_a_status_instead_of_an_error() -> None:
    without_9c = tuple(item for item in ITEMS if item[1] != "9C")
    result = _items({"items": "9C,99"}, html=_ten_k(without_9c))

    omitted, unknown = result["items"]
    assert (omitted["key"], omitted["status"], omitted["text"]) == ("9C", "omitted", None)
    assert (unknown["key"], unknown["status"]) == ("99", "not_in_catalog")


def test_wrong_cik_is_refused_before_download() -> None:
    session = _Session(_detail(cik=2002), {})
    with pytest.raises(CliError) as error:
        handlers.handle_filing_items({"cik": CIK, "accession_number": ACCESSION}, session)
    assert error.value.exit_code == EXIT_BROKER
    assert error.value.data["parties"] == [2002]
    assert session.downloads == []


@pytest.mark.parametrize(("form", "main"), [("20-F", "annual.htm"), ("10-K", "old-10k.txt")])
def test_unsupported_form_or_plain_text_document_is_a_usage_error(form: str, main: str) -> None:
    session = _Session(_detail(form=form, main=main), {})
    with pytest.raises(CliError) as error:
        handlers.handle_filing_items({"cik": CIK, "accession_number": ACCESSION}, session)
    assert error.value.exit_code == EXIT_USAGE
    assert session.downloads == []


def test_item_keys_carry_the_part_only_where_numbers_restart() -> None:
    ten_q = SimpleNamespace(part_scoped=True)
    ten_k = SimpleNamespace(part_scoped=False)
    key = SimpleNamespace(part="II", number="1A")
    assert handlers._item_key(key, ten_q) == "II:1A"
    assert handlers._item_key(key, ten_k) == "1A"
    assert handlers._requested_keys({"items": "ii:1a, 2.02,7"}) == [("II", "1A"), (None, "2.02"), (None, "7")]
    assert handlers._key_matches(key, None, "1A")
    assert not handlers._key_matches(key, "I", "1A")


@pytest.mark.parametrize(
    ("text", "max_chars", "expected"),
    [
        ("aaaa\n\nbbbb\ncccc", 12, (0, 4)),  # blank line before the cap
        ("aaaa\nbbbb\ncccc", 12, (0, 9)),  # no blank line: last line end
        ("aaaaaaaaaaaaaaaa", 5, (0, 5)),  # one long line: hard cut
        ("aaaa\n\nbbbb", 0, (0, 10)),  # 0 = no cap
        ("aaaa\n\nbbbb", 50, (0, 10)),
    ],
)
def test_window_prefers_paragraph_then_line_boundaries(text: str, max_chars: int, expected: tuple[int, int]) -> None:
    assert handlers._window(text, 0, max_chars) == expected


# --- filing-exhibit ----------------------------------------------------------------------------------------------

PRESS_RELEASE = (
    "<html><body><div>Exhibit 99.1</div><div>ALPHA MEMORY REPORTS RECORD QUARTER</div>"
    + "".join(f"<div>Highlight {row}: revenue up {row} percent.</div>" for row in range(30))
    + '<table><tr><td>(in millions)</td><td colspan="2">Q4</td><td colspan="2">Q3</td></tr>'
    "<tr><td>Revenue</td><td>$</td><td>54,229</td><td>$</td><td>41,456</td></tr></table>"
    "</body></html>"
)


def _exhibit(params: dict, detail: FilingDetail | None = None) -> tuple[dict, _Session]:
    session = _Session(detail or _detail(form="8-K", main="alpha-8k.htm"), {"ex991.htm": PRESS_RELEASE})
    result = handlers.handle_filing_exhibit({"cik": CIK, "accession_number": ACCESSION, **params}, session)
    return result, session


def test_exhibit_defaults_to_the_earnings_release_and_lists_html_documents() -> None:
    result, session = _exhibit({"include_tables": True})

    assert session.downloads == ["ex991.htm"]
    assert result["exhibit"] == "EX-99.1"
    assert result["document"]["name"] == "ex991.htm"
    # The schema and the full submission text are not readable exhibits.
    assert [row["type"] for row in result["documents"]] == ["8-K", "EX-99.1"]
    assert result["text"].startswith("Exhibit 99.1\n\nALPHA MEMORY REPORTS RECORD QUARTER")
    assert result["truncated"] is False
    assert result["tables"][-1][-1] == ["Revenue", "$54,229", "$41,456"]


def test_exhibit_pages_like_filing_items() -> None:
    first, _ = _exhibit({"max_chars": 200})
    assert first["truncated"] is True
    assert "offset-chars" in first["hint"]

    second, _ = _exhibit({"max_chars": 200, "offset_chars": first["next_offset"]})
    assert second["offset_chars"] == first["next_offset"]
    assert second["text"].startswith("Highlight")


def test_missing_exhibit_lists_what_the_filing_has_without_downloading() -> None:
    result, session = _exhibit({"exhibit": "ex-99.2"})

    assert session.downloads == []
    assert (result["exhibit"], result["document"], result["text"]) == ("EX-99.2", None, None)
    assert "8-K, EX-99.1" in result["hint"]


def test_exhibit_refuses_another_companys_filing() -> None:
    with pytest.raises(CliError) as error:
        _exhibit({}, detail=_detail(form="8-K", cik=2002))
    assert error.value.exit_code == EXIT_BROKER


# --- filing-notes ----------------------------------------------------------------------------------------------

NOTES = (
    "<div>NOTES TO CONSOLIDATED FINANCIAL STATEMENTS</div>"
    "<div>1. Description of Business</div><div>Alpha Memory Corp designs memory chips.</div>"
    "<div>2. Net Revenues</div><div>Revenue by type was as follows:</div>"
    '<table><tr><td>(in millions)</td><td colspan="2">2025</td><td colspan="2">2024</td></tr>'
    "<tr><td>Product sales</td><td>$</td><td>1,200</td><td>$</td><td>1,000</td></tr>"
    "<tr><td>Services</td><td></td><td>300</td><td></td><td>250</td></tr></table>"
    "<div>3. Leases</div><div>(in thousands)</div>"
    "<table><tr><td>Operating lease cost</td><td>$</td><td>4,500</td></tr></table>"
)


def _notes(params: dict, notes: str = NOTES, detail: FilingDetail | None = None) -> dict:
    html = _ten_k(bodies={**BODIES, "8": STATEMENTS + notes})
    session = _Session(detail or _detail(), {"alpha-10k.htm": html})
    return handlers.handle_filing_notes({"cik": CIK, "accession_number": ACCESSION, **params}, session)


def test_notes_without_selector_list_numbers_titles_and_units() -> None:
    result = _notes({})

    assert result["form"] == "10-K"
    assert (result["item"]["key"], result["item"]["uncertain"]) == ("8", False)
    assert [(note["number"], note["title"], note["tables"], note["units"]) for note in result["notes"]] == [
        (None, "statements", 1, []),
        (1, "Description of Business", 0, []),
        (2, "Net Revenues", 1, ["in millions"]),
        (3, "Leases", 1, ["in thousands"]),
    ]
    assert result["findings"] == []
    assert all("text" not in note for note in result["notes"])


def test_notes_by_number_or_title_word_return_text_and_tables_with_unit() -> None:
    result = _notes({"notes": "2,lease"})

    revenue, leases = result["notes"]
    assert revenue["title"] == "Net Revenues"
    assert revenue["text"].startswith("2. Net Revenues")
    assert revenue["tables"] == [
        {
            "unit": "in millions",
            "grid": [
                ["(in millions)", "2025", "2024"],
                ["Product sales", "$1,200", "$1,000"],
                ["Services", "300", "250"],
            ],
        }
    ]
    assert leases["tables"][0]["unit"] == "in thousands"
    assert leases["truncated"] is False


def test_notes_page_like_filing_items() -> None:
    first = _notes({"notes": "1", "max_chars": 30})
    rest = _notes({"notes": "1", "offset_chars": first["notes"][0]["next_offset"]})

    assert first["notes"][0]["truncated"] is True
    assert "hint" in first
    assert first["notes"][0]["text"] + "\n\n" + rest["notes"][0]["text"] == _notes({"notes": "1"})["notes"][0]["text"]


def test_notes_offset_needs_exactly_one_note() -> None:
    with pytest.raises(CliError) as error:
        _notes({"notes": "2,3", "offset_chars": 10})
    assert error.value.exit_code == EXIT_USAGE


def test_notes_report_a_skipped_number_and_unmatched_selector() -> None:
    result = _notes({"notes": "income tax"}, notes=NOTES.replace("3. Leases", "4. Leases"))

    assert result["notes"] == []
    assert "No note matched" in result["hint"]
    assert [finding["code"] for finding in result["findings"]] == ["note_sequence_gap"]


def test_notes_refuse_an_8k() -> None:
    with pytest.raises(CliError) as error:
        _notes({}, detail=_detail(form="8-K"))
    assert error.value.exit_code == EXIT_USAGE


# --- note-series -----------------------------------------------------------------------------------------------


def _year_notes(fy: int, number: int, product: str, unit: str) -> str:
    return (
        "<div>NOTES TO CONSOLIDATED FINANCIAL STATEMENTS</div>"
        "<div>1. Description of Business</div><div>Alpha Memory Corp designs memory chips.</div>"
        f"<div>{number}. Net Revenues</div><div>Revenue by type was as follows:</div>"
        f'<table><tr><td>({unit})</td><td colspan="2">{fy}</td><td colspan="2">{fy - 1}</td></tr>'
        f"<tr><td>Product sales</td><td>$</td><td>{product}</td><td>$</td><td>1</td></tr></table>"
    )


class _SeriesSession:
    """get_sec() → submissions listing two original 10-Ks, archives serving their HTML."""

    def __init__(self) -> None:
        self.filings_calls: list[dict] = []
        documents = {
            "alpha-2025.htm": _ten_k(bodies={**BODIES, "8": STATEMENTS + _year_notes(2025, 2, "1,200", "in millions")}),
            "alpha-2024.htm": _ten_k(
                bodies={**BODIES, "8": STATEMENTS + _year_notes(2024, 3, "1,000,500", "in thousands")}
            ).replace("2025-12-31", "2024-12-31"),
        }
        entries = [
            SimpleNamespace(
                accession_number=f"0000001001-{fy % 100 + 1:02d}-000008",
                form="10-K",
                filing_date=date(fy + 1, 2, 20),
                report_date=date(fy, 12, 31),
                primary_document=f"alpha-{fy}.htm",
            )
            for fy in (2024, 2025)
        ]

        def filings(cik, *, forms, include_amendments, include_older=False):
            self.filings_calls.append({"forms": forms, "include_amendments": include_amendments})
            return entries

        def download(cik, accession_number, name, *, destination):
            path = Path(destination) / name
            path.write_text(documents[name], encoding="utf-8")
            return path

        self._client = SimpleNamespace(
            submissions=SimpleNamespace(filings=filings), archives=SimpleNamespace(download_filing_document=download)
        )

    def get_sec(self):
        return self._client


def test_note_series_lists_notes_matched_across_years() -> None:
    session = _SeriesSession()
    result = handlers.handle_note_series({"cik": CIK, "years": 2}, session)

    assert [filing["fy"] for filing in result["filings"]] == [2025, 2024]
    assert session.filings_calls[0] == {"forms": ["10-K"], "include_amendments": False}
    revenue = next(note for note in result["notes"] if note["title"] == "Net Revenues")
    assert revenue == {"title": "Net Revenues", "numbers_by_fy": {"2025": 2, "2024": 3}, "tables": 1, "rows": 1}


def test_note_series_with_notes_returns_rows_in_millions() -> None:
    result = handlers.handle_note_series({"cik": CIK, "years": 2, "notes": "revenue"}, _SeriesSession())

    (note,) = result["notes"]
    (row,) = note["tables"][0]["rows"]
    assert row["values_by_fy"] == {"2025": 1200, "2024": 1000.5}
    assert row["unit_filed"] == {"2025": "in millions", "2024": "in thousands"}


def test_note_series_without_10k_is_a_usage_error() -> None:
    session = _SeriesSession()
    session._client.submissions.filings = lambda cik, **kwargs: []
    with pytest.raises(CliError) as error:
        handlers.handle_note_series({"cik": CIK}, session)
    assert error.value.exit_code == EXIT_USAGE
