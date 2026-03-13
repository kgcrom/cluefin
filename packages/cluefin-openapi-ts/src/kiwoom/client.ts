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
import { DomesticAccount } from './domestic-account';
import { DomesticChart } from './domestic-chart';
import { DomesticETF } from './domestic-etf';
import { DomesticForeign } from './domestic-foreign';
import { DomesticMarketCondition } from './domestic-market-condition';
import { DomesticOrder } from './domestic-order';
import { DomesticRankInfo } from './domestic-rank-info';
import { DomesticSector } from './domestic-sector';
import { DomesticStockInfo } from './domestic-stock-info';
import { DomesticTheme } from './domestic-theme';

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

  private domesticAccountInstance?: DomesticAccount;
  private domesticChartInstance?: DomesticChart;
  private domesticEtfInstance?: DomesticETF;
  private domesticForeignInstance?: DomesticForeign;
  private domesticMarketConditionInstance?: DomesticMarketCondition;
  private domesticOrderInstance?: DomesticOrder;
  private domesticRankInfoInstance?: DomesticRankInfo;
  private domesticSectorInstance?: DomesticSector;
  private domesticStockInfoInstance?: DomesticStockInfo;
  private domesticThemeInstance?: DomesticTheme;

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

  public get domesticAccount(): DomesticAccount {
    if (!this.domesticAccountInstance) {
      this.domesticAccountInstance = new DomesticAccount(this);
    }
    return this.domesticAccountInstance;
  }

  public get domesticChart(): DomesticChart {
    if (!this.domesticChartInstance) {
      this.domesticChartInstance = new DomesticChart(this);
    }
    return this.domesticChartInstance;
  }

  public get domesticEtf(): DomesticETF {
    if (!this.domesticEtfInstance) {
      this.domesticEtfInstance = new DomesticETF(this);
    }
    return this.domesticEtfInstance;
  }

  public get domesticForeign(): DomesticForeign {
    if (!this.domesticForeignInstance) {
      this.domesticForeignInstance = new DomesticForeign(this);
    }
    return this.domesticForeignInstance;
  }

  public get domesticMarketCondition(): DomesticMarketCondition {
    if (!this.domesticMarketConditionInstance) {
      this.domesticMarketConditionInstance = new DomesticMarketCondition(this);
    }
    return this.domesticMarketConditionInstance;
  }

  public get domesticOrder(): DomesticOrder {
    if (!this.domesticOrderInstance) {
      this.domesticOrderInstance = new DomesticOrder(this);
    }
    return this.domesticOrderInstance;
  }

  public get domesticRankInfo(): DomesticRankInfo {
    if (!this.domesticRankInfoInstance) {
      this.domesticRankInfoInstance = new DomesticRankInfo(this);
    }
    return this.domesticRankInfoInstance;
  }

  public get domesticSector(): DomesticSector {
    if (!this.domesticSectorInstance) {
      this.domesticSectorInstance = new DomesticSector(this);
    }
    return this.domesticSectorInstance;
  }

  public get domesticStockInfo(): DomesticStockInfo {
    if (!this.domesticStockInfoInstance) {
      this.domesticStockInfoInstance = new DomesticStockInfo(this);
    }
    return this.domesticStockInfoInstance;
  }

  public get domesticTheme(): DomesticTheme {
    if (!this.domesticThemeInstance) {
      this.domesticThemeInstance = new DomesticTheme(this);
    }
    return this.domesticThemeInstance;
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
      if (definition.responseSchema) {
        definition.responseSchema.parse(rawJson);
      }

      return {
        headers: normalizeHeaders(response.headers),
        body: camelizeKeys(rawJson),
      };
    } catch (error) {
      return mapKiwoomError(error);
    }
  }
}
