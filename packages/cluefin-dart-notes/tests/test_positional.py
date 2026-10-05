"""규칙이 모르는 오류는 코퍼스에 아직 없다. 기본 규칙을 빼서 그런 상황을 만들어 위치 기반 수리를 검증한다."""

import pytest

from cluefin_dart_notes import DartXmlRepairer, DartXmlRepairError, PositionalRepair


def fallback_only(**kwargs) -> DartXmlRepairer:
    return DartXmlRepairer(rules=(), **kwargs)


def body_text(raw: str, repairer: DartXmlRepairer) -> tuple[str, object]:
    root, result = repairer.parse(raw.encode())
    return "".join(root.itertext()), result


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("<DOCUMENT><P>R&D 투자</P></DOCUMENT>", "R&D 투자"),
        ("<DOCUMENT><P>< 시장 점유율 ></P></DOCUMENT>", "< 시장 점유율 >"),
        ("<DOCUMENT><P>가나다<Product Share></P></DOCUMENT>", "가나다<Product Share>"),
        ("<DOCUMENT><P><시장 동향></P><P>본문</P></DOCUMENT>", "<시장 동향>본문"),
        ("<DOCUMENT><P>줄바꿈&cr;</P></DOCUMENT>", "줄바꿈&cr;"),
    ],
)
def test_unknown_defects_are_fixed_and_reported(raw, expected):
    text, result = body_text(raw, fallback_only())

    assert text == expected
    assert result.used_fallback
    report = result.reports[-1]
    assert report.rule == "positional"
    assert report.count == 1
    assert report.samples[0].line == 1


def test_fixes_repeat_until_document_parses():
    raw = "<DOCUMENT>\n<P>R&D</P>\n<P>S&P</P>\n<P><시장 동향></P>\n</DOCUMENT>"

    text, result = body_text(raw, fallback_only())

    assert "R&D" in text and "S&P" in text and "<시장 동향>" in text
    report = result.reports[-1]
    assert report.count == 3
    assert [sample.line for sample in report.samples] == [2, 3, 4]


def test_error_at_known_tag_is_not_escaped():
    raw = '<DOCUMENT><P X="a "">본문</P></DOCUMENT>'

    with pytest.raises(DartXmlRepairError, match="알려진 태그와 올바른 참조밖에"):
        fallback_only().parse(raw.encode())


def test_max_fixes_is_enforced_with_partial_report():
    raw = "<DOCUMENT><P>A&B C&D E&F</P></DOCUMENT>"

    with pytest.raises(DartXmlRepairError, match="2회 초과") as excinfo:
        fallback_only(fallback=PositionalRepair(max_fixes=2)).parse(raw.encode())

    assert excinfo.value.reports[-1].rule == "positional"
    assert excinfo.value.reports[-1].count == 2
    assert excinfo.value.last_error is not None


def test_strict_mode_raises_on_first_error():
    with pytest.raises(DartXmlRepairError, match="strict"):
        fallback_only(strict=True).parse(b"<DOCUMENT><P>R&D</P></DOCUMENT>")


def test_multibyte_columns_are_mapped_to_characters():
    raw = "<DOCUMENT><P>한글 한글 한글 R&D</P></DOCUMENT>"

    text, _ = body_text(raw, fallback_only())

    assert text == "한글 한글 한글 R&D"
