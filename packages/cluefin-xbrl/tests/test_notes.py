"""Tests for financial statement note extraction."""

from decimal import Decimal

import pytest

from cluefin_xbrl._types import (
    ConceptLabel,
    NoteLineItem,
    NoteSection,
    ParsedNotes,
    PeriodType,
    PresentationNode,
    TaxonomyInfo,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)
from cluefin_xbrl.notes import _identify_note_role, extract_notes


class TestNoteModels:
    def test_note_line_item_defaults(self):
        item = NoteLineItem(concept_local_name="A", concept_qname="ns:A")
        assert item.dimensions == {}
        assert item.is_abstract is False
        assert item.value is None

    def test_note_line_item_dimensions(self):
        item = NoteLineItem(
            concept_local_name="A",
            concept_qname="ns:A",
            value=Decimal("1000"),
            dimensions={"ns:Axis": "ns:Member"},
        )
        assert item.dimensions == {"ns:Axis": "ns:Member"}
        assert item.value == Decimal("1000")

    def test_note_section_defaults(self):
        section = NoteSection(role_code="D834480", role_uri="http://x/role-D834480")
        assert section.is_consolidated is True
        assert section.line_items == []
        assert section.title is None

    def test_parsed_notes_defaults(self):
        parsed = ParsedNotes(source_file="x.xbrl")
        assert parsed.notes == {}
        assert parsed.entity_id is None


class TestIdentifyNoteRole:
    def test_consolidated_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/ias_19_role-D834480") == ("D834480", True)

    def test_separate_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/ias_19_role-D834485") == ("D834485", False)

    def test_statement_role_is_not_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000") is None

    def test_doc_role_is_not_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/dart-gcd_2024-06-30_role-D999001") is None

    def test_generic_role_is_not_note(self):
        assert _identify_note_role("http://example.com/role/SomeOtherRole") is None


def _make_doc() -> XbrlDocument:
    """확정급여 주석 1개 + 비주석(재무상태표) role 1개를 가진 합성 문서."""
    period = XbrlPeriod(period_type=PeriodType.INSTANT, instant=None)

    # 주석 트리: 추상 컨테이너 -> 값 노드(차원 있음)
    value_node = PresentationNode(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        depth=1,
        order=1.0,
    )
    root_node = PresentationNode(
        concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
        concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
        depth=0,
        order=0.0,
        children=[value_node],
    )
    note_role = "http://dart.fss.or.kr/role/ifrs/ias_19_role-D834480"
    # 비주석 role(재무상태표)도 트리에 넣어 걸러지는지 검증
    stmt_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000"
    stmt_node = PresentationNode(
        concept_local_name="Assets",
        concept_qname="ifrs-full:Assets",
    )

    labels = {
        "DisclosureOfDefinedBenefitPlansAbstract": ConceptLabel(
            concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
            concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
            label_ko="종업원급여에 대한 공시",
            label_en="Disclosure of defined benefit plans",
        ),
        "DefinedBenefitObligationAtPresentValue": ConceptLabel(
            concept_local_name="DefinedBenefitObligationAtPresentValue",
            concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
            label_ko="확정급여채무, 현재가치",
            label_en="Defined benefit obligation, at present value",
        ),
    }
    taxonomy = TaxonomyInfo(
        labels=labels,
        presentation_trees={note_role: [root_node], stmt_role: [stmt_node]},
    )
    fact = XbrlFact(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        value="1000",
        numeric_value=Decimal("1000"),
        unit="iso4217:KRW",
        period=period,
        dimensions={"ifrs-full:Axis": "ifrs-full:Member"},
    )
    return XbrlDocument(
        source_file="entity_test.xbrl",
        facts=[fact],
        entity_id="00000000",
        taxonomy=taxonomy,
    )


class TestExtractNotes:
    def test_requires_taxonomy(self):
        doc = XbrlDocument(source_file="x.xbrl", facts=[])
        with pytest.raises(ValueError):
            extract_notes(doc)

    def test_extracts_only_note_roles(self):
        notes = extract_notes(_make_doc())
        # D834480 주석만, 재무상태표 D210000은 제외
        assert list(notes.notes.keys()) == ["D834480"]

    def test_note_section_metadata(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        assert section.role_code == "D834480"
        assert section.is_consolidated is True
        assert section.title == "종업원급여에 대한 공시"

    def test_dimensions_preserved(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        value_items = [li for li in section.line_items if not li.is_abstract]
        assert len(value_items) == 1
        assert value_items[0].dimensions == {"ifrs-full:Axis": "ifrs-full:Member"}
        assert value_items[0].value == Decimal("1000")

    def test_abstract_node_has_no_value(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        abstract_items = [li for li in section.line_items if li.is_abstract]
        assert any(li.concept_local_name == "DisclosureOfDefinedBenefitPlansAbstract" for li in abstract_items)

    def test_public_api_import(self):
        from cluefin_xbrl import ParsedNotes as PN
        from cluefin_xbrl import extract_notes as en

        assert en is extract_notes
        assert PN is ParsedNotes
