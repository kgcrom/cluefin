from __future__ import annotations

import json
from datetime import date
from types import SimpleNamespace

import pytest
from _handler_fakes import assert_registers_all
from cluefin_openapi.sec import CompanySubmissions, CompanyTickerExchange, FilingEntry

from cluefin_openapi_cli.handlers import sec as handlers
from cluefin_openapi_cli.main import run_cli

# Synthetic companies only: no real company, CIK or accession number (cluefin-sec-notes AGENTS.md).
_TICKERS = [
    CompanyTickerExchange(cik=1001, name="Alpha Memory Corp", ticker="ALPH", exchange="Nasdaq"),
    CompanyTickerExchange(cik=1002, name="Beta Holdings Inc", ticker="BETA-B", exchange="NYSE"),
    CompanyTickerExchange(cik=1002, name="Beta Holdings Inc", ticker="BETA-A", exchange="NYSE"),
    CompanyTickerExchange(cik=1003, name="Gamma Tools Ltd", ticker="GAMT", exchange=None),
]


def _entry(accession: str, form: str, filed: str, items: str | None = None) -> FilingEntry:
    return FilingEntry(
        accession_number=accession,
        form=form,
        filing_date=date.fromisoformat(filed),
        report_date=date.fromisoformat(filed),
        items=items,
        primary_document=f"doc-{accession[-3:]}.htm",
        size=1000,
    )


_COMPANY = CompanySubmissions(
    cik="1001",
    name="Alpha Memory Corp",
    tickers=["ALPH"],
    exchanges=["Nasdaq"],
    sic_description="Semiconductors & Related Devices",
    fiscal_year_end="0903",
    filings=[
        _entry("0000001001-26-000009", "8-K", "2026-09-30", "2.02,9.01"),
        _entry("0000001001-26-000008", "10-K", "2026-09-20"),
        _entry("0000001001-26-000007", "4", "2026-09-10"),
        _entry("0000001001-26-000006", "8-K", "2026-08-26", "5.02,9.01"),
        _entry("0000001001-26-000005", "10-Q/A", "2026-07-01"),
        _entry("0000001001-26-000004", "10-Q", "2026-06-25"),
        _entry("0000001001-26-000003", "8-K", "2026-06-24", "2.02,9.01"),
    ],
)


class _Session:
    """Returns the given client from get_sec() and records nothing else."""

    def __init__(self, *, tickers=(), company=None) -> None:
        self.calls: list[str] = []
        reference = SimpleNamespace(company_tickers_exchange=self._recorded("company_tickers_exchange", list(tickers)))
        submissions = SimpleNamespace(submissions=self._recorded("submissions", company))
        self._client = SimpleNamespace(reference=reference, submissions=submissions)

    def _recorded(self, name: str, value):
        def call(*args, **kwargs):
            self.calls.append(name)
            return value

        return call

    def get_sec(self):
        return self._client


def test_register_sec_handlers() -> None:
    assert_registers_all(handlers.register_sec_handlers, handlers._ALL_HANDLERS, "sec")


@pytest.mark.parametrize("ticker", ["BETA.B", "beta-b", " BETA-B "])
def test_company_lookup_matches_ticker_in_sec_or_dotted_form(ticker: str) -> None:
    result = handlers.handle_company_lookup({"ticker": ticker}, _Session(tickers=_TICKERS))

    assert result["total"] == 1
    assert result["data"] == [{"cik": 1002, "name": "Beta Holdings Inc", "ticker": "BETA-B", "exchange": "NYSE"}]


def test_company_lookup_filters_by_name_and_cik_and_caps_rows() -> None:
    session = _Session(tickers=_TICKERS)
    by_name = handlers.handle_company_lookup({"name": "holdings"}, session)
    assert [row["ticker"] for row in by_name["data"]] == ["BETA-B", "BETA-A"]

    by_cik = handlers.handle_company_lookup({"cik": "0000001003"}, session)
    assert [row["ticker"] for row in by_cik["data"]] == ["GAMT"]

    capped = handlers.handle_company_lookup({"max_rows": 1}, session)
    assert (capped["total"], capped["returned"], capped["truncated"]) == (4, 1, True)
    assert handlers.handle_company_lookup({"max_rows": 0}, session)["returned"] == 4
    assert session.calls == ["company_tickers_exchange"] * 4


def test_filings_defaults_to_annual_quarterly_and_current_reports_with_amendments() -> None:
    result = handlers.handle_filings({"cik": "1001"}, _Session(company=_COMPANY))

    assert [row["form"] for row in result["data"]] == ["8-K", "10-K", "8-K", "10-Q/A", "10-Q", "8-K"]
    assert (result["cik"], result["name"]) == (1001, "Alpha Memory Corp")
    assert result["sic_description"] == "Semiconductors & Related Devices"
    first = result["data"][0]
    assert first == {
        "accession_number": "0000001001-26-000009",
        "form": "8-K",
        "filing_date": "2026-09-30",
        "report_date": "2026-09-30",
        "items": ["2.02", "9.01"],
        "primary_document": "doc-009.htm",
        "size": 1000,
    }
    assert "hint" not in result


def test_filings_filters_forms_amendments_and_eight_k_items() -> None:
    session = _Session(company=_COMPANY)
    quarterly = handlers.handle_filings({"cik": "1001", "forms": "10-q", "include_amendments": False}, session)
    assert [row["form"] for row in quarterly["data"]] == ["10-Q"]

    results = handlers.handle_filings({"cik": "1001", "forms": "8-K", "items": "2.02"}, session)
    assert [row["accession_number"] for row in results["data"]] == ["0000001001-26-000009", "0000001001-26-000003"]

    capped = handlers.handle_filings({"cik": "1001", "max_rows": 2}, session)
    assert (capped["total"], capped["returned"], capped["truncated"]) == (6, 2, True)


def test_filings_without_a_match_lists_what_the_company_did_file() -> None:
    result = handlers.handle_filings({"cik": "1001", "forms": "20-F"}, _Session(company=_COMPANY))

    assert result["total"] == 0
    assert "10-K, 10-Q, 10-Q/A, 4, 8-K" in result["hint"]
    assert "20-F" in result["hint"]


def test_brokers_reports_sec_user_agent_as_configured_without_echoing_it(monkeypatch) -> None:
    agent = "Somebody somebody@example.invalid"
    monkeypatch.setenv("SEC_USER_AGENT", agent)
    result = run_cli(["brokers", "--json"])
    payload = json.loads(result.stdout)

    sec = next(row for row in payload["brokers"] if row["name"] == "sec")
    assert sec["role"] == "reference"
    assert sec["credentials"]["required"] == ["SEC_USER_AGENT"]
    assert sec["credentials"]["configured"] is True
    assert agent not in result.stdout


def test_sec_paths_have_no_category_segment() -> None:
    result = run_cli(["schema", "sec", "filings", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["command"] == "sec.filings"

    usage = run_cli(["sec"])
    assert usage.exit_code == 2
    assert "sec <name>" in usage.stdout
