import pytest

from cluefin_sec_notes import FORM_10K, ItemLabel, match_title, normalize_title, parse_item_label
from cluefin_sec_notes._labels import parse_part


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Item 1A. Risk Factors", ItemLabel(None, ("1A",), "Risk Factors")),
        ("ITEM 7A:QUANTITATIVE", ItemLabel(None, ("7A",), "QUANTITATIVE")),
        ("Item 1.Business", ItemLabel(None, ("1",), "Business")),
        ("item 1a — risk", ItemLabel(None, ("1A",), "risk")),
        ("Items 1 and 2. Business and Properties", ItemLabel(None, ("1", "2"), "Business and Properties")),
        ("ITEMS 1. AND 2.\tBUSINESS AND PROPERTIES", ItemLabel(None, ("1", "2"), "BUSINESS AND PROPERTIES")),
        ("Items 10, 11, 12, and 13 for each", ItemLabel(None, ("10", "11", "12", "13"), "for each")),
        ("Items 10 through 14.", ItemLabel(None, ("10", "11", "12", "13", "14"), "")),
        ("Item 9A(T). Controls", ItemLabel(None, ("9A",), "Controls")),
        ("Item 2.02 Results of Operations", ItemLabel(None, ("2.02",), "Results of Operations")),
        ("PART II, Item 7. MD&A", ItemLabel("II", ("7",), "MD&A")),
        ("Part I — Item 1", ItemLabel("I", ("1",), "")),
    ],
)
def test_parse_item_label(text, expected):
    assert parse_item_label(text) == expected


@pytest.mark.parametrize("text", ["See Item 7 for details", "Itemized deductions", "Item", "Items 1A1"])
def test_not_an_item_label(text):
    assert parse_item_label(text) is None


def test_parse_part():
    assert parse_part("PART II — OTHER INFORMATION") == "II"
    assert parse_part("Part IV") == "IV"
    assert parse_part("Partnership") is None


def test_normalize_title():
    assert normalize_title("Management’s Discussion  &  Analysis") == "management s discussion analysis"


def test_match_title_prefers_longest_title():
    assert match_title(FORM_10K, "Quantitative and Qualitative Disclosures About Market Risk 45").number == "7A"
    assert (
        match_title(
            FORM_10K, "MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS"
        ).number
        == "7"
    )
    assert match_title(FORM_10K, "Submission of Matters to a Vote of Security Holders").number == "4"
    assert match_title(FORM_10K, "Business Overview") is None
    assert match_title(FORM_10K, "Business Segments 5") is None
    assert match_title(FORM_10K, "Risk Factors 1A 13").number == "1A"  # 제목 | Item | 페이지 칸
    assert match_title(FORM_10K, "Business I 1 5").number == "1"  # 제목 | Part | Item | 페이지 칸
    assert match_title(FORM_10K, "Properties II-25").number == "2"
    assert match_title(FORM_10K, "Business").number == "1"
