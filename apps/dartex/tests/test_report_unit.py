"""report.py 단위 테스트."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dartex.report import (
    CompanyInfo,
    ReportInfo,
    _extract_fiscal_year,
    get_report_rcept_nos,
    search_company,
    search_reports,
)


class TestExtractFiscalYear:
    """_extract_fiscal_year 함수 테스트."""

    def test_extract_from_report_name_with_month(self) -> None:
        """보고서명에서 연도.월 형식 추출."""
        assert _extract_fiscal_year("사업보고서 (2024.12)", "20250315") == 2024

    def test_extract_from_report_name_with_correction(self) -> None:
        """기재정정 보고서명에서 연도 추출."""
        assert _extract_fiscal_year("[기재정정]사업보고서 (2023.12)", "20240401") == 2023

    def test_extract_from_report_name_year_only(self) -> None:
        """보고서명에서 연도만 있는 경우."""
        assert _extract_fiscal_year("사업보고서 (2022)", "20230315") == 2022

    def test_fallback_to_rcept_dt_q1(self) -> None:
        """보고서명에서 추출 실패시 접수일자 사용 (1분기)."""
        # 1~3월 접수는 전년도 사업연도
        assert _extract_fiscal_year("사업보고서", "20250315") == 2024

    def test_fallback_to_rcept_dt_q2(self) -> None:
        """보고서명에서 추출 실패시 접수일자 사용 (2분기 이후)."""
        # 4월 이후 접수는 해당 연도
        assert _extract_fiscal_year("사업보고서", "20250415") == 2025


def _create_mock_company_item(
    corp_code: str, corp_name: str, stock_code: str | None = None, corp_cls: str | None = None
) -> MagicMock:
    """Mock company item 생성."""
    item = MagicMock()
    item.corp_code = corp_code
    item.corp_name = corp_name
    item.stock_code = stock_code
    item.corp_cls = corp_cls
    return item


def _create_mock_report_item(corp_code: str, corp_name: str, rcept_no: str, report_nm: str, rcept_dt: str) -> MagicMock:
    """Mock report item 생성."""
    item = MagicMock()
    item.corp_code = corp_code
    item.corp_name = corp_name
    item.rcept_no = rcept_no
    item.report_nm = report_nm
    item.rcept_dt = rcept_dt
    return item


class TestSearchCompany:
    """search_company 함수 테스트."""

    def test_search_company_found(self) -> None:
        """기업 검색 성공 테스트."""
        mock_response = MagicMock()
        mock_response.result.status = "000"
        mock_response.result.list = [
            _create_mock_company_item("00258801", "카카오", "035720", "Y"),
            _create_mock_company_item("00164742", "카카오뱅크", "323410", "Y"),
            _create_mock_company_item("00126380", "삼성전자", "005930", "Y"),
        ]

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.corp_code.return_value = mock_response

            result = search_company("카카오")

            assert len(result) == 2
            assert result[0].corp_code == "00258801"
            assert result[0].corp_name == "카카오"
            assert result[1].corp_code == "00164742"
            assert result[1].corp_name == "카카오뱅크"

    def test_search_company_not_found(self) -> None:
        """기업 검색 결과 없음 테스트."""
        mock_response = MagicMock()
        mock_response.result.status = "000"
        mock_response.result.list = [
            _create_mock_company_item("00126380", "삼성전자", "005930", "Y"),
        ]

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.corp_code.return_value = mock_response

            result = search_company("네이버")

            assert len(result) == 0

    def test_search_company_api_error(self) -> None:
        """API 에러 발생시 빈 목록 반환."""
        mock_response = MagicMock()
        mock_response.result.status = "100"  # 시스템 오류
        mock_response.result.list = None

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.corp_code.return_value = mock_response

            result = search_company("카카오")

            assert len(result) == 0


class TestSearchReports:
    """search_reports 함수 테스트."""

    def test_search_reports_single_page(self) -> None:
        """단일 페이지 보고서 검색 테스트."""
        mock_response = MagicMock()
        mock_response.result.status = "000"
        mock_response.result.total_page = 1
        mock_response.result.list = [
            _create_mock_report_item("00258801", "카카오", "20250324000901", "사업보고서 (2024.12)", "20250324"),
            _create_mock_report_item("00258801", "카카오", "20240325000123", "사업보고서 (2023.12)", "20240325"),
        ]

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.public_disclosure_search.return_value = mock_response

            result = search_reports("00258801", years=5)

            assert len(result) == 2
            assert result[0].rcept_no == "20250324000901"
            assert result[0].fiscal_year == 2024
            assert result[1].rcept_no == "20240325000123"
            assert result[1].fiscal_year == 2023

    def test_search_reports_pagination(self) -> None:
        """페이지네이션 처리 테스트."""
        # First page response
        page1_response = MagicMock()
        page1_response.result.status = "000"
        page1_response.result.total_page = 2
        page1_response.result.list = [
            _create_mock_report_item("00258801", "카카오", "20250324000901", "사업보고서 (2024.12)", "20250324"),
        ]

        # Second page response
        page2_response = MagicMock()
        page2_response.result.status = "000"
        page2_response.result.total_page = 2
        page2_response.result.list = [
            _create_mock_report_item("00258801", "카카오", "20240325000123", "사업보고서 (2023.12)", "20240325"),
        ]

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.public_disclosure_search.side_effect = [
                page1_response,
                page2_response,
            ]

            result = search_reports("00258801", years=5)

            assert len(result) == 2
            assert mock_instance.public_disclosure.public_disclosure_search.call_count == 2

    def test_search_reports_no_results(self) -> None:
        """검색 결과 없음 테스트."""
        mock_response = MagicMock()
        mock_response.result.status = "020"  # 검색 결과 없음
        mock_response.result.list = None

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.public_disclosure_search.return_value = mock_response

            result = search_reports("00000000", years=5)

            assert len(result) == 0


class TestGetReportRceptNos:
    """get_report_rcept_nos 함수 테스트."""

    def test_get_rcept_nos(self) -> None:
        """접수번호 목록 조회 테스트."""
        mock_response = MagicMock()
        mock_response.result.status = "000"
        mock_response.result.total_page = 1
        mock_response.result.list = [
            _create_mock_report_item("00258801", "카카오", "20250324000901", "사업보고서 (2024.12)", "20250324"),
            _create_mock_report_item("00258801", "카카오", "20240325000123", "사업보고서 (2023.12)", "20240325"),
        ]

        with patch("dartex.report._get_dart_client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            mock_instance.public_disclosure.public_disclosure_search.return_value = mock_response

            result = get_report_rcept_nos("00258801", years=5)

            assert result == ["20250324000901", "20240325000123"]
