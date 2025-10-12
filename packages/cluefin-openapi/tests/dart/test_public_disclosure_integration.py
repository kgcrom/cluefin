import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._public_disclosure import PublicDisclosure
from cluefin_openapi.dart._public_disclosure_types import (
    CompanyOverview,
    PublicDisclosureSearch,
    PublicDisclosureSearchItem,
    UniqueNumber,
    UniqueNumberItem,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture
def service(client: Client) -> PublicDisclosure:
    return PublicDisclosure(client)


@pytest.mark.integration
def test_public_disclosure_search(service: PublicDisclosure) -> None:
    time.sleep(1)

    response = service.public_disclosure_search(
        corp_code="00126380",
        page_count=5,
    )

    assert isinstance(response, PublicDisclosureSearch)
    assert response.result.status is not None

    items = response.result.list or []
    assert all(isinstance(item, PublicDisclosureSearchItem) for item in items)


@pytest.mark.integration
def test_company_overview(service: PublicDisclosure) -> None:
    time.sleep(1)

    overview = service.company_overview("00126380")
    assert isinstance(overview, CompanyOverview)
    assert overview.stock_name == "삼성전자"
    assert overview.corp_name


@pytest.mark.integration
def test_corp_code(service: PublicDisclosure) -> None:
    time.sleep(1)

    response = service.corp_code()

    assert isinstance(response, UniqueNumber)
    assert response.result.status == "000"
    assert response.result.message == "정상"

    samsung = next(
        (item for item in (response.result.list or []) if item.corp_code == "00126380"),
        None,
    )

    assert samsung is not None
    assert isinstance(samsung, UniqueNumberItem)
    assert samsung.corp_name == "삼성전자"
    assert samsung.stock_code == "005930"


@pytest.mark.integration
def test_disclosure_document_file_integration(
    service: PublicDisclosure,
    tmp_path,
) -> None:
    time.sleep(1)
    search = service.public_disclosure_search(
        corp_code="00126380",
        page_count=1,
    )
    items = search.result.list or []
    assert items, "공시 검색 결과가 비어 있습니다."

    time.sleep(1)
    destination = tmp_path / "document.xml"
    saved_path = service.disclosure_document_file(
        items[0].rcept_no,
        destination=destination,
        overwrite=True,
    )

    assert saved_path.exists()
    assert saved_path.stat().st_size > 0
