"""Tests for financial statement extraction."""

from decimal import Decimal

import pytest

from cluefin_xbrl._types import StatementType
from cluefin_xbrl.parser import parse_xbrl_file
from cluefin_xbrl.statements import (
    _identify_statement_type,
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
