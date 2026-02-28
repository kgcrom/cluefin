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
