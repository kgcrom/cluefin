import type { z } from 'zod';

export type ApiEnv = 'dev' | 'prod';

type CamelCase<S extends string> = S extends `${infer P}_${infer Q}${infer R}`
  ? `${P}${Uppercase<Q>}${CamelCase<R>}`
  : S;

// 런타임 `toCamelCase` 는 변환 후 첫 글자를 낮춘다(`Output_0` → `output0`). 타입 쪽도
// `Uncapitalize` 로 같은 규칙을 적용해야 한다 — 와이어 키가 대문자로 시작하는 NH PLUG
// 봉투에서만 드러나는 차이이고, 소문자 snake_case 를 쓰는 KIS·키움에는 영향이 없다.
export type CamelizeKeys<T> = T extends (infer U)[]
  ? CamelizeKeys<U>[]
  : T extends Record<string, unknown>
    ? { [K in keyof T as K extends string ? Uncapitalize<CamelCase<K>> : K]: CamelizeKeys<T[K]> }
    : T;

export interface ApiResponse<TBody = Record<string, unknown>> {
  headers: Record<string, string>;
  body: TBody;
}

export interface RateLimitOptions {
  requestsPerSecond: number;
  burst: number;
}

export interface RetryOptions {
  maxRetries: number;
  baseDelayMs: number;
}

export type JsonValue = string | number | boolean | null | JsonObject | JsonArray;

export interface JsonObject {
  [key: string]: JsonValue;
}

export type JsonArray = JsonValue[];

export interface EndpointParamDefinition {
  name: string;
  required: boolean;
  defaultValue?: string | number | boolean | undefined;
}

export interface EndpointBaseDefinition {
  methodName: string;
  params: EndpointParamDefinition[];
}

export interface KisEndpointDefinition extends EndpointBaseDefinition {
  path: string;
  trId?: string | undefined;
  requestMap: Record<string, string>;
  method: 'GET' | 'POST';
}

export interface KiwoomEndpointDefinition extends EndpointBaseDefinition {
  path: string;
  apiId: string;
  bodyMap: Record<string, string>;
  headerParamMap: Record<string, string>;
  responseSchema?: z.ZodTypeAny;
}

export interface NhplugEndpointDefinition extends EndpointBaseDefinition {
  path: string;
  bodyMap: Record<string, string>;
  /** 연속조회(페이지네이션) 지원 여부. true 인 경우에만 `cts`/`cts_flag` 요청 헤더를 붙인다. */
  supportsCts: boolean;
  responseSchema?: z.ZodTypeAny;
}

export interface HttpClientOptions {
  timeoutMs: number;
  retry: RetryOptions;
  rateLimit: RateLimitOptions;
  debug: boolean;
}

export interface HttpRequestOptions {
  method: 'GET' | 'POST';
  url: string;
  headers: Record<string, string>;
  query?: Record<string, string> | undefined;
  body?: Record<string, unknown> | undefined;
}

export type DomainMethods<T extends string, TResponseMap extends Partial<Record<T, unknown>> = Record<T, never>> = {
  [K in T]: (
    input: Record<string, unknown>,
  ) => Promise<ApiResponse<K extends keyof TResponseMap ? TResponseMap[K] : Record<string, unknown>>>;
};

export type FetchLike = typeof fetch;
