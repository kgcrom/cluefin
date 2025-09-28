import os
import time

import dotenv
import pytest

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._periodic_report_key_information import PeriodicReportKeyInformation
from cluefin_openapi.dart._periodic_report_key_information_types import (
    AuditorNameAndOpinion,
    AuditorNameAndOpinionItem,
    AuditServiceContracts,
    AuditServiceContractsItem,
    BoardAndAuditCompensationAbove500m,
    BoardAndAuditCompensationAbove500mItem,
    BoardAndAuditCompensationByType,
    BoardAndAuditCompensationByTypeItem,
    BoardAndAuditCompensationShareholderApproved,
    BoardAndAuditCompensationShareholderApprovedItem,
    BoardAndAuditTotalCompensation,
    BoardAndAuditTotalCompensationItem,
    CapitalChangeStatus,
    CapitalChangeStatusItem,
    DebtSecuritiesIssuancePerformance,
    DebtSecuritiesIssuancePerformanceItem,
    DividendInformation,
    DividendInformationItem,
    EmployeeStatus,
    EmployeeStatusItem,
    ExecutiveStatus,
    ExecutiveStatusItem,
    MajorShareholderChanges,
    MajorShareholderChangesItem,
    MajorShareholderStatus,
    MajorShareholderStatusItem,
    MinorityShareholderStatus,
    MinorityShareholderStatusItem,
    NonAuditServiceContracts,
    NonAuditServiceContractsItem,
    OtherCorporationInvestments,
    OtherCorporationInvestmentsItem,
    OutsideDirectorStatus,
    OutsideDirectorStatusItem,
    OutstandingCommercialPaperBalance,
    OutstandingCommercialPaperBalanceItem,
    OutstandingContingentCapitalSecurities,
    OutstandingContingentCapitalSecuritiesItem,
    OutstandingCorporateBonds,
    OutstandingCorporateBondsItem,
    OutstandingHybridCapitalSecurities,
    OutstandingHybridCapitalSecuritiesItem,
    OutstandingShortTermBonds,
    OutstandingShortTermBondsItem,
    PrivatePlacementFundUsage,
    PrivatePlacementFundUsageItem,
    PublicOfferingFundUsage,
    PublicOfferingFundUsageItem,
    TopFiveIndividualCompensation,
    TopFiveIndividualCompensationItem,
    TotalNumberOfShares,
    TotalNumberOfSharesItem,
    TreasuryStockActivity,
    TreasuryStockActivityItem,
    UnregisteredExecutiveCompensation,
    UnregisteredExecutiveCompensationItem,
)

CORP_CODE = "00126380"
BSNS_YEAR = "2023"
REPRT_CODE = "11011"
REQUEST_DELAY_SECONDS = 1.0

REQUEST_PARAMS = {
    "corp_code": CORP_CODE,
    "bsns_year": BSNS_YEAR,
    "reprt_code": REPRT_CODE,
}

