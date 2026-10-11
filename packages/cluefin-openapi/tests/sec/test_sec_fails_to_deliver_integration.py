"""Live checks of SEC Fails-to-Deliver files (read-only)."""

import pytest

from cluefin_openapi.sec import Client, cusip_symbols

from ._env import SEC_USER_AGENT, requires_user_agent

pytestmark = [pytest.mark.integration, requires_user_agent]

APPLE_CUSIP = "037833100"


@pytest.fixture(scope="module")
def client() -> Client:
    return Client(user_agent=SEC_USER_AGENT or "")


def test_files_cover_every_half_month_since_2009(client: Client):
    files = client.fails_to_deliver.files()

    names = [f.name for f in files]
    assert names == sorted(names, reverse=True)
    assert names[-1] == "cnsfails200907a"
    assert len(files) >= 412  # 2009-07a … 2026-09a, two per month


def test_records_map_cusips_to_tickers(client: Client):
    (file,) = [f for f in client.fails_to_deliver.files() if f.name == "cnsfails202511b"]
    records = client.fails_to_deliver.records(file)  # the zip member has no .txt extension

    assert len(records) > 10_000
    assert {r.settlement_date.month for r in records} == {11}
    assert cusip_symbols(records)[APPLE_CUSIP] == "AAPL"
