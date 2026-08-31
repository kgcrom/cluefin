import { z } from 'zod';
import {
  NhplugApiError,
  NhplugAuthenticationError,
  NhplugNetworkError,
  NhplugServerError,
  NhplugValidationError,
} from '../core/errors.js';
import { MemoryTokenCacheStore, type TokenCacheEntry, type TokenCacheStore } from './token-cache.js';

const tokenResponseSchema = z.object({
  access_token: z.string(),
  scope: z.string(),
  token_type: z.string(),
  expires_in: z.union([z.string(), z.number()]),
});

const tokenRevokeResponseSchema = z
  .object({
    code: z.union([z.string(), z.number()]).optional(),
    message: z.string().optional(),
    error_code: z.string().optional(),
    error_description: z.string().optional(),
  })
  .passthrough();

// 접근토큰 발급/폐기는 운영 도메인 전용(모의투자 미제공). 발급받은 토큰은
// 운영·모의투자 호출 모두에 사용하므로 NhplugAuth 는 env 를 받지 않는다.
export const NHPLUG_AUTH_BASE_URL = 'https://api.nhplug.com:8443';

export interface NhplugAuthOptions {
  appKey: string;
  secretKey: string;
  tokenCacheStore?: TokenCacheStore;
  fetchImpl?: typeof fetch;
}

export interface NhplugTokenResponse {
  accessToken: string;
  scope: string;
  tokenType: string;
  expiresIn: number;
}

export interface NhplugTokenRevokeResponse {
  code?: string | number | undefined;
  message?: string | undefined;
  errorCode?: string | undefined;
  errorDescription?: string | undefined;
}

const nowIso = (): string => new Date().toISOString();

// 캐시 만료 버퍼 1시간. 토큰 응답에 절대 만료시각이 없으므로 cachedAt + expiresIn 으로 계산한다.
const EXPIRY_BUFFER_MS = 60 * 60 * 1000;

const isTokenValid = (entry: TokenCacheEntry): boolean => {
  const cachedAt = new Date(entry.cachedAt).getTime();
  if (Number.isNaN(cachedAt)) {
    return false;
  }
  const expiry = cachedAt + entry.expiresIn * 1000;
  return Date.now() < expiry - EXPIRY_BUFFER_MS;
};

const formEncode = (data: Record<string, string>): string => new URLSearchParams(data).toString();

export class NhplugAuth {
  private readonly tokenCacheStore: TokenCacheStore;
  private readonly fetchImpl: typeof fetch;

  public constructor(private readonly options: NhplugAuthOptions) {
    this.tokenCacheStore = options.tokenCacheStore ?? new MemoryTokenCacheStore();
    this.fetchImpl = options.fetchImpl ?? globalThis.fetch;
  }

  /**
   * Get a cached token, or issue a new one when it is missing/expiring.
   *
   * 접근토큰발급은 서버에서 초당 1회로 제한되며 불필요한 재발급은 계좌 보안 알림을
   * 유발한다 — 캐시 경로를 우회하지 말 것.
   */
  public async generate(): Promise<NhplugTokenResponse> {
    const cached = await this.tokenCacheStore.get();
    if (cached && isTokenValid(cached)) {
      return {
        accessToken: cached.accessToken,
        scope: cached.scope,
        tokenType: cached.tokenType,
        expiresIn: cached.expiresIn,
      };
    }

    const response = await this.fetchImpl(`${NHPLUG_AUTH_BASE_URL}/oauth2/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formEncode({
        appkey: this.options.appKey,
        appsecretkey: this.options.secretKey,
        grant_type: 'client_credentials',
        scope: 'oob',
      }),
    });

    if (response.status === 400) {
      throw new NhplugValidationError('Invalid token request');
    }
    if (response.status === 401) {
      throw new NhplugAuthenticationError('Authentication failed while requesting token');
    }
    if (response.status >= 500) {
      throw new NhplugServerError('NH PLUG token server error');
    }
    if (!response.ok) {
      const body = await response.text().catch(() => '(unable to read body)');
      throw new NhplugApiError(`Unexpected token response status ${response.status}: ${body}`);
    }

    let payload: unknown;
    try {
      payload = await response.json();
    } catch (error) {
      throw new NhplugNetworkError(error instanceof Error ? error.message : 'Failed to parse token response');
    }

    const parsed = tokenResponseSchema.parse(payload);
    const token: NhplugTokenResponse = {
      accessToken: parsed.access_token,
      scope: parsed.scope,
      tokenType: parsed.token_type,
      expiresIn: Number(parsed.expires_in),
    };
    await this.tokenCacheStore.set({ ...token, cachedAt: nowIso() });
    return token;
  }

  /**
   * Revoke an access token (`POST /oauth2/revoke`).
   *
   * `token` 을 생략하면 캐시에 있는 토큰을 폐기하고 캐시도 함께 비운다.
   */
  public async revoke(
    token?: string,
    tokenTypeHint: 'access_token' | 'refresh_token' = 'access_token',
  ): Promise<NhplugTokenRevokeResponse> {
    const cached = await this.tokenCacheStore.get();
    const targetToken = token ?? cached?.accessToken;
    if (!targetToken) {
      throw new NhplugApiError('Cannot revoke token before generate() is called');
    }

    const response = await this.fetchImpl(`${NHPLUG_AUTH_BASE_URL}/oauth2/revoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formEncode({
        token: targetToken,
        token_type_hint: tokenTypeHint,
        appkey: this.options.appKey,
        appsecretkey: this.options.secretKey,
      }),
    });

    if (!response.ok) {
      throw new NhplugApiError(`Failed to revoke token (status ${response.status})`);
    }

    const parsed = tokenRevokeResponseSchema.parse(await response.json());

    // 폐기된 토큰이 캐시에 남아 재사용되지 않도록 정리
    if (cached?.accessToken === targetToken) {
      await this.tokenCacheStore.clear();
    }

    return {
      code: parsed.code,
      message: parsed.message,
      errorCode: parsed.error_code,
      errorDescription: parsed.error_description,
    };
  }
}
