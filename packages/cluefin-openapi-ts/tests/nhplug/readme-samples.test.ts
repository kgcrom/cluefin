import { describe, expect, it } from 'vitest';

import { silentLogger } from '../../src/core/logger';
import { NhplugAuth } from '../../src/nhplug/auth';
import { NhplugClient } from '../../src/nhplug/client';
import { NhplugSocketClient } from '../../src/nhplug/socket-client';

/**
 * README 의 NH PLUG 예제를 그대로 실행해 메서드/필드 이름이 실제 API 와 어긋나지 않는지
 * 확인한다. 타입은 `tsc`(`tests` 포함) 가, 런타임 이름은 이 테스트가 검증한다.
 */

const jsonResponse = (body: unknown): Response =>
  new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });

describe('README NH PLUG samples', () => {
  it('quick start: NhplugAuth.generate() -> NhplugClient -> 계좌목록 -> 국내주식 현재가', async () => {
    const appKey = 'app-key';
    const secretKey = 'secret-key';

    const fetchMock: typeof fetch = async (input) => {
      const url = String(input);
      if (url.endsWith('/oauth2/token')) {
        return jsonResponse({
          access_token: 'issued-token',
          scope: 'oob',
          token_type: 'Bearer',
          expires_in: 86400,
        });
      }
      if (url.endsWith('/n2/acctinfo')) {
        return jsonResponse({
          rsp_cd: '00000',
          rsp_msg: '정상',
          Output_0: [{ acct_no: '00000000000', acct_type: '03' }],
        });
      }
      return jsonResponse({ rsp_cd: 'XA102', rsp_msg: '모의투자 조회가 완료되었습니다', Output_0: {} });
    };

    // 토큰 발급은 운영 도메인 전용이라 NhplugAuth 는 env 를 받지 않는다.
    const auth = new NhplugAuth({ appKey, secretKey, fetchImpl: fetchMock });
    const { accessToken } = await auth.generate();

    // env: 'dev'(기본) = 모의투자(moapi), 'prod' = 운영(실주문)
    const client = new NhplugClient({
      token: accessToken,
      appKey,
      secretKey,
      env: 'dev',
      fetchImpl: fetchMock,
      logger: silentLogger,
    });

    const accounts = await client.common.getAccountList({});
    const account = accounts.body.output0?.[0];
    const actNo = account?.acctNo;

    expect(actNo).toBe('00000000000');
    expect(account?.acctType).toBe('03');

    const price = await client.krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: '005930' });
    expect(price.body).toBeDefined();

    const balance = await client.krstockInquiry.balance({
      actNo,
      bncBseCd: '1', // 주식관련 총 평가(체결기준)
      ltgAotDitCd: '9', // 전체
      aetBse: '1', // 순자산
      qutDitCd: 'UNT', // 통합시세
    });
    expect(balance.body).toBeDefined();
  });

  it('websocket sample: subscribe with a tr_cd channel code', () => {
    const socket = new NhplugSocketClient({ token: 'issued-token', env: 'dev', market: 'kr' });

    expect(socket.env).toBe('dev');
    expect(socket.market).toBe('kr');
    // 구독 메시지는 header.token + body.tr_cd/tr_key 평문 JSON
    const message = socket.parseMessage(
      JSON.stringify({ header: { tr_cd: 'mc', tr_key: '005930' }, body: { iem_cd: '005930' } }),
    );
    expect(message.messageType).toBe('DATA');
    expect(message.trId).toBe('mc');
    expect(message.body).toEqual({ iem_cd: '005930' });
  });
});
