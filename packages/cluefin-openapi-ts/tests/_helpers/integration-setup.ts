import { mkdirSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { beforeEach, expect } from 'vitest';
import type { z } from 'zod';
import { toCamelCase } from '../../src/core/case-convert';
import { ApiError } from '../../src/core/errors';
import type { ApiEnv, ApiResponse } from '../../src/core/types';
import { KisAuth } from '../../src/kis/auth';
import { KisHttpClient } from '../../src/kis/http-client';
import { FileTokenCacheStore } from '../../src/kis/token-cache';
import { KiwoomAuth } from '../../src/kiwoom/auth';
import { KiwoomClient } from '../../src/kiwoom/client';
import { NhplugAuth } from '../../src/nhplug/auth';
import { NhplugClient, SUCCESS_RSP_CODES } from '../../src/nhplug/client';
import {
  FileTokenCacheStore as NhplugFileTokenCacheStore,
  nhplugTokenCacheFileName,
} from '../../src/nhplug/token-cache';

export const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export function setupKiwoomRateLimit(): void {
  beforeEach(async () => {
    await sleep(500);
  });
}

/**
 * NH PLUG 통합 테스트용 호출 간격.
 *
 * 클라이언트 내부 rate limiter 만으로는 실서버 스로틀을 못 피한다 —
 * 파이썬 통합 스위트와 동일하게 테스트마다 1초를 쉰다.
 */
export function setupNhplugRateLimit(): void {
  beforeEach(async () => {
    await sleep(1000);
  });
}

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

export function assertResponseShape(
  body: Record<string, unknown>,
  responseSchema: z.ZodObject<z.ZodRawShape>,
  itemKey?: string,
  itemSchema?: z.ZodObject<z.ZodRawShape>,
): void {
  const expectedKeys = Object.keys(responseSchema.shape).map(toCamelCase).sort();
  const actualKeys = Object.keys(body).sort();
  expect(actualKeys).toEqual(expectedKeys);

  if (itemKey && itemSchema) {
    const itemValue = body[itemKey];
    const expectedItemKeys = Object.keys(itemSchema.shape).map(toCamelCase).sort();
    if (Array.isArray(itemValue) && itemValue.length > 0) {
      const actualItemKeys = Object.keys(itemValue[0] as Record<string, unknown>).sort();
      expect(actualItemKeys).toEqual(expectedItemKeys);
    } else if (
      itemValue &&
      typeof itemValue === 'object' &&
      !Array.isArray(itemValue) &&
      Object.keys(itemValue).length > 0
    ) {
      const actualItemKeys = Object.keys(itemValue as Record<string, unknown>).sort();
      expect(actualItemKeys).toEqual(expectedItemKeys);
    }
  }
}

// ────────────────────────────────────────────────────────────────────────────
// NH PLUG (nhplug)
// ────────────────────────────────────────────────────────────────────────────

/** 테스트가 붙을 NH PLUG 환경. dev = 모의투자(moapi), prod = 운영(실제 체결). */
export const NHPLUG_ENV: ApiEnv = process.env.NHPLUG_ENV?.toLowerCase() === 'prod' ? 'prod' : 'dev';

/** 자격증명이 없으면 통합 테스트를 조용히 건너뛴다 (KIS_CANO 게이팅과 같은 방식). */
export const runNhplugIntegration = runIntegration && !!process.env.NHPLUG_APP_KEY && !!process.env.NHPLUG_SECRET_KEY;

/**
 * 모의투자(moapi)에서 제공되지 않는 API 용 게이트.
 *
 * 파이썬 `_integration_helpers.real_account_only` 와 같은 의미다 — 운영
 * (`NHPLUG_ENV=prod`)에서만 실행된다.
 */
export const runNhplugLiveOnlyIntegration = runNhplugIntegration && NHPLUG_ENV === 'prod';

/** 계좌번호를 직접 지정하고 싶을 때 쓰는 선택적 오버라이드. 없으면 `/n2/acctinfo` 로 찾는다. */
export const NHPLUG_ACCOUNT_NO = process.env.NHPLUG_ACCOUNT_NO ?? '';

export const NHPLUG_TEST_IEM_CD = '005930'; // 삼성전자
export const NHPLUG_TEST_ETF_IEM_CD = '069500'; // KODEX 200
export const NHPLUG_TEST_GB_IEM_CD = 'AAPL'; // 애플
export const NHPLUG_TEST_GB_SYMBOL_CD = 'SPX'; // S&P 500 지수
export const NHPLUG_US_NATION_CD = '200'; // 미국

/**
 * 장 운영시간·영업일·계좌 상태 때문에 "지금은" 검증할 수 없다는 뜻의 rsp_cd.
 * 파이썬 `_integration_helpers.ENV_BLOCKED_CODES` 와 같은 값을 유지할 것.
 */
const NHPLUG_ENV_BLOCKED_CODES: readonly string[] = [
  '14100', // 모의투자 영업일이 아닙니다 (2026-08-22 실측)
];

/**
 * NH PLUG 클라이언트 (프로세스당 1개, 토큰은 파일 캐시 재사용).
 *
 * 토큰 발급은 서버에서 초당 1회로 제한되고 불필요한 재발급마다 계좌 보안 알림이
 * 뜬다. 파이썬 `TokenManager` 와 같은 캐시 파일(tmpdir/cluefin-openapi/
 * `.nhplug_token_cache_<app_key 해시>.json`)을 공유해 실제 발급은 만료 전까지 1회다.
 * 캐시는 env 가 아니라 app_key 로만 구분한다 — 토큰 하나가 운영·모의투자 모두에 쓰인다.
 */
export function getNhplugClient(): Promise<NhplugClient> {
  if (!g.__nhplugClientPromise) {
    g.__nhplugClientPromise = (async () => {
      const appKey = process.env.NHPLUG_APP_KEY;
      const secretKey = process.env.NHPLUG_SECRET_KEY;
      if (!appKey || !secretKey) {
        throw new Error('NHPLUG_APP_KEY and NHPLUG_SECRET_KEY are required');
      }
      const cacheDir = process.env.NHPLUG_TOKEN_CACHE_DIR ?? path.join(os.tmpdir(), 'cluefin-openapi');
      mkdirSync(cacheDir, { recursive: true });
      const tokenCacheStore = new NhplugFileTokenCacheStore(path.join(cacheDir, nhplugTokenCacheFileName(appKey)));
      const auth = new NhplugAuth({ appKey, secretKey, tokenCacheStore });
      const tokenResponse = await auth.generate();
      return new NhplugClient({
        token: tokenResponse.accessToken,
        appKey,
        secretKey,
        env: NHPLUG_ENV,
      });
    })();
  }
  return g.__nhplugClientPromise as Promise<NhplugClient>;
}

/**
 * 호출 환경과 `acct_type` 이 맞는 계좌번호를 `/n2/acctinfo` 에서 한 번만 찾아 캐시한다.
 *
 * 모의투자(dev)는 03 계좌만, 운영(prod)은 01·02 계좌만 유효하다 (krstock·gbstock 공통).
 * 같은 계좌번호가 여러 행으로 내려올 수 있어 첫 매칭을 쓴다.
 */
export function getNhplugAccount(): Promise<string | null> {
  if (!g.__nhplugAccountPromise) {
    g.__nhplugAccountPromise = (async () => {
      if (NHPLUG_ACCOUNT_NO) {
        return NHPLUG_ACCOUNT_NO;
      }
      const client = await getNhplugClient();
      const res = await client.common.getAccountList({});
      const accounts = res.body.output0 ?? [];
      const wanted = NHPLUG_ENV === 'dev' ? ['03'] : ['01', '02'];
      const matched = accounts.find((account) => wanted.includes(account.acctType));
      return matched?.acctNo ?? null;
    })();
  }
  return g.__nhplugAccountPromise as Promise<string | null>;
}

/** vitest TestContext 중 이 헬퍼가 쓰는 부분만 추린 타입. */
export interface SkippableContext {
  skip: (note?: string) => never;
}

/** 계좌가 없으면 실패가 아니라 skip 한다 (KIS 의 KIS_CANO 게이팅과 같은 취지). */
export async function requireNhplugAccount(ctx: SkippableContext): Promise<string> {
  const account = await getNhplugAccount();
  if (!account) {
    const wanted = NHPLUG_ENV === 'dev' ? '03' : '01/02';
    ctx.skip(`${NHPLUG_ENV} 환경에 맞는 계좌(acct_type ${wanted})가 없다`);
  }
  return account;
}

const nhplugRspCode = (error: unknown): { rspCd: string; rspMsg: string } => {
  if (!(error instanceof ApiError)) {
    return { rspCd: '', rspMsg: error instanceof Error ? error.message : String(error) };
  }
  const data = (error.responseData ?? {}) as { rsp_cd?: string; rsp_msg?: string };
  return {
    rspCd: data.rsp_cd ?? (typeof error.errorCode === 'string' ? error.errorCode : ''),
    rspMsg: data.rsp_msg ?? error.message,
  };
};

/**
 * 환경 제약(영업일·장 운영시간·계좌 상태)이면 skip, 그 외 오류는 그대로 실패로 남긴다.
 *
 * 파이썬 `skip_if_env_blocked` 와 같은 역할이다. 조건이 풀리면 코드 수정 없이
 * 실제 검증이 재개된다.
 */
export async function callNhplug<T>(
  ctx: SkippableContext,
  request: () => Promise<ApiResponse<T>>,
): Promise<ApiResponse<T>> {
  try {
    return await request();
  } catch (error) {
    const { rspCd, rspMsg } = nhplugRspCode(error);
    if (NHPLUG_ENV_BLOCKED_CODES.includes(rspCd) || NHPLUG_ENV_BLOCKED_CODES.some((code) => rspMsg.includes(code))) {
      ctx.skip(`장 운영시간/계좌 상태 때문에 검증 불가: [${rspCd}] ${rspMsg}`);
    }
    throw error;
  }
}

/**
 * NH PLUG 응답 봉투 검증.
 *
 * 성공 코드는 `00000` 과 모의투자 조회 성공인 `XA102` 두 가지다 — `00000` 만
 * 성공으로 보면 모의 서버의 정상 응답이 오탐된다.
 */
export function assertNhplugResponse(res: ApiResponse<unknown>): void {
  expect(res).toBeDefined();
  expect(res.body).toBeDefined();
  const body = res.body as { rspCd?: string; rspMsg?: string };
  // 일부 응답(`/n2/acctinfo` 등)은 `rsp_cd` 없이 내려온다. 실패 코드는 클라이언트가
  // 이미 NhplugApiError 로 올리므로, 코드가 있을 때만 성공 코드인지 확인한다.
  if (body.rspCd === undefined) {
    expect(typeof res.body).toBe('object');
    return;
  }
  if (!SUCCESS_RSP_CODES.includes(body.rspCd)) {
    console.error('NH PLUG Error Response:', JSON.stringify(res.body, null, 2));
  }
  expect(SUCCESS_RSP_CODES).toContain(body.rspCd);
}

/**
 * 응답 본문에 스키마에 없는 키가 섞이지 않았는지 확인한다.
 *
 * `Output_N` 블록은 데이터가 있을 때만 내려오므로(스펙 설명) 키 집합 완전 일치가 아니라
 * "실제 키 ⊆ 스키마 키" 부분집합으로 검증한다. 스키마에 없는 필드가 새로 내려오면
 * (= 모델 갱신이 필요하면) 실패한다.
 */
export function assertNhplugResponseShape(body: unknown, responseSchema: z.ZodObject<z.ZodRawShape>): void {
  const expectedKeys = new Set(Object.keys(responseSchema.shape).map(toCamelCase));
  const actualKeys = Object.keys(body as Record<string, unknown>);
  const unexpected = actualKeys.filter((key) => !expectedKeys.has(key)).sort();
  expect(unexpected).toEqual([]);
}
