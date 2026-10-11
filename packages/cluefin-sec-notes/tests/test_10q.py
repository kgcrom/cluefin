"""10-Q: Part마다 Item 번호가 다시 시작한다. 합성 공시는 관찰한 레이아웃만 흉내 낸다."""

from cluefin_sec_notes import MISSING_ITEM, ItemKey, extract_items, parse_filing

COVER = (
    '<div style="display:none"><ix:header><ix:hidden>'
    '<ix:nonNumeric name="dei:DocumentType">10-Q</ix:nonNumeric>'
    '<ix:nonNumeric name="dei:DocumentPeriodEndDate">2025-09-30</ix:nonNumeric>'
    "</ix:hidden></ix:header></div><div>FORM 10-Q</div>"
)
BREAK = '<hr style="page-break-after:always"/>'
PARTS = {"I": "FINANCIAL INFORMATION", "II": "OTHER INFORMATION"}
ITEMS = (
    ("I", "1", "Financial Statements"),
    ("I", "2", "Management’s Discussion and Analysis of Financial Condition and Results of Operations"),
    ("I", "3", "Quantitative and Qualitative Disclosures About Market Risk"),
    ("I", "4", "Controls and Procedures"),
    ("II", "1", "Legal Proceedings"),
    ("II", "1A", "Risk Factors"),
    ("II", "2", "Unregistered Sales of Equity Securities and Use of Proceeds"),
    ("II", "3", "Defaults Upon Senior Securities"),
    ("II", "4", "Mine Safety Disclosures"),
    ("II", "5", "Other Information"),
    ("II", "6", "Exhibits"),
)


def anchor(part: str, number: str) -> str:
    return f"p{part.lower()}i{number.lower()}"


def toc(items=ITEMS) -> str:
    rows, part = [], None
    for item_part, number, title in items:
        if item_part != part:
            part = item_part
            rows.append(f"<tr><td>PART {part}</td><td>{PARTS[part]}</td><td></td></tr>")
        href = f"#{anchor(item_part, number)}"
        rows.append(f'<tr><td><a href="{href}">Item {number}.</a></td><td>{title}</td><td>{len(rows)}</td></tr>')
    return "<table>" + "".join(rows) + "</table>"


def body(items=ITEMS, *, anchored=True, combined_heading=False, after_part_two="") -> str:
    parts, part = [], None
    for item_part, number, title in items:
        heading = f"Item {number}. {title}"
        if item_part != part:
            part = item_part
            part_heading = f"PART {part} — {PARTS[part]}"
            if combined_heading:
                heading = f"{part_heading}<br/>{heading}"
            else:
                parts.append(BREAK + f'<div style="font-weight:700">{part_heading}</div>')
                if part == "II":
                    parts.append(after_part_two)
        tag = f'<div id="{anchor(item_part, number)}"></div>' if anchored else ""
        parts.append(f'{tag}<div style="font-weight:700">{heading}</div><div>Body of {item_part} {number}.</div>')
    return "".join(parts) + BREAK + "<div>SIGNATURES</div><div>signed</div>"


def filing(table_of_contents: str, content: str) -> str:
    return "<html><body>" + COVER + table_of_contents + content + "</body></html>"


def keys(result) -> list[str]:
    return [f"{item.key.part}:{item.key.number}" for item in result]


def test_toc_anchors_keep_part_one_and_part_two_items_apart():
    result = extract_items(parse_filing(filing(toc(), body())))
    assert result.catalog == "10-Q"
    assert keys(result) == [f"{part}:{number}" for part, number, _ in ITEMS]
    assert result.item("1", "II").text == "Item 1. Legal Proceedings\n\nBody of II 1."
    assert result.item("1", "I").text == "Item 1. Financial Statements\n\nBody of I 1."
    assert result.warnings == ()


def test_headings_without_part_take_the_part_heading_above_them():
    result = extract_items(parse_filing(filing("", body(anchored=False))))
    assert keys(result) == [f"{part}:{number}" for part, number, _ in ITEMS]
    assert result.item("1", "II").heading == "Item 1. Legal Proceedings"
    assert result.item("4", "I").text == "Item 4. Controls and Procedures\n\nBody of I 4."  # 뒤 Part 헤딩은 잘라 낸다


def test_part_and_item_in_one_heading_block():
    result = extract_items(parse_filing(filing("", body(anchored=False, combined_heading=True))))
    assert keys(result) == [f"{part}:{number}" for part, number, _ in ITEMS]
    assert result.item("1", "II").heading == "PART II — OTHER INFORMATION"


