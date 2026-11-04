"""split_notes(주석 나누기)와 Table.unit. 합성 HTML 조각만 쓴다(실제 공시 아님)."""

from __future__ import annotations

import pytest

from cluefin_sec_notes import (
    EMPTY_NOTE,
    NOTE_SEQUENCE_GAP,
    STATEMENTS_TITLE,
    Item,
    ItemKey,
    parse_filing,
    split_notes,
    unit_scale,
)

STATEMENTS = (
    "<div>Report of Independent Registered Public Accounting Firm</div>"
    "<div>CONSOLIDATED BALANCE SHEETS</div><div>(in millions)</div>"
    "<table><tr><td>Total assets</td><td>$</td><td>1,000</td></tr></table>"
    "<div>NOTES TO CONSOLIDATED FINANCIAL STATEMENTS</div>"
)
BODY = "<div>The Company recognizes revenue when control transfers to the customer.</div>"
LONG_TITLE = "Redeemable Convertible Preferred Units and Stockholders' Equity (Deficit)"


def _item(html: str) -> Item:
    document = parse_filing(f"<html><body>{html}</body></html>", form="10-K")
    return Item(
        key=ItemKey("II", "8"),
        title="Financial Statements and Supplementary Data",
        start=0,
        end=len(document.blocks),
        method="test",
        confidence=1.0,
        document=document,
    )


def _notes(html: str):
    return split_notes(_item(STATEMENTS + html))


def _titles(split) -> list[tuple[int | None, str]]:
    return [(note.number, note.title) for note in split]


# 헤딩 모양 ------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "heading",
    [
        "<div>{n}. {title}</div>",
        '<div style="font-weight:bold">NOTE {n} — {title}</div>',
        "<div><b>({n}) {title}</b></div>",
        "<table><tr><td>{n}.</td><td>{title}</td></tr></table>",
        "<div>Note {n}</div><div>{title}</div>",
        "<div>{n}) {title}</div>",
        "<table><tr><td></td><td></td></tr><tr><td>{n}.</td><td>{title}</td></tr></table>",
    ],
    ids=[
        "paragraph",
        "bold-note-prefix",
        "parenthesized",
        "table-first-row",
        "two-paragraphs",
        "closing-paren",
        "table-after-blank-row",
    ],
)
def test_heading_shapes(heading: str) -> None:
    html = "".join(heading.format(n=n, title=title) + BODY for n, title in ((1, "Revenue"), (2, "Leases")))

    split = _notes(html)

    assert _titles(split) == [(None, STATEMENTS_TITLE), (1, "Revenue"), (2, "Leases")]
    assert split.findings == ()
    assert split.note(2).text.endswith("control transfers to the customer.")


def test_statements_before_the_first_note_keep_their_tables() -> None:
    split = _notes(f"<div>1. Revenue</div>{BODY}")

    statements = split.notes[0]
    assert (statements.number, statements.label, statements.start) == (None, None, 0)
    assert len(statements.tables) == 1
    assert statements.end == split.note(1).start


def test_long_title_is_not_cut() -> None:
    split = _notes(f"<div>1. Revenue</div>{BODY}<div>2. {LONG_TITLE}</div>{BODY}")

    assert split.note(2).title == LONG_TITLE
    assert len(LONG_TITLE) > 70


def test_lettered_notes() -> None:
    split = _notes(f"<div>Note A – Accounting Policies</div>{BODY}<div>Note B – Inventories</div>{BODY}")

    assert [(note.number, note.label, note.title) for note in split.notes[1:]] == [
        (1, "A", "Accounting Policies"),
        (2, "B", "Inventories"),
    ]


def test_statement_footnotes_lose_to_the_real_notes() -> None:
    footnotes = "".join(f"<div>({n}) Including amounts from a related party of ${n},000</div>" for n in (1, 2, 3))
    split = _notes(f"{footnotes}<div>1. Revenue</div>{BODY}<div>2. Leases</div>{BODY}")

    assert _titles(split)[1:] == [(1, "Revenue"), (2, "Leases")]
    assert "Including amounts" in split.notes[0].text
    assert split.findings == ()


def test_footnote_tied_with_the_real_first_note_loses_on_style() -> None:
    footnote = "<div>(1) Accumulated other comprehensive income</div><div>The notes are an integral part.</div>"
    notes = f"<div>NOTE 1 – BASIS OF PREPARATION.</div>{BODY}<div>NOTE 2 – LEASES.</div>{BODY}"
    split = _notes(footnote + notes)

    assert _titles(split)[1:] == [(1, "BASIS OF PREPARATION"), (2, "LEASES")]


