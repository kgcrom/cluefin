"""Tests for XBRL taxonomy label and presentation processing."""

from cluefin_xbrl.parser import parse_xbrl_file


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
