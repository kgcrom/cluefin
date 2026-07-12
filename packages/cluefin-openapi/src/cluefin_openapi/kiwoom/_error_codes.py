"""Kiwoom API server error-code registry.

Maps the documented ``return_code`` values (API 서버 오류코드) to human-readable
messages and typed exceptions. Kiwoom reports these codes in the response body
(``return_code`` / ``return_msg``) for both token endpoints and TR endpoints.
"""

from typing import Any, Dict, Optional, Type

from ._exceptions import (
    KiwoomAPIError,
    KiwoomAuthenticationError,
    KiwoomAuthorizationError,
    KiwoomRateLimitError,
    KiwoomServerError,
    KiwoomValidationError,
)

# return_code -> documented message (placeholders {?} are filled by the server
# in return_msg; these serve as fallbacks when return_msg is absent).
KIWOOM_ERROR_CODES: Dict[int, str] = {
    1501: "API ID가 Null이거나 값이 없습니다",
    1504: "해당 URI에서는 지원하는 API ID가 아닙니다. API ID={?}, URI={?}",
    1505: "해당 API ID는 존재하지 않습니다. API ID={?}",
    1511: "필수 입력 값에 값이 존재하지 않습니다. 필수입력 파라미터={?}",
    1512: "Http header에 값이 설정되지 않았거나 읽을 수 없습니다",
    1513: "Http Header에 authorization 필드가 설정되어 있어야 합니다",
    1514: "입력으로 들어온 Http Header의 authorization 필드 형식이 맞지 않습니다",
    1515: "Http Header의 authorization 필드 내 Grant Type이 미리 정의된 형식이 아닙니다",
    1516: "Http Header의 authorization 필드 내 Token이 정의되어 있지 않습니다",
    1517: "입력 값 형식이 올바르지 않습니다. 파라미터={?} 실패사유={?}",
    1687: "재귀 호출이 발생하여 API 호출을 제한합니다, API ID={?}",
    1700: "허용된 API 요청 개수를 초과하였습니다. 유량={?}, API ID={?}",
    1701: "허용된 전체 요청 개수를 초과하였습니다. 총유량={?}",
    1702: "허용된 그룹 요청 개수를 초과하였습니다. 총유량={?}, API_ID={?}",
    1901: "시장 코드값이 존재하지 않습니다. 종목코드={?}",
    1902: "종목 정보가 없습니다. 입력한 종목코드 값을 확인바랍니다. 종목코드={?}",
    1903: "종목 정보가 없습니다. 입력한 종목코드, 거래소구분 값을 확인바랍니다. 거래소구분={?}, 종목코드={?}",
    1999: "예기치 못한 에러가 발생했습니다. 실패사유={?}",
    8001: "App Key와 Secret Key 검증에 실패했습니다",
    8002: "App Key와 Secret Key 검증에 실패했습니다. 실패사유={?}",
    8003: "Access Token을 조회하는데 실패했습니다. 실패사유={?}",
    8005: "Token이 유효하지 않습니다",
    8006: "Access Token을 생성하는데 실패했습니다. 실패사유={?}",
    8009: "Access Token을 발급하는데 실패했습니다. 실패사유={?}",
    8010: "Token을 발급받은 IP와 서비스를 요청한 IP가 동일하지 않습니다",
    8011: "Access Token을 발급하는데 실패했습니다. 입력값에 grant_type이 들어오지 않았습니다",
    8012: "Access Token을 발급하는데 실패했습니다. grant_type의 값이 맞지 않습니다",
    8015: "Access Token을 폐기하는데 실패했습니다. 실패사유={?}",
    8016: "Access Token을 폐기하는데 실패했습니다. 입력값에 Token이 들어오지 않았습니다",
    8020: "입력파라미터로 appkey 또는 secretkey가 들어오지 않았습니다.",
    8030: "투자구분(실전/모의)이 달라서 Appkey를 사용할수가 없습니다",
    8031: "투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다",
    8040: "단말기 인증에 실패했습니다",
    8050: "지정단말기 인증에 실패했습니다",
    8103: "토큰 인증 또는 단말기인증에 실패했습니다. 실패사유={?}",
    8104: "모의투자에서 지원하지 않는 API 입니다.",
    8200: "법인 고객은 해당 API를 지원하지 않습니다. API ID={?}, URI={?}",
}

_VALIDATION_CODES = frozenset({1501, 1504, 1505, 1511, 1512, 1517, 1901, 1902, 1903})
_AUTH_CODES = frozenset(
    {
        1513,
        1514,
        1515,
        1516,
        8001,
        8002,
        8003,
        8005,
        8006,
        8009,
        8010,
        8011,
        8012,
        8015,
        8016,
        8020,
        8030,
        8031,
        8040,
        8050,
        8103,
    }
)
_AUTHZ_CODES = frozenset({8104, 8200})
_RATE_LIMIT_CODES = frozenset({1687, 1700, 1701, 1702})
_SERVER_CODES = frozenset({1999})


def parse_return_code(value: Any) -> Optional[int]:
    """Coerce a body return_code (int or numeric string) to int, else None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def error_type_for_code(return_code: int) -> Type[KiwoomAPIError]:
    """Return the exception class for a Kiwoom server error code."""
    if return_code in _VALIDATION_CODES:
        return KiwoomValidationError
    if return_code in _AUTH_CODES:
        return KiwoomAuthenticationError
    if return_code in _AUTHZ_CODES:
        return KiwoomAuthorizationError
    if return_code in _RATE_LIMIT_CODES:
        return KiwoomRateLimitError
    if return_code in _SERVER_CODES:
        return KiwoomServerError
    return KiwoomAPIError


def resolve_kiwoom_error(
    return_code: int,
    return_msg: Optional[str] = None,
    status_code: Optional[int] = None,
    response_data: Optional[Dict[str, Any]] = None,
    request_context: Optional[Dict[str, Any]] = None,
) -> KiwoomAPIError:
    """Build a typed exception for a non-zero Kiwoom ``return_code``.

    The server-provided ``return_msg`` wins over the registry fallback because
    it carries the filled-in placeholders (API ID, 파라미터, 실패사유 등).
    """
    message = return_msg or KIWOOM_ERROR_CODES.get(return_code, "알 수 없는 오류입니다")
    error_cls = error_type_for_code(return_code)
    exc = error_cls(
        f"Kiwoom API error {return_code}: {message}",
        status_code=status_code,
        response_data=response_data,
        request_context=request_context,
    )
    exc.return_code = return_code
    return exc
