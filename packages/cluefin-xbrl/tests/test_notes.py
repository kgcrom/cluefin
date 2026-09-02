"""Tests for financial statement note extraction."""

from datetime import date
from decimal import Decimal

import pytest

from cluefin_xbrl._types import (
    ConceptLabel,
    PeriodType,
    PresentationNode,
    TaxonomyInfo,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)
from cluefin_xbrl.notes import _identify_note_role, extract_notes


class TestIdentifyNoteRole:
    def test_consolidated_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/ias_19_role-D834480") == ("D834480", True)

    def test_separate_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/ias_19_role-D834485") == ("D834485", False)

    def test_statement_role_is_not_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000") is None

    def test_doc_role_is_not_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/dart-gcd_2024-06-30_role-D999001") is None

    def test_generic_role_is_not_note(self):
        assert _identify_note_role("http://example.com/role/SomeOtherRole") is None


def _make_doc(
    note_role: str = "http://dart.fss.or.kr/role/ifrs/ias_19_role-D834480",
    facts: list[XbrlFact] | None = None,
    labels: dict[str, ConceptLabel] | None = None,
) -> XbrlDocument:
    """확정급여 주석 1개 + 비주석(재무상태표) role 1개를 가진 합성 문서."""
    period = XbrlPeriod(period_type=PeriodType.INSTANT, instant=None)

    # 주석 트리: 추상 컨테이너 -> 값 노드(차원 있음)
    value_node = PresentationNode(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        depth=1,
        order=1.0,
    )
    root_node = PresentationNode(
        concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
        concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
        depth=0,
        order=0.0,
        children=[value_node],
    )
    # 비주석 role(재무상태표)도 트리에 넣어 걸러지는지 검증
    stmt_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000"
    stmt_node = PresentationNode(
        concept_local_name="Assets",
        concept_qname="ifrs-full:Assets",
    )

    default_labels = {
        "DisclosureOfDefinedBenefitPlansAbstract": ConceptLabel(
            concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
            concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
            label_ko="종업원급여에 대한 공시",
            label_en="Disclosure of defined benefit plans",
        ),
        "DefinedBenefitObligationAtPresentValue": ConceptLabel(
            concept_local_name="DefinedBenefitObligationAtPresentValue",
            concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
            label_ko="확정급여채무, 현재가치",
            label_en="Defined benefit obligation, at present value",
        ),
    }
    taxonomy = TaxonomyInfo(
        labels=labels if labels is not None else default_labels,
        presentation_trees={note_role: [root_node], stmt_role: [stmt_node]},
    )
    default_fact = XbrlFact(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        value="1000",
        numeric_value=Decimal("1000"),
        unit="iso4217:KRW",
        period=period,
        dimensions={"ifrs-full:Axis": "ifrs-full:Member"},
    )
    return XbrlDocument(
        source_file="entity_test.xbrl",
        facts=facts if facts is not None else [default_fact],
        entity_id="00000000",
        taxonomy=taxonomy,
    )


def _make_obligation_fact(period: XbrlPeriod) -> XbrlFact:
    return XbrlFact(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        value="1000",
        numeric_value=Decimal("1000"),
        unit="iso4217:KRW",
        period=period,
    )


class TestExtractNotes:
    def test_requires_taxonomy(self):
        doc = XbrlDocument(source_file="x.xbrl", facts=[])
        with pytest.raises(ValueError):
            extract_notes(doc)

    def test_extracts_only_note_roles(self):
        notes = extract_notes(_make_doc())
        # D834480 주석만, 재무상태표 D210000은 제외
        assert list(notes.notes.keys()) == ["D834480"]

    def test_note_section_metadata(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        assert section.role_code == "D834480"
        assert section.is_consolidated is True
        assert section.title == "종업원급여에 대한 공시"

    def test_dimensions_preserved(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        value_items = [li for li in section.line_items if not li.is_abstract]
        assert len(value_items) == 1
        assert value_items[0].dimensions == {"ifrs-full:Axis": "ifrs-full:Member"}
        assert value_items[0].value == Decimal("1000")
        assert value_items[0].text_value is None

    def test_abstract_node_has_no_value(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        abstract_items = [li for li in section.line_items if li.is_abstract]
        assert any(li.concept_local_name == "DisclosureOfDefinedBenefitPlansAbstract" for li in abstract_items)

    def test_separate_note_section(self):
        notes = extract_notes(_make_doc(note_role="http://dart.fss.or.kr/role/ifrs/ias_19_role-D834485"))
        section = notes.notes["D834485"]
        assert section.is_consolidated is False

    def test_title_falls_back_to_english_label(self):
        labels = {
            "DisclosureOfDefinedBenefitPlansAbstract": ConceptLabel(
                concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
                concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
                label_en="Disclosure of defined benefit plans",
            ),
        }
        section = extract_notes(_make_doc(labels=labels)).notes["D834480"]
        assert section.title == "Disclosure of defined benefit plans"

    def test_periods_deduplicated(self):
        p_2023 = XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2023, 12, 31))
        p_2022 = XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2022, 12, 31))
        facts = [_make_obligation_fact(p_2023), _make_obligation_fact(p_2023), _make_obligation_fact(p_2022)]
        section = extract_notes(_make_doc(facts=facts)).notes["D834480"]
        assert section.periods == [p_2023, p_2022]

    def test_consolidation_axis_filters_facts(self):
        """연결 주석에는 연결 fact만, 별도 주석에는 별도 fact만 매칭된다."""
        cons_axis = "ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis"

        def _fact(value: str, member: str) -> XbrlFact:
            return XbrlFact(
                concept_local_name="DefinedBenefitObligationAtPresentValue",
                concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
                namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
                value=value,
                numeric_value=Decimal(value),
                dimensions={cons_axis: member, "ifrs-full:Axis": "ifrs-full:Member"},
            )

        facts = [
            _fact("1000", "ifrs-full:ConsolidatedMember"),
            _fact("700", "ifrs-full:SeparateMember"),
        ]
        section = extract_notes(_make_doc(facts=facts)).notes["D834480"]
        value_items = [li for li in section.line_items if not li.is_abstract]
        assert [li.value for li in value_items] == [Decimal("1000")]
        # 연결/별도 축은 섹션의 is_consolidated로 대체되므로 dimensions에서 제거된다
        assert value_items[0].dimensions == {"ifrs-full:Axis": "ifrs-full:Member"}

    def test_text_value_for_string_fact(self):
        fact = XbrlFact(
            concept_local_name="DefinedBenefitObligationAtPresentValue",
            concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
            namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
            value="확정급여제도 관련 서술",
            numeric_value=None,
        )
        section = extract_notes(_make_doc(facts=[fact])).notes["D834480"]
        value_items = [li for li in section.line_items if not li.is_abstract]
        assert len(value_items) == 1
        assert value_items[0].value is None
        assert value_items[0].text_value == "확정급여제도 관련 서술"
