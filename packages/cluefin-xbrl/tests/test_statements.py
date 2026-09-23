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
    _local_name,
    extract_financial_statements,
    statement_to_dicts,
)

_LOCAL_NAME_CASES = [
    pytest.param("ifrs-full:Assets", "Assets", id="colon_separator"),
    pytest.param("http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full#Assets", "Assets", id="hash_separator"),
    pytest.param("http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full/Assets", "Assets", id="slash_separator"),
    pytest.param("Assets", "Assets", id="no_separator"),
]


class TestLocalName:
    @pytest.mark.parametrize("qname, expected", _LOCAL_NAME_CASES)
    def test_local_name(self, qname, expected):
        assert _local_name(qname) == expected


_IDENTIFY_STATEMENT_TYPE_CASES = [
    pytest.param("http://example.com/role/StatementOfFinancialPosition", StatementType.BS, id="financial_position"),
    pytest.param("http://example.com/role/IncomeStatement", StatementType.IS, id="income_statement"),
    pytest.param("http://example.com/role/ProfitOrLoss", StatementType.IS, id="profit_or_loss"),
    pytest.param("http://example.com/role/ComprehensiveIncome", StatementType.CIS, id="comprehensive_income"),
    pytest.param("http://example.com/role/CashFlow", StatementType.CF, id="cash_flow"),
    pytest.param("http://example.com/role/ChangesInEquity", StatementType.SCE, id="changes_in_equity"),
    pytest.param("http://example.com/role/SomeOtherRole", None, id="unknown_role"),
    pytest.param("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000", StatementType.BS, id="dart_role_bs"),
    pytest.param(
        "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210005",
        StatementType.BS,
        id="dart_role_bs_separate",
    ),
    pytest.param("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D310000", StatementType.IS, id="dart_role_is"),
    pytest.param("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D410000", StatementType.CIS, id="dart_role_cis"),
    pytest.param("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D520000", StatementType.CF, id="dart_role_cf"),
    pytest.param("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D610000", StatementType.SCE, id="dart_role_sce"),
    pytest.param("http://dart.fss.or.kr/role/ifrs/ias_10_role-D815000", None, id="dart_note_role_no_match"),
    pytest.param(
        "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D220000",
        StatementType.BS,
        id="dart_role_bs_liquidity_order",
    ),
    pytest.param(
        "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D320000",
        StatementType.IS,
        id="dart_role_is_by_nature",
    ),
    pytest.param(
        "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D420000",
        StatementType.CIS,
        id="dart_role_cis_pretax",
    ),
    pytest.param(
        # 네이버 등은 손익계산서를 단일 포괄손익계산서(D43xxxx)로 공시한다.
        "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D431410",
        StatementType.CIS,
        id="dart_role_single_comprehensive_income",
    ),
    pytest.param(
        "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D510000",
        StatementType.CF,
        id="dart_role_cf_direct",
    ),
]


class TestIdentifyStatementType:
    @pytest.mark.parametrize("linkrole, expected", _IDENTIFY_STATEMENT_TYPE_CASES)
    def test_identify_statement_type(self, linkrole, expected):
        assert _identify_statement_type(linkrole) == expected


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

    def test_other_trailing_digit_defaults_consolidated(self):
        """0/5로 끝나지 않는 D-code(D210003)는 관측된 DART 동작상 연결로 취급된다."""
        assert _is_consolidated_role("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210003") is True


def _make_doc_with_separate(dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact) -> XbrlDocument:
    """연결(D210000) + 별도(D210005) 재무상태표를 가진 합성 문서."""
    consol_node = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
    sep_node = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
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
        presentation_trees={dart_role_bs_consolidated: [consol_node], dart_role_bs_separate: [sep_node]},
    )
    fact = make_xbrl_fact(value="1000")
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

    def test_concept_without_label_has_no_labels(self):
        """라벨링크에 없는 concept은 label_ko/label_en이 모두 None이다."""
        node = PresentationNode(concept_local_name="Unlabeled", concept_qname="ifrs-full:Unlabeled")
        role = "http://example.com/role/StatementOfFinancialPosition"
        taxonomy = TaxonomyInfo(presentation_trees={role: [node]})
        doc = XbrlDocument(source_file="x.xbrl", facts=[], taxonomy=taxonomy)

        bs = extract_financial_statements(doc).statements["BS"]

        assert bs.line_items[0].label_ko is None
        assert bs.line_items[0].label_en is None


def _make_doc_with_dimensional_facts(
    facts: list[XbrlFact], dart_role_bs_consolidated, dart_role_bs_separate
) -> XbrlDocument:
    """연결(D210000) + 별도(D210005) 재무상태표 트리에 임의 fact들을 붙인 합성 문서."""
    node = PresentationNode(concept_local_name="Assets", concept_qname="ifrs-full:Assets")
    taxonomy = TaxonomyInfo(
        presentation_trees={
            dart_role_bs_consolidated: [node.model_copy(deep=True)],
            dart_role_bs_separate: [node.model_copy(deep=True)],
        },
    )
    return XbrlDocument(source_file="x.xbrl", facts=facts, entity_id="00000000", taxonomy=taxonomy)


