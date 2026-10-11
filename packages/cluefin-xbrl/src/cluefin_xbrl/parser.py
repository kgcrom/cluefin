"""XBRL instance document parser using Arelle."""

from __future__ import annotations

import re
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

# SEC filing folders hold the instance next to the linkbases, all as .xml. These are not instances.
_SEC_NON_INSTANCE = re.compile(r"(_(cal|def|lab|pre|ref)\.xml|^FilingSummary\.xml|^R\d+\.xml)$", re.IGNORECASE)
# Root element of an XBRL instance, with or without a namespace prefix (<xbrli:xbrl ...>, <xbrl ...>).
_INSTANCE_ROOT = re.compile(rb"<(?:[A-Za-z_][\w.-]*:)?xbrl[\s>]")
_DEI_NAMESPACE_PREFIX = "http://xbrl.sec.gov/dei/"


class XbrlParseError(Exception):
    """Raised when XBRL parsing fails."""


def parse_xbrl_file(
    path: str | Path,
    *,
    include_taxonomy: bool = False,
    http_user_agent: str | None = None,
) -> XbrlDocument:
    """Parse a single XBRL instance file and extract all facts.

    Args:
        path: Path to the XBRL instance file (.xbrl, or an SEC instance such as ``aapl-20230930_htm.xml``).
        include_taxonomy: If True, also extract taxonomy labels and presentation trees.
        http_user_agent: User-Agent Arelle sends when it downloads referenced taxonomies (SEC filings import
            DEI/SRT schemas from xbrl.sec.gov). SEC asks automated clients to declare "Name email"; Arelle's
            default agent still worked on 2026-10-11. Downloads are cached by Arelle, so this only matters on
            the first parse of a taxonomy version.

    Returns:
        XbrlDocument with all extracted facts.

    Raises:
        FileNotFoundError: If the file does not exist.
        XbrlParseError: If parsing fails.
    """
    file_path = Path(path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"XBRL 파일을 찾을 수 없습니다: {file_path}")

    model_xbrl = _parse_with_session(file_path, http_user_agent=http_user_agent)

    facts = _extract_facts(model_xbrl)

    entity_id = facts[0].entity_id if facts else None
    reporting_end = _reporting_period_end(facts)

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


def parse_xbrl_directory(
    directory: str | Path,
    *,
    include_taxonomy: bool = False,
    http_user_agent: str | None = None,
) -> XbrlDocument:
    """Find and parse the XBRL instance file in a directory.

    Parses the first .xbrl file by name (DART). Without one, looks for an SEC instance: the extracted
    inline-XBRL instance ``*_htm.xml`` first, then any other .xml whose root element is ``xbrl``
    (pre-2019 filings such as ``aapl-20180929.xml``). Linkbases and SEC rendering files are skipped.

    Args:
        directory: Path to directory containing XBRL files.
        include_taxonomy: If True, also extract taxonomy labels and presentation trees.
        http_user_agent: See :func:`parse_xbrl_file`.

    Returns:
        XbrlDocument with all extracted facts.

    Raises:
        FileNotFoundError: If the directory does not exist.
        XbrlParseError: If no .xbrl files are found.
    """
    dir_path = Path(directory).resolve()
    if not dir_path.exists():
        raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {dir_path}")

    instance = next(iter(sorted(dir_path.glob("*.xbrl"))), None) or _find_sec_instance(dir_path)
    if instance is None:
        raise XbrlParseError(f"디렉토리에 XBRL 파일이 없습니다: {dir_path}")

    return parse_xbrl_file(instance, include_taxonomy=include_taxonomy, http_user_agent=http_user_agent)


def _find_sec_instance(dir_path: Path) -> Path | None:
    """Pick the instance document out of an SEC filing folder's .xml files."""
    candidates = [p for p in sorted(dir_path.glob("*.xml")) if not _SEC_NON_INSTANCE.search(p.name)]
    # The SEC-extracted inline instance first; its name is the only reliable signal in a mixed folder.
    candidates.sort(key=lambda p: not p.name.lower().endswith("_htm.xml"))
    return next((p for p in candidates if _looks_like_instance(p)), None)


def _looks_like_instance(path: Path) -> bool:
    """Check the root element name without parsing the document (instances run to tens of MB)."""
    with path.open("rb") as handle:
        head = handle.read(8192)
    return _INSTANCE_ROOT.search(head) is not None


def _reporting_period_end(facts: list[XbrlFact]) -> date | None:
    """The reporting date of the document.

    SEC instances state it as ``dei:DocumentPeriodEndDate``. The latest instant would be wrong there: the
    cover page reports shares outstanding as of a date weeks after the period end. Other instances (DART)
    fall back to the latest instant date.
    """
    for fact in facts:
        if fact.concept_local_name == "DocumentPeriodEndDate" and fact.namespace.startswith(_DEI_NAMESPACE_PREFIX):
            try:
                return date.fromisoformat((fact.value or "").strip())
            except ValueError:
                break
    instant_dates = [f.period.instant for f in facts if f.period and f.period.instant]
    return max(instant_dates) if instant_dates else None


def _parse_with_session(path: Path, *, http_user_agent: str | None = None) -> ModelXbrl:
    """Load an XBRL file using Arelle Session with thread safety."""
    from arelle.api.Session import Session
    from arelle.ModelDocument import Type
    from arelle.RuntimeOptions import RuntimeOptions

    extra_options = {"httpUserAgent": http_user_agent} if http_user_agent else {}
    with _arelle_lock:
        with Session() as session:
            options = RuntimeOptions(
                entrypointFile=str(path),
                keepOpen=True,
                **extra_options,
            )
            session.run(options)
            models = session.get_models()
            if not models:
                raise XbrlParseError(f"XBRL 모델을 로드할 수 없습니다: {path}")
            model_xbrl = models[0]
            # Arelle reports unreadable files through the model's error log rather than raising,
            # so without these checks a broken file parses as a document with zero facts.
            document = model_xbrl.modelDocument
            if document is None:
                errors = ", ".join(str(error) for error in model_xbrl.errors)
                raise XbrlParseError(f"XBRL 문서를 읽을 수 없습니다: {path} ({errors})")
            if document.type not in (Type.INSTANCE, Type.INLINEXBRL):
                raise XbrlParseError(f"XBRL 인스턴스 문서가 아닙니다: {path}")
            return model_xbrl


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
                elif dim_value.isTyped and dim_value.typedMember is not None:
                    dimensions[str(dim_qname)] = dim_value.typedMember.stringValue

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
