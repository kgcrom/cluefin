from cluefin_sec_notes import PAGE_REFERENCE_UNRESOLVED, extract_items, parse_filing

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
    assert len(result.item("15").ranges) == 1  # 문서 목록 Item
    market = result.item("7A")
    assert len(market.ranges) == 1 and market.incorporated_by_reference  # 다른 문서의 쪽

    unresolved = [finding for finding in result.findings if finding.code == PAGE_REFERENCE_UNRESOLVED]
    assert [finding.key.number for finding in unresolved] == ["1A"]


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
    assert len(result.item("8").ranges) == 1
    assert {finding.key.number for finding in result.findings if finding.code == PAGE_REFERENCE_UNRESOLVED} == {
        "1A",
        "8",
    }
