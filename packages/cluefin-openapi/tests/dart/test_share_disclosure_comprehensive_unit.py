import pytest
import requests_mock

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._share_disclosure_comprehensive import ShareDisclosureComprehensive
from cluefin_openapi.dart._share_disclosure_comprehensive_types import (
    ExecutiveMajorShareholderOwnershipReport,
    ExecutiveMajorShareholderOwnershipReportItem,
    LargeHoldingReport,
    LargeHoldingReportItem,
)


@pytest.fixture
def client() -> Client:
    return Client(auth_key="test-auth-key")


def test_large_holding_report_returns_typed_result(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "page_no": "1",
        "page_count": "10",
        "total_count": "1",
        "total_page": "1",
        "list": [
            {
                "rcept_no": "20240315001234",
                "rcept_dt": "20240315",
                "corp_code": "00126380",
                "corp_name": "삼성전자",
                "report_tp": "보고서구분",
                "repror": "홍길동",
                "stkqy": "1000000",
                "stkqy_irds": "50000",
                "stkrt": "5.25",
                "stkrt_irds": "0.15",
                "ctr_stkqy": "500000",
                "ctr_stkrt": "2.50",
                "report_resn": "보고사유",
            }
        ],
    }

    service = ShareDisclosureComprehensive(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/majorstock.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.large_holding_report(corp_code="00126380")

        assert isinstance(result, LargeHoldingReport)
        assert result.result.status == "000"
        assert result.result.total_count == 1
        assert result.result.list is not None
        assert len(result.result.list) == 1
        assert isinstance(result.result.list[0], LargeHoldingReportItem)
        assert result.result.list[0].corp_name == "삼성전자"
        assert result.result.list[0].rcept_no == "20240315001234"
        assert result.result.list[0].stkrt == "5.25"

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["corp_code"] == ["00126380"]


def test_large_holding_report_raises_for_empty_corp_code(client: Client) -> None:
    service = ShareDisclosureComprehensive(client)

    with pytest.raises(ValueError, match="대량보유 상황보고를 조회하려면 corp_code를 지정해야 합니다"):
        service.large_holding_report(corp_code="")

    with pytest.raises(ValueError, match="대량보유 상황보고를 조회하려면 corp_code를 지정해야 합니다"):
        service.large_holding_report(corp_code="   ")


def test_large_holding_report_rejects_non_mapping(client: Client, monkeypatch: pytest.MonkeyPatch) -> None:
    service = ShareDisclosureComprehensive(client)

    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: "not-a-mapping")

    with pytest.raises(TypeError, match="주식등의 대량보유 상황보고 응답은 매핑 타입이어야 합니다"):
        service.large_holding_report(corp_code="00126380")


def test_large_holding_report_handles_minimal_response(client: Client) -> None:
    minimal_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [
            {
                "rcept_no": "20240315001234",
                "rcept_dt": "20240315",
                "corp_code": "00126380",
            }
        ],
    }

    service = ShareDisclosureComprehensive(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/majorstock.json",
            json=minimal_payload,
            status_code=200,
        )

        result = service.large_holding_report(corp_code="00126380")

        assert isinstance(result, LargeHoldingReport)
        assert result.result.status == "000"
        assert len(result.result.list or []) == 1
        item = result.result.list[0]
        assert item.corp_name is None
        assert item.report_tp is None
        assert item.repror is None


def test_executive_major_shareholder_ownership_report_returns_typed_result(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "page_no": "1",
        "page_count": "10",
        "total_count": "1",
        "total_page": "1",
        "list": [
            {
                "rcept_no": "20240315005678",
                "rcept_dt": "20240315",
                "corp_code": "00126380",
                "corp_name": "삼성전자",
                "repror": "김임원",
                "isu_exctv_rgist_at": "Y",
                "isu_exctv_ofcps": "대표이사",
                "isu_main_shrhldr": "N",
                "sp_stock_lmp_cnt": "2000000",
                "sp_stock_lmp_irds_cnt": "100000",
                "sp_stock_lmp_rate": "3.15",
                "sp_stock_lmp_irds_rate": "0.05",
            }
        ],
    }

    service = ShareDisclosureComprehensive(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/elestock.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.executive_major_shareholder_ownership_report(corp_code="00126380")

        assert isinstance(result, ExecutiveMajorShareholderOwnershipReport)
        assert result.result.status == "000"
        assert result.result.total_count == 1
        assert result.result.list is not None
        assert len(result.result.list) == 1
        assert isinstance(result.result.list[0], ExecutiveMajorShareholderOwnershipReportItem)
        assert result.result.list[0].corp_name == "삼성전자"
        assert result.result.list[0].rcept_no == "20240315005678"
        assert result.result.list[0].repror == "김임원"
        assert result.result.list[0].isu_exctv_ofcps == "대표이사"
        assert result.result.list[0].sp_stock_lmp_rate == "3.15"

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["corp_code"] == ["00126380"]


def test_executive_major_shareholder_ownership_report_raises_for_empty_corp_code(client: Client) -> None:
    service = ShareDisclosureComprehensive(client)

    with pytest.raises(ValueError, match="임원·주요주주 소유보고를 조회하려면 corp_code를 지정해야 합니다"):
        service.executive_major_shareholder_ownership_report(corp_code="")

    with pytest.raises(ValueError, match="임원·주요주주 소유보고를 조회하려면 corp_code를 지정해야 합니다"):
        service.executive_major_shareholder_ownership_report(corp_code="   ")


def test_executive_major_shareholder_ownership_report_rejects_non_mapping(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = ShareDisclosureComprehensive(client)

    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: ["unexpected"])

    with pytest.raises(TypeError, match="임원·주요주주 소유보고 응답은 매핑 타입이어야 합니다"):
        service.executive_major_shareholder_ownership_report(corp_code="00126380")


def test_executive_major_shareholder_ownership_report_handles_minimal_response(client: Client) -> None:
    minimal_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [
            {
                "rcept_no": "20240315005678",
                "rcept_dt": "20240315",
                "corp_code": "00126380",
            }
        ],
    }

    service = ShareDisclosureComprehensive(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/elestock.json",
            json=minimal_payload,
            status_code=200,
        )

        result = service.executive_major_shareholder_ownership_report(corp_code="00126380")

        assert isinstance(result, ExecutiveMajorShareholderOwnershipReport)
        assert result.result.status == "000"
        assert result.result.list is not None
        assert len(result.result.list) == 1
        item = result.result.list[0]
        assert item.corp_name is None
        assert item.repror is None
        assert item.isu_exctv_rgist_at is None


def test_large_holding_report_normalizes_corp_code(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [
            {
                "rcept_no": "20240315001234",
                "rcept_dt": "20240315",
                "corp_code": "00126380",
            }
        ],
    }

    service = ShareDisclosureComprehensive(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/majorstock.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.large_holding_report(corp_code="  00126380  ")

        assert isinstance(result, LargeHoldingReport)
        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["corp_code"] == ["00126380"]


def test_executive_major_shareholder_ownership_report_normalizes_corp_code(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [
            {
                "rcept_no": "20240315005678",
                "rcept_dt": "20240315",
                "corp_code": "00126380",
            }
        ],
    }

    service = ShareDisclosureComprehensive(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/elestock.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.executive_major_shareholder_ownership_report(corp_code="  00126380  ")

        assert isinstance(result, ExecutiveMajorShareholderOwnershipReport)
        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["corp_code"] == ["00126380"]
