import { camelizeKeys } from '../core/case-convert.js';
import { KiwoomApiError, KiwoomAuthenticationError, KiwoomServerError, KiwoomValidationError } from '../core/errors.js';
import type { ApiEnv } from '../core/types.js';
import { MemoryTokenCacheStore, type TokenCacheEntry, type TokenCacheStore } from './token-cache.js';

export interface KiwoomAuthOptions {
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  tokenCacheStore?: TokenCacheStore;
  fetchImpl?: typeof fetch;
}

export interface KiwoomTokenResponse {
  tokenType: string;
  token: string;
  expiresDt: string;
}

const getBaseUrl = (env: ApiEnv): string => (env === 'prod' ? 'https://api.kiwoom.com' : 'https://mockapi.kiwoom.com');

// Python `TokenManager.EXPIRY_BUFFER` / `MAX_CACHE_AGE` — keep both sides in sync by hand.
const EXPIRY_BUFFER_MS = 60 * 60 * 1000;
const MAX_CACHE_AGE_MS = 6 * 60 * 60 * 1000;

const nowIso = (): string => new Date().toISOString();

/** Kiwoom wire format ("YYYYMMDDHHMMSS") -> the ISO string Python's `TokenResponse.model_dump(mode="json")`
 * writes to the cache file. Left untouched for anything already ISO-shaped (e.g. a value re-read from cache). */
const toIsoExpiresDt = (raw: string): string => {
  if (!/^\d{14}$/.test(raw)) return raw;
  const y = raw.slice(0, 4);
  const mo = raw.slice(4, 6);
  const d = raw.slice(6, 8);
  const h = raw.slice(8, 10);
  const mi = raw.slice(10, 12);
  const s = raw.slice(12, 14);
  return `${y}-${mo}-${d}T${h}:${mi}:${s}`;
};

/** Mirrors Python `TokenManager._is_token_valid`: cache age <= 6h AND now < expiry - 1h buffer. */
const isCacheValid = (entry: TokenCacheEntry): boolean => {
  const cachedAt = new Date(entry.cachedAt).getTime();
  if (!Number.isNaN(cachedAt) && Date.now() - cachedAt > MAX_CACHE_AGE_MS) {
    return false;
  }
  const expiry = new Date(entry.expiresDt).getTime();
  if (Number.isNaN(expiry)) {
    return false;
  }
  return Date.now() < expiry - EXPIRY_BUFFER_MS;
};

export class KiwoomAuth {
  private readonly baseUrl: string;
  private readonly tokenCacheStore: TokenCacheStore;
  private readonly fetchImpl: typeof fetch;

  public constructor(private readonly options: KiwoomAuthOptions) {
    const env = options.env ?? 'dev';
    this.baseUrl = getBaseUrl(env);
    this.tokenCacheStore = options.tokenCacheStore ?? new MemoryTokenCacheStore();
    this.fetchImpl = options.fetchImpl ?? globalThis.fetch;
  }

  public async generateToken(): Promise<KiwoomTokenResponse> {
    const cached = await this.tokenCacheStore.get();
    if (cached && isCacheValid(cached)) {
      return {
        token: cached.token,
        tokenType: cached.tokenType,
        expiresDt: cached.expiresDt,
      };
    }

    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/token`, {
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

    if (response.status === 400) {
      throw new KiwoomValidationError('Invalid token request');
    }
    if (response.status === 401) {
      throw new KiwoomAuthenticationError('Kiwoom authentication failed');
    }
    if (response.status >= 500) {
      throw new KiwoomServerError('Kiwoom token server error');
    }
    if (!response.ok) {
      throw new KiwoomApiError(`Unexpected token response status ${response.status}`);
    }

    const token = camelizeKeys(await response.json()) as KiwoomTokenResponse;
    // Kiwoom can answer HTTP 200 with a failing body (no token) — never cache that.
    if (!token.token || !token.expiresDt) {
      throw new KiwoomAuthenticationError('Kiwoom token response is missing token or expires_dt');
    }
    await this.tokenCacheStore.set({
      token: token.token,
      tokenType: token.tokenType,
      expiresDt: toIsoExpiresDt(token.expiresDt),
      cachedAt: nowIso(),
    });
    return token;
  }

  public async revokeToken(token: string): Promise<boolean> {
    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/revoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify({
        appkey: this.options.appKey,
        secretkey: this.options.secretKey,
        token,
      }),
    });

    if (!response.ok) {
      throw new KiwoomApiError(`Failed to revoke token (status ${response.status})`);
    }

    return true;
  }
}
