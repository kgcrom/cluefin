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
  KisApiError,
  KisAuthenticationError,
  KisAuthorizationError,
  KisNetworkError,
  KisRateLimitError,
  KisServerError,
  KisTimeoutError,
  KisValidationError,
} from '../core/errors';
import { BaseHttpClient } from '../core/http';
import type { ApiEnv, ApiResponse, KisEndpointDefinition } from '../core/types';
import { createInputSchema, kisEnvelopeSchema } from '../core/validation';
import { DomesticBasicQuote } from './domestic-basic-quote';
import { DomesticStockInfo } from './domestic-stock-info';

export interface KisHttpClientOptions {
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
}

const getBaseUrl = (env: ApiEnv): string =>
  env === 'prod' ? 'https://openapi.koreainvestment.com:9443' : 'https://openapivts.koreainvestment.com:29443';

const stringifyParam = (value: unknown): string => (typeof value === 'string' ? value : String(value));

const mapKisError = (error: unknown): never => {
  if (error instanceof KisApiError) {
    throw error;
  }
  if (error instanceof ApiValidationError) {
    throw new KisValidationError(error.message, error);
  }
  if (error instanceof ApiAuthenticationError) {
    throw new KisAuthenticationError(error.message, error);
  }
  if (error instanceof ApiAuthorizationError) {
    throw new KisAuthorizationError(error.message, error);
  }
  if (error instanceof ApiRateLimitError) {
    throw new KisRateLimitError(error.message, error);
  }
  if (error instanceof ApiServerError) {
    throw new KisServerError(error.message, error);
  }
  if (error instanceof ApiTimeoutError) {
    throw new KisTimeoutError(error.message, error);
  }
  if (error instanceof ApiNetworkError) {
    throw new KisNetworkError(error.message, error);
  }
  if (error instanceof ApiError) {
    throw new KisApiError(error.message, error);
  }
  throw new KisApiError(error instanceof Error ? error.message : 'Unknown KIS client error');
};

export class KisHttpClient {
  private readonly baseUrl: string;
  private readonly http: BaseHttpClient;
  private readonly token: string;
  private readonly appKey: string;
  private readonly secretKey: string;

  private domesticBasicQuoteInstance?: DomesticBasicQuote;
  private domesticStockInfoInstance?: DomesticStockInfo;

  public constructor(options: KisHttpClientOptions) {
    const env = options.env ?? 'prod';
    this.baseUrl = getBaseUrl(env);
    this.token = options.token;
    this.appKey = options.appKey;
    this.secretKey = options.secretKey;
    this.http = new BaseHttpClient(
      {
        timeoutMs: options.timeoutMs ?? 30_000,
        retry: {
          maxRetries: options.maxRetries ?? 3,
          baseDelayMs: 250,
        },
        rateLimit: {
          requestsPerSecond: options.rateLimitRequestsPerSecond ?? 10,
          burst: options.rateLimitBurst ?? 2,
        },
        debug: options.debug ?? false,
      },
      options.fetchImpl,
    );
  }

  public get domesticBasicQuote(): DomesticBasicQuote {
    if (!this.domesticBasicQuoteInstance) {
      this.domesticBasicQuoteInstance = new DomesticBasicQuote(this);
    }
    return this.domesticBasicQuoteInstance;
  }

  public get domesticStockInfo(): DomesticStockInfo {
    if (!this.domesticStockInfoInstance) {
      this.domesticStockInfoInstance = new DomesticStockInfo(this);
    }
    return this.domesticStockInfoInstance;
  }

  public async invokeEndpoint(definition: KisEndpointDefinition, input: Record<string, unknown>): Promise<ApiResponse> {
    try {
      const parsedInput = createInputSchema(definition.params).parse(input);
      const mappedRequest = Object.fromEntries(
        Object.entries(definition.requestMap)
          .map(([apiKey, inputKey]) => {
            const value = parsedInput[inputKey];
            if (value === undefined || value === null) {
              return null;
            }
            return [apiKey, stringifyParam(value)];
          })
          .filter((entry): entry is [string, string] => entry !== null),
      );

      const response = await this.http.request({
        method: definition.method,
        url: `${this.baseUrl}${definition.path}`,
        headers: {
          'content-type': 'application/json;charset=UTF-8',
          accept: 'application/json',
          authorization: `Bearer ${this.token}`,
          appkey: this.appKey,
          appsecret: this.secretKey,
          custtype: 'P',
          tr_id: definition.trId,
        },
        query: definition.method === 'GET' ? mappedRequest : undefined,
        body: definition.method === 'POST' ? mappedRequest : undefined,
      });

      const rawJson = await response.json();
      kisEnvelopeSchema.parse(rawJson);

      return {
        headers: normalizeHeaders(response.headers),
        body: camelizeKeys(rawJson),
      };
    } catch (error) {
      mapKisError(error);
    }
  }
}
