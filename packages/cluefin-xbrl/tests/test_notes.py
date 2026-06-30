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
from cluefin_xbrl.notes import _identify_note_role


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
