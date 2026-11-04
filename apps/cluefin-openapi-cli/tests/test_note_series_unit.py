"""note_series: 합성 grid() 행렬로 해를 잇는 경우를 따로 본다. 모양은 실제 10-K 주석 표를 옮겼고 숫자·이름은 지어냈다."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from cluefin_openapi_cli.note_series import (
    FilingNotes,
    NoteInput,
    TableInput,
    build_series,
    normalize_label,
    normalize_title,
    read_table,
)


def _table(*rows: tuple[str, ...], unit: str | None = None) -> TableInput:
    return TableInput(grid=tuple(rows), unit=unit)


def _filing(fy: int, *notes: NoteInput, statements_unit: str | None = None) -> FilingNotes:
    return FilingNotes(
        fy=fy,
        period_end=date(fy, 12, 31),
        accession_number=f"0000001001-{fy % 100 + 1:02d}-000001",
        notes=(NoteInput(None, "statements", ()), *notes),
        statements_unit=statements_unit,
    )


def _revenue(fy: int, number: int, product: str, services: str, unit: str = "in millions") -> NoteInput:
    table = _table(
        (f"({unit})", str(fy), str(fy - 1)),
        ("Product sales", product, "1"),
        ("Services", services, "1"),
        ("Total net revenues", "—", "1"),
        unit=unit,
    )
    return NoteInput(number, "Net Revenues", (table,))


def _rows(note: dict, table: int = 0) -> dict[str, dict]:
    return {row["label"]: row for row in note["tables"][table]["rows"]}


# 1. 주석 번호가 바뀐다 ----------------------------------------------------------------------------------------


def test_notes_are_matched_by_title_not_number() -> None:
    filings = [
        _filing(2025, _revenue(2025, 2, "$1,200", "300")),
        _filing(2024, _revenue(2024, 3, "$1,000", "250")),
    ]

    (note,) = build_series(filings)

    assert note["numbers_by_fy"] == {"2025": 2, "2024": 3}
    assert _rows(note)["Product sales"]["values_by_fy"] == {"2025": 1200, "2024": 1000}


def test_title_aliases_and_net_are_ignored() -> None:
    assert normalize_title("Net Loss per Share") == normalize_title("Earnings per Share")
    assert normalize_title("Property and Equipment, net") == normalize_title("Property and equipment")
    assert normalize_title("Other (Expense) Income, net") == "other expense income"


def test_selector_uses_latest_number_or_any_title() -> None:
    filings = [
        _filing(2025, _revenue(2025, 2, "1", "1"), NoteInput(3, "Leases", ())),
        _filing(2024, _revenue(2024, 3, "1", "1"), NoteInput(2, "Leases", ())),
    ]

    assert [note["title"] for note in build_series(filings, lambda title, number: number == 3)] == ["Leases"]
    assert [note["title"] for note in build_series(filings, lambda title, number: "revenue" in title.lower())] == [
        "Net Revenues"
    ]


# 2. 표 단위가 바뀐다 -------------------------------------------------------------------------------------------


def test_thousands_are_converted_to_millions_and_unit_filed_is_kept() -> None:
    filings = [
        _filing(2023, _revenue(2023, 2, "$21,223", "2,576")),
        _filing(2022, _revenue(2022, 2, "$18,338,177", "1,869,495", unit="in thousands")),
    ]

    rows = _rows(build_series(filings)[0])

    assert rows["Product sales"]["values_by_fy"] == {"2023": 21223, "2022": 18338.177}
    assert rows["Services"]["unit_filed"] == {"2023": "in millions", "2022": "in thousands"}


def test_percent_and_per_share_values_are_not_scaled() -> None:
    table = _table(
        ("", "2025", "2024"),
        ("Effective tax rate", "21.0%", "20.0%"),
        ("Net income per share", "$1.25", "$1.10"),
        ("Net income", "1,250", "1,100"),
        unit="in thousands, except per share amounts",
    )

    rows = {row.label: row for row in read_table(table, 2025).rows}

    assert (rows["Effective tax rate"].kind, rows["Effective tax rate"].current) == ("percent", Decimal("21.0"))
    assert (rows["Net income per share"].kind, rows["Net income per share"].current) == ("per_share", Decimal("1.25"))
    assert rows["Net income"].current == Decimal("1.250")


def test_table_without_unit_falls_back_to_statements_unit() -> None:
    table = _table(("", "2025"), ("Operating lease cost", "4,500"))

    (row,) = read_table(table, 2025, fallback_unit="in thousands").rows

    assert (row.current, row.unit_filed) == (Decimal("4.500"), "in thousands")


# 3. 같은 주석 안의 표 순서가 바뀐다 -----------------------------------------------------------------------------


def _tax_tables(fy: int) -> tuple[TableInput, TableInput]:
    before_tax = _table(
        ("(in millions)", str(fy), str(fy - 1)),
        ("United States", "(408)", "(1,073)"),
        ("Foreign", "1,005", "1,546"),
        ("Income before income taxes", "597", "473"),
    )
    provision = _table(
        ("(in millions)", str(fy), str(fy - 1)),
        ("Current taxes", "", ""),
        ("United States", "$(35)", "$76"),
        ("Foreign", "381", "106"),
        ("Current taxes", "346", "182"),
        ("Deferred taxes", "", ""),
        ("United States", "(48)", "(15)"),
        ("Foreign", "85", "240"),
        ("Deferred taxes", "37", "225"),
        ("Income tax expense (benefit)", "$383", "$407"),
    )
    return before_tax, provision


def test_tables_are_matched_by_row_labels_when_their_order_changes() -> None:
    before_tax, provision = _tax_tables(2025)
    older_before, older_provision = _tax_tables(2024)
    filings = [
        _filing(2025, NoteInput(6, "Income Taxes", (before_tax, provision))),
        _filing(2024, NoteInput(7, "Income Taxes", (older_provision, older_before))),
    ]

    (note,) = build_series(filings)

    assert [table["index_by_fy"] for table in note["tables"]] == [{"2025": 0, "2024": 1}, {"2025": 1, "2024": 0}]
    assert all(table["unmatched"] == [] for table in note["tables"])


def test_section_headers_keep_repeated_labels_apart() -> None:
    (_, provision) = _tax_tables(2025)

    rows = read_table(provision, 2025).rows

    assert [(row.section, row.label, row.current) for row in rows if row.label == "United States"] == [
        ("Current taxes", "United States", Decimal(-35)),
        ("Deferred taxes", "United States", Decimal(-48)),
    ]
    assert rows[-1].section == ""  # 합계 행 "Deferred taxes"가 구역을 닫는다


def test_unmatched_table_starts_its_own_series_and_lists_missing_years() -> None:
    assumptions = _table(("", "2024"), ("Discount rate", "4.5%"), ("Salary growth", "3.0%"))
    before_tax, _ = _tax_tables(2025)
    older_before, _ = _tax_tables(2024)
    filings = [
        _filing(2025, NoteInput(6, "Income Taxes", (before_tax,))),
        _filing(2024, NoteInput(6, "Income Taxes", (older_before, assumptions))),
    ]

    (note,) = build_series(filings)

    assert [table["unmatched"] for table in note["tables"]] == [[], [2025]]


# 4. 행 이름이 바뀐다 -------------------------------------------------------------------------------------------


def test_label_word_order_plural_and_punctuation_are_the_same_row() -> None:
    assert normalize_label("Income tax expense (benefit)") == normalize_label("Income tax (benefit) expense")
    assert normalize_label("Less: valuation allowance") == normalize_label("Less: valuation allowances")
    assert normalize_label("U.S. federal") == normalize_label("U.S federal")
    assert normalize_label("Loss before income taxes (1)") == normalize_label("Loss before income taxes")


def test_split_label_is_not_merged_but_flagged_as_label_changed() -> None:
    newer = _table(
        ("(in millions)", "2023"),
        ("United States", "(217)"),
        ("Foreign", "801"),
        ("Income (loss) before income taxes", "584"),
    )
    older = _table(
        ("(in millions)", "2022"),
        ("United States", "(232)"),
        ("Foreign - Korea", "186"),
        ("Foreign - Other", "(47)"),
        ("Income (loss) before income taxes", "(93)"),
    )
    filings = [
        _filing(2023, NoteInput(6, "Income Taxes", (newer,))),
        _filing(2022, NoteInput(7, "Income Taxes", (older,))),
    ]

    rows = _rows(build_series(filings)[0])

    assert rows["United States"]["values_by_fy"] == {"2023": -217, "2022": -232}
    assert rows["Foreign"]["values_by_fy"] == {"2023": 801}
    assert rows["Foreign - Korea"]["values_by_fy"] == {"2022": 186}
    assert rows["Foreign"]["label_changed"] == ["Foreign - Korea", "Foreign - Other"]
    assert "label_changed" not in rows["United States"]


def test_row_with_a_new_section_header_still_joins_by_unique_name() -> None:
    newer = _table(("", "2024"), ("Differences resulting from:", ""), ("Stock compensation", "56"))
    older = _table(("", "2023"), ("Stock compensation", "44"))
    filings = [
        _filing(2024, NoteInput(6, "Income Taxes", (newer,))),
        _filing(2023, NoteInput(6, "Income Taxes", (older,))),
    ]

    rows = _rows(build_series(filings)[0])

    assert rows["Stock compensation"]["values_by_fy"] == {"2024": 56, "2023": 44}


# 표 읽기 -------------------------------------------------------------------------------------------------------


def test_only_the_current_year_column_is_used() -> None:
    table = _table(
        ("", "Year Ended December 31,", "", ""), ("(in millions)", "2025", "2024", "2023"), ("Revenue", "10", "9", "8")
    )

    (row,) = read_table(table, 2025).rows

    assert (row.current, row.prior) == (Decimal(10), Decimal(9))


def test_table_without_a_current_year_column_is_skipped() -> None:
    old_format = _table(("(in millions)", "2024", "2023"), ("Taxes at statutory rate", "99", "122"))
    filings = [_filing(2025, NoteInput(6, "Income Taxes", (old_format,)))]

    (note,) = build_series(filings)

    assert note["tables"] == []
    assert note["skipped_tables"] == [{"fy": 2025, "table": 0, "reason": "no current-year column"}]


def test_maturity_years_become_relative_but_other_year_labels_do_not() -> None:
    maturity = _table(("(in millions)", "Long-term debt"), ("2026", "71"), ("2027", "201"), ("Thereafter", "—"))
    expiry = _table(("(in millions)", "Amount"), ("2029", "128"), ("2035 - 2037", "899"))

    assert [row.name for row in read_table(maturity, 2025).rows] == ["fy+1", "fy+2", "thereafter"]
    assert [row.name for row in read_table(expiry, 2025).rows] == ["2029", "2035 2037"]


def test_stacked_year_sections_read_as_current_and_prior() -> None:
    table = _table(
        ("(in millions)", "Level 1", "Total"),
        ("December 31, 2025", "", ""),
        ("Cash equivalents", "10", "10"),
        ("December 31, 2024", "", ""),
        ("Cash equivalents", "7", "7"),
        ("December 31, 2023", "", ""),
        ("Cash equivalents", "5", "5"),
    )

    rows = read_table(table, 2025).rows

    assert [(row.key, row.current, row.prior) for row in rows] == [
        ("31 december/cash equivalent/1 level", Decimal(10), Decimal(7)),
        ("31 december/cash equivalent/total", Decimal(10), Decimal(7)),
    ]


def test_dash_is_zero_and_blank_is_missing() -> None:
    table = _table(("", "2025", "2024"), ("Other", "—", ""), ("Fees", "", "3"))

    rows = {row.label: row for row in read_table(table, 2025).rows}

    assert (rows["Other"].current, rows["Other"].prior) == (Decimal(0), None)
    assert (rows["Fees"].current, rows["Fees"].prior) == (None, Decimal(3))


# 5. 재작성 -------------------------------------------------------------------------------------------------------


def _deferred(fy: int, current: str, prior: str, unit: str = "in millions") -> NoteInput:
    table = _table(
        (f"({unit})", f"December 31, {fy}", f"December 31, {fy - 1}"),
        ("Accrued expenses", str(fy - 1900), str(fy - 1901)),  # 해마다 이어지는 값(재작성 없음)
        ("Other", current, prior),
        unit=unit,
    )
    return NoteInput(6, "Income Taxes", (table,))


def test_next_years_comparative_that_differs_is_flagged_not_corrected() -> None:
    filings = [_filing(2024, _deferred(2024, "48", "36")), _filing(2023, _deferred(2023, "49", "21"))]

    rows = _rows(build_series(filings)[0])

    assert rows["Other"]["values_by_fy"] == {"2024": 48, "2023": 49}
    assert rows["Other"]["restated"] == [{"fy": 2023, "filed_value": 49, "later_value": 36}]
    assert "restated" not in rows["Accrued expenses"]


def test_rounding_from_thousands_to_millions_is_not_restated() -> None:
    filings = [
        _filing(2023, _deferred(2023, "57", "28")),
        _filing(2022, _deferred(2022, "28,513", "40,000", unit="in thousands")),
    ]

    # 28.513 → 28: 반올림 방향이 달라도 한 단위 미만이면 재작성이 아니다.
    assert "restated" not in _rows(build_series(filings)[0])["Other"]


def test_difference_under_half_a_percent_is_rounding() -> None:
    filings = [_filing(2024, _deferred(2024, "48", "1,004")), _filing(2023, _deferred(2023, "1,000", "21"))]

    assert "restated" not in _rows(build_series(filings)[0])["Other"]


def test_row_new_in_the_later_year_has_no_restatement() -> None:
    newer = _table(("(in millions)", "2024", "2023"), ("Stock compensation", "22", "18"), ("Other", "48", "49"))
    older = _table(("(in millions)", "2023", "2022"), ("Other", "49", "21"))
    filings = [
        _filing(2024, NoteInput(6, "Income Taxes", (newer,))),
        _filing(2023, NoteInput(6, "Income Taxes", (older,))),
    ]

    rows = _rows(build_series(filings)[0])

    assert rows["Stock compensation"]["values_by_fy"] == {"2024": 22}
    assert "restated" not in rows["Stock compensation"]
    assert "restated" not in rows["Other"]
