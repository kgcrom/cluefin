from cluefin_sec_notes import ENCODING_FALLBACK, parse_filing
from cluefin_sec_notes._decode import decode_html


def test_declared_encoding_is_used_first():
    data = '<?xml version="1.0" encoding="ISO-8859-1"?><p>caf\xe9</p>'.encode("latin-1")
    assert decode_html(data) == ('<?xml version="1.0" encoding="ISO-8859-1"?><p>café</p>', "iso8859-1", "iso8859-1")


def test_ascii_declaration_with_utf8_bytes_falls_back_and_is_recorded():
    data = "<?xml version='1.0' encoding='ASCII'?><p>Company’s</p>".encode()
    document = parse_filing(data)
    assert document.blocks[0].text == "Company’s"
    assert document.report.encoding == "utf-8"
    assert document.report.declared_encoding == "ascii"
    assert document.report.count(ENCODING_FALLBACK) == 1


def test_undeclared_windows_1252_quotes():
    data = b"<html><body><p>\x93Risk Factors\x94</p></body></html>"
    text, encoding, declared = decode_html(data)
    assert (encoding, declared) == ("cp1252", None)
    assert "“Risk Factors”" in text


def test_meta_charset_declaration():
    data = b'<html><head><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"></head>\x96</html>'
    assert decode_html(data)[1:] == ("cp1252", "cp1252")


def test_utf8_bom():
    assert decode_html(b"\xef\xbb\xbf<p>a</p>") == ("<p>a</p>", "utf-8-sig", "utf-8-sig")
