import io
import logging
import os
import time
import zipfile

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._model import DartStatusCode
from cluefin_openapi.dart._periodic_report_financial_statement import PeriodicReportFinancialStatement
from cluefin_openapi.dart._periodic_report_financial_statement_types import (
    MultiCompanyMajorAccount,
    MultiCompanyMajorAccountItem,
    MultiCompanyMajorIndicator,
    MultiCompanyMajorIndicatorItem,
    SingleCompanyFullStatement,
    SingleCompanyFullStatementItem,
    SingleCompanyMajorAccount,
    SingleCompanyMajorAccountItem,
    SingleCompanyMajorIndicator,
    SingleCompanyMajorIndicatorItem,
    XbrlTaxonomy,
    XbrlTaxonomyItem,
)

logger = logging.getLogger(__name__)

CORP_CODE = "00126380"
BSNS_YEAR = "2024"
REPRT_CODE = "11011"
IDX_CL_CODE = "M210000"
FS_DIV = "CFS"
REQUEST_DELAY_SECONDS = 1.0

REQUEST_PARAMS = {
    "corp_code": CORP_CODE,
    "bsns_year": BSNS_YEAR,
    "reprt_code": REPRT_CODE,
}

ENDPOINTS = [
    (
        "get_single_company_major_accounts",
        SingleCompanyMajorAccount,
        SingleCompanyMajorAccountItem,
        {},
    ),
    (
        "get_multi_company_major_accounts",
        MultiCompanyMajorAccount,
        MultiCompanyMajorAccountItem,
        {},
    ),
    (
        "get_single_company_full_statements",
        SingleCompanyFullStatement,
        SingleCompanyFullStatementItem,
        {"fs_div": FS_DIV},
    ),
    (
        "get_single_company_major_indicators",
        SingleCompanyMajorIndicator,
        SingleCompanyMajorIndicatorItem,
        {"idx_cl_code": IDX_CL_CODE},
    ),
    (
        "get_multi_company_major_indicators",
        MultiCompanyMajorIndicator,
        MultiCompanyMajorIndicatorItem,
        {"idx_cl_code": IDX_CL_CODE},
    ),
]


@pytest.fixture
def client() -> Client:
    time.sleep(REQUEST_DELAY_SECONDS)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture
def service(client: Client) -> PeriodicReportFinancialStatement:
    return PeriodicReportFinancialStatement(client)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("method_name", "response_type", "item_type", "extra_kwargs"),
    ENDPOINTS,
)
def test_periodic_report_financial_statement_endpoints(
    service: PeriodicReportFinancialStatement,
    method_name: str,
    response_type: type,
    item_type: type,
    extra_kwargs: dict,
) -> None:
    time.sleep(REQUEST_DELAY_SECONDS)

    method = getattr(service, method_name)
    response = method(**REQUEST_PARAMS, **extra_kwargs)

    assert isinstance(response, response_type)
    assert response.result is not None
    assert response.result.status == DartStatusCode.SUCCESS

    items = response.result.list or []
    assert all(isinstance(item, item_type) for item in items)

    if items:
        first_item = items[0]
        if hasattr(first_item, "corp_code"):
            assert first_item.corp_code == CORP_CODE


@pytest.mark.integration
def test_get_single_company_major_indicators_returns_expected_fields(
    service: PeriodicReportFinancialStatement,
) -> None:
    time.sleep(REQUEST_DELAY_SECONDS)

    response = service.get_single_company_major_indicators(
        corp_code=CORP_CODE,
        bsns_year=BSNS_YEAR,
        reprt_code=REPRT_CODE,
        idx_cl_code=IDX_CL_CODE,
    )

    assert isinstance(response, SingleCompanyMajorIndicator)
    assert response.result is not None
    assert response.result.status == DartStatusCode.SUCCESS

    items = response.result.list or []
    assert all(item.idx_cl_code == IDX_CL_CODE for item in items)

    if items:
        first_item = items[0]
        assert first_item.corp_code == CORP_CODE
        assert first_item.idx_nm
        if first_item.idx_val is not None:
            assert first_item.idx_val


