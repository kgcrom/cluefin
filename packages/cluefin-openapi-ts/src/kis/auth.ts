import { z } from 'zod';
import { camelizeKeys } from '../core/case-convert';
import {
  KisApiError,
  KisAuthenticationError,
  KisNetworkError,
  KisServerError,
  KisValidationError,
} from '../core/errors';
import type { ApiEnv } from '../core/types';
import { MemoryTokenCacheStore, type TokenCacheEntry, type TokenCacheStore } from './token-cache';

const tokenResponseSchema = z.object({
  access_token: z.string(),
  token_type: z.string(),
  expires_in: z.union([z.string(), z.number()]),
  access_token_token_expired: z.string(),
});

const approvalResponseSchema = z.object({
  approval_key: z.string(),
});

export interface KisAuthOptions {
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  tokenCacheStore?: TokenCacheStore;
  fetchImpl?: typeof fetch;
}

export interface KisTokenResponse {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
  accessTokenTokenExpired: string;
}

export interface KisApprovalResponse {
  approvalKey: string;
}

const getBaseUrl = (env: ApiEnv): string =>
  env === 'prod' ? 'https://openapi.koreainvestment.com:9443' : 'https://openapivts.koreainvestment.com:29443';

const nowIso = (): string => new Date().toISOString();

const isTokenValid = (entry: TokenCacheEntry): boolean => {
  const expiry = new Date(entry.accessTokenTokenExpired).getTime();
  if (Number.isNaN(expiry)) {
    return false;
  }
  const oneHourBufferMs = 60 * 60 * 1000;
  return Date.now() < expiry - oneHourBufferMs;
};

const toTokenEntry = (input: KisTokenResponse): TokenCacheEntry => ({
  accessToken: input.accessToken,
  tokenType: input.tokenType,
  expiresIn: input.expiresIn,
  accessTokenTokenExpired: input.accessTokenTokenExpired,
  cachedAt: nowIso(),
});

export class KisAuth {
  private readonly baseUrl: string;
  private readonly tokenCacheStore: TokenCacheStore;
  private readonly fetchImpl: typeof fetch;

  public constructor(private readonly options: KisAuthOptions) {
    const env = options.env ?? 'dev';
    this.baseUrl = getBaseUrl(env);
    this.tokenCacheStore = options.tokenCacheStore ?? new MemoryTokenCacheStore();
    this.fetchImpl = options.fetchImpl ?? globalThis.fetch;
  }

  public async generate(): Promise<KisTokenResponse> {
    const cached = await this.tokenCacheStore.get();
    if (cached && isTokenValid(cached)) {
      return {
        accessToken: cached.accessToken,
        tokenType: cached.tokenType,
        expiresIn: cached.expiresIn,
        accessTokenTokenExpired: cached.accessTokenTokenExpired,
      };
    }

    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/tokenP`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify({
        grant_type: 'client_credentials',
        appkey: this.options.appKey,
        appsecret: this.options.secretKey,
      }),
    });

    if (response.status === 400) {
      throw new KisValidationError('Invalid token request');
    }
    if (response.status === 401) {
      throw new KisAuthenticationError('Authentication failed while requesting token');
    }
    if (response.status >= 500) {
      throw new KisServerError('KIS token server error');
    }
    if (!response.ok) {
      throw new KisApiError(`Unexpected token response status ${response.status}`);
    }

    let payload: unknown;
    try {
      payload = await response.json();
    } catch (error) {
      throw new KisNetworkError(error instanceof Error ? error.message : 'Failed to parse token response');
    }

    const parsed = tokenResponseSchema.parse(payload);
    const token: KisTokenResponse = {
      accessToken: parsed.access_token,
      tokenType: parsed.token_type,
      expiresIn: Number(parsed.expires_in),
      accessTokenTokenExpired: parsed.access_token_token_expired,
    };
    await this.tokenCacheStore.set(toTokenEntry(token));
    return token;
  }

  public async revoke(token?: string): Promise<boolean> {
    const cached = await this.tokenCacheStore.get();
    const targetToken = token ?? cached?.accessToken;
    if (!targetToken) {
      throw new KisApiError('Cannot revoke token before generate() is called');
    }

    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/revokeP`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify({
        appkey: this.options.appKey,
        appsecret: this.options.secretKey,
        token: targetToken,
      }),
    });

    if (!response.ok) {
      throw new KisApiError(`Failed to revoke token (status ${response.status})`);
    }

    await this.tokenCacheStore.clear();
    return true;
  }

  public async approve(): Promise<KisApprovalResponse> {
    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/Approval`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify({
        grant_type: 'client_credentials',
        appkey: this.options.appKey,
        secretkey: this.options.secretKey,
      }),
    });

    if (!response.ok) {
      throw new KisApiError(`Failed to request approval key (status ${response.status})`);
    }

    const payload = approvalResponseSchema.parse(await response.json());
    return camelizeKeys(payload);
  }
}
