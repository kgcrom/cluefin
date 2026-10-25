"""Data models for XBRL parsed data."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum


class PeriodType(str, Enum):
    """XBRL context period type."""

    INSTANT = "instant"
    DURATION = "duration"
    FOREVER = "forever"


@dataclass(frozen=True, slots=True)
class XbrlPeriod:
    """Represents an XBRL context period."""

    period_type: PeriodType
    instant: date | None = None
    start_date: date | None = None
    end_date: date | None = None


@dataclass(frozen=True, slots=True)
class XbrlFact:
    """A single XBRL fact extracted from an instance document."""

    concept_local_name: str
    concept_qname: str
    namespace: str
    value: str | None = None
    numeric_value: Decimal | None = None
    decimals: str | None = None
    unit: str | None = None
    context_id: str | None = None
    period: XbrlPeriod | None = None
    entity_id: str | None = None
    is_nil: bool = False
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ConceptLabel:
    """Label information for a concept."""

    concept_local_name: str
    concept_qname: str
    label_ko: str | None = None
    label_en: str | None = None


@dataclass(frozen=True, slots=True)
class PresentationNode:
    """A node in the presentation tree hierarchy."""

    concept_local_name: str
    concept_qname: str
    order: float = 0.0
    depth: int = 0
    # Role URI of the arc's preferredLabel (e.g. http://www.xbrl.org/2003/role/periodStartLabel); None when the arc has none.
    preferred_label: str | None = None
    children: list[PresentationNode] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class TaxonomyInfo:
    """Taxonomy label and presentation information."""

    labels: dict[str, ConceptLabel] = field(default_factory=dict)
    presentation_trees: dict[str, list[PresentationNode]] = field(default_factory=dict)
    # linkrole URI → role definition. SEC filings use "{sort code} - {Statement|Disclosure|...} - {title}".
    role_definitions: dict[str, str] = field(default_factory=dict)


class StatementType(str, Enum):
    """Financial statement type."""

    BS = "BS"
    IS = "IS"
    CIS = "CIS"
    CF = "CF"
    SCE = "SCE"


@dataclass(frozen=True, slots=True)
class StatementLineItem:
    """A single line item in a financial statement.

    ``dimensions`` holds the statement-intrinsic dimensional context (e.g. the
    equity component axis on a statement of changes in equity). The
    consolidated/separate axis is resolved at extraction time and not repeated here.

    ``preferred_label`` is the presentation arc's preferredLabel role. It tells apart the rows of a concept
    shown twice, such as the beginning (``periodStartLabel``) and ending (``periodEndLabel``) equity balance.
    """

    concept_local_name: str
    concept_qname: str
    label_ko: str | None = None
    label_en: str | None = None
    value: Decimal | None = None
    unit: str | None = None
    period: XbrlPeriod | None = None
    depth: int = 0
    order: float = 0.0
    is_abstract: bool = False
    dimensions: dict[str, str] = field(default_factory=dict)
    preferred_label: str | None = None


@dataclass(frozen=True, slots=True)
class FinancialStatement:
    """A structured financial statement."""

    statement_type: StatementType
    linkrole: str
    line_items: list[StatementLineItem] = field(default_factory=list)
    periods: list[XbrlPeriod] = field(default_factory=list)
    is_consolidated: bool = True


@dataclass(frozen=True, slots=True)
class ParsedFinancialStatements:
    """Collection of parsed financial statements.

    ``statements`` holds consolidated (연결) statements keyed by type code (BS/IS/CIS/CF/SCE);
    ``separate_statements`` holds the separate (별도) statements with the same keys.
    """

    source_file: str
    entity_id: str | None = None
    statements: dict[str, FinancialStatement] = field(default_factory=dict)
    separate_statements: dict[str, FinancialStatement] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class XbrlDocument:
    """Parsed XBRL instance document."""

    source_file: str
    facts: list[XbrlFact]
    entity_id: str | None = None
    reporting_period_end: date | None = None
    taxonomy: TaxonomyInfo | None = None


@dataclass(frozen=True, slots=True)
class NoteLineItem:
    """A single line item in a financial statement note, with dimensional context.

    ``value`` holds numeric facts; ``text_value`` holds non-numeric facts
    (short narrative strings, dates, etc.) that would otherwise be lost.
    """

    concept_local_name: str
    concept_qname: str
    label_ko: str | None = None
    label_en: str | None = None
    value: Decimal | None = None
    text_value: str | None = None
    unit: str | None = None
    period: XbrlPeriod | None = None
    depth: int = 0
    order: float = 0.0
    is_abstract: bool = False
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class NoteSection:
    """A structured financial statement note (disclosure)."""

    role_code: str
    role_uri: str
    title: str | None = None
    is_consolidated: bool = True
    line_items: list[NoteLineItem] = field(default_factory=list)
    periods: list[XbrlPeriod] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ParsedNotes:
    """Collection of parsed financial statement notes."""

    source_file: str
    entity_id: str | None = None
    notes: dict[str, NoteSection] = field(default_factory=dict)
