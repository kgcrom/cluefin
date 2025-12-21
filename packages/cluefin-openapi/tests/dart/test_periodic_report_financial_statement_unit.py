import io
import types
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Mapping, Type, Union, get_args, get_origin

import pytest
import requests_mock
from pydantic import BaseModel

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._exceptions import DartAPIError
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

BASE_URL = "https://opendart.fss.or.kr"
AUTH_KEY = "test-auth-key"
ACCOUNT_PARAMS = {
    "corp_code": "00126380",
    "bsns_year": "2024",
    "reprt_code": "11011",
}
FULL_STATEMENT_PARAMS = {
    **ACCOUNT_PARAMS,
    "fs_div": "CFS",
}
INDICATOR_PARAMS = {
    **ACCOUNT_PARAMS,
    "idx_cl_code": "M210000",
}
XBRL_PARAMS = {
    "sj_div": "BS1",
}
DOWNLOAD_RECEPT_NO = "20240101000000"
DOWNLOAD_REPRT_CODE: Literal["11011", "11012", "11013", "11014"] = "11011"
DOWNLOAD_QUERY_PARAMS = {
    "rcept_no": DOWNLOAD_RECEPT_NO,
    "reprt_code": DOWNLOAD_REPRT_CODE,
}
SUCCESS_XML = "<result><status>000</status><message>정상적으로 처리되었습니다</message></result>".encode("utf-8")
ERROR_XML = "<result><status>012</status><message>에러</message></result>".encode("utf-8")


@dataclass(frozen=True)
class MethodCase:
    method_name: str
    endpoint: str
    response_type: type[Any]
    item_type: Type[BaseModel]
    params: dict[str, str]
    error_message: str
    overrides: dict[str, Any] | None = None


METHOD_CASES = [
    MethodCase(
        method_name="get_single_company_major_accounts",
        endpoint="/api/fnlttSinglAcnt.json",
        response_type=SingleCompanyMajorAccount,
        item_type=SingleCompanyMajorAccountItem,
        params=dict(ACCOUNT_PARAMS),
        error_message="단일회사 주요계정 API 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_multi_company_major_accounts",
        endpoint="/api/fnlttMultiAcnt.json",
        response_type=MultiCompanyMajorAccount,
        item_type=MultiCompanyMajorAccountItem,
        params=dict(ACCOUNT_PARAMS),
        error_message="다중회사 주요계정 API 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_single_company_full_statements",
        endpoint="/api/fnlttSinglAcntAll.json",
        response_type=SingleCompanyFullStatement,
        item_type=SingleCompanyFullStatementItem,
        params=dict(FULL_STATEMENT_PARAMS),
        error_message="단일회사 전체 재무제표 API 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_single_company_major_indicators",
        endpoint="/api/fnlttSinglIndx.json",
        response_type=SingleCompanyMajorIndicator,
        item_type=SingleCompanyMajorIndicatorItem,
        params=dict(INDICATOR_PARAMS),
        error_message="단일회사 주요 재무지표 API 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_multi_company_major_indicators",
        endpoint="/api/fnlttCmpnyIndx.json",
        response_type=MultiCompanyMajorIndicator,
        item_type=MultiCompanyMajorIndicatorItem,
        params=dict(INDICATOR_PARAMS),
        error_message="다중회사 주요 재무지표 API 응답은 매핑 타입이어야 합니다",
    ),
    MethodCase(
        method_name="get_xbrl_taxonomy",
        endpoint="/api/xbrlTaxonomy.json",
        response_type=XbrlTaxonomy,
        item_type=XbrlTaxonomyItem,
        params=dict(XBRL_PARAMS),
        error_message="XBRL 택사노미 재무제표 양식 API 응답은 매핑 타입이어야 합니다",
    ),
]


