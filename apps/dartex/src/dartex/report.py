"""DART 보고서 조회 모듈.

기업 검색 및 사업보고서 목록 조회 기능을 제공합니다.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from cluefin_openapi.dart._client import Client as DartClient
from pydantic import BaseModel

from dartex.config import settings


class CompanyInfo(BaseModel):
    """기업 정보."""

    corp_code: str  # 8자리 고유번호
    corp_name: str  # 기업명
    stock_code: str | None = None  # 종목코드 (6자리)
    corp_cls: str | None = None  # 시장구분 (Y: KOSPI, K: KOSDAQ, N: KONEX, E: 기타)


class ReportInfo(BaseModel):
    """보고서 정보."""

    corp_code: str
    corp_name: str
    rcept_no: str  # 14자리 접수번호
    report_nm: str  # 보고서명
    rcept_dt: str  # 접수일자 (YYYYMMDD)
    fiscal_year: int  # 사업연도


# 보고서 유형 코드
REPORT_TYPE_ANNUAL = "A001"  # 사업보고서
REPORT_TYPE_SEMI_ANNUAL = "A002"  # 반기보고서
REPORT_TYPE_Q1 = "A003"  # 1분기보고서
REPORT_TYPE_Q3 = "A004"  # 3분기보고서


def _extract_fiscal_year(report_nm: str, rcept_dt: str) -> int:
    """보고서명 또는 접수일자에서 사업연도 추출.

    Args:
        report_nm: 보고서명 (예: "[기재정정]사업보고서 (2024.12)")
        rcept_dt: 접수일자 (YYYYMMDD)

    Returns:
        사업연도 (예: 2024)
    """
    # 보고서명에서 연도 추출 시도 (예: "2024.12" 또는 "(2024)")
    match = re.search(r"\((\d{4})(?:\.\d{1,2})?\)", report_nm)
    if match:
        return int(match.group(1))

    # 실패시 접수일자의 연도 사용 (1월~3월이면 전년도)
    year = int(rcept_dt[:4])
    month = int(rcept_dt[4:6])
    if month <= 3:
        return year - 1
    return year


def _get_dart_client() -> DartClient:
    """DART API 클라이언트 생성."""
    return DartClient(auth_key=settings.dart_auth_key)


def search_company(name: str) -> list[CompanyInfo]:
    """기업명으로 기업 검색.

    Args:
        name: 검색할 기업명 (부분 일치)

    Returns:
        검색된 기업 정보 목록
    """
    client = _get_dart_client()
    try:
        response = client.public_disclosure.corp_code()

        if response.result.status != "000":
            return []

        companies = []
        if response.result.list:
            for item in response.result.list:
                if name in item.corp_name:
                    companies.append(
                        CompanyInfo(
                            corp_code=item.corp_code,
                            corp_name=item.corp_name,
                            stock_code=item.stock_code if item.stock_code else None,
                            corp_cls=item.corp_cls if item.corp_cls else None,
                        )
                    )
        return companies
    finally:
        client.close()


def search_reports(
    corp_code: str,
    years: int = 5,
    report_types: list[str] | None = None,
) -> list[ReportInfo]:
    """기업의 사업보고서 목록 조회.

    Args:
        corp_code: 기업 고유번호 (8자리)
        years: 조회할 연도 수 (기본 5년)
        report_types: 보고서 유형 목록 (기본: 사업보고서만)
            - A001: 사업보고서
            - A002: 반기보고서
            - A003: 1분기보고서
            - A004: 3분기보고서

    Returns:
        보고서 정보 목록 (최신순)
    """
    if report_types is None:
        report_types = [REPORT_TYPE_ANNUAL]

    # 날짜 범위 계산
    end_date = datetime.now()
    start_year = end_date.year - years
    bgn_de = f"{start_year}0101"
    end_de = end_date.strftime("%Y%m%d")

    client = _get_dart_client()
    try:
        all_reports: list[ReportInfo] = []

        for report_type in report_types:
            reports = _fetch_reports_with_pagination(
                client=client,
                corp_code=corp_code,
                bgn_de=bgn_de,
                end_de=end_de,
                report_type=report_type,
            )
            all_reports.extend(reports)

        # 접수일자 기준 최신순 정렬
        all_reports.sort(key=lambda r: r.rcept_dt, reverse=True)
        return all_reports
    finally:
        client.close()


def _fetch_reports_with_pagination(
    client: DartClient,
    corp_code: str,
    bgn_de: str,
    end_de: str,
    report_type: str,
) -> list[ReportInfo]:
    """페이지네이션을 처리하여 모든 보고서 조회.

    Args:
        client: DART API 클라이언트
        corp_code: 기업 고유번호
        bgn_de: 시작일 (YYYYMMDD)
        end_de: 종료일 (YYYYMMDD)
        report_type: 보고서 유형 코드

    Returns:
        보고서 정보 목록
    """
    reports: list[ReportInfo] = []
    page_no = 1
    page_count = 100  # 최대값

    while True:
        response = client.public_disclosure.public_disclosure_search(
            corp_code=corp_code,
            bgn_de=bgn_de,
            end_de=end_de,
            pblntf_ty="A",  # 정기공시
            pblntf_detail_ty=report_type,
            sort="date",
            sort_mth="desc",
            page_no=page_no,
            page_count=page_count,
        )

        # 검색 결과 없음
        if response.result.status == "020":
            break

        # 기타 오류
        if response.result.status != "000":
            break

        if response.result.list:
            for item in response.result.list:
                fiscal_year = _extract_fiscal_year(item.report_nm, item.rcept_dt)
                reports.append(
                    ReportInfo(
                        corp_code=item.corp_code,
                        corp_name=item.corp_name,
                        rcept_no=item.rcept_no,
                        report_nm=item.report_nm,
                        rcept_dt=item.rcept_dt,
                        fiscal_year=fiscal_year,
                    )
                )

        # 마지막 페이지 확인
        total_page = response.result.total_page or 1
        if page_no >= total_page:
            break

        page_no += 1

    return reports


def get_report_rcept_nos(
    corp_code: str,
    years: int = 5,
    report_types: list[str] | None = None,
) -> list[str]:
    """보고서 접수번호 목록 조회.

    downloader 모듈에서 사용할 접수번호 리스트를 반환합니다.

    Args:
        corp_code: 기업 고유번호 (8자리)
        years: 조회할 연도 수 (기본 5년)
        report_types: 보고서 유형 목록

    Returns:
        접수번호 목록
    """
    reports = search_reports(corp_code, years, report_types)
    return [report.rcept_no for report in reports]
