import pytest

from cluefin_sec_notes import (
    EMPTY_ITEM,
    MISSING_ITEM,
    NON_SEQUENTIAL_LAYOUT,
    TOC_NOT_FOUND,
    TOC_TARGET_MISSING,
    UNKNOWN_ITEM,
    ItemKey,
    extract_items,
    parse_filing,
)


def extract(html: str, form: str | None = None):
    return extract_items(parse_filing(html, form=form))


def test_workiva_toc_finds_every_item_with_its_body(synthetic):
    result = extract(synthetic.filing())
    assert [item.key.number for item in result] == [number for _, number, _ in synthetic.TOC_ITEMS]
    assert result.missing == ()
    assert result.warnings == ()
    risk = result.item("1A")
    assert risk.key == ItemKey("I", "1A")
    assert risk.title == "Risk Factors"
    assert risk.method == "toc_anchor"
    assert risk.heading == "Item 1A. Risk Factors"
    assert risk.text == "Item 1A. Risk Factors\n\nBody of item 1A."


def test_toc_region_is_excluded_and_last_item_ends_at_signatures(synthetic):
    result = extract(synthetic.filing())
    summary = result.item("16")
    assert summary.text == "Item 16. Form 10-K Summary\n\nBody of item 16."


def test_paragraph_toc_with_title_only_links(synthetic):
    toc = "".join(
        f'<p><a href="#{synthetic.anchor_id(number)}">{title}</a></p>' for _, number, title in synthetic.TOC_ITEMS
    )
    result = extract(synthetic.filing(toc=toc))
    assert len(result) == len(synthetic.TOC_ITEMS)
    assert result.item("7").heading.startswith("Item 7. Management")


def test_combined_heading_shares_one_range(synthetic):
    items = [("I", "1", "Business"), ("I", "2", "Properties"), ("I", "3", "Legal Proceedings")]
    toc = (
        '<table><tr><td><a href="#b">Items 1 and 2. Business and Properties</a></td><td>1</td></tr>'
        '<tr><td><a href="#c">Item 3. Legal Proceedings</a></td><td>9</td></tr>'
        '<tr><td><a href="#d">Item 4. Mine Safety Disclosures</a></td><td>9</td></tr></table>'
    )
    content = (
        '<div id="b"></div><p>Items 1 and 2. Business and Properties</p><p>We make things.</p>'
        '<div id="c"></div><p>Item 3. Legal Proceedings</p><p>None pending.</p>'
        '<div id="d"></div><p>Item 4. Mine Safety Disclosures</p><p>Not applicable.</p>'
    )
    result = extract(synthetic.filing(toc=toc, content=content))
    business, properties = result.item("1"), result.item("2")
    assert (business.start, business.end) == (properties.start, properties.end)
    assert business.shared_with == (ItemKey("I", "2"),)
    assert properties.shared_with == (ItemKey("I", "1"),)
    assert properties.text == "Items 1 and 2. Business and Properties\n\nWe make things."
    assert items[2][1] == "3"


def test_link_to_page_top_moves_down_to_the_heading(synthetic):
    # 9·9A가 한 페이지이고 두 링크가 모두 페이지 맨 위(머리말 앞)를 가리킨다.
    toc = (
        '<table><tr><td><a href="#p1">Item 8. Financial Statements</a></td></tr>'
        '<tr><td><a href="#p2">Item 9. Changes in and Disagreements</a></td></tr>'
        '<tr><td><a href="#p2">Item 9A. Controls and Procedures</a></td></tr></table>'
    )
    content = (
        '<div id="p1"></div><p>Item 8. Financial Statements</p><p>statements</p><hr/>'
        '<div id="p2"></div><p>Table of Contents</p><p>Item 9. Changes</p><p>None.</p>'
        "<p>Item 9A. Controls and Procedures</p><p>Effective.</p>"
    )
    result = extract(synthetic.filing(toc=toc, content=content))
    assert result.item("9").text == "Item 9. Changes\n\nNone."
    assert result.item("9A").text == "Item 9A. Controls and Procedures\n\nEffective."
    assert "앵커 블록" in result.item("9A").evidence