def test_omitted_part_two_items_are_not_confused_with_part_one_numbers():
    present = [item for item in ITEMS if item[:2] not in {("II", "3"), ("II", "4")}]
    note = "<div>Items 3 and 4 of Part II are not applicable and have been omitted.</div>"
    result = extract_items(parse_filing(filing(toc(present), body(present, after_part_two=note))))
    assert {ItemKey("II", "3"), ItemKey("II", "4")} <= set(result.omitted)
    assert MISSING_ITEM not in {finding.code for finding in result.warnings}


def test_toc_link_to_the_other_parts_heading_is_not_trusted():
    """Part I Item 4 링크가 Part II "Item 4." 앵커를 가리키는 작성 오류."""
    wrong = toc().replace(f'href="#{anchor("I", "4")}"', f'href="#{anchor("II", "4")}"')
    result = extract_items(parse_filing(filing(wrong, body())))
    assert result.item("4", "I").text == "Item 4. Controls and Procedures\n\nBody of I 4."
    assert result.item("4", "II").heading == "Item 4. Mine Safety Disclosures"


def test_item_4t_is_item_4_and_part_two_only_numbers_survive_a_missing_part_heading():
    content = (
        body(anchored=False)
        .replace("Item 4. Controls and Procedures", "Item 4T. Controls and Procedures")
        .replace('<div style="font-weight:700">PART II — OTHER INFORMATION</div>', "")
    )
    result = extract_items(parse_filing(filing("", content)))
    assert result.item("4", "I").heading == "Item 4T. Controls and Procedures"
    assert result.item("5", "II") is not None and result.item("6", "II") is not None  # Part II에만 있는 번호


def test_part_headings_of_a_text_toc_do_not_label_body_items():
    """링크 없는 목차에 "PART I"·"PART II" 헤딩과 Item 표가 있고, 본문은 Part I 헤딩 없이 "Item 1."부터 시작한다."""
    rows = "".join(f"<tr><td>Item {number}.</td><td>{title}</td></tr>" for part, number, title in ITEMS if part == "I")
    rows_two = "".join(
        f"<tr><td>Item {number}.</td><td>{title}</td></tr>" for part, number, title in ITEMS if part == "II"
    )
    text_toc = (
        f"<div>PART I — FINANCIAL INFORMATION</div><table>{rows}</table>"
        f"<div>PART II — OTHER INFORMATION</div><table>{rows_two}</table>"
    )
    content = body(anchored=False).replace('<div style="font-weight:700">PART I — FINANCIAL INFORMATION</div>', "", 1)
    result = extract_items(parse_filing(filing(text_toc, content)))
    assert keys(result) == [f"{part}:{number}" for part, number, _ in ITEMS]


def test_statement_index_table_heads_part_one_item_one():
    """재무제표 앞 색인 쪽이 Part·Item 1 헤딩을 겸하는 표."""
    index = (
        "<table><tr><td></td><td>Page</td></tr><tr><td>PART I — FINANCIAL INFORMATION</td><td></td></tr>"
        "<tr><td>Item 1. Financial Statements (unaudited)</td><td></td></tr>"
        "<tr><td>Consolidated Balance Sheets</td><td>3</td></tr><tr><td>Consolidated Statements of Income</td><td>4</td></tr>"
        "<tr><td>Notes to Consolidated Financial Statements</td><td>5</td></tr></table>"
    )
    content = body(anchored=False).replace(
        '<div style="font-weight:700">PART I — FINANCIAL INFORMATION</div><div style="font-weight:700">Item 1. Financial Statements</div>',
        index,
    )
    result = extract_items(parse_filing(filing("", content)))
    statements = result.item("1", "I")
    assert statements is not None and statements.text.endswith("Body of I 1.")
    assert statements.method == "pattern"
    assert keys(result) == [f"{part}:{number}" for part, number, _ in ITEMS]


def test_statements_without_heading_right_after_the_toc():
    """목차 다음 쪽에 "Item 1." 헤딩 없이 재무상태표부터 싣는 10-Q."""
    statements = "<table><tr><td>Balance Sheet</td><td>2026</td></tr><tr><td>Cash</td><td>$1</td></tr></table>"
    content = body(anchored=False).replace(
        '<div style="font-weight:700">PART I — FINANCIAL INFORMATION</div><div style="font-weight:700">Item 1. Financial Statements</div><div>Body of I 1.</div>',
        statements,
    )
    text_toc = "<table>" + "".join(f"<tr><td>Item {n}.</td><td>{t}</td></tr>" for _, n, t in ITEMS) + "</table>"
    result = extract_items(parse_filing(filing(text_toc, content)))
    statements_item = result.item("1", "I")
    assert statements_item.method == "statements_after_toc"
    assert statements_item.text.startswith("Balance Sheet\t2026")
    assert result.item("2", "I").heading.startswith("Item 2.")
