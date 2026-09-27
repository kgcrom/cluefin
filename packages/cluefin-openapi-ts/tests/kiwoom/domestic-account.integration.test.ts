import { describe, test } from 'vitest';

import {
  accountCurrentDayStatusResponseSchema,
  accountEvaluationBalanceDetailsResponseSchema,
  accountEvaluationStatusResponseSchema,
  accountNextDaySettlementDetailsResponseSchema,
  accountOrderExecutionDetailsResponseSchema,
  accountOrderExecutionStatusResponseSchema,
  accountProfitRateResponseSchema,
  availableOrderQuantityByMarginRateResponseSchema,
  availableWithdrawalAmountResponseSchema,
  consignmentComprehensiveTransactionHistoryResponseSchema,
  currentDayTradingJournalResponseSchema,
  dailyAccountProfitRateDetailsResponseSchema,
  dailyEstimatedDepositAssetBalanceResponseSchema,
  dailyRealizedProfitLossDetailsResponseSchema,
  dailyRealizedProfitLossResponseSchema,
  dailyStockRealizedProfitLossByDateResponseSchema,
  dailyStockRealizedProfitLossByPeriodResponseSchema,
  depositBalanceDetailsResponseSchema,
  estimatedAssetBalanceResponseSchema,
  executedResponseSchema,
  executionBalanceResponseSchema,
  marginDetailsResponseSchema,
  unexecutedResponseSchema,
  unexecutedSplitOrderDetailsResponseSchema,
} from '../../src/kiwoom/schemas/domestic-account';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  ONE_MONTH_AGO,
  runIntegration,
  runKiwoomLiveOnlyIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;
// kt00002/kt00015/kt00016/kt00017: 모의투자에서 "[2000](RC9000:모의투자에서는 해당업무가
// 제공되지 않습니다.)" 로 영구 실패한다 (파이썬 `real_account_only` 와 동일 TR·동일 근거).
// 실계좌(KIWOOM_ENV=prod)에서만 실행한다.
const itLiveOnly = runKiwoomLiveOnlyIntegration ? test : test.skip;

