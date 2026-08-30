import { camelizeKeys, normalizeHeaders } from '../core/case-convert';
import {
  ApiAuthenticationError,
  ApiAuthorizationError,
  ApiError,
  ApiNetworkError,
  ApiRateLimitError,
  ApiServerError,
  ApiTimeoutError,
  ApiValidationError,
  NhplugApiError,
  NhplugAuthenticationError,
  NhplugAuthorizationError,
  NhplugNetworkError,
  NhplugRateLimitError,
  NhplugServerError,
  NhplugTimeoutError,
  NhplugValidationError,
} from '../core/errors';
import { BaseHttpClient } from '../core/http';
import { consoleLogger, type Logger } from '../core/logger';
import type { ApiEnv, ApiResponse, NhplugEndpointDefinition } from '../core/types';
import { createInputSchema, nhplugEnvelopeSchema } from '../core/validation';
import { NhplugCommon } from './common';
import { NhplugKrstockInquiry } from './krstock-inquiry';
import { NhplugKrstockOrder } from './krstock-order';
import { NhplugKrstockQuote } from './krstock-quote';
import { NhplugOverseasStockInquiry } from './overseas-stock-inquiry';
import { NhplugOverseasStockOrder } from './overseas-stock-order';
import { NhplugOverseasStockQuote } from './overseas-stock-quote';

/**
 * body `rsp_cd` 중 성공을 뜻하는 코드.
 *
 * 문서상 성공은 00000 뿐이지만, 모의투자 서버는 일부 조회 API 성공에
 * XA102("모의투자 조회가 완료되었습니다")를 반환한다 (2026-08-22 파이썬 실측).
 * 00000 만 성공으로 보면 정상 응답이 오탐되므로, 새 성공 코드가 실측되면 여기에 추가한다.
 * 파이썬 `_model.SUCCESS_RSP_CODES` 와 같은 값을 유지할 것.
 */
export const SUCCESS_RSP_CODES: readonly string[] = ['00000', 'XA102'];

export interface NhplugClientOptions {
  token: string;
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  debug?: boolean;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  fetchImpl?: typeof fetch;
  /** Sink for API error logs. Defaults to the console; pass `silentLogger` to mute. */
  logger?: Logger;
}

// prod = 운영(실제 주문 체결), dev = 모의투자(moapi)
const getBaseUrl = (env: ApiEnv): string =>
  env === 'prod' ? 'https://api.nhplug.com:8443' : 'https://moapi.nhplug.com:8443';

const stringifyParam = (value: unknown): string => (typeof value === 'string' ? value : String(value));

const mapNhplugError = (error: unknown): never => {
  if (
    error instanceof NhplugApiError ||
    error instanceof NhplugValidationError ||
    error instanceof NhplugAuthenticationError ||
    error instanceof NhplugAuthorizationError ||
    error instanceof NhplugRateLimitError ||
    error instanceof NhplugServerError ||
    error instanceof NhplugTimeoutError ||
    error instanceof NhplugNetworkError
  ) {
    throw error;
  }
  if (error instanceof ApiValidationError) {
    throw new NhplugValidationError(error.message, error);
  }
  if (error instanceof ApiAuthenticationError) {
    throw new NhplugAuthenticationError(error.message, error);
  }
  if (error instanceof ApiAuthorizationError) {
    throw new NhplugAuthorizationError(error.message, error);
  }
  if (error instanceof ApiRateLimitError) {
    throw new NhplugRateLimitError(error.message, error);
  }
  if (error instanceof ApiServerError) {
    throw new NhplugServerError(error.message, error);
  }
  if (error instanceof ApiTimeoutError) {
    throw new NhplugTimeoutError(error.message, error);
  }
  if (error instanceof ApiNetworkError) {
    throw new NhplugNetworkError(error.message, error);
  }
  if (error instanceof ApiError) {
    throw new NhplugApiError(error.message, error);
  }
  throw new NhplugApiError(error instanceof Error ? error.message : 'Unknown NH PLUG client error');
};

/**
 * NH PLUG REST client.
 *
 * 모든 호출은 `POST` + JSON 바디이며, 요청 파라미터는 `Input_0` 봉투로 감싸 전송한다.
 * 응답은 `rsp_cd`/`rsp_msg` + `Output_N` 봉투. 연속조회(페이지네이션)는 요청/응답 헤더
 * `cts`/`cts_flag` 로 처리한다.
 */
export class NhplugClient {
  private readonly baseUrl: string;
  private readonly http: BaseHttpClient;
  private readonly token: string;
  private readonly appKey: string;
  private readonly secretKey: string;
  private readonly logger: Logger;

  private commonInstance?: NhplugCommon;
  private krstockOrderInstance?: NhplugKrstockOrder;
  private krstockInquiryInstance?: NhplugKrstockInquiry;
  private krstockQuoteInstance?: NhplugKrstockQuote;
  private overseasStockOrderInstance?: NhplugOverseasStockOrder;
  private overseasStockInquiryInstance?: NhplugOverseasStockInquiry;
  private overseasStockQuoteInstance?: NhplugOverseasStockQuote;

