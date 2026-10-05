import logging

import pytest
from defusedxml import EntitiesForbidden
from defusedxml.ElementTree import fromstring

from cluefin_dart_notes import DartXmlRepairer, RuleOutcome

# 지금까지 관찰된 결함을 모두 담은 합성 문서. 실제 공시가 아니다.
BROKEN = """<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-NAME ACODE="11012">반기보고서</DOCUMENT-NAME>
<COMPANY-NAME AREGCIK="00000000">가나다 주식회사</COMPANY-NAME>
<BODY>
<SECTION-1>
<TITLE ATOC="Y" AASSOCNOTE="D-0-1-0-0">I. 회사의 개요</TITLE>
<P>R&D 비용과 S&P 등급&cr;다음 줄</P>
<P><시장 동향></P>
<P>< 국가별 등록 현황 ></P>
<P><Product Share Trend></P>
<TABLE BORDER="1"><TBODY><TR><TD ENG="Provisions "">충당부채</TD></TR></TBODY></TABLE>
</SECTION-1>
</BODY>
</DOCUMENT>
"""


def test_default_pipeline_parses_every_known_defect_without_fallback():
    root, result = DartXmlRepairer(strict=True).parse(BROKEN.encode("cp949"))

    assert result.encoding == "cp949"
    assert not result.used_fallback
    assert {report.rule: report.count for report in result.reports} == {
        "decoder": 1,
        "dart-entities": 1,
        "bare-ampersand": 2,
        "unknown-tags": 3,
        "attributes": 1,
    }
    assert root.findtext("DOCUMENT-NAME") == "반기보고서"
    paragraphs = ["".join(p.itertext()) for p in root.iter("P")]
    assert paragraphs == [
        "R&D 비용과 S&P 등급\u2028다음 줄",
        "<시장 동향>",
        "< 국가별 등록 현황 >",
        "<Product Share Trend>",
    ]
    assert root.find(".//TD").get("ENG") == "Provisions "


def test_sample_lines_match_the_raw_file():
    _, result = DartXmlRepairer().parse(BROKEN.encode())

    lines = {report.rule: report.samples[0].line for report in result.reports}
    raw_lines = BROKEN.splitlines()
    assert "R&D" in raw_lines[lines["bare-ampersand"] - 1]
    assert "<시장 동향>" in raw_lines[lines["unknown-tags"] - 1]
    assert 'ENG="Provisions ""' in raw_lines[lines["attributes"] - 1]


def test_repair_returns_parseable_utf8():
    result = DartXmlRepairer().repair(BROKEN.encode("cp949"))

    assert result.xml.startswith(b'<?xml version="1.0" encoding="utf-8"?>')
    assert fromstring(result.xml).findtext(".//COMPANY-NAME") == "가나다 주식회사"


def test_clean_document_has_no_reports():
    _, result = DartXmlRepairer().parse("<DOCUMENT><P>본문</P></DOCUMENT>".encode())

    assert result.reports == ()
    assert result.warnings == ()


def test_suspected_real_tag_is_warned_and_logged(caplog):
    raw = "<DOCUMENT><NEWBLOCK><P>정정</P></NEWBLOCK></DOCUMENT>".encode()

    with caplog.at_level(logging.WARNING):
        _, result = DartXmlRepairer().parse(raw)

    assert any("NEWBLOCK" in warning for warning in result.warnings)
    assert "NEWBLOCK" in caplog.text


def test_fallback_use_is_logged(caplog):
    with caplog.at_level(logging.WARNING):
        _, result = DartXmlRepairer(rules=()).parse("<DOCUMENT><P>R&D</P></DOCUMENT>".encode())

    assert result.used_fallback
    assert "위치 기반" in caplog.text


class StripZeroWidthSpace:
    name = "zero-width-space"

    def apply(self, text: str) -> RuleOutcome:
        return RuleOutcome(text=text.replace("​", ""), count=text.count("​"))


def test_with_rule_inserts_before_named_rule():
    repairer = DartXmlRepairer().with_rule(StripZeroWidthSpace(), before="unknown-tags")

    assert [rule.name for rule in repairer.rules] == [
        "dart-entities",
        "bare-ampersand",
        "zero-width-space",
        "unknown-tags",
        "attributes",
    ]
    root, result = repairer.parse("<DOCUMENT><P>가​나</P></DOCUMENT>".encode())
    assert root.findtext("P") == "가나"
    assert result.reports[0].rule == "zero-width-space"


def test_with_rule_appends_and_keeps_original_unchanged():
    original = DartXmlRepairer()
    extended = original.with_rule(StripZeroWidthSpace())

    assert extended.rules[-1].name == "zero-width-space"
    assert len(original.rules) == 4


def test_with_rule_rejects_unknown_anchor():
    with pytest.raises(ValueError, match="없습니다"):
        DartXmlRepairer().with_rule(StripZeroWidthSpace(), before="missing")


def test_without_rule():
    repairer = DartXmlRepairer().without_rule("attributes")

    assert [rule.name for rule in repairer.rules] == ["dart-entities", "bare-ampersand", "unknown-tags"]
    with pytest.raises(ValueError):
        repairer.without_rule("attributes")


def test_entity_declarations_are_refused():
    """DART 원문에는 DOCTYPE 이 없다. 엔티티 선언이 든 입력은 정리·수리하지 않고 defusedxml 이 거부한다."""
    raw = b'<!DOCTYPE DOCUMENT [<!ENTITY e SYSTEM "file:///etc/passwd">]><DOCUMENT>&e;</DOCUMENT>'

    with pytest.raises(EntitiesForbidden):
        DartXmlRepairer().parse(raw)
