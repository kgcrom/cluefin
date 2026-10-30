import type { z } from 'zod';

import { toCamelCase } from '../core/case-convert.js';
import {
  ApiAuthenticationError,
  ApiError,
  ApiNetworkError,
  ApiRateLimitError,
  ApiServerError,
  ApiTimeoutError,
  ApiValidationError,
  EcosApiError,
  EcosAuthenticationError,
  EcosNetworkError,
  EcosNotFoundError,
  EcosQueryTimeoutError,
  EcosRateLimitError,
  EcosSampleLimitError,
  EcosServerError,
  EcosTimeoutError,
  EcosValidationError,
} from '../core/errors.js';
import { BaseHttpClient } from '../core/http.js';
import { consoleLogger, type Logger } from '../core/logger.js';
import { withRetry } from '../core/retry.js';
import { StatisticCatalog } from './statistic-catalog.js';
import { StatisticGlossary } from './statistic-glossary.js';
import { StatisticSearch } from './statistic-search.js';
import type { EcosLang, EcosPage, EcosPageOptions } from './types.js';

export const ECOS_BASE_URL = 'https://ecos.bok.or.kr/api';

/**
 * 가입 없이 쓰는 공개 시험 키. 한 번에 10행까지지만 쪽 넘김(1/10 → 11/20 …)은 된다.
 * 이름에 key 가 들어가면 대입 값과 상관없이 Codacy 가 하드코딩 비밀번호로 잡아 `SAMPLE` 로 둔다(export 하지 않는다).
 */
const SAMPLE = 'sample';
const SAMPLE_PAGE_SIZE = 10;
/** 문서상 실키 한 번 상한. 실서버는 더 큰 범위도 받지만(2026-10-19 실측) 문서를 따른다. */
const PAGE_SIZE = 1000;

const NO_DATA_CODE = 'INFO-200';

/** 서버는 60초를 넘는 조회를 ERROR-400 으로 끊는다. 클라이언트가 먼저 끊으면 그 답을 못 보고 같은 요청을 재시도한다. */
const DEFAULT_TIMEOUT_MS = 75_000;

export interface EcosClientOptions {
  /** ECOS 인증키. 비우면 공개 시험 키 `sample`(한 번에 10행). */
  authKey?: string | undefined;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  /** 쪽 넘김 상한. 응답이 이상해도 무한히 묻지 않게 둔다. */
  maxPages?: number;
  fetchImpl?: typeof fetch;
  /** Sink for API error logs. Defaults to the console; pass `silentLogger` to mute. */
  logger?: Logger;
}

type ErrorClass = new (message: string, details?: ConstructorParameters<typeof ApiError>[1]) => ApiError;

const ROW_RANGE_ACTION = 'startRow·endRow 는 1 이상 정수이고 startRow ≤ endRow 여야 합니다';
const SAMPLE_LIMIT_ACTION = 'sample 키는 한 번에 10행까지입니다. 범위를 10행 이하로 주거나 생략해 쪽 넘김에 맡기세요';

/** 결과 코드별 예외와 조치 문구. 새로 본 코드는 한 줄 더한다. 표에 없는 코드는 EcosApiError. */
const RESULT_CODE_ERRORS = new Map<string, [ErrorClass, string]>([
  [
    'INFO-100',
    [
      EcosAuthenticationError,
      'ECOS_AUTH_KEY 를 확인하세요. 키가 없으면 ECOS 에서 신청하거나 키 없이 sample(10행)로 쓰세요',
    ],
  ],
  ['ERROR-100', [EcosValidationError, '통계표코드·주기·검색 시작/종료일자 같은 필수 값이 비었는지 확인하세요']],
  [
    'ERROR-101',
    [EcosValidationError, '날짜는 주기 형식을 따릅니다. A=2024, S=2024S1, Q=2024Q1, M=202401, SM=202401S1, D=20240101'],
  ],
  [
    'ERROR-200',
    [EcosValidationError, '요청 유형(json)이 경로에 없거나 잘못됐습니다. 클라이언트 경로 조립을 확인하세요'],
  ],
  ['ERROR-300', [EcosValidationError, ROW_RANGE_ACTION]],
  ['ERROR-301', [EcosValidationError, ROW_RANGE_ACTION]],
  ['ERROR-400', [EcosQueryTimeoutError, '기간을 나눠 여러 번 받거나 항목코드를 지정해 범위를 좁히세요']],
  ['ERROR-500', [EcosServerError, '서비스명을 확인하고, 맞다면 잠시 후 다시 시도하세요']],
  ['ERROR-600', [EcosServerError, 'ECOS 서버 DB 접속 오류입니다. 재시도 후에도 같으면 잠시 뒤 다시 시도하세요']],
  ['ERROR-601', [EcosServerError, '서버 SQL 오류입니다. 통계표·항목코드 조합을 확인하거나 잠시 뒤 다시 시도하세요']],
  [
    'ERROR-602',
    [
      EcosRateLimitError,
      '호출이 너무 많아 제한됐습니다. rateLimitRequestsPerSecond 를 낮추거나 잠시 뒤 다시 시도하세요',
    ],
  ],
]);

