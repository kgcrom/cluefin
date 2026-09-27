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
