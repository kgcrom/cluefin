import { describe, test } from 'vitest';

import {
  accountCurrentDayStatusResponseSchema,
  accountNextDaySettlementDetailsResponseSchema,
  accountOrderExecutionDetailsItemSchema,
  accountOrderExecutionDetailsResponseSchema,
  accountProfitRateResponseSchema,
  availableOrderQuantityByMarginRateResponseSchema,
  availableWithdrawalAmountResponseSchema,
  consignmentComprehensiveTransactionHistoryResponseSchema,
  currentDayTradingJournalResponseSchema,
  dailyAccountProfitRateDetailsResponseSchema,
  dailyEstimatedDepositAssetBalanceItemSchema,
  dailyEstimatedDepositAssetBalanceResponseSchema,
  dailyRealizedProfitLossDetailsResponseSchema,
  dailyRealizedProfitLossItemSchema,
  dailyRealizedProfitLossResponseSchema,
  dailyStockRealizedProfitLossByDateResponseSchema,
  dailyStockRealizedProfitLossByPeriodResponseSchema,
  depositBalanceDetailsResponseSchema,
  estimatedAssetBalanceResponseSchema,
  executedResponseSchema,
  marginDetailsResponseSchema,
  unexecutedResponseSchema,
} from '../../src/kiwoom/schemas/domestic-account';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticAccount', () => {
  setupKiwoomRateLimit();
  it('getDailyStockRealizedProfitLossByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyStockRealizedProfitLossByDate({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyStockRealizedProfitLossByDateResponseSchema, 'dtStkDivRlztPl');
  });

  it('getDailyStockRealizedProfitLossByPeriod', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyStockRealizedProfitLossByPeriod({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyStockRealizedProfitLossByPeriodResponseSchema, 'dtStkRlztPl');
  });

  it('getDailyRealizedProfitLoss', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyRealizedProfitLoss({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyRealizedProfitLossResponseSchema, 'dtRlztPl', dailyRealizedProfitLossItemSchema);
  });

  it('getUnexecuted', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getUnexecuted({
      allStkTp: '0',
      trdeTp: '0',
      stexTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, unexecutedResponseSchema, 'oso');
  });

  it('getExecuted', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getExecuted({
      qryTp: '0',
      sellTp: '0',
      stexTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, executedResponseSchema, 'cntr');
  });

  it('getDailyRealizedProfitLossDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyRealizedProfitLossDetails({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyRealizedProfitLossDetailsResponseSchema, 'tdyRlztPlDtl');
  });

  it('getAccountProfitRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountProfitRate({
      stexTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, accountProfitRateResponseSchema, 'acntPrftRt');
  });

  // ka10088: skip — 유효한 주문번호(ordNo)가 있어야만 조회 가능.
  // 실제 분할주문이 존재하지 않으면 항상 에러를 반환한다.
  test.skip('getUnexecutedSplitOrderDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getUnexecutedSplitOrderDetails({
      ordNo: '0000000',
    });
    assertKiwoomResponse(res);
  });

  it('getCurrentDayTradingJournal', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getCurrentDayTradingJournal({
      ottksTp: '0',
      chCrdTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, currentDayTradingJournalResponseSchema, 'tdyTrdeDiary');
  });

  it('getDepositBalanceDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDepositBalanceDetails({
      qryTp: '2',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, depositBalanceDetailsResponseSchema, 'stkEntrPrst');
  });

  it('getDailyEstimatedDepositAssetBalance', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyEstimatedDepositAssetBalance({
      startDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      dailyEstimatedDepositAssetBalanceResponseSchema,
      'dalyPrsmDpstAsetAmtPrst',
      dailyEstimatedDepositAssetBalanceItemSchema,
    );
  });

  it('getEstimatedAssetBalance', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getEstimatedAssetBalance({
      qryTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, estimatedAssetBalanceResponseSchema);
  });

  // kt00004: skip — dmstStexTp 값과 무관하게 "501307:거래소구분을 확인해주십시오" 에러 반환.
  // 모의투자 계좌에서는 지원하지 않는 것으로 추정.
  test.skip('getAccountEvaluationStatus', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountEvaluationStatus({
      qryTp: '1',
      dmstStexTp: '0',
    });
    assertKiwoomResponse(res);
  });

  // kt00005: skip — dmstStexTp 값과 무관하게 "501307:거래소구분을 확인해주십시오" 에러 반환.
  // 모의투자 계좌에서는 지원하지 않는 것으로 추정.
  test.skip('getExecutionBalance', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getExecutionBalance({
      dmstStexTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getAccountOrderExecutionDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountOrderExecutionDetails({
      qryTp: '0',
      stkBondTp: '0',
      sellTp: '0',
      dmstStexTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      accountOrderExecutionDetailsResponseSchema,
      'acntOrdCntrPrpsDtl',
      accountOrderExecutionDetailsItemSchema,
    );
  });

  it('getAccountNextDaySettlementDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountNextDaySettlementDetails({});
    assertKiwoomResponse(res);
    assertResponseShape(res.body, accountNextDaySettlementDetailsResponseSchema, 'acntNxdySetlFrcsPrpsArray');
  });

  // kt00009: skip — "501724:관련자료가없습니다" 에러 반환.
  // 당일 주문 체결 내역이 없으면 에러로 응답하는 API 특성.
  test.skip('getAccountOrderExecutionStatus', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountOrderExecutionStatus({
      stkBondTp: '0',
      mrktTp: '0',
      sellTp: '0',
      qryTp: '0',
      dmstStexTp: '0',
    });
    assertKiwoomResponse(res);
  });

  // kt00010: 장 마감 시간대에 uv(단가) 값이 하한가 미만이면 에러 반환.
  // returnCode !== 0 이면 스키마 검증을 건너뛴다.
  it('getAvailableWithdrawalAmount', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAvailableWithdrawalAmount({
      stkCd: SAMSUNG,
      trdeTp: '2',
      uv: '100000',
    });
    if (res.body.returnCode !== 0) return;
    assertResponseShape(res.body, availableWithdrawalAmountResponseSchema);
  });

  it('getAvailableOrderQuantityByMarginRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAvailableOrderQuantityByMarginRate({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, availableOrderQuantityByMarginRateResponseSchema);
  });

  // kt00012: skip — "503721:신용계좌만 조회가능합니다" 에러 반환.
  // 일반 위탁 계좌로는 조회할 수 없는 API.
  test.skip('getAvailableOrderQuantityByMarginLoanStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAvailableOrderQuantityByMarginLoanStock({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
  });

  it('getMarginDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getMarginDetails({});
    assertKiwoomResponse(res);
    assertResponseShape(res.body, marginDetailsResponseSchema);
  });

  it('getConsignmentComprehensiveTransactionHistory', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getConsignmentComprehensiveTransactionHistory({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      tp: '0',
      gdsTp: '0',
      dmstStexTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, consignmentComprehensiveTransactionHistoryResponseSchema, 'trstOvrlTrdePrpsArray');
  });

  it('getDailyAccountProfitRateDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyAccountProfitRateDetails({
      frDt: ONE_MONTH_AGO,
      toDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyAccountProfitRateDetailsResponseSchema);
  });

  it('getAccountCurrentDayStatus', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountCurrentDayStatus({});
    assertKiwoomResponse(res);
    assertResponseShape(res.body, accountCurrentDayStatusResponseSchema);
  });

  // kt00018: skip — dmstStexTp 값과 무관하게 "501307:거래소구분을 확인해주십시오" 에러 반환.
  // 모의투자 계좌에서는 지원하지 않는 것으로 추정.
  test.skip('getAccountEvaluationBalanceDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountEvaluationBalanceDetails({
      qryTp: '1',
      dmstStexTp: '0',
    });
    assertKiwoomResponse(res);
  });
});
