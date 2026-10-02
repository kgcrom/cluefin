import { camelizeKeys, normalizeHeaders } from '../core/case-convert.js';
import {
  ApiAuthenticationError,
  ApiAuthorizationError,
  ApiError,
  ApiNetworkError,
  ApiRateLimitError,
  ApiServerError,
  ApiTimeoutError,
  ApiValidationError,
  DartApiError,
  DartAuthenticationError,
  DartAuthorizationError,
  DartNetworkError,
  DartRateLimitError,
  DartServerError,
  DartTimeoutError,
  DartValidationError,
} from '../core/errors.js';
import { BaseHttpClient } from '../core/http.js';
import { consoleLogger, type Logger } from '../core/logger.js';
import type { ApiResponse, DartEndpointDefinition } from '../core/types.js';
import { createInputSchema } from '../core/validation.js';
import { isZip } from '../core/zip.js';
import { MajorShareholderDisclosure } from './major-shareholder-disclosure.js';
import { PeriodicReportFinancialStatement } from './periodic-report-financial-statement.js';
import { PeriodicReportKeyInformation } from './periodic-report-key-information.js';
import { PublicDisclosure } from './public-disclosure.js';
import { DartShareDisclosureComprehensive } from './share-disclosure-comprehensive.js';
import { parseXmlStatus } from './xml.js';

export const DART_BASE_URL = 'https://opendart.fss.or.kr';

/** body `status` 중 성공을 뜻하는 코드. 바이너리 에러 본문(XML) 판별에만 쓴다. */
export const DART_SUCCESS_STATUS = '000';

export interface DartClientOptions {
  /** OpenDART 인증키(`crtfc_key`, 40자). 모든 요청의 쿼리스트링에 붙는다. */
  authKey: string;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  fetchImpl?: typeof fetch;
  /** Sink for API error logs. Defaults to the console; pass `silentLogger` to mute. */
  logger?: Logger;
}

export interface DartBinaryResponse {
  headers: Record<string, string>;
  body: Uint8Array;
}

