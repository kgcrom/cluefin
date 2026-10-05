import pytest

from cluefin_dart_notes import DartXmlRepairError, Decoder

DECLARATION = '<?xml version="1.0" encoding="{}"?>\n'


def test_utf8_document_keeps_text_without_report():
    raw = (DECLARATION.format("utf-8") + "<DOCUMENT>본문</DOCUMENT>").encode("utf-8")

    result = Decoder().decode(raw)

    assert result.encoding == "utf-8"
    assert result.report is None
    assert result.text.endswith("<DOCUMENT>본문</DOCUMENT>")


def test_cp949_bytes_declared_utf8_are_decoded_and_reported():
    raw = (DECLARATION.format("utf-8") + "<DOCUMENT>본문</DOCUMENT>").encode("cp949")

    result = Decoder().decode(raw)

    assert result.encoding == "cp949"
    assert "<DOCUMENT>본문</DOCUMENT>" in result.text
    assert result.report is not None
    assert result.report.rule == "decoder"
    assert result.report.samples[0].line == 1


def test_declaration_is_rewritten_to_utf8():
    raw = (DECLARATION.format("euc-kr") + "<DOCUMENT>본문</DOCUMENT>").encode("cp949")

    result = Decoder().decode(raw)

    assert result.text.startswith(DECLARATION.format("utf-8"))


def test_declared_name_spelling_does_not_count_as_mismatch():
    raw = (DECLARATION.format("UTF8") + "<DOCUMENT/>").encode("utf-8")

    assert Decoder().decode(raw).report is None


def test_bom_is_dropped():
    raw = b"\xef\xbb\xbf" + "<DOCUMENT>본문</DOCUMENT>".encode()

    assert Decoder().decode(raw).text == "<DOCUMENT>본문</DOCUMENT>"


def test_undecodable_bytes_raise():
    with pytest.raises(DartXmlRepairError, match="ascii"):
        Decoder(candidates=("ascii",)).decode("본문".encode())


def test_empty_candidates_are_rejected():
    with pytest.raises(ValueError):
        Decoder(candidates=())


def test_unknown_declared_encoding_is_reported_as_mismatch():
    raw = (DECLARATION.format("x-dart") + "<DOCUMENT/>").encode("utf-8")

    result = Decoder().decode(raw)

    assert result.report is not None
    assert result.text.startswith(DECLARATION.format("utf-8"))
