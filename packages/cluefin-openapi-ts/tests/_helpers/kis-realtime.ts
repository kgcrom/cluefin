// KIS 실시간 통합 테스트 공용: approval key 를 받아 접속·구독하고, 지정한 TR 의 첫 data 이벤트를 기다린다.
// KIS 는 없는 종목코드·모의 미지원 TR 에도 "SUBSCRIBE SUCCESS" 를 답한다(2026-10-11 실측) — 구독 성공은
// 아무것도 검증하지 않으므로 데이터를 받아 파싱하는 것까지 봐야 한다.

import type { ApiEnv } from '../../src/core/types';
import type { WebSocketEvent } from '../../src/core/websocket';
import { KisAuth } from '../../src/kis/auth';
import { KisSocketClient } from '../../src/kis/socket-client';

export const kisEnv: ApiEnv = process.env.KIS_ENV === 'prod' ? 'prod' : 'dev';

const getEnvOrThrow = (key: string): string => {
  const value = process.env[key];
  if (!value) {
    throw new Error(`${key} is required for integration tests`);
  }
  return value;
};

export const createKisSocketClient = async (env: ApiEnv): Promise<KisSocketClient> => {
  const appKey = getEnvOrThrow('KIS_APP_KEY');
  const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
  const { approvalKey } = await new KisAuth({ appKey, secretKey, env }).approve();
  return new KisSocketClient({ approvalKey, appKey, secretKey, env });
};

export interface ReceiveFirstOptions {
  env: ApiEnv;
  trId: string;
  timeoutMs: number;
  subscribe: (client: KisSocketClient) => Promise<void>;
}

/**
 * 접속 후 `subscribe` 를 부르고, `trId` 의 첫 data 이벤트를 돌려준다. 시간 안에 오지 않으면 undefined —
 * 실패로 볼지 skip 할지는 호출부가 정한다(거래가 드문 채권은 skip). 소켓 오류·구독 실패는 reject 한다.
 */
export const receiveFirstKisData = async (options: ReceiveFirstOptions): Promise<WebSocketEvent | undefined> => {
  const client = await createKisSocketClient(options.env);

  return new Promise<WebSocketEvent | undefined>((resolve, reject) => {
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
      options.subscribe(client).catch((error: unknown) => settle(() => reject(error)));
    });
    client.on('data', (event: WebSocketEvent) => {
      if (event.trId === options.trId && event.data) {
        settle(() => resolve(event));
      }
    });
    client.on('error', (event: WebSocketEvent) => {
      settle(() => reject(event.error ?? new Error('WebSocket error')));
    });

    client.connect();
  });
};
