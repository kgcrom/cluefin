"""8-K: 사건마다 해당 Item만 있다. 정답은 제출 이력의 Item 목록(`sec_items`)."""

from datetime import date

from cluefin_sec_notes import FORM_8K, UNKNOWN_ITEM, extract_items, parse_filing
from cluefin_sec_notes._expectations import invariant_violations

BREAK = '<hr style="page-break-after:always"/>'


def filing(report_date: str, *sections: tuple[str, str]) -> str:
    cover = (
        f"<div>FORM 8-K</div><div>CURRENT REPORT</div><div>Date of Report (Date of earliest event reported): {report_date}</div>"
        "<div>Check the appropriate box below if the Form 8-K filing is intended to simultaneously satisfy …</div>"
    )
    body = "".join(
        f'<table><tr><td style="font-weight:700">{heading}</td></tr></table><div>{text}</div>'
        for heading, text in sections
    )
    return "<html><body>" + cover + BREAK + body + "<div>SIGNATURES</div><div>signed</div></body></html>"


EARNINGS = filing(
    "May 1, 2025",
    (
        "Item 2.02 Results of Operations and Financial Condition.",
        "The press release is furnished as Exhibit 99.1. This information shall not be deemed “filed” and shall not be "
        "incorporated by reference into any filing.",
    ),
    ("Item 9.01 Financial Statements and Exhibits.", "(d) Exhibits. 99.1 Press release."),
)


def test_event_items_and_furnished_information_is_not_incorporated():
    result = extract_items(parse_filing(EARNINGS))
    assert result.catalog == "8-K"
    assert [item.key.number for item in result] == ["2.02", "9.01"]
    assert result.item("2.02").title == "Results of Operations and Financial Condition"
    assert not result.item("2.02").incorporated_by_reference  # "shall not be incorporated by reference"
    assert result.missing == () and result.warnings == ()
    assert invariant_violations(result, sec_items=["2.02", "9.01"]) == []
    assert invariant_violations(result, sec_items=["2.02", "7.01"]) == ["extra:9.01", "missing:7.01"]


def test_items_before_2004_use_the_old_numbering():
    result = extract_items(
        parse_filing(
            filing(
                "March 3, 2003",
                ("Item 5. Other Events.", "The company announced a dividend."),
                ("Item 7. Financial Statements and Exhibits.", "(c) Exhibits. 99 Press release."),
            )
        )
    )
    assert [(item.key.number, item.title) for item in result] == [
        ("5", "Other Events"),
        ("7", "Financial Statements and Exhibits"),
    ]
    assert UNKNOWN_ITEM not in {finding.code for finding in result.findings}


def test_old_and_new_numbering_apply_by_date():
    legacy, current = FORM_8K.spec(None, "5"), FORM_8K.spec(None, "5.02")
    assert legacy.applies_to(date(2004, 8, 22)) and not legacy.applies_to(date(2004, 8, 23))
    assert current.applies_to(date(2004, 8, 23)) and not current.applies_to(date(2004, 8, 22))
