/**
 * NH PLUG 국내주식 조회(krstock inquiry) 통합 테스트.
 *
 * 모의투자(`NHPLUG_ENV=dev`)에서 실제 조회를 수행한다. 조회 API 는 주문과 달리 장
 * 운영시간·영업일 제약이 없어 휴일에도 성공한다 (파이썬 스위트 2026-08-22 실측).
 *
 * `actNo` 는 `/n2/acctinfo` 에서 환경에 맞는 계좌(dev = acctType `03`)를 골라 쓰고,
 * 계좌가 없으면 실패가 아니라 skip 한다.
 *
 * `integratedMargin`·`rightsHeld`·`rightsScheduled`·`reservedInquiry` 는 모의투자에서
 * `19999 "모의투자에서는 해당업무가 제공되지 않습니다"` 로 거부되므로 운영에서만 실행한다.
 */
import { describe, expect, test } from 'vitest';

import {
  krStockInquiryAssetStatusResponseSchema,
  krStockInquiryBalanceResponseSchema,
  krStockInquiryBuyableQuantityResponseSchema,
  krStockInquiryDailyOrderExecutionResponseSchema,
  krStockInquiryDailyPnlResponseSchema,
  krStockInquiryIntegratedMarginResponseSchema,
  krStockInquiryRealizedPnlResponseSchema,
  krStockInquiryReservedInquiryResponseSchema,
  krStockInquiryRightsHeldResponseSchema,
  krStockInquiryRightsScheduledResponseSchema,
  krStockInquirySellableQuantityResponseSchema,
  krStockInquiryTradingPnlResponseSchema,
} from '../../src/nhplug/schemas/krstock-inquiry';
import {
  assertNhplugResponse,
  callNhplug,
  getNhplugClient,
  NHPLUG_TEST_IEM_CD,
  nhplugMockOmits,
  ONE_MONTH_AGO,
  requireNhplugAccount,
  runNhplugIntegration,
  runNhplugLiveOnlyIntegration,
  setupNhplugRateLimit,
  TODAY,
} from '../_helpers/integration-setup';
import { assertNhplugMatchesSpec } from '../_helpers/nhplug-response-shape';

const it = runNhplugIntegration ? test : test.skip;
/** 모의투자에서 19999(미지원)로 거부되는 API — 운영(NHPLUG_ENV=prod)에서만 검증 가능하다. */
const liveOnlyIt = runNhplugLiveOnlyIntegration ? test : test.skip;

