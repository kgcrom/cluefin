from decimal import Decimal

import pytest

from cluefin_sec_notes import Cell, Table
from cluefin_sec_notes._grid import parse_amount


def table(*rows) -> Table:
    """행마다 `(글자, 폭)` 또는 글자."""
    return Table(
        rows=tuple(
            tuple(Cell(cell) if isinstance(cell, str) else Cell(cell[0], col_span=cell[1]) for cell in row)
            for row in rows
        ),
        line=1,
        column=1,
    )


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("$59,792", Decimal("59792")),
        ("59,792", Decimal("59792")),
        ("(3,787)", Decimal("-3787")),
        ("$(1.5)", Decimal("-1.5")),
        ("($ 1.5)", Decimal("-1.5")),
        ("12.5%", Decimal("12.5")),
        ("(1.2)%", Decimal("-1.2")),
        ("−4", Decimal("-4")),
        ("€23", Decimal("23")),
        ("1,234 (a)", Decimal("1234")),
        ("7,563*", Decimal("7563")),
        (".5", Decimal("0.5")),
        ("—", None),
        ("", None),
        ("Net income", None),
        ("(3,787", None),
        ("2025", Decimal("2025")),
    ],
)
def test_parse_amount(text, expected):
    assert parse_amount(text) == expected


def test_workiva_value_cells_line_up_under_year_headers():
    grid = table(
        [""] * 18,
        [("Year ended December 31", 3), ("2025", 3), ("", 3), ("2024", 3)],
        [("Revenue", 3), ("", 3), ("", 3), ("", 3)],
        [("Investment banking fees", 3), "$", "9,615", "", ("", 3), "$", "8,910", ""],
        [("Principal transactions", 3), ("27,212", 2), "", ("", 3), ("24,787", 2), ""],
    ).grid()
    assert grid == (
        ("Year ended December 31", "2025", "2024"),
        ("Revenue", "", ""),
        ("Investment banking fees", "$9,615", "$8,910"),
        ("Principal transactions", "27,212", "24,787"),
    )


def test_parentheses_in_the_next_cell_and_text_header_over_two_columns():
    """DFIN식 음수 괄호 칸, 두 해에 걸친 글자 머리("December 31,")와 글자 날짜 머리."""
    grid = table(
        ["", "", ("December 31,", 6), ""],
        ["", "", ("June 30, 2020", 2), "", "", ("June 30, 2019", 2), ""],
        ["Cash", "", "$", "18,248", "", "", "$", "8,028", ""],
        ["Net loss", "", "", "(3,787", ")", "", "", "(1,200", ")"],
        ["Margin", "", "", "12.5", "%", "", "", "—", ""],
    ).grid()
    assert grid == (
        ("", "December 31,", ""),
        ("", "June 30, 2020", "June 30, 2019"),
        ("Cash", "$18,248", "$8,028"),
        ("Net loss", "(3,787)", "(1,200)"),
        ("Margin", "12.5%", "—"),
    )


def test_row_span_pushes_cells_to_the_right():
    rows = (
        (Cell("Segment", row_span=2), Cell("2025"), Cell("2024")),
        (Cell("1"), Cell("2")),
    )
    grid = Table(rows=rows, line=1, column=1).grid()
    assert grid == (("Segment", "2025", "2024"), ("", "1", "2"))


def test_empty_table_and_spacer_rows_disappear():
    assert table(["", ""], ["", ""]).grid() == ()


def test_wide_caption_over_the_label_column_stays_in_the_label_column():
    """폭 8 "(In millions)" 칸이 첫 해 값 열을 라벨 앞으로 끌어내지 않는다."""
    grid = table(
        [""] * 9,
        [("(In millions)", 8), ""],
        ["June 30,", "", ("2026", 2), "", "", ("2025", 2), ""],
        ["Land", "", "$", "10,546", "", "", "$", "9,338", ""],
        ["Buildings", "", "", "182,749", "", "", "", "137,921", ""],
    ).grid()
    assert grid == (
        ("(In millions)", "", ""),
        ("June 30,", "2026", "2025"),
        ("Land", "$10,546", "$9,338"),
        ("Buildings", "182,749", "137,921"),
    )


def test_year_header_over_several_value_columns_does_not_merge_them():
    grid = table(
        ["", ("2025", 4), ("2024", 4)],
        ["", ("Loans", 2), ("Derivatives", 2), ("Loans", 2), ("Derivatives", 2)],
        ["Consumer", "$", "445,845", "$", "402,258", "$", "437,654", "$", "392,810"],
    ).grid()
    assert grid == (
        ("", "2025", "", "2024", ""),
        ("", "Loans", "Derivatives", "Loans", "Derivatives"),
        ("Consumer", "$445,845", "$402,258", "$437,654", "$392,810"),
    )


def test_footnote_mark_cells_join_the_value_on_their_left():
    grid = table(
        ["Company", "Fair Value", "", "% of Net Assets"],
        ["Alpha, Inc.", "4,980", "(2)(9)", "1.2%"],
        ["Losses", "120", "(a)", ""],
    ).grid()
    assert grid == (
        ("Company", "Fair Value", "% of Net Assets"),
        ("Alpha, Inc.", "4,980(2)(9)", "1.2%"),
        ("Losses", "120(a)", ""),
    )
    assert parse_amount("4,980(2)(9)") == Decimal("4980")


def test_small_negative_in_parentheses_is_a_value_not_a_footnote():
    grid = table(["", ("2025", 2), ("2024", 2)], ["Derivatives CVA", "$", "(36)", "$", "29"]).grid()
    assert grid == (("", "2025", "2024"), ("Derivatives CVA", "$(36)", "$29"))
