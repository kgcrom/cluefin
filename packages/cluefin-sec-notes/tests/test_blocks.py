from cluefin_sec_notes import HIDDEN_CONTENT, LAYOUT_TABLE, Link, PageBreak, Paragraph, Table, parse_filing


def blocks(html: str):
    return parse_filing(html).blocks


def test_whitespace_and_nbsp_collapse_and_br_becomes_newline():
    (paragraph,) = blocks("<p>  Item&#160;1A.\n   Risk <br/> Factors </p>")
    assert paragraph.text == "Item 1A. Risk\nFactors"


def test_bold_from_tags_and_font_weight():
    result = blocks(
        '<div><span style="font-weight:700">Item 7.</span> <b>MD&amp;A</b></div>'
        '<div><span style="font-weight:700">Item 8.</span> Financial</div>'
        '<div style="font-weight:bold"><span style="font-weight:400">not bold</span></div>'
    )
    assert [(block.text, block.bold) for block in result] == [
        ("Item 7. MD&A", True),
        ("Item 8. Financial", False),
        ("not bold", False),
    ]


def test_font_size_is_the_size_of_most_characters():
    result = blocks(
        '<div style="font-size:10pt">body <span style="font-size:14pt">Big heading text</span></div>'
        '<p style="font-size:16px">px</p><font size="4">font tag</font><h2>heading</h2>'
    )
    assert [block.font_size for block in result] == [14.0, 12.0, 13.5, 18.0]
    assert result[3].bold


def test_align_from_style_or_attribute():
    result = blocks('<div style="text-align:center">a</div><p align="RIGHT">b</p><p>c</p>')
    assert [block.align for block in result] == ["center", "right", None]


def test_pre_splits_paragraphs_on_blank_lines():
    result = blocks("<pre>ITEM 1.  BUSINESS\n\nThe Company\nmakes things.\n   \nNext</pre>")
    assert [block.text for block in result] == ["ITEM 1. BUSINESS", "The Company\nmakes things.", "Next"]


def test_anchor_on_empty_div_goes_to_next_block():
    document = parse_filing(
        '<a href="#item1a">Risk Factors</a><p>toc end</p>'
        '<div id="item1a"></div><div id="untargeted"><span>Item 1A. Risk Factors</span></div><p>body</p>'
    )
    heading = document.blocks[2]
    assert heading.text == "Item 1A. Risk Factors"
    assert heading.anchors == ("item1a",)
    assert document.anchors == {"item1a": 2}


def test_a_name_anchor_and_trailing_anchor():
    document = parse_filing('<a href="#x">x</a><a href="#end">e</a><p><a name="x"></a>Item 2</p><div id="end"></div>')
    assert document.anchors == {"x": 1, "end": 2}


def test_links_are_recorded_with_text():
    (paragraph,) = blocks('<p><a href="#i1">Item 1.</a> <a href="https://sec.gov">x</a></p>')
    assert paragraph.links == (Link(target="i1", text="Item 1."),)


def test_ix_header_is_hidden_and_dei_collected():
    document = parse_filing(
        '<div style="display:none"><ix:header><ix:hidden>'
        '<ix:nonNumeric name="dei:DocumentType" contextRef="c">10-K</ix:nonNumeric>'
        "</ix:hidden></ix:header></div>"
        '<p>Name: <ix:nonNumeric name="dei:EntityRegistrantName" contextRef="c">Example Corp</ix:nonNumeric></p>'
    )
    assert [block.text for block in document.blocks] == ["Name: Example Corp"]
    assert document.dei == {"DocumentType": "10-K", "EntityRegistrantName": "Example Corp"}
    assert document.form == "10-K"
    assert document.report.fix(HIDDEN_CONTENT).samples[0].context == "<div> 10-K"


def test_empty_hidden_cells_are_dropped_silently():
    document = parse_filing(
        '<table><tr><td style="display:none"/><td>a</td><td>b</td></tr>'
        '<tr><td style="display:none">secret</td><td>c</td><td>d</td></tr></table>'
    )
    (table,) = document.blocks
    assert [[cell.text for cell in row] for row in table.rows] == [["a", "b"], ["c", "d"]]
    assert document.report.count(HIDDEN_CONTENT) == 1


def test_data_table_keeps_spans_bold_and_multi_paragraph_cells():
    (table,) = blocks(
        '<table><tr><th colspan="2"><b>Header</b></th></tr>'
        '<tr><td rowspan="2"><p>line one</p><p>line two</p></td><td>$</td></tr><tr><td>1</td></tr></table>'
    )
    assert isinstance(table, Table)
    assert [(cell.text, cell.col_span, cell.row_span, cell.bold) for row in table.rows for cell in row] == [
        ("Header", 2, 1, True),
        ("line one\nline two", 1, 2, False),
        ("$", 1, 1, False),
        ("1", 1, 1, False),
    ]


def test_heading_laid_out_as_table_row():
    (table,) = blocks("<table><tr><td>Item 1.</td><td></td><td>Business</td></tr></table>")
    assert table.row_text(0) == "Item 1. Business"


def test_layout_tables_are_unwrapped():
    document = parse_filing(
        "<table><tr><td><p>Item 1. Business</p><p>body</p></td></tr></table>"
        "<table><tr><td>side</td><td><table><tr><td>x</td><td>y</td></tr></table></td></tr></table>"
    )
    kinds = [(type(block).__name__, getattr(block, "text", None)) for block in document.blocks]
    assert kinds == [
        ("Paragraph", "Item 1. Business"),
        ("Paragraph", "body"),
        ("Paragraph", "side"),
        ("Table", None),
    ]
    assert document.report.count(LAYOUT_TABLE) == 2


def test_anchor_inside_table_goes_to_table_and_empty_table_passes_it_on():
    document = parse_filing(
        '<a href="#a">a</a><a href="#b">b</a>'
        '<table><tr><td id="a"></td><td></td></tr></table>'
        '<table><tr><td><a name="b"></a>Item 2.</td><td>Properties</td></tr></table>'
    )
    assert document.anchors == {"a": 1, "b": 1}
    assert document.blocks[1].anchors == ("a", "b")


def test_page_breaks_from_style_and_hr_collapse():
    result = blocks(
        '<p>first</p><div style="page-break-after:always"></div><hr/>'
        '<p style="page-break-before: always">second</p><hr><p>third</p>'
    )
    assert [type(block).__name__ for block in result] == [
        "Paragraph",
        "PageBreak",
        "Paragraph",
        "PageBreak",
        "Paragraph",
    ]
    assert isinstance(result[1], PageBreak)


def test_head_script_and_style_are_not_text():
    result = blocks("<html><head><title>t</title><style>p{}</style></head><body><script>x()</script><p>a</p></body>")
    assert [block.text for block in result] == ["a"]


def test_paragraph_position_is_its_element():
    (_, paragraph) = blocks("<p>a</p>\n<div>\n  <span>b</span></div>")
    assert isinstance(paragraph, Paragraph)
    assert (paragraph.line, paragraph.column) == (3, 3)
