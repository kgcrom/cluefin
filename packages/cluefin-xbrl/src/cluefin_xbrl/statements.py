"""Financial statement extraction from parsed XBRL data."""

from __future__ import annotations

import re

from cluefin_xbrl._types import (
    FinancialStatement,
    ParsedFinancialStatements,
    PresentationNode,
    StatementLineItem,
    StatementType,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)

_STATEMENT_TYPE_PATTERNS: dict[str, StatementType] = {
    # Generic XBRL / IFRS linkrole patterns
    "StatementOfFinancialPosition": StatementType.BS,
    "FinancialPosition": StatementType.BS,
    "BalanceSheet": StatementType.BS,
    "IncomeStatement": StatementType.IS,
    "ProfitOrLoss": StatementType.IS,
    "ComprehensiveIncome": StatementType.CIS,
    "CashFlow": StatementType.CF,
    "ChangesInEquity": StatementType.SCE,
    "StatementsOfChangesInEquity": StatementType.SCE,
    # DART XBRL role codes (e.g. role-D210000 consolidated, role-D210005 separate).
    # Statements come in presentation variants with distinct code families:
    # BS 유동/비유동법(D21)·유동성배열법(D22), IS 기능별(D31)·성격별(D32),
    # CIS 세후(D41)·세전(D42)·단일 포괄손익계산서(D43),
    # CF 직접법(D51)·간접법(D52).
    "role-D21": StatementType.BS,
    "role-D22": StatementType.BS,
    "role-D31": StatementType.IS,
    "role-D32": StatementType.IS,
    "role-D41": StatementType.CIS,
    "role-D42": StatementType.CIS,
    "role-D43": StatementType.CIS,
    "role-D51": StatementType.CF,
    "role-D52": StatementType.CF,
    "role-D61": StatementType.SCE,
}

_ROLE_CODE_PATTERN = re.compile(r"role-(D\d+)")

# DART instance documents qualify nearly every fact with this axis; the member
# (ConsolidatedMember / SeparateMember) decides which statement the fact belongs to.
_CONSOLIDATION_AXIS = "ConsolidatedAndSeparateFinancialStatementsAxis"
_SEPARATE_MEMBER = "SeparateMember"

# Axes that form the columns of a statement itself (kept on line items). Facts
# carrying any other axis are note-level breakdowns and are excluded from statements.
_INTRINSIC_AXES_BY_TYPE: dict[StatementType, frozenset[str]] = {
    StatementType.SCE: frozenset({"ComponentsOfEquityAxis"}),
}


def _local_name(qname: str) -> str:
    """Strip a namespace prefix / URI from a qname-like string."""
    for sep in ("#", ":", "/"):
        if sep in qname:
            qname = qname.rsplit(sep, 1)[-1]
    return qname


def _match_statement_fact(
    fact: XbrlFact,
    is_consolidated: bool,
    intrinsic_axes: frozenset[str],
) -> dict[str, str] | None:
    """Decide whether a fact belongs to a statement of the given basis.

    Returns the fact's intrinsic dimensions (consolidation axis removed) when it
    matches, or None when it belongs to the other basis or carries note-level axes.
    Facts without the consolidation axis match either basis.
    """
    extra_dims: dict[str, str] = {}
    for axis, member in fact.dimensions.items():
        if _local_name(axis) == _CONSOLIDATION_AXIS:
            fact_is_separate = _local_name(member) == _SEPARATE_MEMBER
            if fact_is_separate == is_consolidated:
                return None
        else:
            extra_dims[axis] = member

    if any(_local_name(axis) not in intrinsic_axes for axis in extra_dims):
        return None
    return extra_dims


def extract_financial_statements(doc: XbrlDocument) -> ParsedFinancialStatements:
    """Extract structured financial statements from a parsed XBRL document.

    Requires the document to have taxonomy information (parsed with include_taxonomy=True).

    Args:
        doc: XbrlDocument with taxonomy information.

    Returns:
        ParsedFinancialStatements with statements organized by type.

    Raises:
        ValueError: If taxonomy information is not available.
    """
    if doc.taxonomy is None:
        raise ValueError("Taxonomy 정보가 필요합니다. parse_xbrl_file(include_taxonomy=True)로 파싱하세요.")

    facts_by_concept: dict[str, list[XbrlFact]] = {}
    for fact in doc.facts:
        facts_by_concept.setdefault(fact.concept_local_name, []).append(fact)

    statements: dict[str, FinancialStatement] = {}
    separate_statements: dict[str, FinancialStatement] = {}

    for linkrole, roots in doc.taxonomy.presentation_trees.items():
        stmt_type = _identify_statement_type(linkrole)
        if stmt_type is None:
            continue

        is_consolidated = _is_consolidated_role(linkrole)
        target = statements if is_consolidated else separate_statements
        intrinsic_axes = _INTRINSIC_AXES_BY_TYPE.get(stmt_type, frozenset())

        line_items = _flatten_presentation_tree(
            roots, facts_by_concept, doc.taxonomy.labels, is_consolidated, intrinsic_axes
        )

        periods: list[XbrlPeriod] = []
        seen_periods: set[str] = set()
        for item in line_items:
            if item.period is not None:
                period_key = str(item.period)
                if period_key not in seen_periods:
                    seen_periods.add(period_key)
                    periods.append(item.period)

        # Keep first match per type within each (consolidated / separate) group
        if stmt_type.value not in target:
            target[stmt_type.value] = FinancialStatement(
                statement_type=stmt_type,
                linkrole=linkrole,
                line_items=line_items,
                periods=periods,
                is_consolidated=is_consolidated,
            )

    return ParsedFinancialStatements(
        source_file=doc.source_file,
        entity_id=doc.entity_id,
        statements=statements,
        separate_statements=separate_statements,
    )


