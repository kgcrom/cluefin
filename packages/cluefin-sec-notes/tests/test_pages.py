import pytest

from cluefin_sec_notes._furniture import Page
from cluefin_sec_notes._pages import (
    PageIndex,
    PageList,
    find_page_references,
    normalize_label,
    parse_page_list,
    read_spans,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("F-1 through F-20", (("F-1", "F-20"),)),
        ("46–160", (("46", "160"),)),
        ("4-7, 9-10, 71-73", (("4", "7"), ("9", "10"), ("71", "73"))),
        ("2, 4–97,\n127–128,\n193–201", (("2", "2"), ("4", "97"), ("127", "128"), ("193", "201"))),
        ("55 through 119 of this Form 10-K", (("55", "119"),)),
        ("F – 1 to F – 3 and F-9", (("F-1", "F-3"), ("F-9", "F-9"))),
        ("10 and Item 7", (("10", "10"),)),
    ],
)
def test_read_spans(text, expected):
    assert read_spans(text)[0] == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("4–36, 121–127,\n129", PageList(spans=(("4", "36"), ("121", "127"), ("129", "129")))),
        ("201, 203–205 *", PageList(spans=(("201", "201"), ("203", "205")), footnote=True)),
        ("74, (a)", PageList(spans=(("74", "74"),), footnote=True)),
        ("**", PageList(footnote=True)),
        ("(b)", PageList(footnote=True)),
        ("Not Applicable", PageList(not_applicable=True)),
        ("None", PageList(not_applicable=True)),
        ("Business", None),
        ("See Note 3", None),
        ("", None),
    ],
)
def test_parse_page_list(text, expected):
    assert parse_page_list(text) == expected


def test_normalize_label():
    assert normalize_label("f – 3") == "F-3"
    assert normalize_label("II-252") == "II-252"


def _pages(*labels):
    """쪽마다 블록 3개(내용 2 + 쪽 경계 1)."""
    return [Page(start=index * 3, end=index * 3 + 2, label=label) for index, label in enumerate(labels)]


def test_ranges_cover_unlabelled_pages_in_between_and_merge_adjacent_pages():
    index = PageIndex(_pages("1", "2", None, "4", "5", "6"))
    assert index.ranges([("2", "4")]) == (((3, 11),), ())
    assert index.ranges([("1", "1"), ("2", "2"), ("6", "6")]) == (((0, 5), (15, 17)), ())


def test_missing_reversed_and_duplicate_labels_are_unresolved():
    index = PageIndex(_pages("1", "2", "3", "2"))
    assert index.is_ambiguous("2")
    assert index.ranges([("2", "3"), ("3", "1"), ("1", "9"), ("1", "1")]) == (((0, 2),), ("2–3", "3–1", "1–9"))


def test_lettered_section_runs_from_f1_to_the_last_f_page():
    index = PageIndex(_pages("98", "99", None, "F-1", "F-2", None, "F-3", "100", "F-9", None))
    assert index.lettered_section("F") == (9, 20)
    assert index.lettered_section("A") is None


def test_lettered_section_without_f1_starts_at_the_first_f_page():
    index = PageIndex(_pages("10", "F-2", "F-3"))
    assert index.lettered_section("f") == (3, 8)


def test_find_page_references():
    references = find_page_references(
        "Statements begin on page F-1. See pages 46–160 of this report and pages 5 to 7 of the Proxy Statement. "
        "Index on page F-1, et seq. Also page 30."
    )
    assert [(ref.spans, ref.open_ended, ref.external) for ref in references] == [
        ((("F-1", "F-1"),), True, False),
        ((("46", "160"),), False, False),
        ((("5", "7"),), False, True),
        ((("F-1", "F-1"),), True, False),
        ((("30", "30"),), False, False),
    ]


def test_lettered_section_from_a_given_page():
    index = PageIndex(_pages("II-1", "II-2", "II-3", "III-1"))
    assert index.lettered_section("II", "II-2") == (3, 8)
    assert index.lettered_section("II", "II-9") is None
