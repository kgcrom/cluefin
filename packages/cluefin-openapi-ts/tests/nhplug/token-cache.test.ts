import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  FileTokenCacheStore,
  MemoryTokenCacheStore,
  nhplugTokenCacheFileName,
  type TokenCacheEntry,
} from '../../src/nhplug/token-cache';

const entry: TokenCacheEntry = {
  accessToken: 'access-token',
  scope: 'oob',
  tokenType: 'Bearer',
  expiresIn: 86_400,
  cachedAt: '2026-08-22T12:00:00',
};

let tempDirs: string[] = [];

const createCachePath = async (): Promise<string> => {
  const dir = await mkdtemp(join(tmpdir(), 'cluefin-openapi-nhplug-token-cache-'));
  tempDirs.push(dir);
  return join(dir, nhplugTokenCacheFileName('app-key'));
};

afterEach(async () => {
  await Promise.all(tempDirs.map((dir) => rm(dir, { recursive: true, force: true })));
  tempDirs = [];
});

describe('nhplugTokenCacheFileName', () => {
  it('scopes the cache file by app_key only (no env), matching the Python TokenManager', () => {
    // sha256('app-key')[:8] — 파이썬 `_cache_file_name` 과 동일한 규칙
    expect(nhplugTokenCacheFileName('app-key')).toBe('.nhplug_token_cache_2924a27d.json');
    expect(nhplugTokenCacheFileName()).toBe('.nhplug_token_cache.json');
    expect(nhplugTokenCacheFileName('other-key')).not.toBe(nhplugTokenCacheFileName('app-key'));
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
          access_token: 'cached-token',
          scope: 'oob',
          token_type: 'Bearer',
          expires_in: 86400,
        },
        cached_at: '2026-08-22T12:00:00',
      }),
      'utf-8',
    );

    expect(await new FileTokenCacheStore(filePath).get()).toEqual({
      accessToken: 'cached-token',
      scope: 'oob',
      tokenType: 'Bearer',
      expiresIn: 86_400,
      cachedAt: '2026-08-22T12:00:00',
    });
  });

  it('writes the Python-compatible cache format', async () => {
    const filePath = await createCachePath();
    await new FileTokenCacheStore(filePath).set(entry);

    expect(JSON.parse(await readFile(filePath, 'utf-8'))).toEqual({
      token: {
        access_token: 'access-token',
        scope: 'oob',
        token_type: 'Bearer',
        expires_in: 86_400,
      },
      cached_at: '2026-08-22T12:00:00',
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
