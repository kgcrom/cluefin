import { mkdtemp, readdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import { localIsoNow, writeJsonAtomic } from '../../src/core/token-file';

let tempDirs: string[] = [];

const createTempDir = async (): Promise<string> => {
  const dir = await mkdtemp(join(tmpdir(), 'cluefin-openapi-token-file-'));
  tempDirs.push(dir);
  return dir;
};

afterEach(async () => {
  await Promise.all(tempDirs.map((dir) => rm(dir, { recursive: true, force: true })));
  tempDirs = [];
});

describe('localIsoNow', () => {
  it('formats naive local time the way Python datetime.isoformat() does', () => {
    const date = new Date(2026, 0, 2, 3, 4, 5, 6);
    expect(localIsoNow(date)).toBe('2026-01-02T03:04:05.006');
  });

  it('has no Z/offset suffix, which Python 3.10 fromisoformat rejects', () => {
    // uv run --python 3.10 python -c "from datetime import datetime; datetime.fromisoformat('2026-01-02T03:04:05.006Z')"
    // -> ValueError: Invalid isoformat string
    expect(localIsoNow()).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}$/);
  });

  it('round-trips through JS Date as the same instant', () => {
    const date = new Date();
    expect(new Date(localIsoNow(date)).getTime()).toBe(date.getTime());
  });
});

describe('writeJsonAtomic', () => {
  it('writes owner-only JSON and leaves no temp file behind', async () => {
    const dir = await createTempDir();
    const filePath = join(dir, '.token_cache.json');

    await writeJsonAtomic(filePath, { token: 'secret' });

    expect(JSON.parse(await readFile(filePath, 'utf-8'))).toEqual({ token: 'secret' });
    expect((await stat(filePath)).mode & 0o777).toBe(0o600);
    expect(await readdir(dir)).toEqual(['.token_cache.json']);
  });

  it('replaces an existing world-readable file with an owner-only one', async () => {
    const dir = await createTempDir();
    const filePath = join(dir, '.token_cache.json');
    await writeFile(filePath, '{"token":"old"}', { mode: 0o644 });

    await writeJsonAtomic(filePath, { token: 'new' });

    expect(JSON.parse(await readFile(filePath, 'utf-8'))).toEqual({ token: 'new' });
    expect((await stat(filePath)).mode & 0o777).toBe(0o600);
  });

  it('creates the parent directory when missing', async () => {
    const dir = await createTempDir();
    const filePath = join(dir, 'nested', '.token_cache.json');

    await writeJsonAtomic(filePath, { token: 'secret' });

    expect(JSON.parse(await readFile(filePath, 'utf-8'))).toEqual({ token: 'secret' });
  });
});
