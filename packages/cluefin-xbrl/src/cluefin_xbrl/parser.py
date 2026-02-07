"""XBRL instance document parser using Arelle."""

from __future__ import annotations

import threading
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import TYPE_CHECKING

from cluefin_xbrl._types import PeriodType, XbrlDocument, XbrlFact, XbrlPeriod

if TYPE_CHECKING:
    from arelle.ModelInstanceObject import ModelContext
    from arelle.ModelXbrl import ModelXbrl

_arelle_lock = threading.Lock()


class XbrlParseError(Exception):
    """Raised when XBRL parsing fails."""


def parse_xbrl_file(path: str | Path, *, include_taxonomy: bool = False) -> XbrlDocument:
    """Parse a single XBRL instance file and extract all facts.

    Args:
        path: Path to the XBRL instance file (.xbrl).
        include_taxonomy: If True, also extract taxonomy labels and presentation trees.

    Returns:
        XbrlDocument with all extracted facts.

    Raises:
        FileNotFoundError: If the file does not exist.
        XbrlParseError: If parsing fails.
    """
    file_path = Path(path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"XBRL 파일을 찾을 수 없습니다: {file_path}")

    model_xbrl = _parse_with_session(file_path)

    facts = _extract_facts(model_xbrl)

    entity_id = None
    reporting_end = None
    if facts:
        entity_id = facts[0].entity_id
        instant_dates = [f.period.instant for f in facts if f.period and f.period.instant]
        if instant_dates:
            reporting_end = max(instant_dates)

    doc = XbrlDocument(
        source_file=str(file_path),
        facts=facts,
        entity_id=entity_id,
        reporting_period_end=reporting_end,
    )

    if include_taxonomy:
        from cluefin_xbrl.taxonomy import extract_taxonomy

        doc.taxonomy = extract_taxonomy(model_xbrl)

    return doc


def parse_xbrl_directory(directory: str | Path, *, include_taxonomy: bool = False) -> XbrlDocument:
    """Find and parse the XBRL instance file in a directory.

    Searches for .xbrl files in the directory and parses the first one found.

    Args:
        directory: Path to directory containing XBRL files.
        include_taxonomy: If True, also extract taxonomy labels and presentation trees.

    Returns:
        XbrlDocument with all extracted facts.

    Raises:
        FileNotFoundError: If the directory does not exist.
        XbrlParseError: If no .xbrl files are found.
    """
    dir_path = Path(directory).resolve()
    if not dir_path.exists():
        raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {dir_path}")

    xbrl_files = sorted(dir_path.glob("*.xbrl"))
    if not xbrl_files:
        raise XbrlParseError(f"디렉토리에 XBRL 파일이 없습니다: {dir_path}")

    return parse_xbrl_file(xbrl_files[0], include_taxonomy=include_taxonomy)


def _parse_with_session(path: Path) -> ModelXbrl:
    """Load an XBRL file using Arelle Session with thread safety."""
    from arelle.api.Session import Session
    from arelle.RuntimeOptions import RuntimeOptions

    with _arelle_lock:
        with Session() as session:
            options = RuntimeOptions(
                entrypointFile=str(path),
                keepOpen=True,
            )
            session.run(options)
            models = session.get_models()
            if not models:
                raise XbrlParseError(f"XBRL 모델을 로드할 수 없습니다: {path}")
            return models[0]


def _extract_facts(model_xbrl: ModelXbrl) -> list[XbrlFact]:
    """Extract all facts from a loaded XBRL model."""
    facts: list[XbrlFact] = []

    for fact in model_xbrl.factsInInstance:
        context = fact.context
        period = _extract_period(context) if context is not None else None
        entity_id = None
        if context is not None:
            _, entity_id = context.entityIdentifier

        dimensions: dict[str, str] = {}
        if context is not None and context.qnameDims:
            for dim_qname, dim_value in context.qnameDims.items():
                if dim_value.isExplicit:
                    dimensions[str(dim_qname)] = str(dim_value.memberQname)

        unit_str = None
        if fact.unit is not None:
            mul_measures, div_measures = fact.unit.measures
            parts = [str(m) for m in mul_measures]
            if div_measures:
                parts.append("/")
                parts.extend(str(d) for d in div_measures)
            unit_str = " ".join(parts)

        numeric_value = _try_parse_decimal(fact.value) if fact.isNumeric and not fact.isNil else None

        xbrl_fact = XbrlFact(
            concept_local_name=fact.qname.localName,
            concept_qname=str(fact.qname),
            namespace=fact.qname.namespaceURI or "",
            value=fact.value if not fact.isNil else None,
            numeric_value=numeric_value,
            decimals=str(fact.decimals) if fact.isNumeric and fact.decimals is not None else None,
            unit=unit_str,
            context_id=fact.contextID,
            period=period,
            entity_id=entity_id,
            is_nil=fact.isNil,
            dimensions=dimensions,
        )
        facts.append(xbrl_fact)

    return facts


def _extract_period(context: ModelContext) -> XbrlPeriod:
    """Extract period information from an Arelle context.

    Arelle's instant/end datetimes are exclusive (midnight of the next day).
    We subtract 1 day to get the actual reporting date.
    """
    if context.isInstantPeriod:
        instant_dt = context.instantDatetime
        instant_date = _exclusive_to_date(instant_dt)
        return XbrlPeriod(period_type=PeriodType.INSTANT, instant=instant_date)
    elif context.isStartEndPeriod:
        start_dt = context.startDatetime
        end_dt = context.endDatetime
        start_date = start_dt.date() if isinstance(start_dt, datetime) else start_dt
        end_date = _exclusive_to_date(end_dt)
        return XbrlPeriod(period_type=PeriodType.DURATION, start_date=start_date, end_date=end_date)
    else:
        return XbrlPeriod(period_type=PeriodType.FOREVER)


def _exclusive_to_date(dt: datetime | date) -> date:
    """Convert Arelle's exclusive datetime to an inclusive date.

    Arelle represents instant dates as midnight of the following day.
    For example, 2023-12-31 is stored as 2024-01-01T00:00:00.
    We subtract one day to get the actual date.
    """
    if isinstance(dt, datetime) and dt.hour == 0 and dt.minute == 0 and dt.second == 0:
        return (dt - timedelta(days=1)).date()
    if isinstance(dt, datetime):
        return dt.date()
    return dt


def _try_parse_decimal(value: str | None) -> Decimal | None:
    """Try to parse a string value as Decimal."""
    if value is None:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None