def test_missing_target_is_reported_and_heading_fills_the_gap(synthetic):
    content = synthetic.body().replace(f'<div id="{synthetic.anchor_id("7A")}"></div>', "")
    result = extract(synthetic.filing(content=content))
    market_risk = result.item("7A")
    assert market_risk.method == "pattern"
    assert market_risk.text == "Item 7A. Quantitative and Qualitative Disclosures About Market Risk\n\nBody of item 7A."
    assert (
        result.item("7").text
        == "Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations\n\nBody of item 7."
    )
    assert {finding.code for finding in result.warnings} == {TOC_TARGET_MISSING}


def test_without_any_heading_the_item_is_missing_not_guessed(synthetic):
    content = synthetic.body().replace(f'<div id="{synthetic.anchor_id("7A")}"></div>', "").replace("Item 7A. ", "")
    result = extract(synthetic.filing(content=content))
    assert result.item("7A") is None
    assert ItemKey("II", "7A") in result.missing
    assert {finding.code for finding in result.warnings} == {TOC_TARGET_MISSING, MISSING_ITEM}
    assert result.item("7").text.endswith("Body of item 7A.")


def test_items_before_their_since_date_are_not_missing(synthetic):
    old = [item for item in synthetic.TOC_ITEMS if item[1] not in ("1A", "1B", "1C", "9A", "9B", "9C", "16")]
    html = synthetic.filing(toc=synthetic.workiva_toc(old), content=synthetic.body(old)).replace(
        "2025-12-31", "2002-12-31"
    )
    result = extract(html)
    assert result.missing == ()


def test_amendment_missing_items_are_not_warned(synthetic):
    part_three = [item for item in synthetic.TOC_ITEMS if item[0] == "III"]
    html = synthetic.filing(toc=synthetic.workiva_toc(part_three), content=synthetic.body(part_three))
    result = extract(html, form="10-K/A")
    assert len(result.missing) == 17  # Part III 5개와 선택 Item 16을 뺀 나머지
    assert result.warnings == ()


def test_without_toc_headings_are_found_by_pattern(synthetic):
    result = extract(synthetic.filing(toc="", content=synthetic.body(anchored=False)))
    assert TOC_NOT_FOUND in {finding.code for finding in result.findings}
    assert len(result) == len(synthetic.TOC_ITEMS)
    assert {item.method for item in result} == {"pattern"}
    assert result.warnings == ()


def test_non_sequential_layout_is_accepted_and_warned(synthetic):
    items = [item for item in synthetic.TOC_ITEMS if item[1] in ("1", "1A", "7", "8")]
    content = synthetic.body([items[0], items[2], items[1], items[3]])
    result = extract(synthetic.filing(toc=synthetic.workiva_toc(items), content=content))
    assert [item.key.number for item in result] == ["1", "7", "1A", "8"]
    assert NON_SEQUENTIAL_LAYOUT in {finding.code for finding in result.warnings}


def test_heading_only_item_is_empty_but_reserved_is_not(synthetic):
    items = [("II", "5", "Market"), ("II", "6", "[Reserved]"), ("II", "7", "Management’s Discussion")]
    content = (
        f'<div id="{synthetic.anchor_id("5")}"></div><p>Item 5. Market for Registrant’s Common Equity, Related Stockholder '
        "Matters and Issuer Purchases of Equity Securities</p>"
        f'<div id="{synthetic.anchor_id("6")}"></div><p>Item 6. [Reserved]</p>'
        f'<div id="{synthetic.anchor_id("7")}"></div><p>Item 7. MD&amp;A</p><p>text</p>'
    )
    result = extract(synthetic.filing(toc=synthetic.workiva_toc(items), content=content))
    empty = [finding.key.number for finding in result.findings if finding.code == EMPTY_ITEM]
    assert empty == ["5"]


def test_unsupported_form_raises(synthetic):
    with pytest.raises(ValueError, match="20-F"):
        extract("<p>x</p>", form="20-F")