def _is_consolidated_role(linkrole: str) -> bool:
    """Determine whether a statement linkrole is consolidated (연결) or separate (별도).

    By DART convention the role code's trailing digit distinguishes the two: a code ending
    in ``5`` is the separate statement, anything else (e.g. ending in ``0``) is consolidated.
    Roles without a ``D``-code (generic IFRS roles) default to consolidated.
    """
    match = _ROLE_CODE_PATTERN.search(linkrole)
    if match is None:
        return True
    return not match.group(1).endswith("5")


def _identify_statement_type(linkrole: str) -> StatementType | None:
    """Identify the financial statement type from a linkrole URI."""
    for pattern, stmt_type in _STATEMENT_TYPE_PATTERNS.items():
        if pattern in linkrole:
            return stmt_type
    return None


def _flatten_presentation_tree(
    roots: list[PresentationNode],
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
    is_consolidated: bool,
    intrinsic_axes: frozenset[str],
) -> list[StatementLineItem]:
    """Flatten presentation tree and match with facts to create line items."""
    items: list[StatementLineItem] = []
    for root in roots:
        _collect_line_items(root, facts_by_concept, labels, is_consolidated, intrinsic_axes, items)
    return items


def _collect_line_items(
    node: PresentationNode,
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
    is_consolidated: bool,
    intrinsic_axes: frozenset[str],
    items: list[StatementLineItem],
) -> None:
    """Recursively collect line items from a presentation node."""
    label = labels.get(node.concept_local_name)

    label_ko = label.label_ko if label is not None and hasattr(label, "label_ko") else None
    label_en = label.label_en if label is not None and hasattr(label, "label_en") else None

    matched: list[tuple[XbrlFact, dict[str, str]]] = []
    for fact in facts_by_concept.get(node.concept_local_name, []):
        dims = _match_statement_fact(fact, is_consolidated, intrinsic_axes)
        if dims is not None:
            matched.append((fact, dims))

    if matched:
        for fact, dims in matched:
            items.append(
                StatementLineItem(
                    concept_local_name=node.concept_local_name,
                    concept_qname=node.concept_qname,
                    label_ko=label_ko,
                    label_en=label_en,
                    value=fact.numeric_value,
                    unit=fact.unit,
                    period=fact.period,
                    depth=node.depth,
                    order=node.order,
                    is_abstract=False,
                    dimensions=dims,
                )
            )
    else:
        items.append(
            StatementLineItem(
                concept_local_name=node.concept_local_name,
                concept_qname=node.concept_qname,
                label_ko=label_ko,
                label_en=label_en,
                depth=node.depth,
                order=node.order,
                is_abstract=True,
            )
        )

    for child in node.children:
        _collect_line_items(child, facts_by_concept, labels, is_consolidated, intrinsic_axes, items)


def statement_to_dicts(statement: FinancialStatement) -> list[dict]:
    """Convert a FinancialStatement to a list of dictionaries for DataFrame conversion.

    Args:
        statement: FinancialStatement to convert.

    Returns:
        List of dicts with flattened line item data.
    """
    rows = []
    for item in statement.line_items:
        row = {
            "concept": item.concept_local_name,
            "concept_qname": item.concept_qname,
            "label_ko": item.label_ko,
            "label_en": item.label_en,
            "value": float(item.value) if item.value is not None else None,
            "unit": item.unit,
            "depth": item.depth,
            "order": item.order,
            "is_abstract": item.is_abstract,
            "dimensions": dict(item.dimensions),
        }
        if item.period is not None:
            row["period_type"] = item.period.period_type.value
            row["instant"] = str(item.period.instant) if item.period.instant else None
            row["start_date"] = str(item.period.start_date) if item.period.start_date else None
            row["end_date"] = str(item.period.end_date) if item.period.end_date else None
        rows.append(row)
    return rows
