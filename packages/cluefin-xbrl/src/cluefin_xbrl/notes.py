"""Financial statement note (disclosure) extraction from parsed XBRL data."""

from __future__ import annotations

import re

from cluefin_xbrl._types import (
    NoteLineItem,
    NoteSection,
    ParsedNotes,
    PresentationNode,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)
from cluefin_xbrl.statements import _CONSOLIDATION_AXIS, _SEPARATE_MEMBER, _local_name

_NOTE_ROLE_PATTERN = re.compile(r"role-(D8\d+)")


def _match_note_fact(fact: XbrlFact, is_consolidated: bool) -> dict[str, str] | None:
    """Decide whether a fact belongs to a note of the given basis.

    Returns the fact's dimensions with the consolidation axis removed (it is
    redundant with the section's ``is_consolidated`` flag) when the fact matches,
    or None when it belongs to the other basis. Facts without the consolidation
    axis match either basis.
    """
    dims: dict[str, str] = {}
    for axis, member in fact.dimensions.items():
        if _local_name(axis) == _CONSOLIDATION_AXIS:
            fact_is_separate = _local_name(member) == _SEPARATE_MEMBER
            if fact_is_separate == is_consolidated:
                return None
        else:
            dims[axis] = member
    return dims


def extract_notes(doc: XbrlDocument) -> ParsedNotes:
    """Extract structured financial statement notes from a parsed XBRL document.

    Requires the document to have taxonomy information (parsed with ``include_taxonomy=True``).

    Args:
        doc: XbrlDocument with taxonomy information.

    Returns:
        ParsedNotes with note sections keyed by role code.

    Raises:
        ValueError: If taxonomy information is not available.
    """
    if doc.taxonomy is None:
        raise ValueError("Taxonomy 정보가 필요합니다. parse_xbrl_file(include_taxonomy=True)로 파싱하세요.")

    facts_by_concept: dict[str, list[XbrlFact]] = {}
    for fact in doc.facts:
        facts_by_concept.setdefault(fact.concept_local_name, []).append(fact)

    notes: dict[str, NoteSection] = {}

    for linkrole, roots in doc.taxonomy.presentation_trees.items():
        identified = _identify_note_role(linkrole)
        if identified is None:
            continue
        role_code, is_consolidated = identified

        line_items = _flatten_note_tree(roots, facts_by_concept, doc.taxonomy.labels, is_consolidated)

        periods: list[XbrlPeriod] = []
        seen_periods: set[str] = set()
        for item in line_items:
            if item.period is not None:
                period_key = str(item.period)
                if period_key not in seen_periods:
                    seen_periods.add(period_key)
                    periods.append(item.period)

        title = None
        if roots:
            label = doc.taxonomy.labels.get(roots[0].concept_local_name)
            if label is not None:
                title = label.label_ko or label.label_en

        notes[role_code] = NoteSection(
            role_code=role_code,
            role_uri=linkrole,
            title=title,
            is_consolidated=is_consolidated,
            line_items=line_items,
            periods=periods,
        )

    return ParsedNotes(source_file=doc.source_file, entity_id=doc.entity_id, notes=notes)


def _flatten_note_tree(
    roots: list[PresentationNode],
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
    is_consolidated: bool,
) -> list[NoteLineItem]:
    """Flatten a note presentation tree and match with facts to create line items."""
    items: list[NoteLineItem] = []
    for root in roots:
        _collect_note_line_items(root, facts_by_concept, labels, is_consolidated, items)
    return items


def _collect_note_line_items(
    node: PresentationNode,
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
    is_consolidated: bool,
    items: list[NoteLineItem],
) -> None:
    """Recursively collect note line items, preserving dimensions, from a presentation node."""
    label = labels.get(node.concept_local_name)

    label_ko = label.label_ko if label is not None and hasattr(label, "label_ko") else None
    label_en = label.label_en if label is not None and hasattr(label, "label_en") else None

    matched: list[tuple[XbrlFact, dict[str, str]]] = []
    for fact in facts_by_concept.get(node.concept_local_name, []):
        dims = _match_note_fact(fact, is_consolidated)
        if dims is not None:
            matched.append((fact, dims))

    if matched:
        for fact, dims in matched:
            items.append(
                NoteLineItem(
                    concept_local_name=node.concept_local_name,
                    concept_qname=node.concept_qname,
                    label_ko=label_ko,
                    label_en=label_en,
                    value=fact.numeric_value,
                    text_value=fact.value if fact.numeric_value is None else None,
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
            NoteLineItem(
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
        _collect_note_line_items(child, facts_by_concept, labels, is_consolidated, items)


def _identify_note_role(linkrole: str) -> tuple[str, bool] | None:
    """Identify a note (disclosure) role code and consolidated flag from a linkrole URI.

    DART note linkroles carry a role code of the form ``D8xxxxx``. By DART convention a
    code ending in ``0`` is the consolidated note and one ending in ``5`` is the separate note.

    Returns:
        ``(role_code, is_consolidated)`` if the linkrole is a note role, else ``None``.
    """
    match = _NOTE_ROLE_PATTERN.search(linkrole)
    if match is None:
        return None
    role_code = match.group(1)
    is_consolidated = not role_code.endswith("5")
    return role_code, is_consolidated
