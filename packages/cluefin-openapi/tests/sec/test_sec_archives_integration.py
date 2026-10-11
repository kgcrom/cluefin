"""Live checks of SEC Archives downloads (read-only)."""

from datetime import date
from pathlib import Path

import pytest

from cluefin_openapi.sec import Client

from ._env import SEC_USER_AGENT, requires_user_agent

pytestmark = [pytest.mark.integration, requires_user_agent]

APPLE_CIK = 320193
APPLE_FY2023_10K = "0000320193-23-000106"


@pytest.fixture(scope="module")
def client() -> Client:
    return Client(user_agent=SEC_USER_AGENT or "")


def test_filing_index_lists_primary_document(client: Client):
    index = client.archives.filing_index(APPLE_CIK, APPLE_FY2023_10K)
    names = {item.name for item in index.items}
    assert "aapl-20230930.htm" in names
    assert "aapl-20230930_htm.xml" in names


def test_download_primary_document(client: Client, tmp_path: Path):
    path = client.archives.download_filing_document(
        APPLE_CIK, APPLE_FY2023_10K, "aapl-20230930.htm", destination=tmp_path
    )
    head = path.read_bytes()[:2000].lower()
    assert b"<html" in head or b"<?xml" in head


def test_download_inline_xbrl_files(client: Client, tmp_path: Path):
    paths = client.archives.download_xbrl_files(APPLE_CIK, APPLE_FY2023_10K, destination=tmp_path)
    names = {p.name for p in paths}
    assert {
        "aapl-20230930.xsd",
        "aapl-20230930_htm.xml",
        "aapl-20230930_cal.xml",
        "aapl-20230930_def.xml",
        "aapl-20230930_lab.xml",
        "aapl-20230930_pre.xml",
    } <= names
    assert "FilingSummary.xml" not in names


def test_download_pre_inline_xbrl_files(client: Client, tmp_path: Path):
    tenks = client.submissions.filings(APPLE_CIK, forms=["10-K"], include_amendments=False, include_older=True)
    fy2018 = next(entry for entry in tenks if entry.report_date == date(2018, 9, 29))
    assert not fy2018.is_inline_xbrl

    paths = client.archives.download_xbrl_files(APPLE_CIK, fy2018.accession_number, destination=tmp_path)
    names = {p.name for p in paths}
    assert "aapl-20180929.xml" in names
    assert "aapl-20180929.xsd" in names
