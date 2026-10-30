export interface ApiErrorDetails {
  statusCode?: number | undefined;
  responseData?: unknown;
  requestContext?: Record<string, unknown> | undefined;
  retryAfter?: number | undefined;
  errorCode?: number | string | undefined;
}

export class ApiError extends Error {
  public readonly statusCode?: number | undefined;
  public readonly responseData?: unknown;
  public readonly requestContext?: Record<string, unknown> | undefined;
  /** Broker-reported error code (e.g. Kiwoom body return_code), when available. */
  public readonly errorCode?: number | string | undefined;

  public constructor(message: string, details: ApiErrorDetails = {}) {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = details.statusCode;
    this.responseData = details.responseData;
    this.requestContext = details.requestContext;
    this.errorCode = details.errorCode;
  }
}

export class ApiAuthenticationError extends ApiError {}
export class ApiAuthorizationError extends ApiError {}
export class ApiValidationError extends ApiError {}
export class ApiServerError extends ApiError {}
export class ApiNetworkError extends ApiError {}
export class ApiTimeoutError extends ApiError {}

export class ApiRateLimitError extends ApiError {
  public readonly retryAfter?: number | undefined;

  public constructor(message: string, details: ApiErrorDetails = {}) {
    super(message, details);
    this.retryAfter = details.retryAfter;
  }
}

export class KisApiError extends ApiError {}
export class KisAuthenticationError extends ApiAuthenticationError {}
export class KisAuthorizationError extends ApiAuthorizationError {}
export class KisValidationError extends ApiValidationError {}
export class KisServerError extends ApiServerError {}
export class KisNetworkError extends ApiNetworkError {}
export class KisTimeoutError extends ApiTimeoutError {}
export class KisRateLimitError extends ApiRateLimitError {}

export class KiwoomApiError extends ApiError {}
export class KiwoomAuthenticationError extends ApiAuthenticationError {}
export class KiwoomAuthorizationError extends ApiAuthorizationError {}
export class KiwoomValidationError extends ApiValidationError {}
export class KiwoomServerError extends ApiServerError {}
export class KiwoomNetworkError extends ApiNetworkError {}
export class KiwoomTimeoutError extends ApiTimeoutError {}
export class KiwoomRateLimitError extends ApiRateLimitError {}

export class NhplugApiError extends ApiError {}
/** 조회 결과 0건 — 서버는 빈 결과를 성공 코드가 아니라 별도 `rsp_cd` 로 준다 (`NHPLUG_NO_DATA_RSP_CODES`). */
export class NhplugNoDataError extends NhplugApiError {}
/** 모의투자에서 제공하지 않는 업무 — 운영에서만 호출할 수 있다 (`NHPLUG_MOCK_UNSUPPORTED_RSP_CODES`). */
export class NhplugMockUnsupportedError extends NhplugApiError {}
/** 영업일이 아니라 처리할 수 없다 (`NHPLUG_NOT_BUSINESS_DAY_RSP_CODES`). */
export class NhplugNotBusinessDayError extends NhplugApiError {}
export class NhplugAuthenticationError extends ApiAuthenticationError {}
export class NhplugAuthorizationError extends ApiAuthorizationError {}
export class NhplugValidationError extends ApiValidationError {}
export class NhplugServerError extends ApiServerError {}
export class NhplugNetworkError extends ApiNetworkError {}
export class NhplugTimeoutError extends ApiTimeoutError {}
export class NhplugRateLimitError extends ApiRateLimitError {}

export class DartApiError extends ApiError {}
export class DartAuthenticationError extends ApiAuthenticationError {}
export class DartAuthorizationError extends ApiAuthorizationError {}
export class DartValidationError extends ApiValidationError {}
export class DartServerError extends ApiServerError {}
export class DartNetworkError extends ApiNetworkError {}
export class DartTimeoutError extends ApiTimeoutError {}
export class DartRateLimitError extends ApiRateLimitError {}

/** ECOS 는 오류도 HTTP 200 + 본문 `RESULT.CODE` 로 준다. 그 코드(`ERROR-101` 등)가 `errorCode` 에 실린다. */
export class EcosApiError extends ApiError {}
/** INFO-100: 인증키가 유효하지 않다. */
export class EcosAuthenticationError extends ApiAuthenticationError {}
/** 요청 값 오류 (ERROR-100 필수값 누락, 101 날짜 형식, 200 요청유형, 300·301 조회건수). */
export class EcosValidationError extends ApiValidationError {}
/** ERROR-301 중 `sample` 키로 10건을 넘겨 요청한 경우 — 메시지 꼬리로만 구분된다. */
export class EcosSampleLimitError extends EcosValidationError {}
/** 서버 쪽 오류 (ERROR-400·500·600·601, HTTP 5xx). */
export class EcosServerError extends ApiServerError {}
/** ERROR-400: 검색 범위가 커서 서버가 60초 만에 끊었다. 다시 보내도 같으니 기간·항목을 좁혀야 한다. */
export class EcosQueryTimeoutError extends EcosServerError {}
/** HTTP 404 (없는 서비스명). 없는 통계표·데이터는 404가 아니라 빈 결과(INFO-200)다. */
export class EcosNotFoundError extends EcosApiError {}
export class EcosNetworkError extends ApiNetworkError {}
export class EcosTimeoutError extends ApiTimeoutError {}
/** ERROR-602 과도한 호출로 이용 제한, HTTP 429, 또는 레이트 리밋 대기 시간 초과. */
export class EcosRateLimitError extends ApiRateLimitError {}