@pytest.mark.integration
def test_get_single_company_major_indicators_matches_request_metadata(
    service: PeriodicReportFinancialStatement,
) -> None:
    time.sleep(REQUEST_DELAY_SECONDS)

    response = service.get_single_company_major_indicators(
        corp_code=CORP_CODE,
        bsns_year=BSNS_YEAR,
        reprt_code=REPRT_CODE,
        idx_cl_code=IDX_CL_CODE,
    )

    assert response.result is not None
    assert response.result.status == DartStatusCode.SUCCESS

    items = response.result.list or []
    for item in items:
        assert item.bsns_year == BSNS_YEAR
        assert item.reprt_code == REPRT_CODE


@pytest.mark.integration
def test_periodic_report_financial_statement_xbrl_taxonomy(
    service: PeriodicReportFinancialStatement,
) -> None:
    time.sleep(REQUEST_DELAY_SECONDS)

    response = service.get_xbrl_taxonomy("BS1")

    assert isinstance(response, XbrlTaxonomy)
    assert response.result is not None
    assert response.result.status == DartStatusCode.SUCCESS

    items = response.result.list or []
    assert all(isinstance(item, XbrlTaxonomyItem) for item in items)

    if items:
        first_item = items[0]
        assert first_item.account_nm
        assert first_item.sj_div == "BS1"


@pytest.mark.integration
def test_download_financial_statement_xbrl(
    service: PeriodicReportFinancialStatement,
    tmp_path,
) -> None:
    logger.info(f"tmp_path: {tmp_path}")

    time.sleep(REQUEST_DELAY_SECONDS)

    major_accounts = service.get_single_company_major_accounts(**REQUEST_PARAMS)
    account_items = major_accounts.result.list or []
    assert account_items, "단일회사 주요계정 데이터가 비어 있습니다."

    rcept_no = account_items[0].rcept_no
    logger.info(f"rcept_no: {rcept_no}")

    time.sleep(REQUEST_DELAY_SECONDS)

    # ZIP 파일 내용 확인을 위해 raw 바이트 저장
    raw_path = tmp_path / "fnlttXbrl_raw.zip"
    raw_bytes = service.client._get_bytes(
        "/api/fnlttXbrl.xml",
        params={"rcept_no": rcept_no, "reprt_code": REPRT_CODE},
    )
    raw_path.write_bytes(raw_bytes)
    logger.info(f"Raw file saved: {raw_path}")
    logger.info(f"Raw file size: {len(raw_bytes)} bytes")

    # ZIP 파일인 경우 내용 로깅
    buffer = io.BytesIO(raw_bytes)
    if zipfile.is_zipfile(buffer):
        buffer.seek(0)
        with zipfile.ZipFile(buffer) as archive:
            logger.info("=== ZIP 파일 내용 ===")
            for info in archive.infolist():
                logger.info(f"  - {info.filename} ({info.file_size} bytes)")
    else:
        logger.info("응답이 ZIP 파일이 아닙니다")

    # 폴더에 XBRL 파일들 압축 해제
    destination = tmp_path / "xbrl_output"
    saved_path = service.download_financial_statement_xbrl(
        rcept_no=rcept_no,
        reprt_code=REPRT_CODE,
        destination=destination,
        overwrite=True,
    )

    assert saved_path.exists()
    assert saved_path.is_dir()

    # 압축 해제된 파일들 확인
    extracted_files = list(destination.iterdir())
    logger.info(f"=== 압축 해제된 파일 ({len(extracted_files)}개) ===")
    for f in extracted_files:
        logger.info(f"  - {f.name} ({f.stat().st_size} bytes)")

    # XBRL instance 파일이 존재하는지 확인
    xbrl_files = [f for f in extracted_files if f.suffix == ".xbrl"]
    assert xbrl_files, "XBRL instance 파일(.xbrl)이 존재해야 합니다"

    # XBRL 파일 내용 확인
    xbrl_content = xbrl_files[0].read_bytes()
    assert xbrl_content.strip().startswith(b"<")
