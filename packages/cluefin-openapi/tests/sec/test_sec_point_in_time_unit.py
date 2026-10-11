"""Unit tests for `values_as_of`: point-in-time row selection over companyfacts/companyconcept rows.

Rows are shaped after real ones measured 2026-10-11 (CELH restatement, SMCI same-day 10-Q/10-K).
"""

from datetime import date
from decimal import Decimal
from typing import Optional

import pytest

from cluefin_openapi.sec import CompanyConcept, FactValue, values_as_of


def _row(
    accn: str,
    filed: date,
    val: int,
    *,
    end: date = date(2021, 12, 31),
    start: Optional[date] = None,
    form: str = "10-K",
    frame: Optional[str] = None,
) -> FactValue:
    return FactValue(start=start, end=end, val=Decimal(val), accn=accn, form=form, filed=filed, frame=frame)


# CELH AccountsPayableAndAccruedLiabilitiesCurrent at 2021-12-31: original 10-K, next year's restated
# comparative, then a 10-K/A carrying the same restated value and SEC's frame.
ORIGINAL = _row("0000950170-22-003965", date(2022, 3, 16), 91_478_612)
RESTATED = _row("0000950170-23-005612", date(2023, 3, 1), 72_442_000)
AMENDED = _row("0001829126-23-002816", date(2023, 4, 19), 72_442_000, form="10-K/A", frame="CY2021Q4I")
RESTATEMENT_ROWS = [ORIGINAL, RESTATED, AMENDED]


@pytest.mark.parametrize(
    ("as_of", "expected"),
    [
        (date(2022, 3, 16), []),
        (date(2022, 3, 17), [ORIGINAL]),
        (date(2023, 3, 1), [ORIGINAL]),
        (date(2023, 3, 2), [RESTATED]),
        (date(2024, 1, 1), [AMENDED]),
    ],
)
def test_picks_latest_row_filed_before_as_of(as_of, expected):
    assert values_as_of(RESTATEMENT_ROWS, as_of) == expected


def test_row_filed_on_as_of_is_not_yet_public():
    assert values_as_of([ORIGINAL], ORIGINAL.filed) == []


def test_frame_does_not_pull_in_a_later_row():
    picked = values_as_of(RESTATEMENT_ROWS, date(2022, 6, 1))

    assert picked == [ORIGINAL]
    assert picked[0].frame is None


def test_input_order_does_not_matter():
    assert values_as_of(reversed(RESTATEMENT_ROWS), date(2023, 3, 2)) == [RESTATED]


def test_same_day_same_filer_picks_higher_sequence():
    # SMCI ProfitLoss 2017Q3: a 10-Q and the late 10-K were filed the same day with different values.
    quarter = {"start": date(2017, 7, 1), "end": date(2017, 9, 30)}
    tenq = _row("0001375365-19-000076", date(2019, 12, 19), 6_075_000, form="10-Q", **quarter)
    tenk = _row("0001375365-19-000079", date(2019, 12, 19), 6_079_000, frame="CY2017Q3", **quarter)

    assert values_as_of([tenk, tenq], date(2019, 12, 20)) == [tenk]
    assert values_as_of([tenq, tenk], date(2019, 12, 20)) == [tenk]


def test_same_day_different_filers_is_an_error():
    own = _row("0001375365-19-000079", date(2019, 12, 19), 6_079_000)
    agent = _row("0001628280-19-015000", date(2019, 12, 19), 6_075_000)

    with pytest.raises(ValueError, match="0001375365-19-000079") as excinfo:
        values_as_of([own, agent], date(2019, 12, 20))
    assert "0001628280-19-015000" in str(excinfo.value)


def test_same_day_different_filers_before_a_later_row_is_fine():
    own = _row("0001375365-19-000079", date(2019, 12, 19), 6_079_000)
    agent = _row("0001628280-19-015000", date(2019, 12, 19), 6_075_000)
    later = _row("0001375365-20-000064", date(2020, 8, 31), 6_079_000)

    assert values_as_of([own, agent, later], date(2021, 1, 1)) == [later]


def test_one_filing_with_two_values_for_a_period_is_an_error():
    first = _row("0000950170-22-003965", date(2022, 3, 16), 91_478_612)
    second = _row("0000950170-22-003965", date(2022, 3, 16), 91_479_000)

    with pytest.raises(ValueError, match="다른 값"):
        values_as_of([first, second], date(2023, 1, 1))


def test_duplicate_rows_of_one_filing_collapse():
    assert values_as_of([ORIGINAL, ORIGINAL.model_copy()], date(2023, 1, 1)) == [ORIGINAL]


def test_one_row_per_period_ordered_by_end_then_start():
    filed = date(2023, 11, 3)
    instant = _row("0000320193-23-000106", filed, 1, end=date(2023, 9, 30))
    year = _row("0000320193-23-000106", filed, 2, start=date(2022, 9, 25), end=date(2023, 9, 30))
    quarter = _row("0000320193-23-000106", filed, 3, start=date(2023, 7, 2), end=date(2023, 9, 30))
    prior = _row("0000320193-23-000106", filed, 4, end=date(2022, 9, 24))

    assert values_as_of([quarter, year, prior, instant], date(2024, 1, 1)) == [prior, instant, year, quarter]


def test_periods_without_a_public_row_are_dropped():
    future = _row("0000950170-24-000001", date(2024, 2, 1), 5, end=date(2023, 12, 31))

    assert values_as_of([ORIGINAL, future], date(2023, 1, 1)) == [ORIGINAL]


def test_empty_input():
    assert values_as_of([], date(2024, 1, 1)) == []


def test_takes_a_concept_unit_list():
    concept = CompanyConcept.model_validate(
        {
            "cik": 1341766,
            "taxonomy": "us-gaap",
            "tag": "AccountsPayableAndAccruedLiabilitiesCurrent",
            "entityName": "CELSIUS HOLDINGS, INC.",
            "units": {"USD": [row.model_dump(mode="json") for row in RESTATEMENT_ROWS]},
        }
    )

    assert [row.accn for row in values_as_of(concept.units["USD"], date(2023, 3, 2))] == [RESTATED.accn]
