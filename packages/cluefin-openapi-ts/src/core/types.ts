import type { z } from 'zod';

export type ApiEnv = 'dev' | 'prod';

type CamelCase<S extends string> = S extends `${infer P}_${infer Q}${infer R}`
  ? `${P}${Uppercase<Q>}${CamelCase<R>}`
  : S;

export type CamelizeKeys<T> = T extends (infer U)[]
  ? CamelizeKeys<U>[]
  : T extends Record<string, unknown>
    ? { [K in keyof T as K extends string ? CamelCase<K> : K]: CamelizeKeys<T[K]> }
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
