"""Live check of `sec filing-items` / `sec filing-exhibit` against SEC EDGAR (SEC_USER_AGENT from .env.test).

The filings are not named here (cluefin-sec-notes AGENTS.md: no company in the repo). Set
CLUEFIN_SEC_CIK to a US filer, CLUEFIN_SEC_10K_ACCESSION to one of its 10-Ks and CLUEFIN_SEC_8K_ACCESSION to one
of its 8-Ks with item 2.02 and an EX-99.1 earnings release; the test is skipped otherwise. Five requests.
"""

from __future__ import annotations

import os

import dotenv
import pytest
from cluefin_openapi import BrokerClientConfig, BrokerClientFactory

from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers.sec import handle_filing_exhibit, handle_filing_items


class _Session:
    def __init__(self, sec) -> None:
        self._sec = sec

    def get_sec(self):
        return self._sec


@pytest.fixture(scope="module")
def filer() -> tuple[_Session, dict]:
    names = ("CLUEFIN_SEC_CIK", "CLUEFIN_SEC_10K_ACCESSION", "CLUEFIN_SEC_8K_ACCESSION")
    values = {name: os.getenv(name) for name in names}
    if not all(values.values()):
        pytest.skip(f"{' / '.join(names)} are not set")
    dotenv.load_dotenv(dotenv_path=".env.test")
    agent = os.getenv("SEC_USER_AGENT")
    if not agent:
        pytest.skip("SEC_USER_AGENT is not configured")
    # Not BrokerClientConfig.from_env(): it merges the cwd's .env (production) into the config.
    session = _Session(BrokerClientFactory(BrokerClientConfig(sec_user_agent=agent)).create("sec"))
    return session, values


@pytest.mark.integration
def test_ten_k_outline_and_risk_factors_agree(filer) -> None:
    session, values = filer
    base = {"cik": values["CLUEFIN_SEC_CIK"], "accession_number": values["CLUEFIN_SEC_10K_ACCESSION"]}

    toc = handle_filing_items(base, session)
    assert toc["catalog"] == "10-K"
    risk = next(item for item in toc["items"] if item["key"] == "1A")

    read = handle_filing_items({**base, "items": "1A", "max_chars": 0}, session)
    (item,) = read["items"]
    assert item["status"] == "found"
    assert item["chars_total"] == item["chars_returned"] == risk["chars"] > 0


@pytest.mark.integration
def test_eight_k_earnings_release_and_cik_check(filer) -> None:
    session, values = filer
    base = {"cik": values["CLUEFIN_SEC_CIK"], "accession_number": values["CLUEFIN_SEC_8K_ACCESSION"]}

    release = handle_filing_exhibit(base, session)
    assert release["document"]["type"] == "EX-99.1"
    assert release["chars_total"] > 0 and release["text"]

    # A folder opens under any CIK; the detail page's parties are what refuses it.
    with pytest.raises(CliError) as error:
        handle_filing_exhibit({**base, "cik": "1"}, session)
    assert error.value.exit_code == EXIT_BROKER
