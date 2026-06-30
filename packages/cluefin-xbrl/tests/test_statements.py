"""Tests for financial statement extraction."""

from decimal import Decimal

import pytest

from cluefin_xbrl._types import (
    ConceptLabel,
    PeriodType,
    PresentationNode,
    StatementType,
    TaxonomyInfo,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)
from cluefin_xbrl.parser import parse_xbrl_file
from cluefin_xbrl.statements import (
    _identify_statement_type,
    _is_consolidated_role,
    extract_financial_statements,
    statement_to_dicts,
)


class TestIdentifyStatementType:
    def test_financial_position(self):
        assert _identify_statement_type("http://example.com/role/StatementOfFinancialPosition") == StatementType.BS

    def test_income_statement(self):
        assert _identify_statement_type("http://example.com/role/IncomeStatement") == StatementType.IS

    def test_profit_or_loss(self):
        assert _identify_statement_type("http://example.com/role/ProfitOrLoss") == StatementType.IS

    def test_comprehensive_income(self):
        assert _identify_statement_type("http://example.com/role/ComprehensiveIncome") == StatementType.CIS

    def test_cash_flow(self):
        assert _identify_statement_type("http://example.com/role/CashFlow") == StatementType.CF

    def test_changes_in_equity(self):
        assert _identify_statement_type("http://example.com/role/ChangesInEquity") == StatementType.SCE

    def test_unknown_role(self):
        assert _identify_statement_type("http://example.com/role/SomeOtherRole") is None

    def test_dart_role_bs(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000") == StatementType.BS
        )

    def test_dart_role_bs_separate(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210005") == StatementType.BS
        )

    def test_dart_role_is(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D310000") == StatementType.IS
        )

    def test_dart_role_cis(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D410000")
            == StatementType.CIS
        )

    def test_dart_role_cf(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D520000") == StatementType.CF
        )

    def test_dart_role_sce(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D610000")
            == StatementType.SCE
        )

    def test_dart_note_role_no_match(self):
        assert _identify_statement_type("http://dart.fss.or.kr/role/ifrs/ias_10_role-D815000") is None


class TestExtractFinancialStatements:
    def test_from_document(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)

        assert result.source_file.endswith("sample.xbrl")
        assert result.entity_id == "00126380"
        assert "BS" in result.statements

    def test_bs_line_items(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)

        bs = result.statements["BS"]
        assert bs.statement_type == StatementType.BS
        assert "StatementOfFinancialPosition" in bs.linkrole

        concepts = [item.concept_local_name for item in bs.line_items]
        assert "Assets" in concepts
        assert "Equity" in concepts

    def test_line_item_values(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)

        bs = result.statements["BS"]
        assets_items = [item for item in bs.line_items if item.concept_local_name == "Assets"]
        assert len(assets_items) == 1
        assert assets_items[0].value == Decimal("1000000000000")
        assert assets_items[0].label_ko == "자산총계"
        assert assets_items[0].label_en == "Total assets"

    def test_line_item_depth(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)

        bs = result.statements["BS"]
        assets_item = next(i for i in bs.line_items if i.concept_local_name == "Assets")
        equity_item = next(i for i in bs.line_items if i.concept_local_name == "Equity")
        assert assets_item.depth == 0
        assert equity_item.depth == 1

    def test_requires_taxonomy(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=False)
        with pytest.raises(ValueError, match="Taxonomy"):
            extract_financial_statements(doc)


class TestStatementToDicts:
    def test_conversion(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)

        bs = result.statements["BS"]
        dicts = statement_to_dicts(bs)

        assert len(dicts) >= 2
        assets_dict = next(d for d in dicts if d["concept"] == "Assets")
        assert assets_dict["value"] == 1000000000000.0
        assert assets_dict["label_ko"] == "자산총계"
        assert assets_dict["depth"] == 0
        assert "period_type" in assets_dict


class TestIsConsolidatedRole:
    def test_consolidated(self):
        assert _is_consolidated_role("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000") is True

    def test_separate(self):
        assert _is_consolidated_role("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210005") is False

    def test_generic_defaults_consolidated(self):
        assert _is_consolidated_role("http://example.com/role/StatementOfFinancialPosition") is True


def _make_doc_with_separate() -> XbrlDocument:
    """연결(D210000) + 별도(D210005) 재무상태표를 가진 합성 문서."""
    consol_node = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
    sep_node = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
    consol_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000"
    sep_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210005"
    labels = {
        "Assets": ConceptLabel(
            concept_local_name="Assets",
            concept_qname="ifrs-full:Assets",
            label_ko="자산총계",
            label_en="Total assets",
        ),
    }
    taxonomy = TaxonomyInfo(
        labels=labels,
        presentation_trees={consol_role: [consol_node], sep_role: [sep_node]},
    )
    fact = XbrlFact(
        concept_local_name="Assets",
        concept_qname="ifrs-full:Assets",
        namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        value="1000",
        numeric_value=Decimal("1000"),
        period=XbrlPeriod(period_type=PeriodType.INSTANT),
    )
    return XbrlDocument(source_file="x.xbrl", facts=[fact], entity_id="00000000", taxonomy=taxonomy)


class TestSeparateStatements:
    def test_consolidated_in_statements(self):
        result = extract_financial_statements(_make_doc_with_separate())
        assert "BS" in result.statements
        assert result.statements["BS"].is_consolidated is True

    def test_separate_in_separate_statements(self):
        result = extract_financial_statements(_make_doc_with_separate())
        assert "BS" in result.separate_statements
        assert result.separate_statements["BS"].is_consolidated is False

    def test_separate_empty_when_no_separate_role(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)
        assert result.separate_statements == {}
