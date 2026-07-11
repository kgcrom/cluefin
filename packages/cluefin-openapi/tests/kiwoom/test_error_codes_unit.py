"""Tests for Kiwoom API 서버 오류코드 registry and client return_code handling."""

import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._error_codes import (
    KIWOOM_ERROR_CODES,
    error_type_for_code,
    parse_return_code,
    resolve_kiwoom_error,
)
from cluefin_openapi.kiwoom._exceptions import (
    KiwoomAPIError,
    KiwoomAuthenticationError,
    KiwoomAuthorizationError,
    KiwoomRateLimitError,
    KiwoomServerError,
    KiwoomValidationError,
)


@pytest.fixture
def client():
    return Client(token="test_token", env="dev")


def test_registry_covers_documented_codes():
    documented = {
        1501, 1504, 1505, 1511, 1512, 1513, 1514, 1515, 1516, 1517,
        1687, 1700, 1701, 1702, 1901, 1902, 1903, 1999,
        8001, 8002, 8003, 8005, 8006, 8009, 8010, 8011, 8012, 8015, 8016,
        8020, 8030, 8031, 8040, 8050, 8103, 8104, 8200,
    }  # fmt: skip
    assert set(KIWOOM_ERROR_CODES) == documented


def test_parse_return_code():
    assert parse_return_code(0) == 0
    assert parse_return_code("1700") == 1700
    assert parse_return_code(" 8005 ") == 8005
    assert parse_return_code(None) is None
    assert parse_return_code("OK") is None
    assert parse_return_code(True) is None


@pytest.mark.parametrize(
    "code,expected_cls",
    [
        (1501, KiwoomValidationError),
        (1517, KiwoomValidationError),
        (1902, KiwoomValidationError),
        (1513, KiwoomAuthenticationError),
        (8005, KiwoomAuthenticationError),
        (8103, KiwoomAuthenticationError),
        (8104, KiwoomAuthorizationError),
        (8200, KiwoomAuthorizationError),
        (1687, KiwoomRateLimitError),
        (1700, KiwoomRateLimitError),
        (1999, KiwoomServerError),
        (4242, KiwoomAPIError),  # unknown code falls back to the base error
    ],
)
def test_error_type_for_code(code, expected_cls):
    assert error_type_for_code(code) is expected_cls


def test_resolve_kiwoom_error_prefers_server_message():
    exc = resolve_kiwoom_error(1511, return_msg="필수입력 파라미터=stk_cd", status_code=200)
    assert isinstance(exc, KiwoomValidationError)
    assert exc.return_code == 1511
    assert "필수입력 파라미터=stk_cd" in str(exc)


def test_resolve_kiwoom_error_falls_back_to_registry_message():
    exc = resolve_kiwoom_error(8005)
    assert isinstance(exc, KiwoomAuthenticationError)
    assert KIWOOM_ERROR_CODES[8005] in str(exc)


def test_post_raises_on_error_return_code_with_http_200(client):
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 1902, "return_msg": "종목 정보가 없습니다. 종목코드=999999"},
            status_code=200,
        )

        with pytest.raises(KiwoomValidationError) as exc_info:
            client._post("/api/dostk/stkinfo", {"api-id": "ka10001"}, {"stk_cd": "999999"})

    assert exc_info.value.return_code == 1902
    assert exc_info.value.status_code == 200
    assert "종목코드=999999" in str(exc_info.value)


def test_post_maps_error_return_code_on_http_4xx(client):
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 8005, "return_msg": "Token이 유효하지 않습니다"},
            status_code=401,
        )

        with pytest.raises(KiwoomAuthenticationError) as exc_info:
            client._post("/api/dostk/stkinfo", {"api-id": "ka10001"}, {"stk_cd": "005930"})

    assert exc_info.value.return_code == 8005
    assert exc_info.value.status_code == 401


def test_post_succeeds_when_return_code_is_zero(client):
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 0, "return_msg": "정상적으로 처리되었습니다"},
            status_code=200,
        )

        response = client._post("/api/dostk/stkinfo", {"api-id": "ka10001"}, {"stk_cd": "005930"})

    assert response.status_code == 200


def test_error_return_code_is_logged(client):
    records = []
    from loguru import logger

    sink_id = logger.add(lambda message: records.append(message), level="ERROR")
    try:
        with requests_mock.Mocker() as m:
            m.post(
                "https://mockapi.kiwoom.com/api/dostk/stkinfo",
                json={"return_code": 1700, "return_msg": "허용된 API 요청 개수를 초과하였습니다"},
                status_code=200,
            )
            with pytest.raises(KiwoomRateLimitError):
                client._post("/api/dostk/stkinfo", {"api-id": "ka10001"}, {"stk_cd": "005930"})
    finally:
        logger.remove(sink_id)

    assert any("return_code=1700" in str(record) for record in records)
