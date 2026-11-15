import { describe, expect, it } from 'vitest';

import { silentLogger } from '../../src/core/logger';
import { NhplugAuth } from '../../src/nhplug/auth';
import { NhplugClient } from '../../src/nhplug/client';
import { getNhplugSocketUrl, NhplugSocketClient } from '../../src/nhplug/socket-client';

/**
 * README 의 NH PLUG 예제를 그대로 실행해 메서드/필드 이름이 실제 API 와 어긋나지 않는지
 * 확인한다. 런타임 이름은 이 테스트가 검증한다. 타입은 게이트가 보지 않으니(`typecheck` 는 `src` 만)
 * 예제를 바꾸면 `npx tsc -p tsconfig.json --noEmit` 출력에서 이 파일을 찾아본다.
 *
 * 예제는 조회를 모의투자(dev)로, 시세를 운영(prod)으로 나눠 부른다 — 모의투자는 시세 API 를
 * 거절하기 때문이다(`IGW40023`, 소켓은 `WSS10006`). 그래서 호출이 어느 도메인으로 갔는지도 본다.
 */

const MOCK_HOST = 'https://moapi.nhplug.com:8443';
const LIVE_HOST = 'https://api.nhplug.com:8443';

const jsonResponse = (body: unknown): Response =>
  new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });

describe('README NH PLUG samples', () => {
  it('quick start: 토큰 하나로 모의투자 계좌목록·잔고와 운영 현재가를 부른다', async () => {
    const credentials = { appKey: 'app-key', secretKey: 'secret-key' } as const;
    const { appKey, secretKey } = credentials;
    const calledUrls: string[] = [];

    const fetchMock: typeof fetch = async (input) => {
      const url = String(input);
      calledUrls.push(url);
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
          Output_0: [
            { acct_no: '11111111111', acct_type: '01' },
            { acct_no: '00000000000', acct_type: '03' },
          ],
        });
      }
      if (url.startsWith(LIVE_HOST)) {
        return jsonResponse({ rsp_cd: '00000', rsp_msg: '정상', Output_0: {} });
      }
      return jsonResponse({ rsp_cd: 'XA102', rsp_msg: '모의투자 조회가 완료되었습니다', Output_0: {} });
    };

    // 토큰 발급은 운영 도메인 전용이라 NhplugAuth 는 env 를 받지 않는다.
    const auth = new NhplugAuth({ appKey, secretKey, fetchImpl: fetchMock });
    const { accessToken } = await auth.generate();

    // 조회·주문은 모의투자(dev, moapi)로 먼저 확인한다.
    const mock = new NhplugClient({
      token: accessToken,
      appKey,
      secretKey,
      env: 'dev',
      fetchImpl: fetchMock,
      logger: silentLogger,
    });

    // 모의투자에서 유효한 계좌는 acctType '03' 뿐이다.
    const accounts = await mock.common.getAccountList({});
    const actNo = accounts.body.output0?.find((account) => account.acctType === '03')?.acctNo;
    expect(actNo).toBe('00000000000');

    const balance = await mock.krstockInquiry.balance({
      actNo,
      bncBseCd: '1', // 주식관련 총 평가(체결기준)
      ltgAotDitCd: '9', // 전체
      aetBse: '1', // 순자산
      qutDitCd: 'UNT', // 통합시세
    });
    expect(balance.body).toBeDefined();

    // 시세는 운영 전용 — 같은 토큰으로 prod 클라이언트를 하나 더 만든다.
    const live = new NhplugClient({
      token: accessToken,
      appKey,
      secretKey,
      env: 'prod',
      fetchImpl: fetchMock,
      logger: silentLogger,
    });
    const price = await live.krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: '005930' });
    expect(price.body).toBeDefined();

    expect(calledUrls).toEqual([
      `${LIVE_HOST}/oauth2/token`,
      `${MOCK_HOST}/n2/acctinfo`,
      `${MOCK_HOST}/krstock/inquiry/v1/balance`,
      `${LIVE_HOST}/krstock/quote/v1/currentPrice`,
    ]);
  });

  it('websocket sample: 운영 소켓에 tr_cd 채널 코드로 구독한다', () => {
    // connect() 를 부르지 않으므로 네트워크에 닿지 않는다.
    const socket = new NhplugSocketClient({ token: 'issued-token', env: 'prod', market: 'kr' });

    expect(socket.env).toBe('prod');
    expect(socket.market).toBe('kr');
    expect(getNhplugSocketUrl(socket.env, socket.market)).toBe('wss://api.nhplug.com:7070/websocket');
    // 서버 푸시는 header.tr_cd/tr_key + body 평문 JSON
    const message = socket.parseMessage(
      JSON.stringify({ header: { tr_cd: 'mc', tr_key: '005930' }, body: { iem_cd: '005930' } }),
    );
    expect(message.messageType).toBe('DATA');
    expect(message.trId).toBe('mc');
    expect(message.trKey).toBe('005930');
    expect(message.body).toEqual({ iem_cd: '005930' });
  });
});