def test_pattern_chain_skips_cross_reference_paragraphs(synthetic):
    content = (
        "<p>Item 1. Business</p><p>We make things.</p>"
        "<p>Item 7 of this report discusses results in detail and should be read with the risk factors.</p>"
        "<p>Item 1A. Risk Factors</p><p>Risks.</p>"
        "<p>Item 7. Management’s Discussion and Analysis</p><p>Results.</p>"
        "<p>Item 8. Financial Statements and Supplementary Data</p><p>Numbers.</p>"
    )
    result = extract(synthetic.filing(toc="", content=content))
    assert [(item.key.number, item.heading) for item in result] == [
        ("1", "Item 1. Business"),
        ("1A", "Item 1A. Risk Factors"),
        ("7", "Item 7. Management’s Discussion and Analysis"),
        ("8", "Item 8. Financial Statements and Supplementary Data"),
    ]
    assert result.item("1").text == (
        "Item 1. Business\n\nWe make things.\n\n"
        "Item 7 of this report discusses results in detail and should be read with the risk factors."
    )


def test_text_toc_without_links_is_not_taken_for_headings(synthetic):
    toc = "<p>Item 1. Business 3</p><p>Item 1A. Risk Factors 9</p><p>Item 2. Properties 20</p><p>Item 3. Legal 21</p>"
    content = "<p>Item 1. Business</p><p>a</p><p>Item 1A. Risk Factors</p><p>b</p><p>Item 2. Properties</p><p>c</p><p>Item 3. Legal Proceedings</p><p>d</p>"
    result = extract(synthetic.filing(toc=toc, content=content))
    assert result.item("1").text == "Item 1. Business\n\na"
    assert result.item("3").text == "Item 3. Legal Proceedings\n\nd"


def test_long_paragraph_counts_as_heading_only_when_title_follows(synthetic):
    risk = "Item 1A. Risk Factors. " + "Our business faces risks. " * 20
    cross = "Item 7 describes " + "results of operations in more detail. " * 20
    content = f"<p>Item 1. Business</p><p>a</p><p>{risk}</p><p>{cross}</p><p>Item 2. Properties</p><p>c</p>"
    result = extract(synthetic.filing(toc="", content=content))
    assert [item.key.number for item in result] == ["1", "1A", "2"]
    assert result.item("1A").text.startswith("Item 1A. Risk Factors. Our business")


def test_unknown_item_is_reported(synthetic):
    content = "<p>Item 1. Business</p><p>a</p><p>Item 1D. Artificial Intelligence</p><p>b</p><p>Item 2. Properties</p><p>c</p>"
    result = extract(synthetic.filing(toc="", content=content))
    unknown = [finding for finding in result.warnings if finding.code == UNKNOWN_ITEM]
    assert [finding.message for finding in unknown] == ["카탈로그에 없는 Item: 'Item 1D. Artificial Intelligence'"]
    assert result.item("1").text == "Item 1. Business\n\na\n\nItem 1D. Artificial Intelligence\n\nb"


def test_incorporated_by_reference_items(synthetic):
    content = (
        "<p>Item 9B. Other Information</p><p>None.</p><p>PART III</p>"
        "<p>Item 10. Directors, Executive Officers and Corporate Governance</p>"
        "<p>The information required by this item will be included in our Proxy Statement for the 2026 annual "
        "meeting and is incorporated herein by reference.</p>"
        "<p>Item 11. Executive Compensation</p><p>Refer to pages 12 through 21 of the Proxy Statement, which are "
        "incorporated herein by reference.</p>"
        "<p>Item 12. Security Ownership</p><p>" + "A long table of owners. " * 200 + "incorporated by reference.</p>"
    )
    result = extract(synthetic.filing(toc="", content=content))
    assert [(item.key.number, item.incorporated_by_reference) for item in result] == [
        ("9B", False),
        ("10", True),
        ("11", True),
        ("12", False),
    ]
    # 다음 Part 헤딩은 앞 Item 끝에서 잘라 낸다.
    assert result.item("9B").text == "Item 9B. Other Information\n\nNone."
