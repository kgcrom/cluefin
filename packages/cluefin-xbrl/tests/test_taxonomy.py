"""Tests for XBRL taxonomy label and presentation processing."""

from types import SimpleNamespace

from arelle import XbrlConst

from cluefin_xbrl.parser import parse_xbrl_file
from cluefin_xbrl.taxonomy import _build_presentation_node, _extract_labels


class TestExtractLabels:
    def test_returns_korean_and_english(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)

        assert doc.taxonomy is not None
        labels = doc.taxonomy.labels

        assert "Assets" in labels
        assert labels["Assets"].label_ko == "자산총계"
        assert labels["Assets"].label_en == "Total assets"

        assert "Equity" in labels
        assert labels["Equity"].label_ko == "자본총계"
        assert labels["Equity"].label_en == "Total equity"

        assert "Revenue" in labels
        assert labels["Revenue"].label_ko == "수익(매출액)"
        assert labels["Revenue"].label_en == "Revenue"

    def test_standard_label_wins_over_terse(self, sample_xbrl_path):
        # 픽스처의 Assets에는 표준 레이블("자산총계")과 terse 레이블("자산")이 모두 있다.
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)

        assert doc.taxonomy.labels["Assets"].label_ko == "자산총계"

    def test_concept_qname_preserved(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)

        labels = doc.taxonomy.labels
        assert labels["Assets"].concept_qname == "sample:Assets"


class TestExtractPresentationTrees:
    def test_builds_hierarchy(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)

        assert doc.taxonomy is not None
        trees = doc.taxonomy.presentation_trees

        role = "http://example.com/role/StatementOfFinancialPosition"
        assert role in trees

        roots = trees[role]
        assert len(roots) == 1
        assert roots[0].concept_local_name == "Assets"
        assert roots[0].depth == 0

    def test_children_ordering(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)

        trees = doc.taxonomy.presentation_trees
        role = "http://example.com/role/StatementOfFinancialPosition"
        root = trees[role][0]

        assert len(root.children) == 1
        child = root.children[0]
        assert child.concept_local_name == "Equity"
        assert child.order == 1.0
        assert child.depth == 1

    def test_without_taxonomy(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=False)
        assert doc.taxonomy is None


class TestBuildPresentationNodeDepthAndOrder:
    """전용 합성 픽스처(pres_tree)로 3형제 정렬과 깊이 2 이상의 손자 노드를 검증한다."""

    def test_three_siblings_sorted_by_order(self, fixtures_dir):
        doc = parse_xbrl_file(fixtures_dir / "pres_tree" / "pres_tree.xbrl", include_taxonomy=True)

        role = "http://example.com/role/PresTreeRole"
        root = doc.taxonomy.presentation_trees[role][0]

        assert [c.concept_local_name for c in root.children] == ["ChildB", "ChildA", "ChildC"]
        assert [c.order for c in root.children] == [1.0, 2.0, 3.0]

    def test_grandchild_has_depth_two(self, fixtures_dir):
        doc = parse_xbrl_file(fixtures_dir / "pres_tree" / "pres_tree.xbrl", include_taxonomy=True)

        role = "http://example.com/role/PresTreeRole"
        root = doc.taxonomy.presentation_trees[role][0]
        child_b = next(c for c in root.children if c.concept_local_name == "ChildB")

        assert len(child_b.children) == 1
        grandchild = child_b.children[0]
        assert grandchild.concept_local_name == "Grandchild"
        assert grandchild.depth == 2
        assert grandchild.order == 1.0


class _QName:
    def __init__(self, local_name):
        self.localName = local_name

    def __str__(self):
        return f"sample:{self.localName}"


class TestDanglingRelationships:
    """관계의 대상이 해석되지 않으면(toModelObject=None) 그 관계만 건너뛴다."""

    def test_presentation_skips_unresolved_child(self):
        root = SimpleNamespace(qname=_QName("Root"))
        child = SimpleNamespace(qname=_QName("Child"))
        rels_by_concept = {
            "Root": [SimpleNamespace(order=2.0, toModelObject=child), SimpleNamespace(order=1.0, toModelObject=None)],
            "Child": [],
        }
        rel_set = SimpleNamespace(fromModelObject=lambda concept: rels_by_concept[concept.qname.localName])

        node = _build_presentation_node(rel_set, root, depth=0)

        assert [c.concept_local_name for c in node.children] == ["Child"]
        assert node.children[0].order == 2.0

    def test_labels_skip_unresolved_label(self):
        label = SimpleNamespace(role=XbrlConst.standardLabel, xmlLang="ko", text="자산")
        rels = [SimpleNamespace(toModelObject=None), SimpleNamespace(toModelObject=label)]
        label_rels = SimpleNamespace(fromModelObject=lambda concept: rels)
        model_xbrl = SimpleNamespace(
            relationshipSet=lambda arcrole: label_rels,
            qnameConcepts={_QName("Assets"): object()},
        )

        labels = _extract_labels(model_xbrl)

        assert labels["Assets"].label_ko == "자산"
        assert labels["Assets"].label_en is None
