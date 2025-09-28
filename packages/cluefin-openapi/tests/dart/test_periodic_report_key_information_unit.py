from dataclasses import dataclass
from typing import Type

import pytest
import requests_mock
from pydantic import BaseModel

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

BASE_URL = "https://opendart.fss.or.kr"
AUTH_KEY = "test-auth-key"
BASE_PARAMS = {
    "corp_code": "00126380",
    "bsns_year": "2024",
    "reprt_code": "11011",
}


@dataclass(frozen=True)
class MethodCase:
    method_name: str
    endpoint: str
    response_type: type
    item_type: Type[BaseModel]
    error_message: str
    overrides: dict[str, object] | None = None


METHOD_CASES = [
    MethodCase(
        method_name="get_capital_change_status",
        endpoint="/api/irdsSttus.json",
        response_type=CapitalChangeStatus,
        item_type=CapitalChangeStatusItem,
        error_message="증자(감자) 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_dividend_information",
        endpoint="/api/alotMatter.json",
        response_type=DividendInformation,
        item_type=DividendInformationItem,
        error_message="배당 관련 사항 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_treasury_stock_activity",
        endpoint="/api/tesstkAcqsDspsSttus.json",
        response_type=TreasuryStockActivity,
        item_type=TreasuryStockActivityItem,
        error_message="자기주식 취득 및 처분 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_major_shareholder_status",
        endpoint="/api/hyslrSttus.json",
        response_type=MajorShareholderStatus,
        item_type=MajorShareholderStatusItem,
        error_message="최대주주 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_major_shareholder_changes",
        endpoint="/api/hyslrChgSttus.json",
        response_type=MajorShareholderChanges,
        item_type=MajorShareholderChangesItem,
        error_message="최대주주 변동현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_minority_shareholder_status",
        endpoint="/api/mrhlSttus.json",
        response_type=MinorityShareholderStatus,
        item_type=MinorityShareholderStatusItem,
        error_message="소액주주 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_executive_status",
        endpoint="/api/exctvSttus.json",
        response_type=ExecutiveStatus,
        item_type=ExecutiveStatusItem,
        error_message="임원 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_employee_status",
        endpoint="/api/empSttus.json",
        response_type=EmployeeStatus,
        item_type=EmployeeStatusItem,
        error_message="직원 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_board_and_audit_compensation_above_500m",
        endpoint="/api/hmvAuditIndvdlBySttus.json",
        response_type=BoardAndAuditCompensationAbove500m,
        item_type=BoardAndAuditCompensationAbove500mItem,
        error_message="이사·감사 개별 보수현황(5억 이상) 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_board_and_audit_total_compensation",
        endpoint="/api/hmvAuditAllSttus.json",
        response_type=BoardAndAuditTotalCompensation,
        item_type=BoardAndAuditTotalCompensationItem,
        error_message="이사·감사 전체 보수지급금액 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_top_five_individual_compensation",
        endpoint="/api/indvdlByPay.json",
        response_type=TopFiveIndividualCompensation,
        item_type=TopFiveIndividualCompensationItem,
        error_message="개인별 보수지급 금액(5억 이상 상위 5인) 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_other_corporation_investments",
        endpoint="/api/otrCprInvstmntSttus.json",
        response_type=OtherCorporationInvestments,
        item_type=OtherCorporationInvestmentsItem,
        error_message="타법인 출자현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_total_number_of_shares",
        endpoint="/api/stockTotqySttus.json",
        response_type=TotalNumberOfShares,
        item_type=TotalNumberOfSharesItem,
        error_message="주식의 총수 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_debt_securities_issuance_performance",
        endpoint="/api/detScritsIsuAcmslt.json",
        response_type=DebtSecuritiesIssuancePerformance,
        item_type=DebtSecuritiesIssuancePerformanceItem,
        error_message="채무증권 발행실적 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_outstanding_commercial_paper_balance",
        endpoint="/api/entrprsBilScritsNrdmpBlce.json",
        response_type=OutstandingCommercialPaperBalance,
        item_type=OutstandingCommercialPaperBalanceItem,
        error_message="기업어음증권 미상환 잔액 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_outstanding_short_term_bonds",
        endpoint="/api/srtpdPsndbtNrdmpBlce.json",
        response_type=OutstandingShortTermBonds,
        item_type=OutstandingShortTermBondsItem,
        error_message="단기사채 미상환 잔액 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_outstanding_corporate_bonds",
        endpoint="/api/cprndNrdmpBlce.json",
        response_type=OutstandingCorporateBonds,
        item_type=OutstandingCorporateBondsItem,
        error_message="회사채 미상환 잔액 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_outstanding_hybrid_capital_securities",
        endpoint="/api/newCaplScritsNrdmpBlce.json",
        response_type=OutstandingHybridCapitalSecurities,
        item_type=OutstandingHybridCapitalSecuritiesItem,
        error_message="신종자본증권 미상환 잔액 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_outstanding_contingent_capital_securities",
        endpoint="/api/cndlCaplScritsNrdmpBlce.json",
        response_type=OutstandingContingentCapitalSecurities,
        item_type=OutstandingContingentCapitalSecuritiesItem,
        error_message="조건부 자본증권 미상환 잔액 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_auditor_name_and_opinion",
        endpoint="/api/accnutAdtorNmNdAdtOpinion.json",
        response_type=AuditorNameAndOpinion,
        item_type=AuditorNameAndOpinionItem,
        error_message="회계감사인 명칭과 감사의견 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_audit_service_contracts",
        endpoint="/api/adtServcCnclsSttus.json",
        response_type=AuditServiceContracts,
        item_type=AuditServiceContractsItem,
        error_message="감사용역 계약현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_non_audit_service_contracts",
        endpoint="/api/accnutAdtorNonAdtServcCnclsSttus.json",
        response_type=NonAuditServiceContracts,
        item_type=NonAuditServiceContractsItem,
        error_message="비감사용역 계약체결 현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_outside_director_status",
        endpoint="/api/outcmpnyDrctrNdChangeSttus.json",
        response_type=OutsideDirectorStatus,
        item_type=OutsideDirectorStatusItem,
        error_message="사외이사 및 변동현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_unregistered_executive_compensation",
        endpoint="/api/unrstExctvMendngSttus.json",
        response_type=UnregisteredExecutiveCompensation,
        item_type=UnregisteredExecutiveCompensationItem,
        error_message="미등기임원 보수현황 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_board_and_audit_compensation_shareholder_approved",
        endpoint="/api/drctrAdtAllMendngSttusGmtsckConfmAmount.json",
        response_type=BoardAndAuditCompensationShareholderApproved,
        item_type=BoardAndAuditCompensationShareholderApprovedItem,
        error_message="이사·감사 전체 보수현황(주주총회 승인금액) 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_board_and_audit_compensation_by_type",
        endpoint="/api/drctrAdtAllMendngSttusMendngPymntamtTyCl.json",
        response_type=BoardAndAuditCompensationByType,
        item_type=BoardAndAuditCompensationByTypeItem,
        error_message="이사·감사 전체 보수현황(보수지급금액 유형별) 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_public_offering_fund_usage",
        endpoint="/api/pssrpCptalUseDtls.json",
        response_type=PublicOfferingFundUsage,
        item_type=PublicOfferingFundUsageItem,
        error_message="공모자금 사용내역 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_private_placement_fund_usage",
        endpoint="/api/prvsrpCptalUseDtls.json",
        response_type=PrivatePlacementFundUsage,
        item_type=PrivatePlacementFundUsageItem,
        error_message="사모자금 사용내역 응답은 매핑 타입이어야 합니다",
    ),
]


