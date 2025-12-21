"""report.py integration 테스트."""

import logging
import time

import pytest

from dartex.report import (
    get_corp_code_by_stock_code,
    search_reports,
)

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_get_corp_code_by_stock_code() -> None:
    """stock_code로 corp_code 조회 테스트."""
    time.sleep(1)
    corp_code = get_corp_code_by_stock_code("035720")  # 카카오

    logger.info("stock_code: 035720 -> corp_code: %s", corp_code)

    assert corp_code == "00258801"


@pytest.mark.integration
def test_search_reports_by_stock_code_and_years() -> None:
    """stock_code와 years로 정기보고서 목록 조회 테스트.

    예시: 카카오(035720) 6년치 전체 정기보고서 (1분기, 반기, 3분기, 사업보고서)
    """
    time.sleep(1)
    corp_code = get_corp_code_by_stock_code("035720")
    assert corp_code is not None

    time.sleep(1)
    reports = search_reports(
        corp_code=corp_code,
        years=6,
    )

    logger.info("=" * 60)
    logger.info("카카오(035720) 6년치 정기보고서 조회 결과: %d건", len(reports))
    logger.info("=" * 60)
    for report in reports:
        logger.info(
            "[%s] %s (접수번호: %s, 접수일: %s)",
            report.fiscal_year,
            report.report_nm,
            report.rcept_no,
            report.rcept_dt,
        )

    assert len(reports) >= 1
    for report in reports:
        assert report.corp_code == corp_code
        # 정기보고서: 사업보고서, 반기보고서, 분기보고서
        assert any(keyword in report.report_nm for keyword in ["사업보고서", "반기보고서", "분기보고서"])
