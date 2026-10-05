"""규칙별로 "정리 전 파싱 실패 → 정리 후 성공 → 텍스트 보존"을 확인한다. 조각은 모두 합성이다."""

import pytest
from defusedxml.ElementTree import ParseError, fromstring

from cluefin_dart_notes import (
    DEFAULT_RULES,
    EscapeBareAmpersand,
    EscapeUnknownTags,
    NormalizeAttributes,
    ReplaceDartEntities,
)


def text_of(xml: str) -> str:
    return "".join(fromstring(xml.encode()).itertext())


def assert_unparseable(xml: str) -> None:
    with pytest.raises(ParseError):
        fromstring(xml.encode())


class TestReplaceDartEntities:
    def test_cr_becomes_newline_without_changing_line_count(self):
        raw = "<P>첫 줄&cr;&cr;둘째 줄</P>"
        assert_unparseable(raw)

        outcome = ReplaceDartEntities().apply(raw)

        assert outcome.count == 2
        assert text_of(outcome.text) == "첫 줄\n\n둘째 줄"
        assert outcome.text.count("\n") == raw.count("\n")

    def test_custom_entities(self):
        outcome = ReplaceDartEntities({"nbsp": " "}).apply("<P>a&nbsp;b&cr;</P>")

        assert outcome.count == 1
        assert "&#160;" in outcome.text
        assert "&cr;" in outcome.text

    def test_no_entities_is_noop(self):
        assert ReplaceDartEntities({}).apply("<P>&cr;</P>").text == "<P>&cr;</P>"


class TestEscapeBareAmpersand:
    def test_bare_ampersands_are_escaped(self):
        raw = "<P>R&D 투자와 S&P 등급, A & B</P>"
        assert_unparseable(raw)

        outcome = EscapeBareAmpersand().apply(raw)

        assert outcome.count == 3
        assert text_of(outcome.text) == "R&D 투자와 S&P 등급, A & B"
        assert outcome.samples[0].column == 5

    def test_valid_references_are_kept(self):
        raw = "<P>&amp; &lt; &gt; &quot; &apos; &#169; &#xA9;</P>"

        outcome = EscapeBareAmpersand().apply(raw)

        assert outcome.count == 0
        assert outcome.text == raw

    def test_running_before_dart_entities_keeps_cr_as_literal_text(self):
        """순서를 바꾸면 `&cr;`이 줄바꿈이 아니라 글자 그대로 남는다 — 기본 순서가 엔티티 먼저인 이유."""
        outcome = EscapeBareAmpersand().apply("<P>a&cr;b</P>")

        assert text_of(outcome.text) == "a&cr;b"


class TestEscapeUnknownTags:
    @pytest.mark.parametrize(
        "raw",
        [
            "<P><시장 동향></P>",
            "<P><이사ㆍ감사></P>",
            "<P><Product Share Trend></P>",
            "<P>< 국가별 등록 현황 ></P>",
            "<P><2024></P>",
            "<P>약정 내용<㈜가나 제1회 사채></P>",
        ],
    )
    def test_tag_shaped_text_is_escaped(self, raw):
        assert_unparseable(raw)

        outcome = EscapeUnknownTags().apply(raw)

        assert outcome.count == 1
        assert text_of(outcome.text) == raw[len("<P>") : -len("</P>")]

    def test_known_tags_and_markup_are_kept(self):
        raw = '<?xml version="1.0"?><!-- c --><DOCUMENT><SECTION-1><P>a<BR/>b</P><TABLE-GROUP/></SECTION-1></DOCUMENT>'

        outcome = EscapeUnknownTags().apply(raw)

        assert outcome.count == 0
        assert outcome.text == raw

    def test_tag_name_prefix_is_not_mistaken_for_known_tag(self):
        outcome = EscapeUnknownTags().apply("<P><PROGRAM 안내></P>")

        assert outcome.count == 1

    def test_unknown_name_with_closing_tag_warns(self):
        raw = "<DOCUMENT><NEWBLOCK><P>정정</P></NEWBLOCK><P><North Tower></P></DOCUMENT>"

        outcome = EscapeUnknownTags().apply(raw)

        assert outcome.count == 3
        assert len(outcome.warnings) == 1
        assert "NEWBLOCK" in outcome.warnings[0]

    def test_custom_known_tags(self):
        outcome = EscapeUnknownTags(known_tags={"P", "NEWBLOCK"}).apply("<P><NEWBLOCK>a</NEWBLOCK></P>")

        assert outcome.count == 0


class TestNormalizeAttributes:
    def test_extra_quote_is_dropped(self):
        raw = '<P><TITLE ENG="Provisions for contracts "" ATOC="Y">충당부채</TITLE></P>'
        assert_unparseable(raw)

        outcome = NormalizeAttributes().apply(raw)

        assert outcome.count == 1
        element = fromstring(outcome.text.encode()).find("TITLE")
        assert element.get("ENG") == "Provisions for contracts "
        assert element.text == "충당부채"

    def test_duplicate_attribute_keeps_first(self):
        raw = '<P><TD WIDTH="10" WIDTH="20">셀</TD></P>'
        assert_unparseable(raw)

        outcome = NormalizeAttributes().apply(raw)

        assert fromstring(outcome.text.encode()).find("TD").get("WIDTH") == "10"

    def test_clean_tags_are_untouched(self):
        raw = '<P>\n<TD  WIDTH="10"\n ALIGN=\'LEFT\'>셀</TD><BR/><IMG SRC="a.jpg"/></P>'

        outcome = NormalizeAttributes().apply(raw)

        assert outcome.count == 0
        assert outcome.text == raw


def test_default_rules_order():
    assert [rule.name for rule in DEFAULT_RULES] == ["dart-entities", "bare-ampersand", "unknown-tags", "attributes"]
