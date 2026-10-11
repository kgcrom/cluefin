import pytest

from cluefin_sec_notes import PAGE_REFERENCE_UNRESOLVED, UncertainItemError, extract_items, parse_filing

BREAK = '<hr style="page-break-after:always"/>'


def page(label: str, *paragraphs: str) -> str:
    return "".join(f"<div>{text}</div>" for text in paragraphs) + f"<div>{label}</div>" + BREAK


def filing(*pages: str) -> str:
    return "<html><body><div>FORM 10-K</div>" + BREAK + "".join(pages) + "</body></html>"


PAGES = (
    page(
        "1",
        "Item 1. Business",
        "We make things.",
        "Item 1A. Risk Factors",
        "Risk factors appear on pages 30 through 31.",
    ),
    page(
        "2",
        "Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations",
        "Management’s discussion appears on pages 5–6. Read it with the statements on pages F-1 through F-2.",
        "Item 7A. Quantitative and Qualitative Disclosures About Market Risk",
        "Refer to pages 5 through 6 of the Annual Report to Shareholders, incorporated herein by reference.",
        "Item 8. Financial Statements and Supplementary Data",
        "The financial statements begin on page F-1 and are incorporated herein by reference.",
    ),
    page("3", "Item 9A. Controls and Procedures", "Our controls work.", "Management’s report is on page F-2."),
    page("4", "Item 15. Exhibits and Financial Statement Schedules", "Financial statements: pages F-1 through F-2."),
    page("5", "MD&A part one."),
    page("6", "MD&A part two."),
    page("7", "SIGNATURES", "Signed."),
    page("F-1", "Balance sheet."),
    page("F-2", "Notes to the statements."),
)


def test_items_follow_page_references_into_the_same_document():
    result = extract_items(parse_filing(filing(*PAGES)))

    mdna = result.item("7")
    assert len(mdna.ranges) == 2
    assert mdna.text.endswith("MD&A part one.\n\nMD&A part two.")  # 둘째 참조(F-쪽)는 따르지 않는다

    statements = result.item("8")
    assert statements.text.endswith("Balance sheet.\n\nNotes to the statements.")
    assert not statements.incorporated_by_reference  # 본문이 이 문서에 있다

    assert len(result.item("9A").ranges) == 1  # 쪽 하나는 곁가지 참조
    # 문서 목록 Item: 쪽 참조를 따르지 않고, 뒤에 붙은 MD&A 쪽(Item 7이 가져감)도 빼다
    assert (
        result.item("15").text
        == "Item 15. Exhibits and Financial Statement Schedules\n\nFinancial statements: pages F-1 through F-2."
    )
    market = result.item("7A")
    assert len(market.ranges) == 1 and market.incorporated_by_reference  # 다른 문서의 쪽

    unresolved = [finding for finding in result.findings if finding.code == PAGE_REFERENCE_UNRESOLVED]
    assert [finding.key.number for finding in unresolved] == ["1A"]


def test_exhibit_index_after_the_f_pages_stays_in_the_exhibits_item():
    pages = [
        *PAGES[:6],
        page("F-1", "Balance sheet."),
        page("F-2", "Notes to the statements."),
        "<div>EXHIBIT INDEX</div>",
    ]
    pages.append(page("7", "SIGNATURES", "Signed."))
    result = extract_items(parse_filing(filing(*pages)))
    assert result.item("8").text.endswith("Balance sheet.\n\nNotes to the statements.")
    exhibits = result.item("15")
    assert len(exhibits.ranges) == 2
    assert exhibits.text.endswith("Financial statements: pages F-1 through F-2.\n\nEXHIBIT INDEX")


def test_statements_item_takes_f_pages_without_page_numbers():
    pages = list(PAGES)
    pages[1] = page(
        "2",
        "Item 8. Financial Statements and Supplementary Data",
        "This information appears following Item 15 of this Report.",
    )
    result = extract_items(parse_filing(filing(*pages)))
    assert result.item("8").text.endswith("Balance sheet.\n\nNotes to the statements.")


def test_f_pages_starting_with_another_items_heading_skip_that_heading():
    pages = list(PAGES)
    pages[3] = ""
    pages[7] = page("F-1", "Item 15. Exhibits and Financial Statement Schedules", "Balance sheet.")
    result = extract_items(parse_filing(filing(*pages)))
    statements = result.item("8")
    assert "Item 15." not in statements.text
    assert statements.text.endswith("Balance sheet.\n\nNotes to the statements.")


def test_without_page_numbers_nothing_is_added():
    html = filing(*PAGES).replace("<div>F-1</div>", "").replace("<div>F-2</div>", "")
    result = extract_items(parse_filing(html))
    with pytest.raises(UncertainItemError):
        result.item("8")
    assert len(result.item("8", strict=False).ranges) == 1
    assert {finding.key.number for finding in result.findings if finding.code == PAGE_REFERENCE_UNRESOLVED} == {
        "1A",
        "8",
    }


def _index_table(*rows: tuple[str, ...]) -> str:
    return (
        "<table>" + "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows) + "</table>"
    )


def test_cross_reference_index_sets_item_ranges_from_page_numbers():
    index = _index_table(
        ("Item Number", "", "Page"),
        ("Part I", "", ""),
        ("1.", "Business", "2, 4"),
        ("1A.", "Risk Factors", "3"),
        ("1B.", "Unresolved Staff Comments", "Not Applicable"),
        ("Part III", "", ""),
        ("11.", "Executive Compensation", "**"),
        ("15.", "Exhibits and Financial Statement Schedules", "99"),
    )
    html = filing(
        f"<div>FORM 10-K CROSS-REFERENCE INDEX</div>{index}<div>1</div>{BREAK}",
        page("2", "OVERVIEW", "We make things."),
        page("3", "RISK FACTORS", "Things may go wrong."),
        page("4", "MORE ABOUT THE BUSINESS", "We sell things."),
    )
    result = extract_items(parse_filing(html))

    business = result.item("1")
    assert business.method == "cross_reference"
    assert business.text == "OVERVIEW\n\nWe make things.\n\nMORE ABOUT THE BUSINESS\n\nWe sell things."
    assert result.item("1A").text == "RISK FACTORS\n\nThings may go wrong."
    assert {key.number for key in result.omitted} >= {"1B", "11"}  # 공시가 이 문서에 없다고 밝혔다
    assert not {finding.key.number for finding in result.warnings if finding.key} & {"1B", "11"}
    unresolved = [finding for finding in result.findings if finding.code == PAGE_REFERENCE_UNRESOLVED]
    assert [finding.key.number for finding in unresolved] == ["15"]
