import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
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

CORP_CODE = "00126380"
BSNS_YEAR = "2023"
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
    assert response.result.status is not None

    items = response.result.list or []
    assert all(isinstance(item, item_type) for item in items)

    if items:
        first_item = items[0]
        if hasattr(first_item, "corp_code"):
            assert first_item.corp_code == CORP_CODE


@pytest.mark.integration
def test_periodic_report_financial_statement_xbrl_taxonomy(
    service: PeriodicReportFinancialStatement,
) -> None:
    time.sleep(REQUEST_DELAY_SECONDS)

    response = service.get_xbrl_taxonomy("BS1")

    assert isinstance(response, XbrlTaxonomy)
    assert response.result is not None
    assert response.result.status is not None

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
    time.sleep(REQUEST_DELAY_SECONDS)

    major_accounts = service.get_single_company_major_accounts(**REQUEST_PARAMS)
    account_items = major_accounts.result.list or []
    assert account_items, "단일회사 주요계정 데이터가 비어 있습니다."

    rcept_no = account_items[0].rcept_no

    time.sleep(REQUEST_DELAY_SECONDS)

    destination = tmp_path / "fnlttXbrl.xml"
    saved_path = service.download_financial_statement_xbrl(
        rcept_no=rcept_no,
        reprt_code=REPRT_CODE,
        destination=destination,
        overwrite=True,
    )

    assert saved_path.exists()
    assert saved_path.stat().st_size > 0
    assert saved_path.read_bytes().strip().startswith(b"<")
