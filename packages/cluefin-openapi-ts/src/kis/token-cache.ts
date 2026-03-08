export interface TokenCacheEntry {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
  accessTokenTokenExpired: string;
  cachedAt: string;
}

export interface TokenCacheStore {
  get(): Promise<TokenCacheEntry | null>;
  set(entry: TokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

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
 * Reads/writes the same JSON format used by `cluefin_openapi.kis._token_manager`,
 * so the TypeScript and Python packages can share a single cached token and avoid
 * the KIS 1-request-per-minute rate limit on token generation.
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
          token_type?: string;
          expires_in?: number;
          access_token_token_expired?: string;
        };
        cached_at?: string;
      };
      const t = data.token;
      if (!t?.access_token) return null;
      return {
        accessToken: t.access_token,
        tokenType: t.token_type ?? 'Bearer',
        expiresIn: Number(t.expires_in ?? 86400),
        accessTokenTokenExpired: t.access_token_token_expired ?? '',
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
        token_type: entry.tokenType,
        expires_in: entry.expiresIn,
        access_token_token_expired: entry.accessTokenTokenExpired,
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
