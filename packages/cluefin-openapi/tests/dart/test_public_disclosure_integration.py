import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._model import DartStatusCode
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
    assert response.result.status == DartStatusCode.SUCCESS

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
    assert response.result.status == DartStatusCode.SUCCESS
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


@pytest.mark.integration
def test_public_disclosure_search_pblntf_ty_a_ignores_detail_type(service: PublicDisclosure) -> None:
    """pblntf_ty=A(정기공시) 지정 시 pblntf_detail_ty가 무시되는지 검증.

    DART API에서 pblntf_ty=A를 지정하면 pblntf_detail_ty 파라미터와 관계없이
    모든 정기공시(사업보고서, 반기보고서, 분기보고서)를 반환합니다.
    """
    time.sleep(1)

    # pblntf_ty=A와 pblntf_detail_ty=A001(사업보고서) 함께 지정
    response_with_detail = service.public_disclosure_search(
        pblntf_ty="A",
        pblntf_detail_ty="A001",  # 사업보고서
        page_count=100,
    )

    detail_report_names = [item.report_nm for item in (response_with_detail.result.list or [])]

    # pblntf_detail_ty=A001(사업보고서)을 지정했지만 반기/분기 보고서도 포함되는지 확인
    has_non_annual = any("반기" in name or "분기" in name for name in detail_report_names)

    # pblntf_detail_ty가 무시되면 반기/분기 보고서도 포함됨
    assert has_non_annual, (
        "pblntf_ty=A와 pblntf_detail_ty=A001 지정 시에도 반기/분기 보고서가 포함되어야 합니다. "
        f"이는 DART API가 pblntf_detail_ty를 무시하기 때문입니다. 조회된 보고서: {detail_report_names[:10]}"
    )
