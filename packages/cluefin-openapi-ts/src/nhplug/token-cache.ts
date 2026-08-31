import { createHash } from 'node:crypto';

export interface TokenCacheEntry {
  accessToken: string;
  scope: string;
  tokenType: string;
  expiresIn: number;
  cachedAt: string;
}

export interface TokenCacheStore {
  get(): Promise<TokenCacheEntry | null>;
  set(entry: TokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

/**
 * Build the credential-scoped cache file name used by the Python TokenManager.
 *
 * NH PLUG 토큰은 운영 도메인에서만 발급되고 운영·모의투자 호출에 공유되므로
 * 캐시는 env 가 아니라 app_key 로만 구분한다 (`_token_manager._cache_file_name`).
 */
export const nhplugTokenCacheFileName = (appKey?: string): string => {
  const suffix = appKey ? `_${createHash('sha256').update(appKey, 'utf-8').digest('hex').slice(0, 8)}` : '';
  return `.nhplug_token_cache${suffix}.json`;
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
 * `cluefin_openapi.nhplug._token_manager` 와 동일한 JSON 포맷(snake_case)을 읽고 쓴다.
 * 토큰 응답에는 절대 만료시각 필드가 없으므로, 만료는 `cached_at + expires_in` 으로
 * 계산한다 — 파이썬과 TS 가 같은 캐시 파일을 공유할 수 있도록 포맷을 바꾸지 말 것.
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
          access_token?: string;
          scope?: string;
          token_type?: string;
          expires_in?: number;
        };
        cached_at?: string;
      };
      const t = data.token;
      if (!t?.access_token) return null;
      return {
        accessToken: t.access_token,
        scope: t.scope ?? 'oob',
        tokenType: t.token_type ?? 'Bearer',
        expiresIn: Number(t.expires_in ?? 86400),
        cachedAt: data.cached_at ?? new Date().toISOString(),
      };
    } catch {
      return null;
    }
  }

  public async set(entry: TokenCacheEntry): Promise<void> {
    const fs = await import('node:fs/promises');
    const data = {
      token: {
        access_token: entry.accessToken,
        scope: entry.scope,
        token_type: entry.tokenType,
        expires_in: entry.expiresIn,
      },
      cached_at: entry.cachedAt,
    };
    await fs.writeFile(this.filePath, JSON.stringify(data, null, 2), 'utf-8');
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
