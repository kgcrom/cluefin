import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  FileTokenCacheStore,
  kiwoomTokenCacheFileName,
  MemoryTokenCacheStore,
  type TokenCacheEntry,
} from '../../src/kiwoom/token-cache';

const entry: TokenCacheEntry = {
  token: 'access-token',
  tokenType: 'Bearer',
  expiresDt: '2026-05-05T12:00:00',
  cachedAt: '2026-05-04T12:00:00',
};

let tempDirs: string[] = [];

const createCachePath = async (): Promise<string> => {
  const dir = await mkdtemp(join(tmpdir(), 'cluefin-openapi-kiwoom-token-cache-'));
  tempDirs.push(dir);
  return join(dir, kiwoomTokenCacheFileName('dev', 'app-key'));
};

afterEach(async () => {
  await Promise.all(tempDirs.map((dir) => rm(dir, { recursive: true, force: true })));
  tempDirs = [];
});

describe('kiwoomTokenCacheFileName', () => {
  it('matches the Python TokenManager._cache_file_name output', () => {
    // uv run python -c "from cluefin_openapi.kiwoom._token_manager import TokenManager as T; print(T._cache_file_name('prod','abc'))"
    // sha256('abc')[:8] == 'ba7816bf'
    expect(kiwoomTokenCacheFileName('prod', 'abc')).toBe('.kiwoom_token_cache_prod_ba7816bf.json');
    expect(kiwoomTokenCacheFileName('dev', 'abc')).toBe('.kiwoom_token_cache_dev_ba7816bf.json');
    expect(kiwoomTokenCacheFileName()).toBe('.kiwoom_token_cache.json');
  });
});

describe('MemoryTokenCacheStore', () => {
  it('stores and clears an in-memory token entry', async () => {
    const store = new MemoryTokenCacheStore();

    expect(await store.get()).toBeNull();
    await store.set(entry);
    expect(await store.get()).toEqual(entry);
    await store.clear();
    expect(await store.get()).toBeNull();
  });
});

describe('FileTokenCacheStore', () => {
  it('returns null when the cache file is missing', async () => {
    expect(await new FileTokenCacheStore(await createCachePath()).get()).toBeNull();
  });

  it('reads the JSON written by the Python TokenManager', async () => {
    const filePath = await createCachePath();
    await writeFile(
      filePath,
      JSON.stringify({
        token: {
          expires_dt: '2026-05-05T12:00:00',
          token_type: 'Bearer',
          token: 'cached-token',
        },
        cached_at: '2026-05-04T12:00:00',
      }),
      'utf-8',
    );

    expect(await new FileTokenCacheStore(filePath).get()).toEqual({
      token: 'cached-token',
      tokenType: 'Bearer',
      expiresDt: '2026-05-05T12:00:00',
      cachedAt: '2026-05-04T12:00:00',
    });
  });

  it('writes the Python-compatible cache format', async () => {
    const filePath = await createCachePath();
    await new FileTokenCacheStore(filePath).set(entry);

    expect(JSON.parse(await readFile(filePath, 'utf-8'))).toEqual({
      token: {
        expires_dt: '2026-05-05T12:00:00',
        token_type: 'Bearer',
        token: 'access-token',
      },
      cached_at: '2026-05-04T12:00:00',
    });
  });

  it('round-trips its own written file', async () => {
    const filePath = await createCachePath();
    const store = new FileTokenCacheStore(filePath);

    await store.set(entry);
    expect(await store.get()).toEqual(entry);

    await store.clear();
    expect(await store.get()).toBeNull();
    await expect(store.clear()).resolves.toBeUndefined();
  });
});
