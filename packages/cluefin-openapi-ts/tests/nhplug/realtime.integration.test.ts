/**
 * NH PLUG 실시간 시세(WebSocket) 통합 테스트. 파이썬 `tests/nhplug/test_realtime_integration.py` 와 같은 기준.
 *
 * 시세 채널은 운영 전용이다 — 모의 소켓(:17070)은 `oc` 구독에 `WSS10006 "허용되지 않는 tr_cd 입니다."` 를
 * 답한다(2026-10-12 실측). 그래서 `NHPLUG_ENV=prod` 이고 해당 시장이 열려 있을 때만 돈다. 시세 구독만
 * 하므로 주문은 나가지 않는다. 장중에 005930 이 30초 안에 안 오면 실패다.
 */
import { describe, expect, test } from 'vitest';

import { runNhplugLiveOnlyIntegration } from '../_helpers/integration-setup';
import { isKrxContinuousHours, isUsMarketHours } from '../_helpers/market-hours';
import { receiveFirstNhplugBody } from '../_helpers/nhplug-realtime';

const domesticTest = runNhplugLiveOnlyIntegration && isKrxContinuousHours() ? test : test.skip;
const overseasTest = runNhplugLiveOnlyIntegration && isUsMarketHours() ? test : test.skip;

const KR_STOCK = '005930';
const US_STOCK = 'AAPL';
const RECEIVE_TIMEOUT_MS = 30_000;

describe('NH PLUG realtime integration (domestic)', () => {
  domesticTest('should receive execution data (oc)', async () => {
    const body = await receiveFirstNhplugBody({
      market: 'kr',
      trCd: 'oc',
      trKey: KR_STOCK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
    });

    expect(body, `no oc data for ${KR_STOCK} within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    expect(body?.code).toBe(KR_STOCK);
    expect(body?.price).toBeTruthy();
    expect(body?.time).toBeTruthy();
  });

  domesticTest('should receive orderbook data (ob)', async () => {
    const body = await receiveFirstNhplugBody({
      market: 'kr',
      trCd: 'ob',
      trKey: KR_STOCK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
    });

    expect(body, `no ob data for ${KR_STOCK} within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    expect(body?.code).toBe(KR_STOCK);
    expect(body?.offer).toBeTruthy();
    expect(body?.bid).toBeTruthy();
  });
});

// 미국 지연시세(rc·rh). 실시간(RC·RH)은 유료시세 약정 고객만 받는다.
describe('NH PLUG realtime integration (overseas, delayed)', () => {
  overseasTest('should receive delayed execution data (rc)', async () => {
    const body = await receiveFirstNhplugBody({
      market: 'gb',
      trCd: 'rc',
      trKey: US_STOCK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
    });

    expect(body, `no rc data for ${US_STOCK} within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    expect(String(body?.gicz15)).toMatch(/AAPL$/);
    expect(body?.trdprc_1z17).toBeTruthy();
  });

  overseasTest('should receive delayed orderbook data (rh)', async () => {
    const body = await receiveFirstNhplugBody({
      market: 'gb',
      trCd: 'rh',
      trKey: US_STOCK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
    });

    expect(body, `no rh data for ${US_STOCK} within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    expect(String(body?.gicz15)).toMatch(/AAPL$/);
    expect(body?.best_ask1z17).toBeTruthy();
  });
});
