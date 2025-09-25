import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._periodic_report_key_information import PeriodicReportKeyInformation
from cluefin_openapi.dart._periodic_report_key_information_types import (
    CapitalChangeStatus,
    CapitalChangeStatusItem,
    DividendInformation,
    DividendInformationItem,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture
def service(client: Client) -> PeriodicReportKeyInformation:
    return PeriodicReportKeyInformation(client)


@pytest.mark.integration
def test_get_capital_change_status_integration(service: PeriodicReportKeyInformation) -> None:
    time.sleep(1)

    response = service.get_capital_change_status(
        corp_code="00126380",  # 삼성전자
        bsns_year="2023",
        reprt_code="11011",  # 사업보고서
    )

    assert isinstance(response, CapitalChangeStatus)
    assert response.result.status is not None

    items = response.result.list or []
    assert all(isinstance(item, CapitalChangeStatusItem) for item in items)

    if items:
        first_item = items[0]
        assert first_item.rcept_no is not None
        assert first_item.corp_code == "00126380"


@pytest.mark.integration
def test_get_dividend_information_integration(service: PeriodicReportKeyInformation) -> None:
    time.sleep(1)

    response = service.get_dividend_information(
        corp_code="00126380",  # 삼성전자
        bsns_year="2023",
        reprt_code="11011",  # 사업보고서
    )

    assert isinstance(response, DividendInformation)
    assert response.result.status is not None

    items = response.result.list or []
    assert all(isinstance(item, DividendInformationItem) for item in items)

    if items:
        first_item = items[0]
        assert first_item.rcept_no is not None
        assert first_item.corp_code == "00126380"
