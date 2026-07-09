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

    def test_dart_role_bs_liquidity_order(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D220000") == StatementType.BS
        )

    def test_dart_role_is_by_nature(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D320000") == StatementType.IS
        )

    def test_dart_role_cis_pretax(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D420000")
            == StatementType.CIS
        )

    def test_dart_role_single_comprehensive_income(self):
        """네이버 등은 손익계산서를 단일 포괄손익계산서(D43xxxx)로 공시한다."""
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D431410")
            == StatementType.CIS
        )

    def test_dart_role_cf_direct(self):
        assert (
            _identify_statement_type("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D510000") == StatementType.CF
        )


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


class TestFirstMatchPerType:
    def test_keeps_first_linkrole_per_type(self):
        """같은 유형(BS)의 linkrole이 둘이면 먼저 순회된 것만 유지된다."""
        node_a = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
        node_b = PresentationNode(concept_local_name="Equity", concept_qname="ifrs-full:Equity")
        role_a = "http://dart.fss.or.kr/role/ifrs/dart_role-D210000"
        role_b = "http://example.com/role/StatementOfFinancialPosition"
        taxonomy = TaxonomyInfo(presentation_trees={role_a: [node_a], role_b: [node_b]})
        doc = XbrlDocument(source_file="x.xbrl", facts=[], taxonomy=taxonomy)

        result = extract_financial_statements(doc)

        assert list(result.statements.keys()) == ["BS"]
        assert result.statements["BS"].linkrole == role_a


class TestStatementToDictsWithoutPeriod:
    def test_abstract_item_has_no_period_keys(self):
        node = PresentationNode(concept_local_name="AssetsAbstract", concept_qname="ifrs-full:AssetsAbstract")
        role = "http://example.com/role/StatementOfFinancialPosition"
        taxonomy = TaxonomyInfo(presentation_trees={role: [node]})
        doc = XbrlDocument(source_file="x.xbrl", facts=[], taxonomy=taxonomy)

        bs = extract_financial_statements(doc).statements["BS"]
        dicts = statement_to_dicts(bs)

        assert len(dicts) == 1
        assert dicts[0]["is_abstract"] is True
        assert dicts[0]["value"] is None
        assert "period_type" not in dicts[0]


_CONS_AXIS = "ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis"


def _make_assets_fact(value: str, dimensions: dict[str, str]) -> XbrlFact:
    return XbrlFact(
        concept_local_name="Assets",
        concept_qname="ifrs-full:Assets",
        namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        value=value,
        numeric_value=Decimal(value),
        period=XbrlPeriod(period_type=PeriodType.INSTANT),
        dimensions=dimensions,
    )


def _make_doc_with_dimensional_facts(facts: list[XbrlFact]) -> XbrlDocument:
    """연결(D210000) + 별도(D210005) 재무상태표 트리에 임의 fact들을 붙인 합성 문서."""
    consol_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000"
    sep_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210005"
    node = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
    taxonomy = TaxonomyInfo(
        presentation_trees={
            consol_role: [node.model_copy(deep=True)],
            sep_role: [node.model_copy(deep=True)],
        },
    )
    return XbrlDocument(source_file="x.xbrl", facts=facts, entity_id="00000000", taxonomy=taxonomy)


class TestConsolidationFactFiltering:
    """DART instance 문서는 fact에 연결/별도 축을 달아 구분하므로 본표 추출 시 이를 필터링해야 한다."""

    def test_facts_split_by_consolidation_member(self):
        facts = [
            _make_assets_fact("1000", {_CONS_AXIS: "ifrs-full:ConsolidatedMember"}),
            _make_assets_fact("700", {_CONS_AXIS: "ifrs-full:SeparateMember"}),
        ]
        result = extract_financial_statements(_make_doc_with_dimensional_facts(facts))

        cons_values = [i.value for i in result.statements["BS"].line_items if not i.is_abstract]
        sep_values = [i.value for i in result.separate_statements["BS"].line_items if not i.is_abstract]
        assert cons_values == [Decimal("1000")]
        assert sep_values == [Decimal("700")]

    def test_fact_without_axis_matches_both_bases(self):
        facts = [_make_assets_fact("1000", {})]
        result = extract_financial_statements(_make_doc_with_dimensional_facts(facts))

        assert [i.value for i in result.statements["BS"].line_items] == [Decimal("1000")]
        assert [i.value for i in result.separate_statements["BS"].line_items] == [Decimal("1000")]

    def test_note_level_dimensions_excluded_from_statement(self):
        """부문 등 주석용 축이 붙은 fact는 본표에서 제외된다."""
        facts = [
            _make_assets_fact("1000", {_CONS_AXIS: "ifrs-full:ConsolidatedMember"}),
            _make_assets_fact(
                "300",
                {
                    _CONS_AXIS: "ifrs-full:ConsolidatedMember",
                    "ifrs-full:SegmentsAxis": "entity:VehicleMember",
                },
            ),
        ]
        result = extract_financial_statements(_make_doc_with_dimensional_facts(facts))

        values = [i.value for i in result.statements["BS"].line_items if not i.is_abstract]
        assert values == [Decimal("1000")]

    def test_only_dimensional_facts_yield_abstract_item(self):
        facts = [_make_assets_fact("300", {"ifrs-full:SegmentsAxis": "entity:VehicleMember"})]
        result = extract_financial_statements(_make_doc_with_dimensional_facts(facts))

        items = result.statements["BS"].line_items
        assert len(items) == 1
        assert items[0].is_abstract is True

    def test_sce_keeps_equity_component_axis(self):
        """자본변동표의 자본구성요소 축은 본질적 컬럼이므로 유지되고 dimensions에 남는다."""
        sce_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D610000"
        node = PresentationNode(concept_local_name="Equity", concept_qname="ifrs-full:Equity")
        taxonomy = TaxonomyInfo(presentation_trees={sce_role: [node]})
        fact = XbrlFact(
            concept_local_name="Equity",
            concept_qname="ifrs-full:Equity",
            namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
            value="500",
            numeric_value=Decimal("500"),
            period=XbrlPeriod(period_type=PeriodType.INSTANT),
            dimensions={
                _CONS_AXIS: "ifrs-full:ConsolidatedMember",
                "ifrs-full:ComponentsOfEquityAxis": "ifrs-full:IssuedCapitalMember",
            },
        )
        doc = XbrlDocument(source_file="x.xbrl", facts=[fact], taxonomy=taxonomy)

        sce = extract_financial_statements(doc).statements["SCE"]
        assert [i.value for i in sce.line_items] == [Decimal("500")]
        # 연결/별도 축은 제거되고 자본구성요소 축만 남는다
        assert sce.line_items[0].dimensions == {"ifrs-full:ComponentsOfEquityAxis": "ifrs-full:IssuedCapitalMember"}


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
