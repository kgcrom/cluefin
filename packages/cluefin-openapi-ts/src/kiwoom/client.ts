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
  KiwoomApiError,
  KiwoomAuthenticationError,
  KiwoomAuthorizationError,
  KiwoomNetworkError,
  KiwoomRateLimitError,
  KiwoomServerError,
  KiwoomTimeoutError,
  KiwoomValidationError,
} from '../core/errors';
import { BaseHttpClient } from '../core/http';
import type { ApiEnv, ApiResponse, KiwoomEndpointDefinition } from '../core/types';
import { createInputSchema, kiwoomEnvelopeSchema } from '../core/validation';
import { DomesticChart } from './domestic-chart';
import { DomesticRankInfo } from './domestic-rank-info';
import { DomesticStockInfo } from './domestic-stock-info';

export interface KiwoomClientOptions {
  token: string;
  env?: ApiEnv;
  debug?: boolean;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  fetchImpl?: typeof fetch;
}

const getBaseUrl = (env: ApiEnv): string => (env === 'prod' ? 'https://api.kiwoom.com' : 'https://mockapi.kiwoom.com');

const stringifyParam = (value: unknown): string => (typeof value === 'string' ? value : String(value));

const mapKiwoomError = (error: unknown): never => {
  if (error instanceof KiwoomApiError) {
    throw error;
  }
  if (error instanceof ApiValidationError) {
    throw new KiwoomValidationError(error.message, error);
  }
  if (error instanceof ApiAuthenticationError) {
    throw new KiwoomAuthenticationError(error.message, error);
  }
  if (error instanceof ApiAuthorizationError) {
    throw new KiwoomAuthorizationError(error.message, error);
  }
  if (error instanceof ApiRateLimitError) {
    throw new KiwoomRateLimitError(error.message, error);
  }
  if (error instanceof ApiServerError) {
    throw new KiwoomServerError(error.message, error);
  }
  if (error instanceof ApiTimeoutError) {
    throw new KiwoomTimeoutError(error.message, error);
  }
  if (error instanceof ApiNetworkError) {
    throw new KiwoomNetworkError(error.message, error);
  }
  if (error instanceof ApiError) {
    throw new KiwoomApiError(error.message, error);
  }
  throw new KiwoomApiError(error instanceof Error ? error.message : 'Unknown Kiwoom client error');
};

export class KiwoomClient {
  private readonly baseUrl: string;
  private readonly http: BaseHttpClient;
  private readonly token: string;

  private domesticChartInstance?: DomesticChart;
  private domesticStockInfoInstance?: DomesticStockInfo;
  private domesticRankInfoInstance?: DomesticRankInfo;

  public constructor(options: KiwoomClientOptions) {
    const env = options.env ?? 'dev';
    this.baseUrl = getBaseUrl(env);
    this.token = options.token;
    this.http = new BaseHttpClient(
      {
        timeoutMs: options.timeoutMs ?? 30_000,
        retry: {
          maxRetries: options.maxRetries ?? 3,
          baseDelayMs: 300,
        },
        rateLimit: {
          requestsPerSecond: options.rateLimitRequestsPerSecond ?? 2,
          burst: options.rateLimitBurst ?? 1,
        },
        debug: options.debug ?? false,
      },
      options.fetchImpl,
    );
  }

  public get domesticChart(): DomesticChart {
    if (!this.domesticChartInstance) {
      this.domesticChartInstance = new DomesticChart(this);
    }
    return this.domesticChartInstance;
  }

  public get domesticStockInfo(): DomesticStockInfo {
    if (!this.domesticStockInfoInstance) {
      this.domesticStockInfoInstance = new DomesticStockInfo(this);
    }
    return this.domesticStockInfoInstance;
  }

  public get domesticRankInfo(): DomesticRankInfo {
    if (!this.domesticRankInfoInstance) {
      this.domesticRankInfoInstance = new DomesticRankInfo(this);
    }
    return this.domesticRankInfoInstance;
  }

  public async invokeEndpoint(
    definition: KiwoomEndpointDefinition,
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

      const continuationHeaders = Object.fromEntries(
        Object.entries(definition.headerParamMap)
          .map(([headerName, inputKey]) => {
            const value = parsedInput[inputKey];
            if (value === undefined || value === null) {
              return null;
            }
            return [headerName, stringifyParam(value)];
          })
          .filter((entry): entry is [string, string] => entry !== null),
      );

      const response = await this.http.request({
        method: 'POST',
        url: `${this.baseUrl}${definition.path}`,
        headers: {
          'content-type': 'application/json',
          accept: 'application/json',
          authorization: `Bearer ${this.token}`,
          'api-id': definition.apiId,
          ...continuationHeaders,
        },
        body,
      });

      const rawJson = await response.json();
      kiwoomEnvelopeSchema.parse(rawJson);

      return {
        headers: normalizeHeaders(response.headers),
        body: camelizeKeys(rawJson),
      };
    } catch (error) {
      mapKiwoomError(error);
    }
  }
}
