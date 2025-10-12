import io
import zipfile
from pathlib import Path

import pytest
import requests_mock

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._exceptions import DartAPIError
from cluefin_openapi.dart._public_disclosure import PublicDisclosure
from cluefin_openapi.dart._public_disclosure_types import (
    CompanyOverview,
    PublicDisclosureSearch,
    PublicDisclosureSearchItem,
    UniqueNumber,
)


@pytest.fixture
def client() -> Client:
    return Client(auth_key="test-auth-key")


def test_public_disclosure_search_returns_typed_result(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "page_no": "1",
        "page_count": "10",
        "total_count": "1",
        "total_page": "1",
        "list": [
            {
                "corp_cls": "Y",
                "corp_name": "삼성전자",
                "corp_code": "00126380",
                "stock_code": "005930",
                "report_nm": "사업보고서",
                "rcept_no": "20240315001234",
                "flr_nm": "홍길동",
                "rcept_dt": "20240315",
                "rm": "공",
            }
        ],
    }

    service = PublicDisclosure(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/list.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.public_disclosure_search(
            corp_code="00126380",
            page_count=1,
        )

        assert isinstance(result, PublicDisclosureSearch)
        assert result.result.status == "000"
        assert result.result.total_count == 1
        assert result.result.list is not None
        assert len(result.result.list) == 1
        assert isinstance(result.result.list[0], PublicDisclosureSearchItem)
        assert result.result.list[0].corp_name == "삼성전자"

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["corp_code"] == ["00126380"]
        assert last_request.qs["page_count"] == ["1"]


def test_public_disclosure_search_rejects_non_mapping(client: Client, monkeypatch: pytest.MonkeyPatch) -> None:
    service = PublicDisclosure(client)

    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: "not-a-mapping")

    with pytest.raises(TypeError):
        service.public_disclosure_search()


def test_company_overview_returns_model(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "corp_name": "삼성전자",
        "corp_name_eng": "Samsung Electronics Co., Ltd.",
        "stock_name": "삼성전자",
        "stock_code": "005930",
        "ceo_nm": "한종희",
        "corp_cls": "Y",
        "jurir_no": "110111-0640266",
        "bizr_no": "124-81-00998",
        "adres": "경기도 수원시",
        "hm_url": "http://www.samsung.com",
        "ir_url": "http://www.samsung.com/ir",
        "phn_no": "02-2255-0114",
        "fax_no": "02-2255-0115",
        "induty_code": "264",
        "est_dt": "19690113",
        "acc_mt": "12",
    }

    service = PublicDisclosure(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/company.json",
            json=expected_payload,
            status_code=200,
        )

        overview = service.company_overview("00126380")

        assert isinstance(overview, CompanyOverview)
        assert overview.corp_name == "삼성전자"
        assert overview.stock_code == "005930"

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["corp_code"] == ["00126380"]


def test_company_overview_rejects_non_mapping(client: Client, monkeypatch: pytest.MonkeyPatch) -> None:
    service = PublicDisclosure(client)

    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: ["unexpected"])

    with pytest.raises(TypeError):
        service.company_overview("00126380")


def test_corp_code_returns_parsed_corp_codes(client: Client) -> None:
    xml_payload = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<result>
  <status>000</status>
  <message>정상적으로 처리되었습니다</message>
  <list>
    <corp_code>00126380</corp_code>
    <corp_name>삼성전자</corp_name>
    <corp_eng_name>Samsung Electronics Co., Ltd.</corp_eng_name>
    <stock_code>005930</stock_code>
    <corp_cls>Y</corp_cls>
    <modify_date>20240101</modify_date>
  </list>
  <list>
    <corp_code>01234567</corp_code>
    <corp_name>비상장기업</corp_name>
    <stock_code></stock_code>
    <modify_date>20231231</modify_date>
  </list>
</result>
"""

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("CORPCODE.xml", xml_payload)
    buffer.seek(0)

    service = PublicDisclosure(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/corpCode.xml",
            content=buffer.read(),
            status_code=200,
        )

        corp_code_response = service.corp_code()

        assert isinstance(corp_code_response, UniqueNumber)
        assert corp_code_response.result.status == "000"
        assert corp_code_response.result.message == "정상"
        assert corp_code_response.result.list is not None
        assert len(corp_code_response.result.list) == 2

        first = corp_code_response.result.list[0]
        assert first.corp_code == "00126380"
        assert first.corp_name == "삼성전자"
        assert first.corp_eng_name == "Samsung Electronics Co., Ltd."
        assert first.stock_code == "005930"
        assert first.corp_cls == "Y"
        assert first.modify_date == "20240101"

        second = corp_code_response.result.list[1]
        assert second.corp_code == "01234567"
        assert second.corp_eng_name is None
        assert second.stock_code is None

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]


def test_disclosure_document_file_persists_payload(
    client: Client,
    tmp_path: Path,
) -> None:
    payload = b"<document>sample</document>"
    destination = tmp_path / "report.xml"
    service = PublicDisclosure(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/document.xml",
            content=payload,
            status_code=200,
        )

        saved_path = service.disclosure_document_file(
            "20240315001234",
            destination=destination,
        )

        assert saved_path == destination
        assert saved_path.read_bytes() == payload

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["rcept_no"] == ["20240315001234"]


def test_disclosure_document_file_raises_on_dart_error(
    client: Client,
    tmp_path: Path,
) -> None:
    error_payload = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<result>\n"
        "  <status>013</status>\n"
        "  <message>유효하지 않은 접수번호입니다.</message>\n"
        "</result>\n"
    ).encode("utf-8")

    destination = tmp_path / "error.xml"
    service = PublicDisclosure(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/document.xml",
            content=error_payload,
            status_code=200,
        )

        with pytest.raises(DartAPIError) as exc_info:
            service.disclosure_document_file(
                "00000000000000",
                destination=destination,
            )

        assert "유효하지 않은" in str(exc_info.value)


def test_disclosure_document_file_respects_overwrite_flag(
    client: Client,
    tmp_path: Path,
) -> None:
    destination = tmp_path / "document.xml"
    destination.write_text("existing")
    service = PublicDisclosure(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/document.xml",
            content=b"<root/>",
            status_code=200,
        )

        with pytest.raises(FileExistsError):
            service.disclosure_document_file(
                "20240315001234",
                destination=destination,
            )

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["rcept_no"] == ["20240315001234"]
