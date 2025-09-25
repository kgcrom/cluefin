from typing import Mapping

import pytest
import requests_mock

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._periodic_report_key_information import PeriodicReportKeyInformation
from cluefin_openapi.dart._periodic_report_key_information_types import (
    CapitalChangeStatus,
    CapitalChangeStatusItem,
    DividendInformation,
)


@pytest.fixture
def client() -> Client:
    return Client(auth_key="test-auth-key")


def test_get_capital_change_status_returns_typed_result(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [
            {
                "rcept_no": "20240315001234",
                "corp_cls": "Y",
                "corp_code": "00126380",
                "corp_name": "삼성전자",
                "isu_dcrs_de": "20240101",
                "isu_dcrs_stle": "유상증자",
                "isu_dcrs_stock_knd": "보통주",
                "isu_dcrs_qy": "1000000",
                "isu_dcrs_mstvdv_fval_amount": "5000",
                "isu_dcrs_mstvdv_amount": "50000",
                "stlm_dt": "20240315",
            }
        ],
    }

    service = PeriodicReportKeyInformation(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/irdsSttus.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.get_capital_change_status(
            corp_code="00126380",
            bsns_year="2024",
            reprt_code="11011",
        )

        assert isinstance(result, CapitalChangeStatus)
        assert result.result.status == "000"
        assert result.result.message == "정상적으로 처리되었습니다"
        assert result.result.list is not None
        assert len(result.result.list) == 1
        assert isinstance(result.result.list[0], CapitalChangeStatusItem)
        assert result.result.list[0].corp_name == "삼성전자"
        assert result.result.list[0].corp_code == "00126380"
        assert result.result.list[0].isu_dcrs_stle == "유상증자"

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["corp_code"] == ["00126380"]
        assert last_request.qs["bsns_year"] == ["2024"]
        assert last_request.qs["reprt_code"] == ["11011"]


def test_get_capital_change_status_rejects_non_mapping(client: Client, monkeypatch: pytest.MonkeyPatch) -> None:
    service = PeriodicReportKeyInformation(client)

    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: "not-a-mapping")

    with pytest.raises(TypeError) as exc_info:
        service.get_capital_change_status(
            corp_code="00126380",
            bsns_year="2024",
            reprt_code="11011",
        )

    assert "증자(감자) 현황 응답은 매핑 타입이어야 합니다" in str(exc_info.value)


def test_get_dividend_information_returns_typed_result(client: Client) -> None:
    expected_payload = {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [
            {
                "rcept_no": "20190401004781",
                "corp_cls": "Y",
                "corp_code": "00126380",
                "corp_name": "삼성전자",
                "se": "현금배당수익률(%)",
                "stock_knd": "우선주",
                "thstrm": "4.50",
                "frmtrm": "2.10",
                "lwfr": "2.00",
                "stlm_dt": "2018-12-31",
            },
            {
                "rcept_no": "20190401004781",
                "corp_cls": "Y",
                "corp_code": "00126380",
                "corp_name": "삼성전자",
                "se": "주식배당수익률(%)",
                "stock_knd": "보통주",
                "thstrm": "-",
                "frmtrm": "-",
                "lwfr": "-",
                "stlm_dt": "2018-12-31",
            },
        ],
    }

    service = PeriodicReportKeyInformation(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            "https://opendart.fss.or.kr/api/alotMatter.json",
            json=expected_payload,
            status_code=200,
        )

        result = service.get_dividend_information(
            corp_code="00126380",
            bsns_year="2024",
            reprt_code="11011",
        )

        assert isinstance(result, DividendInformation)
        assert result.result.status == "000"
        assert result.result.message == "정상적으로 처리되었습니다"
        assert result.result.list is not None
        assert len(result.result.list) == 2
        assert result.result.list[0].corp_name == "삼성전자"
        assert result.result.list[0].corp_code == "00126380"
        assert result.result.list[0].se == "현금배당수익률(%)"
        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == ["test-auth-key"]
        assert last_request.qs["corp_code"] == ["00126380"]
        assert last_request.qs["bsns_year"] == ["2024"]
        assert last_request.qs["reprt_code"] == ["11011"]


def test_get_dividend_information_rejects_non_mapping(client: Client, monkeypatch: pytest.MonkeyPatch) -> None:
    service = PeriodicReportKeyInformation(client)

    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: ["not-a-mapping"])

    with pytest.raises(TypeError) as exc_info:
        service.get_dividend_information(
            corp_code="00126380",
            bsns_year="2024",
            reprt_code="11011",
        )

    assert "배당 관련 사항 응답은 매핑 타입이어야 합니다" in str(exc_info.value)
