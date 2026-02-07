"""Financial statement extraction from parsed XBRL data."""

from __future__ import annotations

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
    "StatementOfFinancialPosition": StatementType.BS,
    "FinancialPosition": StatementType.BS,
    "BalanceSheet": StatementType.BS,
    "BS": StatementType.BS,
    "IncomeStatement": StatementType.IS,
    "ProfitOrLoss": StatementType.IS,
    "IS": StatementType.IS,
    "ComprehensiveIncome": StatementType.CIS,
    "CIS": StatementType.CIS,
    "CashFlow": StatementType.CF,
    "CF": StatementType.CF,
    "ChangesInEquity": StatementType.SCE,
    "StatementsOfChangesInEquity": StatementType.SCE,
    "SCE": StatementType.SCE,
}


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

    for linkrole, roots in doc.taxonomy.presentation_trees.items():
        stmt_type = _identify_statement_type(linkrole)
        if stmt_type is None:
            continue

        line_items = _flatten_presentation_tree(roots, facts_by_concept, doc.taxonomy.labels)

        periods: list[XbrlPeriod] = []
        seen_periods: set[str] = set()
        for item in line_items:
            if item.period is not None:
                period_key = str(item.period)
                if period_key not in seen_periods:
                    seen_periods.add(period_key)
                    periods.append(item.period)

        statements[stmt_type.value] = FinancialStatement(
            statement_type=stmt_type,
            linkrole=linkrole,
            line_items=line_items,
            periods=periods,
        )

    return ParsedFinancialStatements(
        source_file=doc.source_file,
        entity_id=doc.entity_id,
        statements=statements,
    )


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
) -> list[StatementLineItem]:
    """Flatten presentation tree and match with facts to create line items."""
    items: list[StatementLineItem] = []
    for root in roots:
        _collect_line_items(root, facts_by_concept, labels, items)
    return items


def _collect_line_items(
    node: PresentationNode,
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
    items: list[StatementLineItem],
) -> None:
    """Recursively collect line items from a presentation node."""
    concept_facts = facts_by_concept.get(node.concept_local_name, [])
    label = labels.get(node.concept_local_name)

    label_ko = label.label_ko if label is not None and hasattr(label, "label_ko") else None
    label_en = label.label_en if label is not None and hasattr(label, "label_en") else None

    if concept_facts:
        for fact in concept_facts:
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
        _collect_line_items(child, facts_by_concept, labels, items)


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
        }
        if item.period is not None:
            row["period_type"] = item.period.period_type.value
            row["instant"] = str(item.period.instant) if item.period.instant else None
            row["start_date"] = str(item.period.start_date) if item.period.start_date else None
            row["end_date"] = str(item.period.end_date) if item.period.end_date else None
        rows.append(row)
    return rows