  public constructor(options: NhplugClientOptions) {
    const env = options.env ?? 'dev';
    this.baseUrl = getBaseUrl(env);
    this.token = options.token;
    this.appKey = options.appKey;
    this.secretKey = options.secretKey;
    this.logger = options.logger ?? consoleLogger;
    this.http = new BaseHttpClient(
      {
        timeoutMs: options.timeoutMs ?? 30_000,
        retry: {
          maxRetries: options.maxRetries ?? 3,
          baseDelayMs: 300,
        },
        rateLimit: {
          // NH 권고 기본값: 초당 20건, 버스트 3건.
          requestsPerSecond: options.rateLimitRequestsPerSecond ?? 20,
          burst: options.rateLimitBurst ?? 3,
        },
        debug: options.debug ?? false,
      },
      options.fetchImpl,
    );
  }

  /** 공통 (계좌·실시간 세션) */
  public get common(): NhplugCommon {
    if (!this.commonInstance) {
      this.commonInstance = new NhplugCommon(this);
    }
    return this.commonInstance;
  }

  /** 국내주식 주문 */
  public get krstockOrder(): NhplugKrstockOrder {
    if (!this.krstockOrderInstance) {
      this.krstockOrderInstance = new NhplugKrstockOrder(this);
    }
    return this.krstockOrderInstance;
  }

  /** 국내주식 조회 */
  public get krstockInquiry(): NhplugKrstockInquiry {
    if (!this.krstockInquiryInstance) {
      this.krstockInquiryInstance = new NhplugKrstockInquiry(this);
    }
    return this.krstockInquiryInstance;
  }

  /** 국내주식 시세 */
  public get krstockQuote(): NhplugKrstockQuote {
    if (!this.krstockQuoteInstance) {
      this.krstockQuoteInstance = new NhplugKrstockQuote(this);
    }
    return this.krstockQuoteInstance;
  }

  /** 해외주식 주문 */
  public get overseasStockOrder(): NhplugOverseasStockOrder {
    if (!this.overseasStockOrderInstance) {
      this.overseasStockOrderInstance = new NhplugOverseasStockOrder(this);
    }
    return this.overseasStockOrderInstance;
  }

  /** 해외주식 조회 */
  public get overseasStockInquiry(): NhplugOverseasStockInquiry {
    if (!this.overseasStockInquiryInstance) {
      this.overseasStockInquiryInstance = new NhplugOverseasStockInquiry(this);
    }
    return this.overseasStockInquiryInstance;
  }

  /** 해외주식 시세 */
  public get overseasStockQuote(): NhplugOverseasStockQuote {
    if (!this.overseasStockQuoteInstance) {
      this.overseasStockQuoteInstance = new NhplugOverseasStockQuote(this);
    }
    return this.overseasStockQuoteInstance;
  }

  public async invokeEndpoint(
    definition: NhplugEndpointDefinition,
    input: Record<string, unknown>,
  ): Promise<ApiResponse> {
    try {
      const parsedInput = createInputSchema(definition.params).parse(input);

      const body = Object.fromEntries(
        Object.entries(definition.bodyMap)
          .map(([apiKey, inputKey]) => {
            const value = parsedInput[inputKey];
            if (value === undefined || value === null) {
              return null;
            }
            return [apiKey, stringifyParam(value)];
          })
          .filter((entry): entry is [string, string] => entry !== null),
      );

      // 연속조회: 이전 응답 헤더의 `cts` 값을 그대로 넘기면 다음 페이지를 받는다.
      const continuationHeaders: Record<string, string> = {};
      const cts = parsedInput.cts;
      if (definition.supportsCts && cts !== undefined && cts !== null) {
        continuationHeaders.cts = stringifyParam(cts);
        continuationHeaders.cts_flag = 'Y';
      }

      const response = await this.http.request({
        method: 'POST',
        url: `${this.baseUrl}${definition.path}`,
        headers: {
          'content-type': 'application/json',
          accept: 'application/json',
          authorization: `Bearer ${this.token}`,
          'x-client-id': this.appKey,
          'x-client-secret': this.secretKey,
          ...continuationHeaders,
        },
        // 요청 파라미터는 항상 `Input_0` 봉투로 감싼다.
        body: { Input_0: body },
      });

      const rawJson = await response.json();
      const envelope = nhplugEnvelopeSchema.parse(rawJson);

      // HTTP 200 이어도 body `rsp_cd` 가 실패일 수 있으므로 여기서 확인한다.
      const rspCd = envelope.rsp_cd;
      if (rspCd !== undefined && !SUCCESS_RSP_CODES.includes(rspCd)) {
        throw new NhplugApiError(`API error ${rspCd}: ${envelope.rsp_msg ?? ''}`, {
          statusCode: response.status,
          responseData: rawJson,
          requestContext: { path: definition.path },
          errorCode: rspCd,
        });
      }

      if (definition.responseSchema) {
        definition.responseSchema.parse(rawJson);
      }

      return {
        headers: normalizeHeaders(response.headers),
        body: camelizeKeys(rawJson),
      };
    } catch (error) {
      this.logger.error('NH PLUG API request failed', {
        path: definition.path,
        message: error instanceof Error ? error.message : String(error),
        ...(error instanceof ApiError && error.errorCode !== undefined ? { rspCd: error.errorCode } : {}),
      });
      return mapNhplugError(error);
    }
  }
}
