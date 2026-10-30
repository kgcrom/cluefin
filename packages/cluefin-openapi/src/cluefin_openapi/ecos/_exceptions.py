"""ECOS(한국은행 경제통계) Open API Exception classes.

ECOS는 오류도 HTTP 200으로 돌려주고 본문 `{"RESULT": {"CODE": "ERROR-101", "MESSAGE": "…"}}` 로 알린다.
`code` 에 그 결과 코드가 실린다. HTTP 단계 오류(404·5xx·타임아웃·연결)는 `code` 가 None.
"""

from typing import Any


class EcosAPIError(Exception):
    """Base exception class for ECOS API errors."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
        hint: str | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.response_data = response_data
        self.request_context = request_context or {}
        # 결과 코드별로 무엇을 고치면 되는지. 서버 메시지는 명세 문구 그대로라 조치까지는 알려 주지 않는다.
        self.hint = hint

    def __str__(self) -> str:
        if self.code:
            tail = f" (조치: {self.hint})" if self.hint else ""
            return f"ECOS API Error [{self.code}]: {self.message}{tail}"
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


class EcosQueryTimeoutError(EcosServerError):
    """ERROR-400: 검색 범위가 커서 서버가 60초 만에 끊었다. 다시 보내도 같으니 기간·항목을 좁혀야 한다."""


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
    response_data: dict[str, Any] | None = None,
    request_context: dict[str, Any] | None = None,
) -> None:
    """본문 `RESULT.CODE` 를 예외로 바꿔 던진다. 데이터 없음(INFO-200)은 호출 전에 걸러진다.

    코드는 `INFO-100`·`ERROR-101` 꼴이고, 같은 ERROR-301 이 건수 타입 오류·시작>끝·sample 10건 초과를 함께 뜻한다
    (메시지 꼬리만 다르다). 명세의 코드 목록은 ECOS 개발 명세서(https://ecos.bok.or.kr/api/)의 "OpenAPI 메세지" 표.
    """
    common = {"code": code, "response_data": response_data, "request_context": request_context}
    if code == SAMPLE_LIMIT_CODE and SAMPLE_LIMIT_HINT in message:
        raise EcosSampleLimitError(message, hint=_SAMPLE_LIMIT_ACTION, **common)
    error_cls, hint = _RESULT_CODE_ERRORS.get(code, (EcosAPIError, None))
    raise error_cls(message or "ECOS 오류", hint=hint, **common)


_ROW_RANGE_ACTION = "start_row·end_row 는 1 이상 정수이고 start_row ≤ end_row 여야 합니다"
_SAMPLE_LIMIT_ACTION = "sample 키는 한 번에 10행까지입니다. 범위를 10행 이하로 주거나 생략해 쪽 넘김에 맡기세요"

# 새로 본 코드는 여기에 한 줄 더한다. 표에 없는 코드는 EcosAPIError. 문구는 명세의 "OpenAPI 메세지" 표를 따른다.
_RESULT_CODE_ERRORS: dict[str, tuple[type, str]] = {
    "INFO-100": (
        EcosAuthenticationError,
        "ECOS_AUTH_KEY 를 확인하세요. 키가 없으면 ECOS 에서 신청하거나 키 없이 sample(10행)로 쓰세요",
    ),
    "ERROR-100": (EcosRequestError, "통계표코드·주기·검색 시작/종료일자 같은 필수 값이 비었는지 확인하세요"),
    "ERROR-101": (
        EcosRequestError,
        "날짜는 주기 형식을 따릅니다. A=2024, S=2024S1, Q=2024Q1, M=202401, SM=202401S1, D=20240101",
    ),
    "ERROR-200": (EcosRequestError, "요청 유형(json)이 경로에 없거나 잘못됐습니다. 클라이언트 경로 조립을 확인하세요"),
    "ERROR-300": (EcosRequestError, _ROW_RANGE_ACTION),
    "ERROR-301": (EcosRequestError, _ROW_RANGE_ACTION),
    "ERROR-400": (EcosQueryTimeoutError, "기간을 나눠 여러 번 받거나 항목코드를 지정해 범위를 좁히세요"),
    "ERROR-500": (EcosServerError, "서비스명을 확인하고, 맞다면 잠시 후 다시 시도하세요"),
    "ERROR-600": (EcosServerError, "ECOS 서버 DB 접속 오류입니다. 재시도 후에도 같으면 잠시 뒤 다시 시도하세요"),
    "ERROR-601": (EcosServerError, "서버 SQL 오류입니다. 통계표·항목코드 조합을 확인하거나 잠시 뒤 다시 시도하세요"),
    "ERROR-602": (
        EcosRateLimitError,
        "호출이 너무 많아 제한됐습니다. rate_limit_requests_per_second 를 낮추거나 잠시 뒤 다시 시도하세요",
    ),
}

# 일시적이라 같은 요청을 다시 보내 볼 만한 코드. ERROR-400(범위 과다)·601(SQL)은 다시 보내도 같다.
RETRYABLE_RESULT_CODES = frozenset({"ERROR-600", "ERROR-602"})

# ERROR-301 은 건수 타입 오류·시작>끝·sample 10건 초과가 같은 코드라 메시지 꼬리로만 가른다.
# 문구가 바뀌면 일반 EcosRequestError 로 떨어질 뿐이라(상위 클래스) 잡는 쪽이 깨지지 않는다.
SAMPLE_LIMIT_CODE = "ERROR-301"
SAMPLE_LIMIT_HINT = "sample"
