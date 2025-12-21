import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._model import DartStatusCode
from cluefin_openapi.dart._share_disclosure_comprehensive import ShareDisclosureComprehensive
from cluefin_openapi.dart._share_disclosure_comprehensive_types import (
    ExecutiveMajorShareholderOwnershipReport,
    ExecutiveMajorShareholderOwnershipReportItem,
    LargeHoldingReport,
    LargeHoldingReportItem,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture
def service(client: Client) -> ShareDisclosureComprehensive:
    return ShareDisclosureComprehensive(client)


@pytest.mark.integration
def test_large_holding_report_integration(service: ShareDisclosureComprehensive) -> None:
    time.sleep(1)

    response = service.large_holding_report(corp_code="00126380")

    assert isinstance(response, LargeHoldingReport)
    assert response.result.status == DartStatusCode.SUCCESS

    items = response.result.list or []
    assert all(isinstance(item, LargeHoldingReportItem) for item in items)

    if items:
        first_item = items[0]
        assert first_item.rcept_no is not None
        assert first_item.rcept_dt is not None
        assert first_item.corp_code == "00126380"


@pytest.mark.integration
def test_executive_major_shareholder_ownership_report_integration(service: ShareDisclosureComprehensive) -> None:
    time.sleep(1)

    response = service.executive_major_shareholder_ownership_report(corp_code="00126380")

    assert isinstance(response, ExecutiveMajorShareholderOwnershipReport)
    assert response.result.status == DartStatusCode.SUCCESS

    items = response.result.list or []
    assert all(isinstance(item, ExecutiveMajorShareholderOwnershipReportItem) for item in items)

    if items:
        first_item = items[0]
        assert first_item.rcept_no is not None
        assert first_item.rcept_dt is not None
        assert first_item.corp_code == "00126380"


@pytest.mark.integration
def test_large_holding_report_with_different_corp_codes(service: ShareDisclosureComprehensive) -> None:
    corp_codes = ["00126380", "00164779"]

    for corp_code in corp_codes:
        time.sleep(1)

        response = service.large_holding_report(corp_code=corp_code)

        assert isinstance(response, LargeHoldingReport)
        assert response.result.status == DartStatusCode.SUCCESS

        if response.result.list:
            for item in response.result.list:
                assert isinstance(item, LargeHoldingReportItem)
                assert item.corp_code == corp_code


@pytest.mark.integration
def test_executive_major_shareholder_ownership_report_with_different_corp_codes(
    service: ShareDisclosureComprehensive,
) -> None:
    corp_codes = ["00126380", "00164779"]

    for corp_code in corp_codes:
        time.sleep(1)

        response = service.executive_major_shareholder_ownership_report(corp_code=corp_code)

        assert isinstance(response, ExecutiveMajorShareholderOwnershipReport)
        assert response.result.status == DartStatusCode.SUCCESS

        if response.result.list:
            for item in response.result.list:
                assert isinstance(item, ExecutiveMajorShareholderOwnershipReportItem)
                assert item.corp_code == corp_code
