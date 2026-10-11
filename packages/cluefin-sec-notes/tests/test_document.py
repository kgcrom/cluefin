from pathlib import Path

from cluefin_sec_notes import Paragraph, load_filing, parse_filing


def test_form_from_argument_wins():
    document = parse_filing("<p>FORM 10-Q</p>", form="10-k / a")
    assert document.form == "10-K/A"


def test_form_from_cover():
    html = "<p>UNITED STATES SECURITIES AND EXCHANGE COMMISSION</p><p>Form 10-K/A</p><p>(Amendment No. 1)</p>"
    assert parse_filing(html).form == "10-K/A"
    assert parse_filing("<p>FORM 8-K</p>").form == "8-K"
    assert parse_filing("<p>no form here</p>").form is None


def test_text_joins_blocks_and_table_cells():
    document = parse_filing(
        "<p>a</p><table><tr><td>x</td><td>1</td></tr><tr><td>y</td><td>2</td></tr></table><hr><p>b</p>"
    )
    assert document.text() == "a\n\nx\t1\ny\t2\n\nb"
    assert document.text(2) == "b"


def test_load_filing_keeps_source(tmp_path: Path):
    path = tmp_path / "filing.htm"
    path.write_bytes(b"<p>Item 1.</p>")
    document = load_filing(path, form="10-K")
    assert document.source == path
    assert isinstance(document.blocks[0], Paragraph)
