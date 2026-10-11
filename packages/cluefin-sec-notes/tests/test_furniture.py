from cluefin_sec_notes import PAGE_FURNITURE, Page, parse_filing

BREAK = '<hr style="page-break-after:always"/>'


def page(number: int, *body: str, header: str = "Example Corp | 2025 Form 10-K") -> str:
    return f"<p>{header}</p>" + "".join(f"<p>{text}</p>" for text in body) + f"<p>{number}</p>" + BREAK


def test_repeated_headers_and_page_numbers_are_removed_with_page_labels():
    html = (
        page(1, "Item 1. Business", "We make things.")
        + page(2, "More business.")
        + page(3, "Item 1A. Risk Factors", "Risks.")
    )
    document = parse_filing(html)
    assert [block.text for block in document.blocks if hasattr(block, "text")] == [
        "Item 1. Business",
        "We make things.",
        "More business.",
        "Item 1A. Risk Factors",
        "Risks.",
    ]
    assert document.pages == (Page(0, 2, "1"), Page(3, 4, "2"), Page(5, 7, "3"))
    assert document.report.count(PAGE_FURNITURE) == 6


def test_item_headings_are_compared_verbatim_not_as_numbers():
    # 쪽마다 새 Item이 시작해도("Item 7.", "Item 8.", "Item 9.") 숫자를 지워 같은 줄로 보지 않는다.
    html = page(1, "Item 7.", "a") + page(2, "Item 8.", "b") + page(3, "Item 9.", "c")
    texts = [block.text for block in parse_filing(html).blocks if hasattr(block, "text")]
    assert texts == ["Item 7.", "a", "Item 8.", "b", "Item 9.", "c"]


def test_running_item_header_repeated_verbatim_is_removed():
    html = (
        page(1, "body one", header="Item 1A")
        + page(2, "body two", header="Item 1A")
        + page(3, "body three", header="Item 1A")
    )
    assert [block.text for block in parse_filing(html).blocks if hasattr(block, "text")] == [
        "body one",
        "body two",
        "body three",
    ]


def test_page_number_from_repeated_footer_text():
    html = "".join(page(number, "Body text.", header="") for number in (1, 2, 3))
    for number in (1, 2, 3):
        html = html.replace(f"<p>{number}</p>", f"<p>{number + 4} December 2025 Form 10-K</p>")
    document = parse_filing(html)
    assert [page.label for page in document.pages] == ["5", "6", "7"]
    # 마침표로 끝나는 문장은 쪽 끝에 반복돼도 본문이다.
    assert [block.text for block in document.blocks if hasattr(block, "text")] == ["Body text."] * 3


def test_anchor_on_removed_header_moves_to_next_block():
    html = '<a href="#p2">go</a>' + page(1, "first") + '<div id="p2"></div>' + page(2, "second") + page(3, "third")
    document = parse_filing(html)
    assert document.blocks[document.anchors["p2"]].text == "second"


def test_without_page_breaks_nothing_is_removed():
    document = parse_filing("<p>1</p><p>body</p><p>2</p>")
    assert [block.text for block in document.blocks] == ["1", "body", "2"]
    assert document.pages == ()