/** 일시적이라 같은 요청을 다시 보내 볼 만한 코드. ERROR-400(범위 과다)·601(SQL)은 다시 보내도 같다. */
const RETRYABLE_RESULT_CODES = new Set(['ERROR-600', 'ERROR-602']);

/** ERROR-301 은 건수 타입 오류·시작>끝·sample 10건 초과가 같은 코드라 메시지 꼬리로만 가른다. */
const SAMPLE_LIMIT_CODE = 'ERROR-301';
const SAMPLE_LIMIT_HINT = 'sample';

/** 본문 `RESULT.CODE` 를 예외로 바꾼다. 데이터 없음(INFO-200)은 호출 전에 걸러진다. */
const resultError = (
  code: string,
  message: string,
  responseData: unknown,
  requestContext: Record<string, unknown>,
): ApiError => {
  const common = { errorCode: code, responseData, requestContext };
  if (code === SAMPLE_LIMIT_CODE && message.includes(SAMPLE_LIMIT_HINT)) {
    return new EcosSampleLimitError(`ECOS [${code}] ${message} (조치: ${SAMPLE_LIMIT_ACTION})`, common);
  }
  const known = RESULT_CODE_ERRORS.get(code);
  if (!known) {
    return new EcosApiError(`ECOS [${code}] ${message || 'ECOS 오류'}`, common);
  }
  const [ErrorCls, hint] = known;
  return new ErrorCls(`ECOS [${code}] ${message || 'ECOS 오류'} (조치: ${hint})`, common);
};

const isEcosError = (error: unknown): boolean =>
  error instanceof EcosApiError ||
  error instanceof EcosAuthenticationError ||
  error instanceof EcosValidationError ||
  error instanceof EcosServerError ||
  error instanceof EcosRateLimitError ||
  error instanceof EcosTimeoutError ||
  error instanceof EcosNetworkError;

/** HTTP 단계 오류(BaseHttpClient)를 ECOS 예외로 바꾼다. 메시지에 섞인 키는 가린다. */
const toEcosError = (
  error: unknown,
  redact: (text: string) => string,
  requestContext: Record<string, unknown>,
): ApiError => {
  if (isEcosError(error)) {
    return error as ApiError;
  }
  if (!(error instanceof ApiError)) {
    return new EcosApiError(error instanceof Error ? redact(error.message) : 'Unknown ECOS client error', {
      requestContext,
    });
  }
  const message = redact(error.message);
  const details = { statusCode: error.statusCode, requestContext };
  if (error.statusCode === 404) return new EcosNotFoundError('ECOS 서비스를 찾을 수 없습니다 (HTTP 404)', details);
  if (error instanceof ApiValidationError) return new EcosValidationError(message, details);
  if (error instanceof ApiAuthenticationError) return new EcosAuthenticationError(message, details);
  if (error instanceof ApiRateLimitError) return new EcosRateLimitError(message, details);
  if (error instanceof ApiServerError) return new EcosServerError(message, details);
  if (error instanceof ApiTimeoutError) return new EcosTimeoutError(message, details);
  if (error instanceof ApiNetworkError) return new EcosNetworkError(message, details);
  return new EcosApiError(message, details);
};

const isRecord = (value: unknown): value is Record<string, unknown> =>
  value !== null && typeof value === 'object' && !Array.isArray(value);

/** 와이어 키 `STAT_CODE` → `statCode`. 공용 toCamelCase 는 대문자 키를 `sTATCode` 로 만들어 소문자로 먼저 내린다. */
export const camelizeEcosKeys = (row: Record<string, unknown>): Record<string, unknown> =>
  Object.fromEntries(Object.entries(row).map(([key, value]) => [toCamelCase(key.toLowerCase()), value]));

