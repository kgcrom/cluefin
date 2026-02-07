"""XBRL taxonomy label and presentation linkbase processing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_xbrl._types import ConceptLabel, PresentationNode, TaxonomyInfo

if TYPE_CHECKING:
    from arelle.ModelDtsObject import ModelConcept, ModelRelationship
    from arelle.ModelRelationshipSet import ModelRelationshipSet
    from arelle.ModelXbrl import ModelXbrl


def extract_taxonomy(model_xbrl: ModelXbrl) -> TaxonomyInfo:
    """Extract taxonomy labels and presentation trees from a loaded XBRL model.

    Args:
        model_xbrl: Arelle ModelXbrl object with loaded DTS.

    Returns:
        TaxonomyInfo with labels and presentation trees.
    """
    labels = _extract_labels(model_xbrl)
    presentation_trees = _extract_presentation_trees(model_xbrl)
    return TaxonomyInfo(labels=labels, presentation_trees=presentation_trees)


def _extract_labels(model_xbrl: ModelXbrl) -> dict[str, ConceptLabel]:
    """Extract Korean and English labels from the concept-label relationship set."""
    from arelle import XbrlConst

    label_rels: ModelRelationshipSet = model_xbrl.relationshipSet(XbrlConst.conceptLabel)
    labels: dict[str, ConceptLabel] = {}

    for qname, concept in model_xbrl.qnameConcepts.items():
        rels = label_rels.fromModelObject(concept)
        if not rels:
            continue

        label_ko = None
        label_en = None

        for rel in rels:
            label_obj = rel.toModelObject
            if label_obj is None:
                continue
            lang = label_obj.xmlLang
            if lang == "ko":
                label_ko = label_obj.text
            elif lang == "en":
                label_en = label_obj.text

        if label_ko is not None or label_en is not None:
            local_name = qname.localName
            labels[local_name] = ConceptLabel(
                concept_local_name=local_name,
                concept_qname=str(qname),
                label_ko=label_ko,
                label_en=label_en,
            )

    return labels


def _extract_presentation_trees(model_xbrl: ModelXbrl) -> dict[str, list[PresentationNode]]:
    """Extract presentation trees organized by linkrole."""
    from arelle import XbrlConst

    all_pres_rels: ModelRelationshipSet = model_xbrl.relationshipSet(XbrlConst.parentChild)
    trees: dict[str, list[PresentationNode]] = {}

    for linkrole in all_pres_rels.linkRoleUris:
        role_rels: ModelRelationshipSet = model_xbrl.relationshipSet(XbrlConst.parentChild, linkrole)
        root_concepts = role_rels.rootConcepts

        root_nodes = []
        for root_concept in root_concepts:
            node = _build_presentation_node(role_rels, root_concept, depth=0)
            root_nodes.append(node)

        root_nodes.sort(key=lambda n: n.order)
        trees[linkrole] = root_nodes

    return trees


def _build_presentation_node(
    rel_set: ModelRelationshipSet,
    concept: ModelConcept,
    depth: int,
    order: float = 0.0,
) -> PresentationNode:
    """Recursively build a presentation tree node."""
    child_rels: list[ModelRelationship] = rel_set.fromModelObject(concept)
    children = []

    for rel in sorted(child_rels, key=lambda r: r.order):
        child_concept = rel.toModelObject
        if child_concept is None:
            continue
        child_node = _build_presentation_node(rel_set, child_concept, depth=depth + 1, order=rel.order)
        children.append(child_node)

    return PresentationNode(
        concept_local_name=concept.qname.localName,
        concept_qname=str(concept.qname),
        order=order,
        depth=depth,
        children=children,
    )