def build_payload(item_type: Type[BaseModel], overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    overrides = overrides or {}
    list_item: dict[str, Any] = {}
    for name, field in item_type.model_fields.items():
        if name in overrides:
            list_item[name] = overrides[name]
            continue
        list_item[name] = _default_value(field.annotation, name)
    return {
        "status": "000",
        "message": "정상적으로 처리되었습니다",
        "list": [list_item],
    }


def _default_value(annotation: Any, field_name: str) -> Any:
    origin = get_origin(annotation)
    if origin is None:
        if annotation is int:
            return 1
        if annotation is float:
            return 1.0
        return f"{field_name}-value"
    if origin is Literal:
        return get_args(annotation)[0]
    if origin in (types.UnionType, Union):
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if not args:
            return None
        return _default_value(args[0], field_name)
    return f"{field_name}-value"


def assert_query_params(request, expected: dict[str, str]) -> None:
    for key, value in expected.items():
        actual_values = request.qs[key]
        if isinstance(value, str):
            assert [item.lower() for item in actual_values] == [value.lower()]
        else:
            assert actual_values == [value]


@pytest.fixture
def client() -> Client:
    return Client(auth_key=AUTH_KEY)


@pytest.mark.parametrize("case", METHOD_CASES, ids=lambda case: case.method_name)
def test_periodic_report_financial_statement_methods_return_typed_results(client: Client, case: MethodCase) -> None:
    payload = build_payload(case.item_type, overrides=case.overrides)
    service = PeriodicReportFinancialStatement(client)
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(f"{BASE_URL}{case.endpoint}", json=payload, status_code=200)
        result = getattr(service, case.method_name)(**case.params)
    assert isinstance(result, case.response_type)
    assert result.result.status == "000"
    assert result.result.message == "정상적으로 처리되었습니다"
    assert result.result.list is not None
    assert len(result.result.list) == 1
    item = result.result.list[0]
    assert isinstance(item, case.item_type)
    expected_list = payload.get("list")
    assert isinstance(expected_list, list)
    expected_item = expected_list[0]
    assert isinstance(expected_item, dict)
    assert item.model_dump(by_alias=True) == expected_item
    last_request = mock_requests.last_request
    assert last_request is not None
    assert last_request.qs["crtfc_key"] == [AUTH_KEY]
    assert_query_params(last_request, case.params)


@pytest.mark.parametrize("case", METHOD_CASES, ids=lambda case: case.method_name)
def test_periodic_report_financial_statement_methods_reject_non_mapping_payloads(
    client: Client, case: MethodCase, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(client, "_get", lambda *args, **kwargs: "not-a-mapping")
    service = PeriodicReportFinancialStatement(client)
    method = getattr(service, case.method_name)
    with pytest.raises(TypeError) as exc_info:
        method(**case.params)
    assert case.error_message in str(exc_info.value)


def test_get_single_company_major_indicators_passes_payload_to_parser(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = PeriodicReportFinancialStatement(client)
    params = dict(INDICATOR_PARAMS)
    payload: Mapping[str, object] = {"result": {"status": "000", "message": "ok", "list": []}}
    captured: dict[str, object] = {}

    def fake_get(endpoint: str, params: Mapping[str, str]) -> Mapping[str, object]:
        captured["endpoint"] = endpoint
        captured["params"] = params
        return payload

    sentinel = object()

    def fake_parse(
        cls,
        raw_payload: Mapping[str, object],
        *,
        list_model: type[BaseModel],
        result_key: str = "result",
    ):
        captured["parse_payload"] = raw_payload
        captured["list_model"] = list_model
        captured["result_key"] = result_key
        captured["cls"] = cls
        return sentinel

    monkeypatch.setattr(client, "_get", fake_get)
    monkeypatch.setattr(SingleCompanyMajorIndicator, "parse", classmethod(fake_parse))

    result = service.get_single_company_major_indicators(**params)

    assert result is sentinel
    assert captured["endpoint"] == "/api/fnlttSinglIndx.json"
    assert captured["params"] == params
    assert captured["parse_payload"] is payload
    assert captured["list_model"] is SingleCompanyMajorIndicatorItem
    assert captured["result_key"] == "result"
    assert captured["cls"] is SingleCompanyMajorIndicator


def test_get_single_company_major_indicators_reports_payload_type_in_error(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = PeriodicReportFinancialStatement(client)
    monkeypatch.setattr(client, "_get", lambda *_args, **_kwargs: [])

    with pytest.raises(TypeError) as exc_info:
        service.get_single_company_major_indicators(**INDICATOR_PARAMS)

    assert (
        str(exc_info.value) == "단일회사 주요 재무지표 API 응답은 매핑 타입이어야 합니다. 수신한 타입: <class 'list'>"
    )


def test_download_financial_statement_xbrl_writes_plain_xml(tmp_path: Path, client: Client) -> None:
    service = PeriodicReportFinancialStatement(client)
    xml_bytes = SUCCESS_XML
    destination = tmp_path / "fnltt.xml"
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            f"{BASE_URL}/api/fnlttXbrl.xml",
            content=xml_bytes,
            status_code=200,
        )
        result = service.download_financial_statement_xbrl(
            rcept_no=DOWNLOAD_RECEPT_NO,
            reprt_code=DOWNLOAD_REPRT_CODE,
            destination=destination,
        )
    assert result == destination
    assert destination.read_bytes() == xml_bytes
    last_request = mock_requests.last_request
    assert last_request is not None
    assert last_request.qs["crtfc_key"] == [AUTH_KEY]
    assert_query_params(last_request, DOWNLOAD_QUERY_PARAMS)


def test_download_financial_statement_xbrl_extracts_zip(tmp_path: Path, client: Client) -> None:
    service = PeriodicReportFinancialStatement(client)
    xml_bytes = SUCCESS_XML
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("document.xml", xml_bytes)
    buffer.seek(0)
    destination = tmp_path / "unzipped.xml"
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            f"{BASE_URL}/api/fnlttXbrl.xml",
            content=buffer.getvalue(),
            status_code=200,
        )
        result = service.download_financial_statement_xbrl(
            rcept_no=DOWNLOAD_RECEPT_NO,
            reprt_code=DOWNLOAD_REPRT_CODE,
            destination=destination,
        )
    assert result == destination
    assert destination.read_bytes() == xml_bytes


def test_download_financial_statement_xbrl_raises_on_error_status(tmp_path: Path, client: Client) -> None:
    service = PeriodicReportFinancialStatement(client)
    error_xml = ERROR_XML
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            f"{BASE_URL}/api/fnlttXbrl.xml",
            content=error_xml,
            status_code=200,
        )
        with pytest.raises(DartAPIError) as exc_info:
            service.download_financial_statement_xbrl(
                rcept_no=DOWNLOAD_RECEPT_NO,
                reprt_code=DOWNLOAD_REPRT_CODE,
                destination=tmp_path / "error.xml",
            )
    message = str(exc_info.value)
    assert message.startswith("DART API Error:")
    assert message.endswith("에러")


def test_download_financial_statement_xbrl_rejects_existing_file(
    tmp_path: Path, client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "existing.xml"
    destination.write_text("existing")
    monkeypatch.setattr(client, "_get_bytes", lambda *args, **kwargs: SUCCESS_XML)
    service = PeriodicReportFinancialStatement(client)
    with pytest.raises(FileExistsError):
        service.download_financial_statement_xbrl(
            rcept_no=DOWNLOAD_RECEPT_NO,
            reprt_code=DOWNLOAD_REPRT_CODE,
            destination=destination,
        )


def test_download_financial_statement_xbrl_raises_when_zip_has_no_xml(tmp_path: Path, client: Client) -> None:
    service = PeriodicReportFinancialStatement(client)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("readme.txt", "no xml")
    buffer.seek(0)
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get(
            f"{BASE_URL}/api/fnlttXbrl.xml",
            content=buffer.getvalue(),
            status_code=200,
        )
        with pytest.raises(DartAPIError) as exc_info:
            service.download_financial_statement_xbrl(
                rcept_no=DOWNLOAD_RECEPT_NO,
                reprt_code=DOWNLOAD_REPRT_CODE,
                destination=tmp_path / "missing.xml",
            )
    message = str(exc_info.value)
    assert message.startswith("DART API Error:")
    assert message.endswith("ZIP 파일에 XML 데이터가 포함되어있지 않습니다.")
