"""ECOS(한국은행 경제통계) Open API Exception classes.

ECOS는 오류도 HTTP 200으로 돌려주고 본문 `{"RESULT": {"CODE": "ERROR-101", "MESSAGE": "…"}}` 로 알린다.
`code` 에 그 결과 코드가 실린다. HTTP 단계 오류(404·5xx·타임아웃·연결)는 `code` 가 None.
"""

from typing import Any, Dict, Optional


class EcosAPIError(Exception):
    """Base exception class for ECOS API errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.response_data = response_data
        self.request_context = request_context or {}

    def __str__(self) -> str:
        if self.code:
            return f"ECOS API Error [{self.code}]: {self.message}"
        if self.status_code:
            return f"ECOS API Error [{self.status_code}]: {self.message}"
        return f"ECOS API Error: {self.message}"


class EcosAuthenticationError(EcosAPIError):
    """INFO-100: 인증키가 유효하지 않다."""


class EcosRequestError(EcosAPIError):
    """요청 값 오류 (ERROR-100 필수값 누락, 101 날짜 형식, 200 요청유형, 300·301 조회건수)."""


class EcosSampleLimitError(EcosRequestError):
    """ERROR-301 중 `sample` 키로 10건을 넘겨 요청한 경우.

    서버는 건수 타입 오류와 같은 코드를 쓰고 메시지 끝에 "sample은 최대 10건…"을 붙인다.
    """


class EcosServerError(EcosAPIError):
    """서버 쪽 오류 (ERROR-400 60초 타임아웃, 500, 600 DB 연결, 601 SQL, HTTP 5xx)."""


class EcosRateLimitError(EcosAPIError):
    """ERROR-602 과도한 호출로 이용 제한, HTTP 429, 또는 클라이언트 레이트 리밋 대기 시간 초과."""


class EcosNotFoundError(EcosAPIError):
    """HTTP 404 (없는 서비스명). 없는 통계표·데이터는 404가 아니라 빈 결과(INFO-200)다."""


class EcosTimeoutError(EcosAPIError):
    """Exception raised for request timeout errors."""


class EcosNetworkError(EcosAPIError):
    """Exception raised for network connection errors."""


def raise_for_result(
    code: str,
    message: str,
    response_data: Optional[Dict[str, Any]] = None,
    request_context: Optional[Dict[str, Any]] = None,
) -> None:
    """본문 `RESULT.CODE` 를 예외로 바꿔 던진다. 데이터 없음(INFO-200)은 호출 전에 걸러진다.

    코드는 `INFO-100`·`ERROR-101` 꼴이고, 같은 ERROR-301 이 건수 타입 오류·시작>끝·sample 10건 초과를 함께 뜻한다
    (메시지 꼬리만 다르다). 명세의 코드 목록은 `docs/ecos_spec/*.xls` 의 "OpenAPI 메세지" 표.
    """
    common = {"code": code, "response_data": response_data, "request_context": request_context}
    if code == SAMPLE_LIMIT_CODE and SAMPLE_LIMIT_HINT in message:
        raise EcosSampleLimitError(message, **common)
    error_cls = _RESULT_CODE_ERRORS.get(code, EcosAPIError)
    raise error_cls(message or "ECOS 오류", **common)


# 새로 본 코드는 여기에 한 줄 더한다. 표에 없는 코드는 EcosAPIError.
_RESULT_CODE_ERRORS: Dict[str, type] = {
    "INFO-100": EcosAuthenticationError,
    "ERROR-100": EcosRequestError,
    "ERROR-101": EcosRequestError,
    "ERROR-200": EcosRequestError,
    "ERROR-300": EcosRequestError,
    "ERROR-301": EcosRequestError,
    "ERROR-400": EcosServerError,
    "ERROR-500": EcosServerError,
    "ERROR-600": EcosServerError,
    "ERROR-601": EcosServerError,
    "ERROR-602": EcosRateLimitError,
}

# ERROR-301 은 건수 타입 오류·시작>끝·sample 10건 초과가 같은 코드라 메시지 꼬리로만 가른다.
# 문구가 바뀌면 일반 EcosRequestError 로 떨어질 뿐이라(상위 클래스) 잡는 쪽이 깨지지 않는다.
SAMPLE_LIMIT_CODE = "ERROR-301"
SAMPLE_LIMIT_HINT = "sample"
