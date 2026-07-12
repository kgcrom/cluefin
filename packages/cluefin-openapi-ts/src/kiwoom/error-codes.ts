import {
  type ApiError,
  type ApiErrorDetails,
  KiwoomApiError,
  KiwoomAuthenticationError,
  KiwoomAuthorizationError,
  KiwoomRateLimitError,
  KiwoomServerError,
  KiwoomValidationError,
} from '../core/errors';

/**
 * Kiwoom API 서버 오류코드 registry.
 *
 * Kiwoom reports these codes in the response body (`return_code` / `return_msg`)
 * for both token endpoints and TR endpoints. Placeholders `{?}` are filled by
 * the server in `return_msg`; these entries serve as fallbacks.
 */
export const KIWOOM_ERROR_CODES: Readonly<Partial<Record<number, string>>> = {
  1501: 'API ID가 Null이거나 값이 없습니다',
  1504: '해당 URI에서는 지원하는 API ID가 아닙니다. API ID={?}, URI={?}',
  1505: '해당 API ID는 존재하지 않습니다. API ID={?}',
  1511: '필수 입력 값에 값이 존재하지 않습니다. 필수입력 파라미터={?}',
  1512: 'Http header에 값이 설정되지 않았거나 읽을 수 없습니다',
  1513: 'Http Header에 authorization 필드가 설정되어 있어야 합니다',
  1514: '입력으로 들어온 Http Header의 authorization 필드 형식이 맞지 않습니다',
  1515: 'Http Header의 authorization 필드 내 Grant Type이 미리 정의된 형식이 아닙니다',
  1516: 'Http Header의 authorization 필드 내 Token이 정의되어 있지 않습니다',
  1517: '입력 값 형식이 올바르지 않습니다. 파라미터={?} 실패사유={?}',
  1687: '재귀 호출이 발생하여 API 호출을 제한합니다, API ID={?}',
  1700: '허용된 API 요청 개수를 초과하였습니다. 유량={?}, API ID={?}',
  1701: '허용된 전체 요청 개수를 초과하였습니다. 총유량={?}',
  1702: '허용된 그룹 요청 개수를 초과하였습니다. 총유량={?}, API_ID={?}',
  1901: '시장 코드값이 존재하지 않습니다. 종목코드={?}',
  1902: '종목 정보가 없습니다. 입력한 종목코드 값을 확인바랍니다. 종목코드={?}',
  1903: '종목 정보가 없습니다. 입력한 종목코드, 거래소구분 값을 확인바랍니다. 거래소구분={?}, 종목코드={?}',
  1999: '예기치 못한 에러가 발생했습니다. 실패사유={?}',
  8001: 'App Key와 Secret Key 검증에 실패했습니다',
  8002: 'App Key와 Secret Key 검증에 실패했습니다. 실패사유={?}',
  8003: 'Access Token을 조회하는데 실패했습니다. 실패사유={?}',
  8005: 'Token이 유효하지 않습니다',
  8006: 'Access Token을 생성하는데 실패했습니다. 실패사유={?}',
  8009: 'Access Token을 발급하는데 실패했습니다. 실패사유={?}',
  8010: 'Token을 발급받은 IP와 서비스를 요청한 IP가 동일하지 않습니다',
  8011: 'Access Token을 발급하는데 실패했습니다. 입력값에 grant_type이 들어오지 않았습니다',
  8012: 'Access Token을 발급하는데 실패했습니다. grant_type의 값이 맞지 않습니다',
  8015: 'Access Token을 폐기하는데 실패했습니다. 실패사유={?}',
  8016: 'Access Token을 폐기하는데 실패했습니다. 입력값에 Token이 들어오지 않았습니다',
  8020: '입력파라미터로 appkey 또는 secretkey가 들어오지 않았습니다.',
  8030: '투자구분(실전/모의)이 달라서 Appkey를 사용할수가 없습니다',
  8031: '투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다',
  8040: '단말기 인증에 실패했습니다',
  8050: '지정단말기 인증에 실패했습니다',
  8103: '토큰 인증 또는 단말기인증에 실패했습니다. 실패사유={?}',
  8104: '모의투자에서 지원하지 않는 API 입니다.',
  8200: '법인 고객은 해당 API를 지원하지 않습니다. API ID={?}, URI={?}',
};

const VALIDATION_CODES = new Set([1501, 1504, 1505, 1511, 1512, 1517, 1901, 1902, 1903]);
const AUTH_CODES = new Set([
  1513, 1514, 1515, 1516, 8001, 8002, 8003, 8005, 8006, 8009, 8010, 8011, 8012, 8015, 8016, 8020, 8030, 8031, 8040,
  8050, 8103,
]);
const AUTHZ_CODES = new Set([8104, 8200]);
const RATE_LIMIT_CODES = new Set([1687, 1700, 1701, 1702]);
const SERVER_CODES = new Set([1999]);

/** Coerce a body return_code (number or numeric string) to a number, else undefined. */
export const parseKiwoomReturnCode = (value: unknown): number | undefined => {
  if (typeof value === 'number' && Number.isFinite(value)) {
    return value;
  }
  if (typeof value === 'string' && value.trim() !== '') {
    const parsed = Number.parseInt(value.trim(), 10);
    return Number.isFinite(parsed) ? parsed : undefined;
  }
  return undefined;
};

/** Build the typed Kiwoom error for a non-zero body return_code. */
export const resolveKiwoomError = (
  returnCode: number,
  returnMsg?: string | undefined,
  details: ApiErrorDetails = {},
): ApiError => {
  // The server-provided return_msg wins over the registry fallback because it
  // carries the filled-in placeholders (API ID, 파라미터, 실패사유 등).
  // eslint-disable-next-line security/detect-object-injection -- returnCode is a parsed number.
  const message = `Kiwoom API error ${returnCode}: ${returnMsg ?? KIWOOM_ERROR_CODES[returnCode] ?? '알 수 없는 오류입니다'}`;
  const errorDetails: ApiErrorDetails = { ...details, errorCode: returnCode };

  if (VALIDATION_CODES.has(returnCode)) {
    return new KiwoomValidationError(message, errorDetails);
  }
  if (AUTH_CODES.has(returnCode)) {
    return new KiwoomAuthenticationError(message, errorDetails);
  }
  if (AUTHZ_CODES.has(returnCode)) {
    return new KiwoomAuthorizationError(message, errorDetails);
  }
  if (RATE_LIMIT_CODES.has(returnCode)) {
    return new KiwoomRateLimitError(message, errorDetails);
  }
  if (SERVER_CODES.has(returnCode)) {
    return new KiwoomServerError(message, errorDetails);
  }
  return new KiwoomApiError(message, errorDetails);
};
