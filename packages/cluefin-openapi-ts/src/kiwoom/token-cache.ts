import { createHash } from 'node:crypto';

import { writeJsonAtomic } from '../core/token-file.js';

export interface TokenCacheEntry {
  token: string;
  tokenType: string;
  expiresDt: string;
  cachedAt: string;
}

export interface TokenCacheStore {
  get(): Promise<TokenCacheEntry | null>;
  set(entry: TokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

/**
 * Build the env- and credential-scoped cache file name used by the Python TokenManager.
 *
 * 키움 토큰은 실전(prod)/모의(dev) 서버끼리, 그리고 서로 다른 app_key 끼리 호환되지
 * 않는다 (`8031` "투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다"). Python
 * `cluefin_openapi.kiwoom._token_manager.TokenManager._cache_file_name` 과 정확히
 * 동일한 포맷이어야 파이썬·TS 가 같은 캐시 파일을 공유한다 — 한쪽만 바꾸지 말 것.
 */
export const kiwoomTokenCacheFileName = (env?: string, appKey?: string): string => {
  const parts: string[] = [];
  if (env) parts.push(env);
  if (appKey) parts.push(createHash('sha256').update(appKey, 'utf-8').digest('hex').slice(0, 8));
  const suffix = parts.length > 0 ? `_${parts.join('_')}` : '';
  return `.kiwoom_token_cache${suffix}.json`;
};

export class MemoryTokenCacheStore implements TokenCacheStore {
  private cache: TokenCacheEntry | null = null;

  public async get(): Promise<TokenCacheEntry | null> {
    return this.cache;
  }

  public async set(entry: TokenCacheEntry): Promise<void> {
    this.cache = entry;
  }

  public async clear(): Promise<void> {
    this.cache = null;
  }
}

/**
 * File-based token cache store compatible with the Python TokenManager.
 *
 * `cluefin_openapi.kiwoom._token_manager` 와 동일한 JSON 포맷을 읽고 쓴다:
 * `{"token": {"expires_dt": <ISO8601>, "token_type": ..., "token": <plain>}, "cached_at": <ISO8601>}`.
 * 포맷을 바꾸면 파이썬과 캐시 파일을 공유할 수 없다.
 */
export class FileTokenCacheStore implements TokenCacheStore {
  private readonly filePath: string;

  public constructor(filePath: string) {
    this.filePath = filePath;
  }

  public async get(): Promise<TokenCacheEntry | null> {
    try {
      const fs = await import('node:fs/promises');
      const raw = await fs.readFile(this.filePath, 'utf-8');
      const data = JSON.parse(raw) as {
        token?: {
          token?: string;
          token_type?: string;
          expires_dt?: string;
        };
        cached_at?: string;
      };
      const t = data.token;
      if (!t || !t.token || !t.expires_dt) return null;
      return {
        token: t.token,
        tokenType: t.token_type ?? 'bearer',
        expiresDt: t.expires_dt,
        cachedAt: data.cached_at ?? new Date().toISOString(),
      };
    } catch {
      return null;
    }
  }

  public async set(entry: TokenCacheEntry): Promise<void> {
    const data = {
      token: {
        expires_dt: entry.expiresDt,
        token_type: entry.tokenType,
        token: entry.token,
      },
      cached_at: entry.cachedAt,
    };
    await writeJsonAtomic(this.filePath, data);
  }

  public async clear(): Promise<void> {
    try {
      const fs = await import('node:fs/promises');
      await fs.unlink(this.filePath);
    } catch {
      // Ignore if file doesn't exist
    }
  }
}
