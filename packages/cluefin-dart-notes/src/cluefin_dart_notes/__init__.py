"""cluefin-dart-notes: DART 공시 원문(dart4 XML) 파서"""

__version__ = "0.1.0"

from cluefin_dart_notes._amount import parse_amount
from cluefin_dart_notes._blocks import Block, Cell, Heading, Paragraph, Table, extract_blocks, table_to_rows
from cluefin_dart_notes._document import (
    AUDIT_REPORT_CODES,
    PERIODIC_REPORT_CODES,
    DartDocument,
    Section,
    load_document,
    parse_document,
)
from cluefin_dart_notes._find import business_description, company_overview, find_section, find_sections
from cluefin_dart_notes._notes import Note, NoteSplit, extract_notes, notes_sections, split_notes
from cluefin_dart_notes.repair import (
    DEFAULT_RULES,
    KNOWN_TAGS,
    DartXmlRepairer,
    DartXmlRepairError,
    Decoder,
    EscapeBareAmpersand,
    EscapeUnknownTags,
    NormalizeAttributes,
    PositionalRepair,
    RepairReport,
    RepairResult,
    RepairRule,
    RepairSample,
    ReplaceDartEntities,
    RuleOutcome,
)

__all__ = [
    "AUDIT_REPORT_CODES",
    "Block",
    "Cell",
    "DEFAULT_RULES",
    "KNOWN_TAGS",
    "Note",
    "NoteSplit",
    "PERIODIC_REPORT_CODES",
    "DartDocument",
    "DartXmlRepairError",
    "DartXmlRepairer",
    "Decoder",
    "EscapeBareAmpersand",
    "Heading",
    "EscapeUnknownTags",
    "NormalizeAttributes",
    "Paragraph",
    "PositionalRepair",
    "RepairReport",
    "RepairResult",
    "RepairRule",
    "RepairSample",
    "ReplaceDartEntities",
    "RuleOutcome",
    "Section",
    "Table",
    "business_description",
    "company_overview",
    "extract_blocks",
    "extract_notes",
    "find_section",
    "find_sections",
    "load_document",
    "notes_sections",
    "parse_amount",
    "parse_document",
    "split_notes",
    "table_to_rows",
]