ENDPOINTS = [
    (
        "get_capital_change_status",
        CapitalChangeStatus,
        CapitalChangeStatusItem,
    ),
    (
        "get_dividend_information",
        DividendInformation,
        DividendInformationItem,
    ),
    (
        "get_treasury_stock_activity",
        TreasuryStockActivity,
        TreasuryStockActivityItem,
    ),
    (
        "get_major_shareholder_status",
        MajorShareholderStatus,
        MajorShareholderStatusItem,
    ),
    (
        "get_major_shareholder_changes",
        MajorShareholderChanges,
        MajorShareholderChangesItem,
    ),
    (
        "get_minority_shareholder_status",
        MinorityShareholderStatus,
        MinorityShareholderStatusItem,
    ),
    (
        "get_executive_status",
        ExecutiveStatus,
        ExecutiveStatusItem,
    ),
    (
        "get_employee_status",
        EmployeeStatus,
        EmployeeStatusItem,
    ),
    (
        "get_board_and_audit_compensation_above_500m",
        BoardAndAuditCompensationAbove500m,
        BoardAndAuditCompensationAbove500mItem,
    ),
    (
        "get_board_and_audit_total_compensation",
        BoardAndAuditTotalCompensation,
        BoardAndAuditTotalCompensationItem,
    ),
    (
        "get_top_five_individual_compensation",
        TopFiveIndividualCompensation,
        TopFiveIndividualCompensationItem,
    ),
    (
        "get_other_corporation_investments",
        OtherCorporationInvestments,
        OtherCorporationInvestmentsItem,
    ),
    (
        "get_total_number_of_shares",
        TotalNumberOfShares,
        TotalNumberOfSharesItem,
    ),
    (
        "get_debt_securities_issuance_performance",
        DebtSecuritiesIssuancePerformance,
        DebtSecuritiesIssuancePerformanceItem,
    ),
    (
        "get_outstanding_commercial_paper_balance",
        OutstandingCommercialPaperBalance,
        OutstandingCommercialPaperBalanceItem,
    ),
    (
        "get_outstanding_short_term_bonds",
        OutstandingShortTermBonds,
        OutstandingShortTermBondsItem,
    ),
    (
        "get_outstanding_corporate_bonds",
        OutstandingCorporateBonds,
        OutstandingCorporateBondsItem,
    ),
    (
        "get_outstanding_hybrid_capital_securities",
        OutstandingHybridCapitalSecurities,
        OutstandingHybridCapitalSecuritiesItem,
    ),
    (
        "get_outstanding_contingent_capital_securities",
        OutstandingContingentCapitalSecurities,
        OutstandingContingentCapitalSecuritiesItem,
    ),
    (
        "get_auditor_name_and_opinion",
        AuditorNameAndOpinion,
        AuditorNameAndOpinionItem,
    ),
    (
        "get_audit_service_contracts",
        AuditServiceContracts,
        AuditServiceContractsItem,
    ),
    (
        "get_non_audit_service_contracts",
        NonAuditServiceContracts,
        NonAuditServiceContractsItem,
    ),
    (
        "get_outside_director_status",
        OutsideDirectorStatus,
        OutsideDirectorStatusItem,
    ),
    (
        "get_unregistered_executive_compensation",
        UnregisteredExecutiveCompensation,
        UnregisteredExecutiveCompensationItem,
    ),
    (
        "get_board_and_audit_compensation_shareholder_approved",
        BoardAndAuditCompensationShareholderApproved,
        BoardAndAuditCompensationShareholderApprovedItem,
    ),
    (
        "get_board_and_audit_compensation_by_type",
        BoardAndAuditCompensationByType,
        BoardAndAuditCompensationByTypeItem,
    ),
    (
        "get_public_offering_fund_usage",
        PublicOfferingFundUsage,
        PublicOfferingFundUsageItem,
    ),
    (
        "get_private_placement_fund_usage",
        PrivatePlacementFundUsage,
        PrivatePlacementFundUsageItem,
    ),
]


@pytest.fixture
def client() -> Client:
    time.sleep(REQUEST_DELAY_SECONDS)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("DART_AUTH_KEY", ""))


@pytest.fixture
def service(client: Client) -> PeriodicReportKeyInformation:
    return PeriodicReportKeyInformation(client)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("method_name", "response_type", "item_type"),
    ENDPOINTS,
)
def test_periodic_report_key_information_endpoints(
    service: PeriodicReportKeyInformation,
    method_name: str,
    response_type: type,
    item_type: type,
) -> None:
    time.sleep(REQUEST_DELAY_SECONDS)

    method = getattr(service, method_name)
    response = method(**REQUEST_PARAMS)

    assert isinstance(response, response_type)
    assert response.result is not None
    assert response.result.status is not None

    items = response.result.list or []
    assert all(isinstance(item, item_type) for item in items)

    if items:
        first_item = items[0]
        assert first_item.rcept_no
        if hasattr(first_item, "corp_code"):
            assert first_item.corp_code == CORP_CODE