def test_title_colon_is_dropped() -> None:
    split = _notes(f"<div>1. Stock-based compensation:</div>{BODY}")

    assert split.note(1).title == "Stock-based compensation"


def test_sentence_after_number_is_not_a_heading() -> None:
    body = "<div>2. The Company leases offices under non-cancelable leases.</div>"
    split = _notes(f"<div>1. Revenue</div>{body}<div>2. Leases</div>{BODY}")

    assert _titles(split)[1:] == [(1, "Revenue"), (2, "Leases")]


def test_continued_heading_on_a_later_page_does_not_start_a_note() -> None:
    split = _notes(f"<div>1. Revenue</div>{BODY}<div>1. Revenue (continued)</div>{BODY}<div>2. Leases</div>{BODY}")

    assert [note.number for note in split.notes[1:]] == [1, 2]


def test_first_note_must_be_number_one() -> None:
    split = _notes(f"<div>3. Retinal Imaging Device</div>{BODY}<div>1. Revenue</div>{BODY}")

    assert _titles(split)[1:] == [(1, "Revenue")]


# Finding ------------------------------------------------------------------------------------------------------


def test_skipped_number_is_reported() -> None:
    split = _notes(f"<div>1. Revenue</div>{BODY}<div>3. Income Taxes</div>{BODY}")

    assert [note.number for note in split.notes[1:]] == [1, 3]
    assert [finding.code for finding in split.findings] == [NOTE_SEQUENCE_GAP]
    assert split.findings[0].key == ItemKey("II", "8")


def test_number_far_ahead_is_not_a_heading() -> None:
    split = _notes(f"<div>1. Revenue</div>{BODY}<div>9. Income Taxes</div>{BODY}")

    assert [note.number for note in split.notes[1:]] == [1]
    assert split.findings == ()


def test_heading_without_body_is_reported() -> None:
    split = _notes(f"<div>1. Revenue</div><div>2. Leases</div>{BODY}")

    assert [finding.code for finding in split.findings] == [EMPTY_NOTE]
    assert "note 1" in split.findings[0].message


def test_no_heading_leaves_everything_in_statements() -> None:
    split = _notes(BODY)

    assert _titles(split) == [(None, STATEMENTS_TITLE)]


# Table.unit ---------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("html", "unit", "scale"),
    [
        ("<div>(in thousands)</div><table><tr><td>Revenue</td><td>1,000</td></tr></table>", "in thousands", 1_000),
        (
            "<table><tr><td>(In millions, except per share data)</td><td>2025</td></tr>"
            "<tr><td>Revenue</td><td>1,000</td></tr></table>",
            "In millions, except per share data",
            1_000_000,
        ),
        (
            "<table><tr><td>($ in billions)</td><td>2025</td></tr><tr><td>Revenue</td><td>1.5</td></tr></table>",
            "$ in billions",
            1_000_000_000,
        ),
        (
            "<div>Other receivables are summarized as follows (in millions).</div>"
            "<table><tr><td>Revenue</td><td>1,000</td></tr></table>",
            "in millions",
            1_000_000,
        ),
        (
            "<div>(Dollars in thousands, except per share amounts)</div><hr/>"
            "<table><tr><td>Revenue</td><td>1,000</td></tr></table>",
            "Dollars in thousands, except per share amounts",
            1_000,
        ),
    ],
    ids=["paragraph", "head-row-except", "head-row-billions", "end-of-sentence", "across-page-break"],
)
def test_table_unit(html: str, unit: str, scale: int) -> None:
    table = parse_filing(f"<html><body>{html}</body></html>").blocks[-1]

    assert table.unit == unit
    assert unit_scale(table.unit) == scale


def test_unit_is_not_carried_past_the_next_table_or_from_body_rows() -> None:
    html = (
        "<div>(in thousands)</div><table><tr><td>Revenue</td><td>1,000</td></tr></table>"
        "<table><tr><td>Revenue</td><td>1,000</td></tr><tr><td>Note: amounts in millions</td><td>2</td></tr></table>"
        "<div>The following table shows the assumptions used.</div>"
        "<table><tr><td>Discount rate</td><td>4.5%</td></tr></table>"
    )
    first, second, third = (block for block in parse_filing(html).blocks if hasattr(block, "rows"))

    assert first.unit == "in thousands"
    assert second.unit is None
    assert third.unit is None
    assert unit_scale(None) is None
