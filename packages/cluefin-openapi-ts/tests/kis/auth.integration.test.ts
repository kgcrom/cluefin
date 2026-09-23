import { mkdirSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { expect, test } from 'vitest';

import { KisAuth } from '../../src/kis/auth';
import { FileTokenCacheStore, kisTokenCacheFileName } from '../../src/kis/token-cache';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
// The token cache file is shared with Python, so revoking here kills the token every other
// KIS run (both languages) is reusing and forces a re-issue (1/min limit). Opt in explicitly.
const runRevoke = runIntegration && process.env.KIS_TEST_REVOKE === '1';
const integrationTest = runRevoke ? test : test.skip;

integrationTest('KisAuth integration should generate and revoke token (KIS_TEST_REVOKE=1)', async () => {
  const appKey = process.env.KIS_APP_KEY;
  const secretKey = process.env.KIS_SECRET_KEY;
  if (!appKey || !secretKey) {
    throw new Error('KIS_APP_KEY and KIS_SECRET_KEY are required for integration tests');
  }

  const env = process.env.KIS_ENV === 'prod' ? 'prod' : 'dev';
  const cacheDir = process.env.KIS_TOKEN_CACHE_DIR ?? path.join(os.tmpdir(), 'cluefin-openapi');
  mkdirSync(cacheDir, { recursive: true });
  const tokenCacheStore = new FileTokenCacheStore(path.join(cacheDir, kisTokenCacheFileName(env, appKey)));
  const auth = new KisAuth({ appKey, secretKey, env, tokenCacheStore });

  const tokenResponse = await auth.generate();
  expect(typeof tokenResponse.accessToken).toBe('string');
  expect(tokenResponse.accessToken.length).toBeGreaterThan(0);
  expect(typeof tokenResponse.tokenType).toBe('string');
  expect(typeof tokenResponse.expiresIn).toBe('number');
  expect(typeof tokenResponse.accessTokenTokenExpired).toBe('string');

  const revokeResult = await auth.revoke(tokenResponse.accessToken);
  expect(revokeResult).toBe(true);
});
