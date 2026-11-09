"""`note_figures`: standard note accounts out of XBRL facts. Synthetic facts, no real filings."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from cluefin_xbrl import PeriodType, XbrlFact, XbrlPeriod

from cluefin_openapi_cli.note_figures import NOTE_ITEMS, note_figures

END = date(2025, 12, 31)
AXIS = "ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis"


def _fact(qname: str, value: str, start: date = date(2025, 1, 1), end: date = END, **dims: str) -> XbrlFact:
    return XbrlFact(
        concept_local_name=qname.split(":")[1],
        concept_qname=qname,
        namespace="",
        numeric_value=Decimal(value),
        period=XbrlPeriod(period_type=PeriodType.DURATION, start_date=start, end_date=end),
        dimensions=dict(dims),
    )


def test_reads_each_basis_from_the_consolidation_axis() -> None:
    facts = [
        _fact("ifrs-full:DepreciationPropertyPlantAndEquipment", "300", **{AXIS: "ifrs-full:ConsolidatedMember"}),
        _fact("ifrs-full:DepreciationPropertyPlantAndEquipment", "120", **{AXIS: "ifrs-full:SeparateMember"}),
    ]

    figures = note_figures(facts, END, ["consolidated", "separate"])

    assert figures["consolidated"]["depreciation_ppe"] == "300"
    assert figures["separate"]["depreciation_ppe"] == "120"
    assert figures["consolidated"]["amortisation_intangibles"] is None
    assert set(figures["consolidated"]) == set(NOTE_ITEMS)


def test_fact_without_the_axis_counts_for_either_basis() -> None:
    facts = [_fact("ifrs-full:IncomeTaxesPaidRefundClassifiedAsOperatingActivities", "55")]

    figures = note_figures(facts, END, ["consolidated", "separate"])

    assert figures["consolidated"]["income_taxes_paid"] == "55"
    assert figures["separate"]["income_taxes_paid"] == "55"


def test_breakdown_by_another_axis_is_skipped() -> None:
    facts = [
        _fact(
            "ifrs-full:DepreciationPropertyPlantAndEquipment",
            "80",
            **{
                AXIS: "ifrs-full:ConsolidatedMember",
                "ifrs-full:ClassesOfPropertyPlantAndEquipmentAxis": "ifrs-full:BuildingsMember",
            },
        )
    ]

    assert note_figures(facts, END, ["consolidated"])["consolidated"]["depreciation_ppe"] is None


def test_longest_period_ending_on_the_report_end_wins() -> None:
    # A Q3 report carries the quarter and the year-to-date; the year-to-date is the figure.
    facts = [
        _fact("ifrs-full:FinanceCosts", "10", start=date(2025, 7, 1), end=date(2025, 9, 30)),
        _fact("ifrs-full:FinanceCosts", "30", start=date(2025, 1, 1), end=date(2025, 9, 30)),
        _fact("ifrs-full:FinanceCosts", "40", start=date(2024, 1, 1), end=date(2024, 12, 31)),
    ]

    assert note_figures(facts, date(2025, 9, 30), ["consolidated"])["consolidated"]["finance_costs"] == "30"


def test_first_listed_id_wins() -> None:
    facts = [
        _fact("dart:InterestExpenseFinanceExpense", "7"),
        _fact("ifrs-full:InterestExpense", "9"),
    ]

    assert note_figures(facts, END, ["consolidated"])["consolidated"]["interest_expense"] == "9"


def test_no_period_end_gives_nothing() -> None:
    facts = [_fact("ifrs-full:FinanceCosts", "30")]

    assert note_figures(facts, None, ["consolidated"])["consolidated"]["finance_costs"] is None