class TestConsolidationFactFiltering:
    """DART instance 문서는 fact에 연결/별도 축을 달아 구분하므로 본표 추출 시 이를 필터링해야 한다."""

    def test_facts_split_by_consolidation_member(
        self, consolidated_axis, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact
    ):
        facts = [
            make_xbrl_fact(value="1000", dimensions={consolidated_axis: "ifrs-full:ConsolidatedMember"}),
            make_xbrl_fact(value="700", dimensions={consolidated_axis: "ifrs-full:SeparateMember"}),
        ]
        doc = _make_doc_with_dimensional_facts(facts, dart_role_bs_consolidated, dart_role_bs_separate)
        result = extract_financial_statements(doc)

        cons_values = [i.value for i in result.statements["BS"].line_items if not i.is_abstract]
        sep_values = [i.value for i in result.separate_statements["BS"].line_items if not i.is_abstract]
        assert cons_values == [Decimal("1000")]
        assert sep_values == [Decimal("700")]

    def test_fact_without_axis_matches_both_bases(
        self, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact
    ):
        facts = [make_xbrl_fact(value="1000")]
        doc = _make_doc_with_dimensional_facts(facts, dart_role_bs_consolidated, dart_role_bs_separate)
        result = extract_financial_statements(doc)

        assert [i.value for i in result.statements["BS"].line_items] == [Decimal("1000")]
        assert [i.value for i in result.separate_statements["BS"].line_items] == [Decimal("1000")]

    def test_note_level_dimensions_excluded_from_statement(
        self, consolidated_axis, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact
    ):
        """부문 등 주석용 축이 붙은 fact는 본표에서 제외된다."""
        facts = [
            make_xbrl_fact(value="1000", dimensions={consolidated_axis: "ifrs-full:ConsolidatedMember"}),
            make_xbrl_fact(
                value="300",
                dimensions={
                    consolidated_axis: "ifrs-full:ConsolidatedMember",
                    "ifrs-full:SegmentsAxis": "entity:VehicleMember",
                },
            ),
        ]
        doc = _make_doc_with_dimensional_facts(facts, dart_role_bs_consolidated, dart_role_bs_separate)
        result = extract_financial_statements(doc)

        values = [i.value for i in result.statements["BS"].line_items if not i.is_abstract]
        assert values == [Decimal("1000")]

    def test_only_dimensional_facts_yield_abstract_item(
        self, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact
    ):
        facts = [make_xbrl_fact(value="300", dimensions={"ifrs-full:SegmentsAxis": "entity:VehicleMember"})]
        doc = _make_doc_with_dimensional_facts(facts, dart_role_bs_consolidated, dart_role_bs_separate)
        result = extract_financial_statements(doc)

        items = result.statements["BS"].line_items
        assert len(items) == 1
        assert items[0].is_abstract is True

    def test_unrecognized_consolidation_member_treated_as_consolidated(
        self, consolidated_axis, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact
    ):
        """ConsolidatedMember/SeparateMember 어느 쪽도 아닌 멤버는 관측된 현재 동작상
        연결(consolidated) 쪽에만 매칭되고 별도 쪽에서는 제외된다."""
        facts = [make_xbrl_fact(value="1000", dimensions={consolidated_axis: "ifrs-full:SomeOtherMember"})]
        doc = _make_doc_with_dimensional_facts(facts, dart_role_bs_consolidated, dart_role_bs_separate)
        result = extract_financial_statements(doc)

        cons_values = [i.value for i in result.statements["BS"].line_items if not i.is_abstract]
        sep_values = [i.value for i in result.separate_statements["BS"].line_items if not i.is_abstract]
        assert cons_values == [Decimal("1000")]
        assert sep_values == []

    def test_sce_keeps_equity_component_axis(self, consolidated_axis):
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
                consolidated_axis: "ifrs-full:ConsolidatedMember",
                "ifrs-full:ComponentsOfEquityAxis": "ifrs-full:IssuedCapitalMember",
            },
        )
        doc = XbrlDocument(source_file="x.xbrl", facts=[fact], taxonomy=taxonomy)

        sce = extract_financial_statements(doc).statements["SCE"]
        assert [i.value for i in sce.line_items] == [Decimal("500")]
        # 연결/별도 축은 제거되고 자본구성요소 축만 남는다
        assert sce.line_items[0].dimensions == {"ifrs-full:ComponentsOfEquityAxis": "ifrs-full:IssuedCapitalMember"}


class TestSeparateStatements:
    def test_consolidated_in_statements(self, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact):
        doc = _make_doc_with_separate(dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact)
        result = extract_financial_statements(doc)
        assert "BS" in result.statements
        assert result.statements["BS"].is_consolidated is True

    def test_separate_in_separate_statements(self, dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact):
        doc = _make_doc_with_separate(dart_role_bs_consolidated, dart_role_bs_separate, make_xbrl_fact)
        result = extract_financial_statements(doc)
        assert "BS" in result.separate_statements
        assert result.separate_statements["BS"].is_consolidated is False

    def test_separate_empty_when_no_separate_role(self, sample_xbrl_path):
        doc = parse_xbrl_file(sample_xbrl_path, include_taxonomy=True)
        result = extract_financial_statements(doc)
        assert result.separate_statements == {}
