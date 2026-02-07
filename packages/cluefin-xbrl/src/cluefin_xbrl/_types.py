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


class XbrlDocument(BaseModel):
    """Parsed XBRL instance document."""

    source_file: str
    facts: list[XbrlFact]
    entity_id: Optional[str] = None
    reporting_period_end: Optional[date] = None
