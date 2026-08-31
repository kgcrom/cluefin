/**
 * NH PLUG 해외주식 조회(gbstock inquiry) 통합 테스트.
 *
 * 모의투자(`NHPLUG_ENV=dev`)에서 실제 조회를 수행한다. 조회 API 는 장 운영시간·영업일
 * 제약이 없어 휴일에도 성공한다. 주문 카테고리(gbstock order)는 실제 체결이 발생하므로
 * 통합 테스트를 두지 않는다.
 *
 * 계좌는 `/n2/acctinfo` 에서 환경에 맞는 것(dev = acctType `03`)을 고르며,
 * 없으면 실패가 아니라 skip 한다.
 */
import { describe, test } from 'vitest';

import {
  overseasStockInquiryBalanceResponseSchema,
  overseasStockInquiryBuyableAmountResponseSchema,
  overseasStockInquiryDailyTransactionResponseSchema,
  overseasStockInquiryMarginResponseSchema,
  overseasStockInquiryPeriodPnlDetailResponseSchema,
  overseasStockInquiryPeriodPnlResponseSchema,
  overseasStockInquiryReservedInquiryResponseSchema,
  overseasStockInquiryUnexecutedResponseSchema,
} from '../../src/nhplug/schemas/overseas-stock-inquiry';
import {
  assertNhplugResponse,
  assertNhplugResponseShape,
  callNhplug,
  getNhplugClient,
  NHPLUG_TEST_GB_IEM_CD,
  NHPLUG_US_NATION_CD,
  ONE_MONTH_AGO,
  requireNhplugAccount,
  runNhplugIntegration,
  setupNhplugRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

const it = runNhplugIntegration ? test : test.skip;

describe('Nhplug OverseasStockInquiry', () => {
  setupNhplugRateLimit();

  it('balance', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.balance({
        actNo,
        qutIqrDitCd: '9', // 전체
        fcSecTrdNatCd: NHPLUG_US_NATION_CD,
        curCd: 'KRW', // 전체
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryBalanceResponseSchema);
  });

  it('buyableAmount', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 매수가능금액 "조회"다 — 주문을 넣지 않는다.
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.buyableAmount({
        actNo,
        pcsDit: '1', // 매수가능금액조회
        fcSecTrdNatCd: NHPLUG_US_NATION_CD,
        iemCd: NHPLUG_TEST_GB_IEM_CD,
        wtmCurKndCd: '2', // 원화
        ossOrrKndCd: '1', // GTS(미국시장주문)
        ahiNmnPrTpCd: '03', // 시장가
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryBuyableAmountResponseSchema);
  });

  it('unexecuted', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 당일 주문이 없어도 조회 자체는 성공한다.
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.unexecuted({
        orrDt: TODAY,
        actNo,
        ossSbyDitCd: '0', // 전체
        sotDit: '0', // 주문번호순
        ostCnsDit: '0', // 전체
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryUnexecutedResponseSchema);
  });

  it('reservedInquiry', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 예약주문 "조회"다 — 예약주문 접수는 통합 테스트를 두지 않는다.
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.reservedInquiry({
        fcMktDitCd: '000', // 전체
        bkgOrrDt: TODAY,
        actNo,
        sbyDitCd: '0', // 전체
        bkgOrrCanYn: '0', // 전체
        ossOrrKndCd: '0', // 전체
        bkgOrrTpCd: '0', // 전체
        wtmCurKndCd: '0', // 전체
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryReservedInquiryResponseSchema);
  });

  it('dailyTransaction', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.dailyTransaction({
        actNo,
        iqrStaDt: ONE_MONTH_AGO,
        iqrEndDt: TODAY,
        actTrdCfcCd: '00', // 전체
        iemMlfCd: '00001', // 외화주식
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryDailyTransactionResponseSchema);
  });

  it('periodPnl', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.periodPnl({
        actNo,
        iqrDit: '2', // 원화기준
        staOrrDt: ONE_MONTH_AGO,
        endOrrDt: TODAY,
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryPeriodPnlResponseSchema);
  });

  it('periodPnlDetail', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 거래가 없어도 성공해야 한다.
    const res = await callNhplug(ctx, () =>
      client.overseasStockInquiry.periodPnlDetail({
        actNo,
        iqrDit: '2', // 원화기준
        orrDt: TODAY,
        fcSecTrdNatCd: NHPLUG_US_NATION_CD,
        trdCurCd: 'USD',
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryPeriodPnlDetailResponseSchema);
  });

  it('margin', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () => client.overseasStockInquiry.margin({ actNo }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockInquiryMarginResponseSchema);
  });
});