const encodeSegment = (value: string): string => {
  const text = String(value).trim();
  if (!text) {
    throw new RangeError('ECOS 요청 경로에 빈 값을 넣을 수 없습니다');
  }
  return encodeURIComponent(text);
};

interface WirePage {
  total: number;
  rows: unknown[];
  rowCount: number | null;
}

const EMPTY_PAGE: WirePage = { total: 0, rows: [], rowCount: null };

/**
 * 한국은행 ECOS(경제통계시스템) Open API 클라이언트.
 *
 * 인증키는 URL 경로에 들어간다. 그래서 예외·로그의 `requestContext` 에는 URL 대신 키를 가린 경로만 남긴다.
 * 오류도 HTTP 200 + 본문 `RESULT` 로 오므로 상태 코드가 아니라 본문으로 분기한다.
 */
export class EcosClient {
  public readonly authKey: string;
  public readonly maxPages: number;
  private readonly http: BaseHttpClient;
  private readonly maxRetries: number;
  private readonly logger: Logger;

  private statisticSearchInstance?: StatisticSearch;
  private statisticCatalogInstance?: StatisticCatalog;
  private statisticGlossaryInstance?: StatisticGlossary;

  public constructor(options: EcosClientOptions = {}) {
    this.authKey = options.authKey || SAMPLE;
    this.maxPages = options.maxPages ?? 100;
    this.maxRetries = options.maxRetries ?? 3;
    this.logger = options.logger ?? consoleLogger;
    this.http = new BaseHttpClient(
      {
        timeoutMs: options.timeoutMs ?? DEFAULT_TIMEOUT_MS,
        retry: { maxRetries: this.maxRetries, baseDelayMs: 300 },
        // Python 클라이언트 기본값과 동일: 초당 5건, 버스트 5건.
        rateLimit: {
          requestsPerSecond: options.rateLimitRequestsPerSecond ?? 5,
          burst: options.rateLimitBurst ?? 5,
        },
        debug: false,
      },
      options.fetchImpl,
    );
  }

  public get isSample(): boolean {
    return this.authKey === SAMPLE;
  }

  public get pageSize(): number {
    return this.isSample ? SAMPLE_PAGE_SIZE : PAGE_SIZE;
  }

  /** 통계 조회 (StatisticSearch) */
  public get statisticSearch(): StatisticSearch {
    if (!this.statisticSearchInstance) {
      this.statisticSearchInstance = new StatisticSearch(this);
    }
    return this.statisticSearchInstance;
  }

  /** 통계 목록 (StatisticTableList · StatisticItemList · KeyStatisticList) */
  public get statisticCatalog(): StatisticCatalog {
    if (!this.statisticCatalogInstance) {
      this.statisticCatalogInstance = new StatisticCatalog(this);
    }
    return this.statisticCatalogInstance;
  }

  /** 통계 용어·메타 (StatisticWord · StatisticMeta) */
  public get statisticGlossary(): StatisticGlossary {
    if (!this.statisticGlossaryInstance) {
      this.statisticGlossaryInstance = new StatisticGlossary(this);
    }
    return this.statisticGlossaryInstance;
  }

  /**
   * 서비스 하나를 불러 행을 `schema` 로 검증해 돌려준다. 도메인 클래스가 쓰는 공용 진입점.
   *
   * 행 범위를 주면 그 쪽만, 안 주면 `list_total_count` 를 다 채울 때까지 쪽 넘김한다.
   */
  public async getRows<Row>(
    service: string,
    segments: readonly string[],
    schema: z.ZodType<Row>,
    options: EcosPageOptions = {},
  ): Promise<EcosPage<Row>> {
    const lang = options.lang ?? 'kr';
    const page = await this.collect(service, segments, lang, options.startRow, options.endRow);
    const rows: Row[] = [];
    for (const raw of page.rows) {
      const parsed = schema.safeParse(isRecord(raw) ? camelizeEcosKeys(raw) : raw);
      if (!parsed.success) {
        throw new EcosApiError(`ECOS ${service} 응답 행이 명세와 다릅니다: ${parsed.error.message}`, {
          responseData: raw,
          requestContext: { method: 'GET', service },
        });
      }
      rows.push(parsed.data);
    }
    return { listTotalCount: page.total, rowCount: page.rowCount, rows };
  }

