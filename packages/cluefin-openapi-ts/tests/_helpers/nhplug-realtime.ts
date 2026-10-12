// NH PLUG 실시간 통합 테스트 공용: 운영 소켓에 접속·구독하고, 지정한 채널·종목의 첫 시세 body 를 기다린다.
// 운영은 없는 종목(999999)에도 rsp_cd 00000 을 답하고, 그 구독 응답도 tr_cd 가 붙어 data 이벤트로 온다
// (2026-10-12 실측) — 구독 성공은 검증 수단이 아니고 tr_key 가 맞는 시세를 받아야 한다.

import type { WebSocketEvent } from '../../src/core/websocket';
import { type NhplugMarket, NhplugSocketClient } from '../../src/nhplug/socket-client';
import { getNhplugToken } from './integration-setup';

export interface ReceiveFirstNhplugOptions {
  market: NhplugMarket;
  trCd: string;
  /** 구독 키. 푸시의 tr_key 가 이 값을 포함하면 맞는 것으로 본다(해외는 `AAPL` → `USAAAPL`). */
  trKey: string;
  timeoutMs: number;
}

/**
 * 운영 소켓에 접속해 `trCd`/`trKey` 를 구독하고 첫 시세 body 를 돌려준다. 시간 안에 오지 않으면
 * undefined — 실패로 볼지는 호출부가 정한다. 소켓 오류·구독 실패는 reject 한다.
 */
export const receiveFirstNhplugBody = async (
  options: ReceiveFirstNhplugOptions,
): Promise<Record<string, unknown> | undefined> => {
  const client = new NhplugSocketClient({ token: await getNhplugToken(), env: 'prod', market: options.market });

  return new Promise<Record<string, unknown> | undefined>((resolve, reject) => {
    let settled = false;
    const settle = (finish: () => void): void => {
      if (settled) {
        return;
      }
      settled = true;
      clearTimeout(timer);
      client.close();
      finish();
    };
    const timer = setTimeout(() => settle(() => resolve(undefined)), options.timeoutMs);

    client.on('connected', () => {
      client.subscribe(options.trCd, options.trKey).catch((error: unknown) => settle(() => reject(error)));
    });
    client.on('data', (event: WebSocketEvent) => {
      const { body, trKey } = event;
      if (event.trId === options.trCd && trKey?.includes(options.trKey) && body) {
        settle(() => resolve(body));
      }
    });
    client.on('error', (event: WebSocketEvent) => {
      settle(() => reject(event.error ?? new Error('WebSocket error')));
    });

    client.connect();
  });
};
