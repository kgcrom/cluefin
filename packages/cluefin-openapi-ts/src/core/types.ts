export type ApiEnv = 'dev' | 'prod';

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
  defaultValue?: string | number | boolean;
}

export interface EndpointBaseDefinition {
  methodName: string;
  params: EndpointParamDefinition[];
}

export interface KisEndpointDefinition extends EndpointBaseDefinition {
  path: string;
  trId: string;
  requestMap: Record<string, string>;
  method: 'GET' | 'POST';
}

export interface KiwoomEndpointDefinition extends EndpointBaseDefinition {
  path: string;
  apiId: string;
  bodyMap: Record<string, string>;
  headerParamMap: Record<string, string>;
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
  query?: Record<string, string>;
  body?: Record<string, unknown>;
}

export type FetchLike = typeof fetch;
