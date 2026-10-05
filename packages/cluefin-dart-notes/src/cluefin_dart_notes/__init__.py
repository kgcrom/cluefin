"""cluefin-dart-notes: DART 공시 원문(dart4 XML) 파서"""

__version__ = "0.1.0"

from cluefin_dart_notes._document import (
    AUDIT_REPORT_CODES,
    PERIODIC_REPORT_CODES,
    DartDocument,
    Section,
    load_document,
    parse_document,
)
from cluefin_dart_notes._find import business_description, company_overview, find_section, find_sections
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
    "DEFAULT_RULES",
    "KNOWN_TAGS",
    "PERIODIC_REPORT_CODES",
    "DartDocument",
    "DartXmlRepairError",
    "DartXmlRepairer",
    "Decoder",
    "EscapeBareAmpersand",
    "EscapeUnknownTags",
    "NormalizeAttributes",
    "PositionalRepair",
    "RepairReport",
    "RepairResult",
    "RepairRule",
    "RepairSample",
    "ReplaceDartEntities",
    "RuleOutcome",
    "Section",
    "business_description",
    "company_overview",
    "find_section",
    "find_sections",
    "load_document",
    "parse_document",
]
