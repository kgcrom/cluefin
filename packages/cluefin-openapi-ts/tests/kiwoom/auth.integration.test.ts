import { expect, test } from 'bun:test';

import { KiwoomAuth } from '../../src/kiwoom/auth';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
const integrationTest = runIntegration ? test : test.skip;

integrationTest('KiwoomAuth integration should generate and revoke token', async () => {
  const appKey = process.env.KIWOOM_APP_KEY;
  const secretKey = process.env.KIWOOM_SECRET_KEY;
  if (!appKey || !secretKey) {
    throw new Error('KIWOOM_APP_KEY and KIWOOM_SECRET_KEY are required for integration tests');
  }

  const env = process.env.KIWOOM_ENV === 'prod' ? 'prod' : 'dev';
  const auth = new KiwoomAuth({
    appKey,
    secretKey,
    env,
  });

  const tokenResponse = await auth.generateToken();
  expect(typeof tokenResponse.token).toBe('string');
  expect(tokenResponse.token.length).toBeGreaterThan(0);
  expect(tokenResponse.tokenType.startsWith('Bearer')).toBe(true);
  expect(tokenResponse.expiresDt).toMatch(/^\d{14}$/u);

  const revokeResult = await auth.revokeToken(tokenResponse.token);
  expect(revokeResult).toBe(true);
});
