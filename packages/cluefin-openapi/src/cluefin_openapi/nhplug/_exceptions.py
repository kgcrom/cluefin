"""Custom exceptions for NH PLUG API client."""

from typing import Any, Dict, Optional, Type

from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES


class NHPlugAPIError(Exception):
    """Base exception for all NH PLUG API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        self.request_context = request_context or {}

    @property
    def rsp_cd(self) -> Optional[str]:
        """응답 body 의 `rsp_cd` — HTTP 200 실패와 HTTP 400 입력 오류(IGW…) 모두 담긴다."""
        data = self.response_data
        return data.get("rsp_cd") if isinstance(data, dict) else None

    def __str__(self) -> str:
        base_msg = self.message
        if self.status_code:
            base_msg = f"[{self.status_code}] {base_msg}"
        return base_msg


class NHPlugAuthenticationError(NHPlugAPIError):
    """Raised when authentication fails (401 Unauthorized)."""

    pass


class NHPlugAuthorizationError(NHPlugAPIError):
    """Raised when authorization fails (403 Forbidden)."""

    pass


class NHPlugRateLimitError(NHPlugAPIError):
    """Raised when rate limit is exceeded (429 Too Many Requests).

    NH guidance: retry 429 with the SAME token — re-issuing a token on 429
    triggers security alerts on the account.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
        self.retry_after = retry_after


class NHPlugValidationError(NHPlugAPIError):
    """Raised when request validation fails (400 Bad Request)."""

    pass


class NHPlugServerError(NHPlugAPIError):
    """Raised when server returns 5xx errors."""

    pass


class NHPlugNetworkError(NHPlugAPIError):
    """Raised when network-related errors occur."""

    pass


class NHPlugTimeoutError(NHPlugAPIError):
    """Raised when request times out."""

    pass


# HTTP 200 + body rsp_cd 실패 중 뜻이 확인된 코드. 모르는 코드는 NHPlugAPIError 로 올린다.
# 새 코드가 실측되면 해당 갈래에 추가한다.


class NHPlugNoDataError(NHPlugAPIError):
    """조회 결과가 0건이다.

    서버는 빈 결과를 성공 코드가 아니라 별도 rsp_cd 로 준다 — 잔고·거래내역이 없는 계좌에서 난다.
    """

    pass


class NHPlugMockUnsupportedError(NHPlugAPIError):
    """모의투자에서 제공하지 않는 업무다. 운영(prod)에서만 호출할 수 있다."""

    pass


class NHPlugNotBusinessDayError(NHPlugAPIError):
    """영업일이 아니라 처리할 수 없다."""

    pass


NO_DATA_RSP_CODES: tuple[str, ...] = (
    "13578",  # 조회할 내역이 없습니다 — 국내 rightsScheduled, 해외 unexecuted 등 (2026-09-27 운영)
    "11512",  # 데이터가 존재하지 않습니다 — 국내 dailyOrderExecution (2026-09-27 운영)
    "16935",  # 해당 잔고가 없습니다 — 국내 sellableQuantity (2026-09-27 운영)
)
MOCK_UNSUPPORTED_RSP_CODES: tuple[str, ...] = (
    "19999",  # 모의투자에서는 해당업무가 제공되지 않습니다 (2026-09-27 모의, HTTP 200)
)
NOT_BUSINESS_DAY_RSP_CODES: tuple[str, ...] = (
    "14100",  # 모의투자 영업일이 아닙니다 (2026-08-22 토요일 모의)
)

_RSP_CD_ERROR_TYPES: Dict[str, Type[NHPlugAPIError]] = {
    **dict.fromkeys(NO_DATA_RSP_CODES, NHPlugNoDataError),
    **dict.fromkeys(MOCK_UNSUPPORTED_RSP_CODES, NHPlugMockUnsupportedError),
    **dict.fromkeys(NOT_BUSINESS_DAY_RSP_CODES, NHPlugNotBusinessDayError),
}


def raise_for_rsp_cd(response_data: Dict[str, Any]) -> None:
    """HTTP 200 이어도 body `rsp_cd` 가 실패일 수 있으므로 확인한다.

    뜻이 확인된 코드는 전용 예외(모두 NHPlugAPIError 하위)로, 나머지는 NHPlugAPIError 로 올린다.
    """
    rsp_cd = response_data.get("rsp_cd")
    if rsp_cd is None or rsp_cd in SUCCESS_RSP_CODES:
        return
    error_type = _RSP_CD_ERROR_TYPES.get(rsp_cd, NHPlugAPIError)
    raise error_type(
        f"API error {rsp_cd}: {response_data.get('rsp_msg', '')}",
        status_code=200,
        response_data=response_data,
    )
