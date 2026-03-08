import { expect } from 'vitest';

import path from 'node:path';

import { KisAuth } from '../../src/kis/auth';
import { KisHttpClient } from '../../src/kis/http-client';
import { FileTokenCacheStore } from '../../src/kis/token-cache';
import { KiwoomAuth } from '../../src/kiwoom/auth';
import { KiwoomClient } from '../../src/kiwoom/client';
import type { ApiResponse } from '../../src/core/types';

export const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
export const runAccountIntegration = runIntegration && !!process.env.KIS_CANO;

export const SAMSUNG = '005930';
export const KODEX200 = '069500';

export const KIS_CANO = process.env.KIS_CANO ?? '';
export const KIS_ACNT_PRDT_CD = process.env.KIS_ACNT_PRDT_CD ?? '01';

const fmt = (d: Date): string => d.toISOString().slice(0, 10).replace(/-/g, '');

export const TODAY = fmt(new Date());
export const ONE_MONTH_AGO = fmt(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000));

const g = globalThis as Record<string, unknown>;

export function getKisClient(): Promise<KisHttpClient> {
  if (!g.__kisClientPromise) {
    g.__kisClientPromise = (async () => {
      const appKey = process.env.KIS_APP_KEY;
      const secretKey = process.env.KIS_SECRET_KEY;
      if (!appKey || !secretKey) {
        throw new Error('KIS_APP_KEY and KIS_SECRET_KEY are required');
      }
      const env = process.env.KIS_ENV === 'prod' ? 'prod' : 'dev';
      // Share token cache with Python cluefin-openapi to avoid KIS 1-req/min rate limit
      const cacheDir = process.env.KIS_TOKEN_CACHE_DIR ?? path.resolve(__dirname, '../../../../data');
      const tokenCacheStore = new FileTokenCacheStore(path.join(cacheDir, '.kis_token_cache.json'));
      const auth = new KisAuth({ appKey, secretKey, env, tokenCacheStore });
      const tokenResponse = await auth.generate();
      return new KisHttpClient({
        token: tokenResponse.accessToken,
        appKey,
        secretKey,
        env,
      });
    })();
  }
  return g.__kisClientPromise as Promise<KisHttpClient>;
}

export function getKiwoomClient(): Promise<KiwoomClient> {
  if (!g.__kiwoomClientPromise) {
    g.__kiwoomClientPromise = (async () => {
      const appKey = process.env.KIWOOM_APP_KEY;
      const secretKey = process.env.KIWOOM_SECRET_KEY;
      if (!appKey || !secretKey) {
        throw new Error('KIWOOM_APP_KEY and KIWOOM_SECRET_KEY are required');
      }
      const env = process.env.KIWOOM_ENV === 'prod' ? 'prod' : 'dev';
      const auth = new KiwoomAuth({ appKey, secretKey, env });
      const tokenResponse = await auth.generateToken();
      return new KiwoomClient({ token: tokenResponse.token, env });
    })();
  }
  return g.__kiwoomClientPromise as Promise<KiwoomClient>;
}

export function assertKisResponse(res: ApiResponse): void {
  expect(res).toBeDefined();
  expect(res.body).toBeDefined();
  if (res.body.rtCd !== '0') {
    console.error('KIS Error Response:', JSON.stringify(res.body, null, 2));
  }
  expect(res.body.rtCd).toEqual('0');
}

export function assertKiwoomResponse(res: ApiResponse): void {
  expect(res).toBeDefined();
  expect(res.body).toBeDefined();
  if (res.body.returnCode !== 0) {
    console.error('Kiwoom Error Response:', JSON.stringify(res.body, null, 2));
  }
  expect(res.body.returnCode).toEqual(0);
}