def build_payload(item_type: Type[BaseModel], overrides: dict[str, object] | None = None) -> dict[str, object]:
    overrides = overrides or {}
    common_values = {
        "rcept_no": "20240101000000",
        "corp_cls": "Y",
        "corp_code": BASE_PARAMS["corp_code"],
        "corp_name": "Sample Corp",
        "bsns_year": BASE_PARAMS["bsns_year"],
        "stlm_dt": "2024-12-31",
    }
    list_item: dict[str, object] = {}
    for field_name, field in item_type.model_fields.items():
        if field_name in overrides:
            list_item[field_name] = overrides[field_name]
            continue
        if field_name in common_values:
            list_item[field_name] = common_values[field_name]
            continue
        annotation = field.annotation
        if annotation is int:
            list_item[field_name] = 1
        elif annotation is float:
            list_item[field_name] = 1.0
        else:
            list_item[field_name] = f"{field_name}-value"
    return {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [list_item],
    }


@pytest.fixture
def client() -> Client:
    return Client(auth_key=AUTH_KEY)


@pytest.mark.parametrize("case", METHOD_CASES, ids=lambda case: case.method_name)
def test_periodic_report_methods_return_typed_results(client: Client, case: MethodCase) -> None:
    payload = build_payload(case.item_type, overrides=case.overrides)
    service = PeriodicReportKeyInformation(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(f"{BASE_URL}{case.endpoint}", json=payload, status_code=200)

        result = getattr(service, case.method_name)(**BASE_PARAMS)

        assert isinstance(result, case.response_type)
        assert result.result.status == "000"
        assert result.result.message == "정상적으로 처리되었습니다"
        assert result.result.list is not None
        assert len(result.result.list) == 1

        item = result.result.list[0]
        assert isinstance(item, case.item_type)
        payload_list = payload.get("list")
        assert isinstance(payload_list, list)
        expected_item = payload_list[0]
        assert isinstance(expected_item, dict)
        assert item.model_dump(by_alias=True) == expected_item

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == [AUTH_KEY]
        assert last_request.qs["corp_code"] == [BASE_PARAMS["corp_code"]]
        assert last_request.qs["bsns_year"] == [BASE_PARAMS["bsns_year"]]
        assert last_request.qs["reprt_code"] == [BASE_PARAMS["reprt_code"]]


@pytest.mark.parametrize("case", METHOD_CASES, ids=lambda case: case.method_name)
def test_periodic_report_methods_reject_non_mapping_payloads(
    client: Client, case: MethodCase, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: "not-a-mapping")
    service = PeriodicReportKeyInformation(client)
    method = getattr(service, case.method_name)

    with pytest.raises(TypeError) as exc_info:
        method(**BASE_PARAMS)

    assert case.error_message in str(exc_info.value)


def test_get_dividend_information_excludes_none_parameters(client: Client) -> None:
    payload = build_payload(DividendInformationItem)
    params = BASE_PARAMS.copy()
    service = PeriodicReportKeyInformation(client)

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            f"{BASE_URL}/api/alotMatter.json",
            json=payload,
            status_code=200,
        )

        result = service.get_dividend_information(**params)

        assert isinstance(result, DividendInformation)
        assert result.result.status == "000"
        assert result.result.list is not None
        assert len(result.result.list) == 1

        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.qs["crtfc_key"] == [AUTH_KEY]
        assert last_request.qs["corp_code"] == [BASE_PARAMS["corp_code"]]
        assert last_request.qs["bsns_year"] == [BASE_PARAMS["bsns_year"]]
