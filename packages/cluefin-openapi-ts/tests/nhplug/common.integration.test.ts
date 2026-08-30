/**
 * NH PLUG 공통(common) 통합 테스트.
 *
 * `/n2/acctinfo` 는 다른 모든 카테고리의 선행 조건이다 — 조회·주문 API 의 `actNo` 는
 * 여기서 받은 계좌번호를 쓴다. 모의투자(dev)는 `acctType === '03'` 계좌만 유효하다.
 *
 * `closeWebsocketSession` 은 계좌의 실시간 세션을 끊는 상태 변경 호출이라 통합
 * 테스트를 두지 않는다 (단위 테스트로만 검증).
 */
import { describe, expect, test } from 'vitest';

import { accountListResponseSchema } from '../../src/nhplug/schemas/common';
import {
  assertNhplugResponse,
  assertNhplugResponseShape,
  callNhplug,
  getNhplugClient,
  requireNhplugAccount,
  runNhplugIntegration,
  setupNhplugRateLimit,
} from '../_helpers/integration-setup';

const it = runNhplugIntegration ? test : test.skip;

describe('Nhplug Common', () => {
  setupNhplugRateLimit();

  it('getAccountList', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.common.getAccountList({}));

    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, accountListResponseSchema);
  });

  it('환경에 맞는 계좌(acctType)를 찾을 수 있다', async (ctx) => {
    // 계좌가 없으면 실패가 아니라 skip 된다 — 이후 조회 테스트도 같은 이유로 skip 된다.
    const account = await requireNhplugAccount(ctx);
    expect(account.length).toBeGreaterThan(0);
  });
});