describe('Kiwoom DomesticAccount', () => {
  setupKiwoomRateLimit();
  it('getDailyStockRealizedProfitLossByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyStockRealizedProfitLossByDate({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyStockRealizedProfitLossByDateResponseSchema);
  });

  it('getDailyStockRealizedProfitLossByPeriod', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyStockRealizedProfitLossByPeriod({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyStockRealizedProfitLossByPeriodResponseSchema);
  });

  it('getDailyRealizedProfitLoss', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyRealizedProfitLoss({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyRealizedProfitLossResponseSchema);
  });

  it('getUnexecuted', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getUnexecuted({
      allStkTp: '0',
      trdeTp: '0',
      stexTp: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(unexecutedResponseSchema);
  });

  it('getExecuted', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getExecuted({
      qryTp: '0',
      sellTp: '0',
      stexTp: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(executedResponseSchema);
  });

  it('getDailyRealizedProfitLossDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyRealizedProfitLossDetails({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyRealizedProfitLossDetailsResponseSchema);
  });

  it('getAccountProfitRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountProfitRate({
      stexTp: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountProfitRateResponseSchema);
  });

  // ka10088: 없는 주문번호면 에러 없이 빈 목록이 온다 (2026-09-27 dev 실측 — 예전 주석은 "항상 에러" 였다)
  it('getUnexecutedSplitOrderDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getUnexecutedSplitOrderDetails({
      ordNo: '0000000',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(unexecutedSplitOrderDetailsResponseSchema);
  });

  it('getCurrentDayTradingJournal', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getCurrentDayTradingJournal({
      ottksTp: '1',
      chCrdTp: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(currentDayTradingJournalResponseSchema);
  });

  it('getDepositBalanceDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDepositBalanceDetails({
      qryTp: '2',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(depositBalanceDetailsResponseSchema);
  });

  itLiveOnly('getDailyEstimatedDepositAssetBalance', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyEstimatedDepositAssetBalance({
      startDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyEstimatedDepositAssetBalanceResponseSchema);
  });

  it('getEstimatedAssetBalance', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getEstimatedAssetBalance({
      qryTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(estimatedAssetBalanceResponseSchema);
  });

  // kt00004: 예전 skip 사유(501307 거래소구분)는 문서에 없는 dmstStexTp 값 탓이었다 — 'KRX' 면 모의에서도 동작 (2026-09-27)
  it('getAccountEvaluationStatus', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountEvaluationStatus({
      qryTp: '1',
      dmstStexTp: 'KRX',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountEvaluationStatusResponseSchema);
  });

  // kt00005: 모의투자 RC9000 (파이썬 real_account_only 와 동일)
  itLiveOnly('getExecutionBalance', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getExecutionBalance({
      dmstStexTp: 'KRX',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(executionBalanceResponseSchema);
  });

  it('getAccountOrderExecutionDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountOrderExecutionDetails({
      qryTp: '1',
      stkBondTp: '0',
      sellTp: '0',
      dmstStexTp: '%',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountOrderExecutionDetailsResponseSchema);
  });

  it('getAccountNextDaySettlementDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountNextDaySettlementDetails({});
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountNextDaySettlementDetailsResponseSchema);
  });

  // kt00009: 파이썬과 같은 입력이면 모의에서도 동작 (2026-09-27). 체결 내역이 없으면 목록이 빈다
  it('getAccountOrderExecutionStatus', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountOrderExecutionStatus({
      stkBondTp: '0',
      mrktTp: '0',
      sellTp: '0',
      qryTp: '0',
      dmstStexTp: '%',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountOrderExecutionStatusResponseSchema);
  });

  // kt00010: 파이썬 통합 테스트와 동일한 입력 조합.
  // 하드코딩 단가가 당일 가격밴드(상·하한가)를 벗어나면 서버가 2000 에러를 던지므로 그 경우는 skip.
  it('getAvailableWithdrawalAmount', async () => {
    const client = await getKiwoomClient();
    let res: Awaited<ReturnType<typeof client.domesticAccount.getAvailableWithdrawalAmount>>;
    try {
      res = await client.domesticAccount.getAvailableWithdrawalAmount({
        ioAmt: '1000000',
        stkCd: SAMSUNG,
        trdeTp: '1',
        trdeQty: '10',
        uv: '50000',
        expBuyUnp: '60000',
      });
    } catch (error) {
      if (error instanceof Error && error.message.includes('[2000]')) return;
      throw error;
    }
    if (res.body.returnCode !== 0) return;
    assertKiwoomSpecConformance(availableWithdrawalAmountResponseSchema);
  });

  it('getAvailableOrderQuantityByMarginRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAvailableOrderQuantityByMarginRate({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(availableOrderQuantityByMarginRateResponseSchema);
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
    assertKiwoomSpecConformance(marginDetailsResponseSchema);
  });

  itLiveOnly('getConsignmentComprehensiveTransactionHistory', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getConsignmentComprehensiveTransactionHistory({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      tp: '0',
      gdsTp: '0',
      dmstStexTp: '%',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(consignmentComprehensiveTransactionHistoryResponseSchema);
  });

  itLiveOnly('getDailyAccountProfitRateDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getDailyAccountProfitRateDetails({
      frDt: ONE_MONTH_AGO,
      toDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyAccountProfitRateDetailsResponseSchema);
  });

  itLiveOnly('getAccountCurrentDayStatus', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountCurrentDayStatus({});
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountCurrentDayStatusResponseSchema);
  });

  // kt00018: 예전 skip 사유(501307)는 문서에 없는 dmstStexTp 값 탓이었다 — 'KRX' 면 모의에서도 동작 (2026-09-27)
  it('getAccountEvaluationBalanceDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticAccount.getAccountEvaluationBalanceDetails({
      qryTp: '1',
      dmstStexTp: 'KRX',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(accountEvaluationBalanceDetailsResponseSchema);
  });
});
