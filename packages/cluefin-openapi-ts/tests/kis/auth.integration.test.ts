import path from 'node:path';

import { expect, test } from 'vitest';

import { KisAuth } from '../../src/kis/auth';
import { FileTokenCacheStore } from '../../src/kis/token-cache';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
const integrationTest = runIntegration ? test : test.skip;

integrationTest('KisAuth integration should generate and revoke token', async () => {
  const appKey = process.env.KIS_APP_KEY;
  const secretKey = process.env.KIS_SECRET_KEY;
  if (!appKey || !secretKey) {
    throw new Error('KIS_APP_KEY and KIS_SECRET_KEY are required for integration tests');
  }

  const env = process.env.KIS_ENV === 'prod' ? 'prod' : 'dev';
  const cacheDir = process.env.KIS_TOKEN_CACHE_DIR ?? path.resolve(__dirname, '../../../../data');
  const tokenCacheStore = new FileTokenCacheStore(path.join(cacheDir, '.kis_token_cache.json'));
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
