"""note_xbrl: companyfacts 응답을 흉내 낸 CompanyFacts 모델로 행에 개념을 붙인다. 회사·숫자는 지어냈다."""

from __future__ import annotations

from datetime import date

from cluefin_openapi.sec import CompanyFacts

from cluefin_openapi_cli.note_xbrl import attach_xbrl, fact_index

PERIOD_ENDS = {2025: date(2025, 12, 31), 2024: date(2024, 12, 31), 2023: date(2023, 12, 31)}


def _fact(fy: int, val: int, *, filed: str, form: str = "10-K", fp: str = "FY", instant: bool = False) -> dict:
    fact = {"end": f"{fy}-12-31", "val": val, "accn": "0000001001-26-000001", "fy": fy, "fp": fp, "form": form}
    fact["filed"] = filed
    if not instant:
        fact["start"] = f"{fy}-01-01"
    return fact


def _facts(concepts: dict[str, list[dict]]) -> CompanyFacts:
    return CompanyFacts.model_validate(
        {
            "cik": 1001,
            "entityName": "Alpha Memory Corp",
            "facts": {"us-gaap": {name: {"units": {"USD": facts}} for name, facts in concepts.items()}},
        }
    )


def _row(values: dict[str, float], unit: str = "in millions", kind: str = "amount") -> dict:
    return {
        "label": "Operating lease cost",
        "kind": kind,
        "values_by_fy": values,
        "unit_filed": {fy: unit for fy in values},
    }


def _notes(*rows: dict) -> list[dict]:
    return [{"title": "Leases", "tables": [{"rows": list(rows)}]}]


LEASE_COST = [
    _fact(2025, 703_000_000, filed="2026-02-20"),
    _fact(2024, 595_000_000, filed="2025-02-20"),
    _fact(2024, 595_000_000, filed="2026-02-20"),
    _fact(2023, 457_400_000, filed="2024-02-20"),
    _fact(2023, 460_000_000, filed="2025-02-20"),  # 다음 해 공시가 고친 값
    _fact(2022, 410_000_000, filed="2025-02-20", fp="Q4"),  # 연간 10-K 값이 아니다
]


def test_row_gets_the_concept_matching_its_values_and_latest_filed_series() -> None:
    row = _row({"2025": 703, "2024": 595})
    index = fact_index(
        _facts({"OperatingLeaseCost": LEASE_COST, "LeaseCost": [_fact(2025, 788_000_000, filed="2026-02-20")]})
    )

    matched, total = attach_xbrl(_notes(row), index, PERIOD_ENDS)

    assert (matched, total) == (1, 1)
    assert row["xbrl"] == {
        "concept": "us-gaap:OperatingLeaseCost",
        "matched_fy": [2025, 2024],
        # 2023 은 HTML 표에 없지만 태그에는 있어 낸다. 같은 기간은 가장 늦게 제출된 값, 처음 값은 따로.
        "values_by_fy": {"2025": 703, "2024": 595, "2023": 460},
        "first_filed_by_fy": {"2023": 457.4},
    }


def test_values_match_within_one_unit_of_the_filed_unit_and_ignore_sign() -> None:
    thousands = _row({"2023": -457.4}, unit="in thousands")
    off_by_thousand = _row({"2023": 457.401}, unit="in thousands")
    index = fact_index(_facts({"OperatingLeaseCost": LEASE_COST[3:4]}))

    attach_xbrl(_notes(thousands, off_by_thousand), index, PERIOD_ENDS)

    assert thousands["xbrl"]["concept"] == "us-gaap:OperatingLeaseCost"
    assert "xbrl" not in off_by_thousand


def test_two_valued_row_needs_two_matching_years() -> None:
    row = _row({"2025": 703, "2024": 1})
    index = fact_index(_facts({"OperatingLeaseCost": LEASE_COST}))

    attach_xbrl(_notes(row), index, PERIOD_ENDS)

    assert "xbrl" not in row


def test_single_year_row_is_left_alone_when_another_concept_has_the_same_value() -> None:
    row = _row({"2025": 8})
    other = [_fact(2025, 8_000_000, filed="2026-02-20")]
    index = fact_index(_facts({"TaxCredits": other, "PaymentsForOtherInvesting": other}))

    attach_xbrl(_notes(row), index, PERIOD_ENDS)

    assert "xbrl" not in row


def test_instant_and_quarterly_or_non_10k_facts() -> None:
    balance = _row({"2025": 1302, "2024": 1091})
    quarterly = _row({"2024": 410})
    index = fact_index(
        _facts(
            {
                "DeferredTaxAssetsNet": [
                    _fact(2025, 1_302_000_000, filed="2026-02-20", instant=True),
                    _fact(2024, 1_091_000_000, filed="2025-02-20", instant=True),
                ],
                "OperatingLeaseCost": [_fact(2024, 410_000_000, filed="2025-02-20", form="10-Q")],
            }
        )
    )

    attach_xbrl(_notes(balance, quarterly), index, PERIOD_ENDS)

    assert balance["xbrl"]["concept"] == "us-gaap:DeferredTaxAssetsNet"
    assert "xbrl" not in quarterly


def test_percent_and_zero_rows_are_skipped() -> None:
    percent = _row({"2025": 21}, kind="percent")
    zero = _row({"2025": 0})
    index = fact_index(_facts({"Rate": [_fact(2025, 21_000_000, filed="2026-02-20")]}))

    assert attach_xbrl(_notes(percent, zero), index, PERIOD_ENDS) == (0, 1)
