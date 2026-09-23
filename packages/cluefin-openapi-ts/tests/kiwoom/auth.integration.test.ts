import { describe, expect, test } from 'vitest';

import { KiwoomAuth } from '../../src/kiwoom/auth';
import { setupKiwoomRateLimit } from '../_helpers/integration-setup';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
// Kiwoom hands back the SAME token while one is still valid, so revoking here also kills the
// token cached in the shared (Python/TS) cache file — every later run then fails with 8005
// until the cache ages out. Opt in explicitly, like KIS_TEST_REVOKE / NHPLUG_TEST_REVOKE.
const runRevoke = runIntegration && process.env.KIWOOM_TEST_REVOKE === '1';
const integrationTest = runRevoke ? test : test.skip;

describe('KiwoomAuth', () => {
  setupKiwoomRateLimit();

  integrationTest('KiwoomAuth integration should generate and revoke token (KIWOOM_TEST_REVOKE=1)', async () => {
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
});