const KEY_PARAM = /crtfc_key=[^&\s"']*/g;

/** 에러 메시지·로그에 인증키가 URL 째로 섞여 들어가는 경우를 대비해 마스킹한다. */
const redactKey = (message: string): string => message.replace(KEY_PARAM, 'crtfc_key=***');

const isDartError = (error: unknown): boolean =>
  error instanceof DartApiError ||
  error instanceof DartAuthenticationError ||
  error instanceof DartAuthorizationError ||
  error instanceof DartValidationError ||
  error instanceof DartRateLimitError ||
  error instanceof DartServerError ||
  error instanceof DartTimeoutError ||
  error instanceof DartNetworkError;

const mapDartError = (error: unknown): never => {
  if (isDartError(error)) {
    throw error;
  }
  if (error instanceof ApiError) {
    const message = redactKey(error.message);
    if (error instanceof ApiValidationError) throw new DartValidationError(message, error);
    if (error instanceof ApiAuthenticationError) throw new DartAuthenticationError(message, error);
    if (error instanceof ApiAuthorizationError) throw new DartAuthorizationError(message, error);
    if (error instanceof ApiRateLimitError) throw new DartRateLimitError(message, error);
    if (error instanceof ApiServerError) throw new DartServerError(message, error);
    if (error instanceof ApiTimeoutError) throw new DartTimeoutError(message, error);
    if (error instanceof ApiNetworkError) throw new DartNetworkError(message, error);
    throw new DartApiError(message, error);
  }
  throw new DartApiError(error instanceof Error ? redactKey(error.message) : 'Unknown DART client error');
};

/**
 * OpenDART REST client.
 *
 * 모든 호출은 `GET` + 쿼리스트링이고 인증은 토큰이 아니라 `crtfc_key` 쿼리 파라미터다.
 * HTTP 200 이어도 body `status` 가 `013`(조회 결과 없음) 등일 수 있으며, JSON 엔드포인트는
 * Python 클라이언트와 같이 이를 throw 하지 않고 그대로 돌려준다. 바이너리 엔드포인트(ZIP)만
 * 에러가 XML 본문(`<result><status>`)으로 오므로 여기서 `DartApiError` 로 바꾼다.
 */
export class DartClient {
  private readonly http: BaseHttpClient;
  private readonly authKey: string;
  private readonly logger: Logger;

  private publicDisclosureInstance?: PublicDisclosure;
  private shareDisclosureComprehensiveInstance?: DartShareDisclosureComprehensive;
  private periodicReportFinancialStatementInstance?: PeriodicReportFinancialStatement;
  private periodicReportKeyInformationInstance?: PeriodicReportKeyInformation;
  private majorShareholderDisclosureInstance?: MajorShareholderDisclosure;

  public constructor(options: DartClientOptions) {
    this.authKey = options.authKey;
    this.logger = options.logger ?? consoleLogger;
    this.http = new BaseHttpClient(
      {
        timeoutMs: options.timeoutMs ?? 30_000,
        retry: { maxRetries: options.maxRetries ?? 3, baseDelayMs: 300 },
        // Python 클라이언트 기본값과 동일: 초당 5건, 버스트 10건.
        rateLimit: {
          requestsPerSecond: options.rateLimitRequestsPerSecond ?? 5,
          burst: options.rateLimitBurst ?? 10,
        },
        debug: false,
      },
      options.fetchImpl,
    );
  }

  /** 공시정보 (공시검색·기업개황·공시서류 원본·고유번호) */
  public get publicDisclosure(): PublicDisclosure {
    if (!this.publicDisclosureInstance) {
      this.publicDisclosureInstance = new PublicDisclosure(this);
    }
    return this.publicDisclosureInstance;
  }

  /** 지분공시 종합정보 (대량보유 상황보고·임원/주요주주 소유보고) */
  public get shareDisclosureComprehensive(): DartShareDisclosureComprehensive {
    if (!this.shareDisclosureComprehensiveInstance) {
      this.shareDisclosureComprehensiveInstance = new DartShareDisclosureComprehensive(this);
    }
    return this.shareDisclosureComprehensiveInstance;
  }

  /** 정기보고서 재무정보 (주요계정·전체 재무제표·주요지표·XBRL) */
  public get periodicReportFinancialStatement(): PeriodicReportFinancialStatement {
    if (!this.periodicReportFinancialStatementInstance) {
      this.periodicReportFinancialStatementInstance = new PeriodicReportFinancialStatement(this);
    }
    return this.periodicReportFinancialStatementInstance;
  }

  /** 정기보고서 주요정보 (증자·배당·주주·임원·보수·채무증권·감사·자금사용 등) */
  public get periodicReportKeyInformation(): PeriodicReportKeyInformation {
    if (!this.periodicReportKeyInformationInstance) {
      this.periodicReportKeyInformationInstance = new PeriodicReportKeyInformation(this);
    }
    return this.periodicReportKeyInformationInstance;
  }

  /** 주요사항보고서 주요정보 (자기주식·증자·감자·사채 발행·합병/분할·양수도 결정 등) */
  public get majorShareholderDisclosure(): MajorShareholderDisclosure {
    if (!this.majorShareholderDisclosureInstance) {
      this.majorShareholderDisclosureInstance = new MajorShareholderDisclosure(this);
    }
    return this.majorShareholderDisclosureInstance;
  }

  /** JSON 엔드포인트 호출. 응답 키는 camelCase 로 바뀐다. */
  public async invokeEndpoint(
    definition: DartEndpointDefinition,
    input: Record<string, unknown>,
  ): Promise<ApiResponse> {
    try {
      const response = await this.send(definition, input);
      const rawJson: unknown = await response.json();
      if (definition.responseSchema) {
        definition.responseSchema.parse(rawJson);
      }
      return { headers: normalizeHeaders(response.headers), body: camelizeKeys(rawJson) as Record<string, unknown> };
    } catch (error) {
      return this.fail(definition, error);
    }
  }

  /** 바이너리(ZIP/XML) 엔드포인트 호출. 에러 XML 본문은 `DartApiError` 로 변환한다. */
  public async invokeBinaryEndpoint(
    definition: DartEndpointDefinition,
    input: Record<string, unknown>,
  ): Promise<DartBinaryResponse> {
    try {
      const response = await this.send(definition, input);
      const body = new Uint8Array(await response.arrayBuffer());
      this.assertNotErrorBody(body, definition.path);
      return { headers: normalizeHeaders(response.headers), body };
    } catch (error) {
      return this.fail(definition, error);
    }
  }

  private async send(definition: DartEndpointDefinition, input: Record<string, unknown>): Promise<Response> {
    const parsedInput = createInputSchema(definition.params).parse(input);

    // 입력 이름 → 와이어 키. 동적 프로퍼티 접근 없이 입력을 훑어 쿼리를 만든다.
    const wireKeyOf = new Map(Object.entries(definition.queryMap).map(([wireKey, inputKey]) => [inputKey, wireKey]));
    const query: Record<string, string> = {};
    for (const [inputKey, value] of Object.entries(parsedInput)) {
      const wireKey = wireKeyOf.get(inputKey);
      if (wireKey !== undefined && value !== undefined && value !== null) {
        query[wireKey] = String(value);
      }
    }
    query.crtfc_key = this.authKey;

    return this.http.request({
      method: 'GET',
      url: `${DART_BASE_URL}${definition.path}`,
      headers: { accept: 'application/json' },
      query,
    });
  }

  /** ZIP 이 아닌데 `<` 로 시작하면 에러 XML 인지 확인한다. 상태가 `000` 이 아니면 throw. */
  private assertNotErrorBody(body: Uint8Array, path: string): void {
    if (isZip(body)) {
      return;
    }
    const head = new TextDecoder('utf-8').decode(body.subarray(0, 4096)).trimStart();
    if (!head.startsWith('<')) {
      return;
    }
    const status = parseXmlStatus(new TextDecoder('utf-8').decode(body));
    if (status && status.status !== DART_SUCCESS_STATUS) {
      throw new DartApiError(status.message || `DART error ${status.status}`, {
        responseData: status,
        requestContext: { path },
        errorCode: status.status,
      });
    }
  }

  private fail(definition: DartEndpointDefinition, error: unknown): never {
    this.logger.error('DART API request failed', {
      path: definition.path,
      message: error instanceof Error ? redactKey(error.message) : String(error),
      ...(error instanceof ApiError && error.errorCode !== undefined ? { status: error.errorCode } : {}),
    });
    return mapDartError(error);
  }
}
