from cluefin_sec_notes import IMPLICIT_CLOSE, MISNESTED_END, STRAY_END_TAG, UNCLOSED_AT_EOF, UNKNOWN_TAG, parse_filing
from cluefin_sec_notes._report import ReportCollector
from cluefin_sec_notes._tree import build_tree


def texts(html: str) -> list[str]:
    return [block.text for block in parse_filing(html).blocks]


def test_deep_nesting_is_not_truncated():
    # lxml은 huge_tree 없이 깊이 256을 넘으면 말없이 버린다. 재귀로 돌면 Python 재귀 한도(1000)에서 깨진다.
    depth = 5000
    html = "<div>" * depth + "<p>deep text</p>" + "</div>" * depth + "<p>after</p>"
    assert texts(html) == ["deep text", "after"]


def test_unclosed_paragraph_is_closed_by_next_and_recorded():
    document = parse_filing("<body><p>first<p>second</body>")
    assert [block.text for block in document.blocks] == ["first", "second"]
    samples = document.report.fix(IMPLICIT_CLOSE).samples
    assert [sample.context for sample in samples] == ["<p> closes <p>", "</body> closes p"]


def test_optional_end_tags_closed_by_parent_are_not_misnested():
    document = parse_filing("<table><tr><td><p>a</td><td>b</td></tr></table>")
    assert document.report.count(MISNESTED_END) == 0
    assert document.report.count(IMPLICIT_CLOSE) == 1


def test_misnested_end_tag_position():
    document = parse_filing("<div>\n<div><span>text</div>\n</div>")
    fix = document.report.fix(MISNESTED_END)
    assert fix.count == 1
    assert (fix.samples[0].line, fix.samples[0].column) == (2, 16)
    assert fix.samples[0].context == "</div> closes span"


def test_stray_end_tag_is_ignored():
    document = parse_filing("<p>a</font>b</p>")
    assert [block.text for block in document.blocks] == ["ab"]
    assert document.report.count(STRAY_END_TAG) == 1


def test_stray_end_tag_inside_cell_does_not_close_outer_div():
    document = parse_filing("<div><table><tr><td>a</div></td><td>b</td></tr></table>after</div>")
    assert document.blocks[0].rows[0][1].text == "b"
    assert document.report.count(STRAY_END_TAG) == 1


def test_unclosed_at_eof_ignores_structural_tags():
    document = parse_filing("<html><body><div><span>a")
    assert document.report.count(UNCLOSED_AT_EOF) == 2


def test_unknown_tag_text_is_kept():
    document = parse_filing("<p>a <newtag>b</newtag></p>")
    assert document.blocks[0].text == "a b"
    assert document.report.unknown_tags == (("newtag", 1),)
    assert document.report.count(UNKNOWN_TAG) == 1


def test_typed_dimension_inside_ix_header_is_not_unknown():
    html = (
        '<div style="display:none"><ix:header><ix:resources><xbrli:context>'
        "<us-gaap:somethingaxis.domain>x</us-gaap:somethingaxis.domain></xbrli:context></ix:resources></ix:header></div>"
    )
    assert parse_filing(html).report.unknown_tags == ()


def test_node_position_is_one_based():
    root = build_tree("<p>\n  <b>x</b></p>", ReportCollector())
    bold = next(node for node in root.iter() if node.tag == "b")
    assert (bold.line, bold.column) == (2, 3)
