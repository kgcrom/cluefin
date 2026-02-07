"""Pydantic models for XBRL parsed data."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PeriodType(str, Enum):
    """XBRL context period type."""

    INSTANT = "instant"
    DURATION = "duration"
    FOREVER = "forever"


class XbrlPeriod(BaseModel):
    """Represents an XBRL context period."""

    model_config = ConfigDict(frozen=True)

    period_type: PeriodType
    instant: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class XbrlFact(BaseModel):
    """A single XBRL fact extracted from an instance document."""

    model_config = ConfigDict(frozen=True)

    concept_local_name: str
    concept_qname: str
    namespace: str
    value: Optional[str] = None
    numeric_value: Optional[Decimal] = None
    decimals: Optional[str] = None
    unit: Optional[str] = None
    context_id: Optional[str] = None
    period: Optional[XbrlPeriod] = None
    entity_id: Optional[str] = None
    is_nil: bool = False
    dimensions: dict[str, str] = {}


class ConceptLabel(BaseModel):
    """Label information for a concept."""

    model_config = ConfigDict(frozen=True)

    concept_local_name: str
    concept_qname: str
    label_ko: Optional[str] = None
    label_en: Optional[str] = None


class PresentationNode(BaseModel):
    """A node in the presentation tree hierarchy."""

    concept_local_name: str
    concept_qname: str
    order: float = 0.0
    depth: int = 0
    children: list[PresentationNode] = []


class TaxonomyInfo(BaseModel):
    """Taxonomy label and presentation information."""

    labels: dict[str, ConceptLabel] = {}
    presentation_trees: dict[str, list[PresentationNode]] = {}


class StatementType(str, Enum):
    """Financial statement type."""

    BS = "BS"
    IS = "IS"
    CIS = "CIS"
    CF = "CF"
    SCE = "SCE"


class StatementLineItem(BaseModel):
    """A single line item in a financial statement."""

    concept_local_name: str
    concept_qname: str
    label_ko: Optional[str] = None
    label_en: Optional[str] = None
    value: Optional[Decimal] = None
    unit: Optional[str] = None
    period: Optional[XbrlPeriod] = None
    depth: int = 0
    order: float = 0.0
    is_abstract: bool = False


class FinancialStatement(BaseModel):
    """A structured financial statement."""

    statement_type: StatementType
    linkrole: str
    line_items: list[StatementLineItem] = []
    periods: list[XbrlPeriod] = []


class ParsedFinancialStatements(BaseModel):
    """Collection of parsed financial statements."""

    source_file: str
    entity_id: Optional[str] = None
    statements: dict[str, FinancialStatement] = {}


class XbrlDocument(BaseModel):
    """Parsed XBRL instance document."""

    source_file: str
    facts: list[XbrlFact]
    entity_id: Optional[str] = None
    reporting_period_end: Optional[date] = None
    taxonomy: Optional[TaxonomyInfo] = None