  private async collect(
    service: string,
    segments: readonly string[],
    lang: EcosLang,
    startRow: number | undefined,
    endRow: number | undefined,
  ): Promise<WirePage> {
    if (startRow !== undefined || endRow !== undefined) {
      const first = startRow ?? 1;
      return this.getPage(service, first, endRow ?? first + this.pageSize - 1, segments, lang);
    }

    const rows: unknown[] = [];
    let total = 0;
    for (let index = 0; index < this.maxPages; index += 1) {
      const first = index * this.pageSize + 1;
      const page = await this.getPage(service, first, first + this.pageSize - 1, segments, lang);
      total = page.total;
      rows.push(...page.rows);
      if (page.rows.length === 0 || rows.length >= total) {
        return { total, rows, rowCount: null };
      }
    }
    throw new EcosApiError(
      `쪽 넘김 상한(${this.maxPages}쪽 × ${this.pageSize}행)에 닿았습니다. 전체 ${total}행 중 ${rows.length}행만 받았습니다. ` +
        '기간·항목을 좁히거나 실키(ECOS_AUTH_KEY)를 쓰세요.',
      { requestContext: { method: 'GET', service } },
    );
  }

  /** 한 쪽을 받는다. 데이터 없음(INFO-200)은 빈 쪽, 일시 오류(600·602)는 재시도. */
  private async getPage(
    service: string,
    startRow: number,
    endRow: number,
    segments: readonly string[],
    lang: EcosLang,
  ): Promise<WirePage> {
    if (!Number.isInteger(startRow) || !Number.isInteger(endRow) || startRow < 1 || endRow < startRow) {
      throw new RangeError(`행 범위는 1 ≤ startRow ≤ endRow 정수여야 합니다. 받은 값: ${startRow}/${endRow}`);
    }
    const tail = [lang, String(startRow), String(endRow), ...segments.map(encodeSegment)].join('/');
    const url = `${ECOS_BASE_URL}/${service}/${encodeURIComponent(this.authKey)}/json/${tail}`;
    const requestContext = { method: 'GET', service, path: `/${service}/***/json/${tail}` };

    try {
      return await withRetry(
        () => this.fetchPage(service, url, requestContext),
        { maxRetries: this.maxRetries, baseDelayMs: 300 },
        (error) => error instanceof ApiError && RETRYABLE_RESULT_CODES.has(String(error.errorCode)),
      );
    } catch (error) {
      const mapped = toEcosError(error, (text) => this.redact(text), requestContext);
      this.logger.error('ECOS API request failed', {
        path: requestContext.path,
        message: mapped.message,
        ...(mapped.errorCode !== undefined ? { status: mapped.errorCode } : {}),
      });
      throw mapped;
    }
  }

  private async fetchPage(service: string, url: string, requestContext: Record<string, unknown>): Promise<WirePage> {
    let body: unknown;
    try {
      const response = await this.http.request({ method: 'GET', url, headers: { accept: 'application/json' } });
      body = await response.json();
    } catch (error) {
      throw toEcosError(error, (text) => this.redact(text), requestContext);
    }
    if (!isRecord(body)) {
      throw new EcosApiError('ECOS 응답이 JSON 객체가 아닙니다', { statusCode: 200, requestContext });
    }

    const result = body.RESULT;
    if (isRecord(result)) {
      const code = String(result.CODE ?? '');
      if (code === NO_DATA_CODE) {
        return EMPTY_PAGE;
      }
      throw resultError(code, String(result.MESSAGE ?? ''), body, requestContext);
    }

    const page = new Map(Object.entries(body)).get(service);
    if (!isRecord(page)) {
      throw new EcosApiError(`ECOS 응답에 '${service}' 블록이 없습니다`, { responseData: body, requestContext });
    }
    return {
      total: Number(page.list_total_count ?? 0),
      rows: Array.isArray(page.row) ? page.row : [],
      rowCount: typeof page.row_count === 'number' ? page.row_count : null,
    };
  }

  /** 오류 메시지에 키가 든 URL 이 섞여 오는 경우를 대비해 가린다. sample 은 비밀이 아니고 서버 메시지에도 나온다. */
  private redact(text: string): string {
    if (this.isSample) {
      return text;
    }
    return text.split(encodeURIComponent(this.authKey)).join('***').split(this.authKey).join('***');
  }
}
