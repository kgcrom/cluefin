"""`sec financial-summary` and `sec_summary`: synthetic companyfacts, no network."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest
from cluefin_openapi.sec import SecNotFoundError
from cluefin_openapi.sec._xbrl_api_types import CompanyFacts

from cluefin_openapi_cli import sec_summary as ss
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.handlers import sec as handlers


def _fact(
    end: str, val: float, *, start: str | None = None, form: str = "10-K", fp: str = "FY", filed: str = "2026-02-20"
):
    return {
        "start": start,
        "end": end,
        "val": val,
        "accn": "0000000001-26-000001",
        "fy": 2025,
        "fp": fp,
        "form": form,
        "filed": filed,
    }


def _facts(concepts: dict[str, list[dict]]) -> CompanyFacts:
    return CompanyFacts.model_validate(
        {
            "cik": 1001,
            "entityName": "Alpha Corp",
            "facts": {"us-gaap": {name: {"units": {"USD": values}} for name, values in concepts.items()}},
        }
    )


FY25 = {"start": "2025-01-01"}
GENERAL = {
    "Assets": [_fact("2025-12-31", 900e6), _fact("2024-12-31", 800e6)],
    "RevenueFromContractWithCustomerExcludingAssessedTax": [_fact("2025-12-31", 500e6, **FY25)],
    "NetIncomeLoss": [_fact("2025-12-31", 50e6, **FY25)],
}


def test_takes_the_concept_the_filer_used_and_names_it() -> None:
    summary = ss.summarize(_facts(GENERAL), 3)

    latest = summary["years"][0]
    assert [year["period_end"] for year in summary["years"]] == ["2025-12-31", "2024-12-31"]
    assert latest["revenue"] == 500
    assert summary["account_match"]["revenue"] == "RevenueFromContractWithCustomerExcludingAssessedTax"
    # No ProfitLoss without noncontrolling interests: net income falls back to NetIncomeLoss.
    assert latest["net_income"] == 50
    assert summary["account_match"]["gross_profit"] is None
    assert "deposits" not in latest


def test_first_listed_concept_wins() -> None:
    concepts = {**GENERAL, "Revenues": [_fact("2025-12-31", 510e6, **FY25)]}

    assert ss.summarize(_facts(concepts), 1)["years"][0]["revenue"] == 510


def test_latest_filed_value_replaces_the_original() -> None:
    concepts = {
        **GENERAL,
        "Revenues": [
            _fact("2025-12-31", 510e6, filed="2026-02-20", **FY25),
            _fact("2025-12-31", 505e6, filed="2027-02-20", **FY25),  # next year's comparative column, restated
        ],
    }

    assert ss.summarize(_facts(concepts), 1)["years"][0]["revenue"] == 505


@pytest.mark.parametrize(
    "fact",
    [
        pytest.param(_fact("2025-12-31", 130e6, start="2025-10-01"), id="quarter_inside_10k"),
        pytest.param(_fact("2025-12-31", 130e6, form="10-Q", fp="Q3", **FY25), id="ten_q"),
    ],
)
def test_non_annual_values_are_ignored(fact) -> None:
    concepts = {**GENERAL, "Revenues": [fact]}

    assert ss.summarize(_facts(concepts), 1)["years"][0]["revenue"] == 500


def test_bank_gets_financial_accounts_only_through_a_marker() -> None:
    bank = {
        **GENERAL,
        "Deposits": [_fact("2025-12-31", 600e6)],
        "InterestIncomeExpenseNet": [_fact("2025-12-31", 40e6, **FY25)],
    }
    retailer = {**GENERAL, "InterestIncomeExpenseNet": [_fact("2025-12-31", -2e6, **FY25)]}

    bank_year = ss.summarize(_facts(bank), 1)["years"][0]
    assert bank_year["deposits"] == 600
    assert bank_year["net_interest_income"] == 40
    assert "net_interest_income" not in ss.summarize(_facts(retailer), 1)["years"][0]


def test_no_ten_k_year_gives_none() -> None:
    assert ss.summarize(_facts({"Assets": [_fact("2025-09-30", 1e6, form="10-Q", fp="Q3")]}), 3) is None


def _session(company_facts) -> SimpleNamespace:
    def facts(cik):
        if company_facts is None:
            raise SecNotFoundError("not found")
        return company_facts

    sec = SimpleNamespace(
        xbrl=SimpleNamespace(company_facts=facts),
        submissions=SimpleNamespace(
            submissions=lambda cik: SimpleNamespace(sic="3571", sic_description="Electronic Computers")
        ),
    )
    return SimpleNamespace(get_sec=lambda: sec)


def test_handler_returns_header_and_summary() -> None:
    out = handlers.handle_financial_summary({"cik": "1001", "years": 2}, _session(_facts(GENERAL)))

    assert out["entity_name"] == "Alpha Corp"
    assert out["sic"] == "3571"
    assert out["unit"] == "USD millions"
    assert len(out["years"]) == 2


@pytest.mark.parametrize(
    "company_facts",
    [
        pytest.param(None, id="no_companyfacts"),
        pytest.param(_facts({"Assets": [_fact("2025-09-30", 1e6, form="10-Q", fp="Q3")]}), id="ten_q_only"),
    ],
)
def test_handler_not_found(company_facts) -> None:
    with pytest.raises(CliError) as caught:
        handlers.handle_financial_summary({"cik": "1001"}, _session(company_facts))

    assert caught.value.error_type == "NotFound"


def test_tables_do_not_share_keys_and_have_markers() -> None:
    assert not set(ss.COMMON_ITEMS) & set(ss.FINANCIAL_ITEMS)
    assert {"deposits", "loans", "noninterest_income"} <= ss.FINANCIAL_MARKERS
    assert "net_interest_income" not in ss.FINANCIAL_MARKERS
    assert date(2025, 12, 31) in ss.annual_values(_facts(GENERAL))["us-gaap_Assets"]
