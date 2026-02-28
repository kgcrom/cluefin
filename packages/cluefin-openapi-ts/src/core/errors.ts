export interface ApiErrorDetails {
  statusCode?: number;
  responseData?: unknown;
  requestContext?: Record<string, unknown>;
  retryAfter?: number;
}

export class ApiError extends Error {
  public readonly statusCode?: number;
  public readonly responseData?: unknown;
  public readonly requestContext?: Record<string, unknown>;

  public constructor(message: string, details: ApiErrorDetails = {}) {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = details.statusCode;
    this.responseData = details.responseData;
    this.requestContext = details.requestContext;
  }
}

export class ApiAuthenticationError extends ApiError {}
export class ApiAuthorizationError extends ApiError {}
export class ApiValidationError extends ApiError {}
export class ApiServerError extends ApiError {}
export class ApiNetworkError extends ApiError {}
export class ApiTimeoutError extends ApiError {}

export class ApiRateLimitError extends ApiError {
  public readonly retryAfter?: number;

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
