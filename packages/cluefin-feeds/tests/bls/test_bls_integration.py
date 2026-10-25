"""Live checks against api.bls.gov (read-only).

키 없이(v1) 하루 25회 한도가 있어 호출을 최소로 둔다. `.env.test` 에 BLS_REGISTRATION_KEY 가 있으면 v2 로 보낸다.
"""

import datetime as dt
import os
from decimal import Decimal
from pathlib import Path

import dotenv
import pytest

from cluefin_feeds.bls import CPI_U_ALL_ITEMS, Client

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env.test")

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client() -> Client:
    return Client(registration_key=os.getenv("BLS_REGISTRATION_KEY"))


def test_cpi_2015_annual_average(client: Client):
    series = client.timeseries([CPI_U_ALL_ITEMS], 2015, 2015, annual_average=True).get(CPI_U_ALL_ITEMS)
    annual = next(row for row in series.data if row.period == "M13")
    assert annual.value == Decimal("237.017")
    assert len([row for row in series.data if row.month]) == 12
    assert all(not row.model_extra for row in series.data)


def test_recent_cpi(client: Client):
    year = dt.date.today().year
    result = client.timeseries([CPI_U_ALL_ITEMS], year - 1, year)
    assert result.messages == [] or all("No Data" in m for m in result.messages)
    latest = result.get(CPI_U_ALL_ITEMS).data[-1]
    assert latest.year >= year - 1
    assert latest.value is not None