describe('Nhplug KrstockInquiry', () => {
  setupNhplugRateLimit();

  it('assetStatus', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.assetStatus({
        actNo,
        ealAlyCd: '2', // 시가평가
        aetBse: '1', // 순자산
        qutDitCd: 'UNT', // 통합시세
        alyQutCd: '2', // 전체장 — 스펙 필수(260911 추가)
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/assetStatus',
      res.body,
      krStockInquiryAssetStatusResponseSchema,
      nhplugMockOmits(
        'Output_0.cus_fnm',
        'Output_0.rnm_cfm_no',
        'Output_0.ctc_tp_cd_nm',
        'Output_0.act_amn_tab_cd',
        'Output_0.act_pdt_llf_cd',
        'Output_0.amn_emp_fnm',
        'Output_0.ima_wtm',
      ),
    );
  });

  it('balance', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.balance({
        actNo,
        bncBseCd: '1', // 주식관련 총 평가(체결기준)
        ltgAotDitCd: '9', // 전체
        aetBse: '1', // 순자산
        qutDitCd: 'UNT', // 통합시세
        alyQutCd: '2', // 전체장 — 스펙 필수(260911 추가)
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/balance',
      res.body,
      krStockInquiryBalanceResponseSchema,
      nhplugMockOmits(
        'Output_0.fc_dca',
        'Output_0.fc_mgg_amt',
        'Output_0.fc_orr_pbl_amt',
        'Output_0.fnn_amt',
        'Output_0.rit_eal_amt',
        'Output_0.orr_pbl_amt',
        'Output_0.act_no',
      ),
    );
    // 연속조회 플래그는 응답 헤더로 내려온다.
    expect(res.headers.ctsFlag).toBeDefined();
  });

  it('dailyOrderExecution', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 주문 이력이 없어도 조회 자체는 성공한다. 모의 서버는 성공에 XA102 를 반환한다.
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.dailyOrderExecution({
        actNo,
        orrDt: TODAY,
        ostCnsDit: '0', // 전체
        orrMktCd: '00', // 전체 — 스펙 필수
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/dailyOrderExecution',
      res.body,
      krStockInquiryDailyOrderExecutionResponseSchema,
    );
  });

  it('buyableQuantity', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // nmnPrTpCd="05"(시장가)를 써서 orrPr(주문가격) 입력을 피한다 — 조회 전용이며 주문이 아니다.
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.buyableQuantity({
        actNo,
        iemCd: NHPLUG_TEST_IEM_CD,
        ostDitCd: '1', // 현금
        nmnPrTpCd: '05', // 시장가 — orrPr 불필요
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/buyableQuantity',
      res.body,
      krStockInquiryBuyableQuantityResponseSchema,
      nhplugMockOmits(
        'Output_0.sll_ctc_amt1',
        'Output_0.byn_ctc_amt1',
        'Output_0.sdr_xps1',
        'Output_0.sll_ctc_amt',
        'Output_0.ost_byn_ctc_amt',
        'Output_0.sdr_xps',
        'Output_0.byn_ny_cns_orr_amt',
        'Output_0.int_rt',
        'Output_0.orr_pr',
        'Output_0.rp_eal_amt',
        'Output_0.ny_stl_qty',
      ),
    );
  });

  it('sellableQuantity', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 보유 잔고가 없어 매도가능수량이 0이어도 조회 자체는 성공한다.
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.sellableQuantity({
        actNo,
        iemCd: NHPLUG_TEST_IEM_CD,
        cfdLonCd: '00', // 일반거래(현금)
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/sellableQuantity',
      res.body,
      krStockInquirySellableQuantityResponseSchema,
      nhplugMockOmits(
        'Output_0.cus_fnm',
        'Output_0.ost_dit_cd',
        'Output_0.cfd_lon_cd',
        'Output_0.cfd_lon_cd_nm',
        'Output_0.ttn_tp_cd',
        'Output_0.ttn_tp_cd_nm',
        'Output_0.sll_ny_stl_qty',
        'Output_0.byn_ny_stl_qty',
        'Output_0.phs_uit_pr',
      ),
    );
  });

  it('realizedPnl', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.realizedPnl({
        actNo,
        iqrDitCd1: '0', // 전체
        feeDitCd: '1', // 온라인
        qutDitCd: 'UNT', // 통합시세
        alyQutCd: '2', // 전체장 — 스펙 필수(260911 추가)
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/realizedPnl',
      res.body,
      krStockInquiryRealizedPnlResponseSchema,
      nhplugMockOmits(
        'Output_0.cus_fnm',
        'Output_0.rnm_cfm_no',
        'Output_0.act_atv_tp_dtl_cd',
        'Output_0.act_amn_tab_cd',
        'Output_0.act_pdt_llf_cd',
      ),
    );
  });

  it('dailyPnl', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.dailyPnl({ actNo, iqrStaDt: ONE_MONTH_AGO, iqrEndDt: TODAY }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/dailyPnl',
      res.body,
      krStockInquiryDailyPnlResponseSchema,
      nhplugMockOmits('Output_0.act_fnm'),
    );
  });

  it('tradingPnl', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.tradingPnl({ actNo, iqrStaDt: ONE_MONTH_AGO, iqrEndDt: TODAY }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/tradingPnl',
      res.body,
      krStockInquiryTradingPnlResponseSchema,
      nhplugMockOmits(
        'Output_0.iem_cd',
        'Output_0.byn_uit_pr',
        'Output_0.sll_uit_pr',
        'Output_0.fee_sum',
        'Output_0.tax_sum',
      ),
    );
  });

  liveOnlyIt('integratedMargin (모의투자 미지원 — 19999)', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () => client.krstockInquiry.integratedMargin({ actNo }));
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/integratedMargin',
      res.body,
      krStockInquiryIntegratedMarginResponseSchema,
    );
  });

  liveOnlyIt('rightsHeld (모의투자 미지원 — 19999)', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () => client.krstockInquiry.rightsHeld({ actNo, staDt: ONE_MONTH_AGO }));
    assertNhplugResponse(res);
    assertNhplugMatchesSpec('/krstock/inquiry/v1/rightsHeld', res.body, krStockInquiryRightsHeldResponseSchema);
  });

  liveOnlyIt('rightsScheduled (모의투자 미지원 — 19999)', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    const res = await callNhplug(ctx, () => client.krstockInquiry.rightsScheduled({ actNo }));
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/rightsScheduled',
      res.body,
      krStockInquiryRightsScheduledResponseSchema,
    );
  });

  liveOnlyIt('reservedInquiry (모의투자 미지원 — 19999)', async (ctx) => {
    const client = await getNhplugClient();
    const actNo = await requireNhplugAccount(ctx);
    // 조회 전용이다 — 예약주문 접수(reservedOrder)는 통합 테스트를 두지 않는다.
    const res = await callNhplug(ctx, () =>
      client.krstockInquiry.reservedInquiry({
        actNo,
        sbyDitCd: '0', // 전체
        bkgOrrTpCd: '0', // 전체
      }),
    );
    assertNhplugResponse(res);
    assertNhplugMatchesSpec(
      '/krstock/inquiry/v1/reservedInquiry',
      res.body,
      krStockInquiryReservedInquiryResponseSchema,
    );
  });
});
