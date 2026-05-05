import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import { FileTokenCacheStore, MemoryTokenCacheStore, type TokenCacheEntry } from '../../src/kis/token-cache';

const entry: TokenCacheEntry = {
  accessToken: 'access-token',
  tokenType: 'Bearer',
  expiresIn: 86_400,
  accessTokenTokenExpired: '2026-05-05T12:00:00Z',
  cachedAt: '2026-05-04T12:00:00Z',
};

let tempDirs: string[] = [];

const createCachePath = async (): Promise<string> => {
  const dir = await mkdtemp(join(tmpdir(), 'cluefin-openapi-token-cache-'));
  tempDirs.push(dir);
  return join(dir, 'kis-token-cache.json');
};

afterEach(async () => {
  await Promise.all(tempDirs.map((dir) => rm(dir, { recursive: true, force: true })));
  tempDirs = [];
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
    const store = new FileTokenCacheStore(await createCachePath());

    expect(await store.get()).toBeNull();
  });

  it('reads the Python-compatible cache format with fallback values', async () => {
    const filePath = await createCachePath();
    await writeFile(
      filePath,
      JSON.stringify({
        token: {
          access_token: 'cached-token',
          access_token_token_expired: '2026-05-05T12:00:00Z',
        },
      }),
      'utf-8',
    );

    const store = new FileTokenCacheStore(filePath);

    expect(await store.get()).toMatchObject({
      accessToken: 'cached-token',
      tokenType: 'Bearer',
      expiresIn: 86_400,
      accessTokenTokenExpired: '2026-05-05T12:00:00Z',
    });
    expect((await store.get())?.cachedAt).toEqual(expect.any(String));
  });

  it('writes the Python-compatible cache format', async () => {
    const filePath = await createCachePath();
    const store = new FileTokenCacheStore(filePath);

    await store.set(entry);

    expect(JSON.parse(await readFile(filePath, 'utf-8'))).toEqual({
      token: {
        access_token: 'access-token',
        token_type: 'Bearer',
        expires_in: 86_400,
        access_token_token_expired: '2026-05-05T12:00:00Z',
      },
      cached_at: '2026-05-04T12:00:00Z',
    });
  });

  it('clears the cache file and ignores missing files', async () => {
    const filePath = await createCachePath();
    const store = new FileTokenCacheStore(filePath);

    await store.set(entry);
    await store.clear();

    expect(await store.get()).toBeNull();
    await expect(store.clear()).resolves.toBeUndefined();
  });
});
