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
