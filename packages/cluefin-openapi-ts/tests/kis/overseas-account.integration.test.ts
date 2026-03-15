import { describe, test } from 'vitest';
import {
  getBalanceBySettlementOutput1ItemSchema,
  getBalanceBySettlementOutput2ItemSchema,
  getBalanceBySettlementResponseSchema,
  getBuyTradableAmountResponseSchema,
  getCurrentBalanceByConclusionOutput1ItemSchema,
  getCurrentBalanceByConclusionOutput2ItemSchema,
  getCurrentBalanceByConclusionResponseSchema,
  getDailyTransactionHistoryItemSchema,
  getDailyTransactionHistoryResponseSchema,
  getLimitOrderExecutionHistoryOutput1ItemSchema,
  getLimitOrderExecutionHistoryOutput3ItemSchema,
  getLimitOrderExecutionHistoryResponseSchema,
  getLimitOrderNumberItemSchema,
  getLimitOrderNumberResponseSchema,
  getMarginAggregateItemSchema,
  getMarginAggregateResponseSchema,
  getPeriodProfitLossOutputItemSchema,
  getPeriodProfitLossResponseSchema,
  getReserveOrdersResponseSchema,
  getStockBalanceOutput1ItemSchema,
  getStockBalanceResponseSchema,
  getStockConclusionHistoryItemSchema,
  getStockConclusionHistoryResponseSchema,
  getStockNotConclusionHistoryItemSchema,
  getStockNotConclusionHistoryResponseSchema,
} from '../../src/kis/schemas/overseas-account';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  KIS_ACNT_PRDT_CD,
  KIS_CANO,
  ONE_MONTH_AGO,
  runAccountIntegration,
  TODAY,
} from '../_helpers/integration-setup';

const it = runAccountIntegration ? test : test.skip;

describe('KIS OverseasAccount', () => {
  it('getBuyTradableAmount', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getBuyTradableAmount({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      ovrsOrdUnpr: '150',
      itemCd: 'AAPL',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBuyTradableAmountResponseSchema);
  });

  it('getStockBalance', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockBalance({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      trCrcyCd: 'USD',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockBalanceResponseSchema);
    assertResponseShape(res.body, getStockBalanceResponseSchema, 'output1', getStockBalanceOutput1ItemSchema);
  });

  it('getStockNotConclusionHistory', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockNotConclusionHistory({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      sortSqn: 'DS',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockNotConclusionHistoryResponseSchema,
      'output',
      getStockNotConclusionHistoryItemSchema,
    );
  });

  it('getStockConclusionHistory', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockConclusionHistory({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      pdno: '%',
      ordStrtDt: ONE_MONTH_AGO,
      ordEndDt: TODAY,
      sllBuyDvsn: '0',
      ccldNccsDvsn: '0',
      ovrsExcgCd: 'NASD',
      sortSqn: 'DS',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockConclusionHistoryResponseSchema,
      'output',
      getStockConclusionHistoryItemSchema,
    );
  });

  it('getCurrentBalanceByConclusion', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getCurrentBalanceByConclusion({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      wcrcFrcrDvsnCd: '02',
      natnCd: '840',
      trMketCd: '00',
      inqrDvsnCd: '00',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getCurrentBalanceByConclusionResponseSchema);
    assertResponseShape(
      res.body,
      getCurrentBalanceByConclusionResponseSchema,
      'output1',
      getCurrentBalanceByConclusionOutput1ItemSchema,
    );
    assertResponseShape(
      res.body,
      getCurrentBalanceByConclusionResponseSchema,
      'output2',
      getCurrentBalanceByConclusionOutput2ItemSchema,
    );
  });

  it('getReserveOrders', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getReserveOrders({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      inqrStrtDt: ONE_MONTH_AGO,
      inqrEndDt: TODAY,
      inqrDvsnCd: '0',
      prdtTypeCd: '512',
      ovrsExcgCd: 'NASD',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getReserveOrdersResponseSchema);
  });

  it('getBalanceBySettlement', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getBalanceBySettlement({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      bassDt: TODAY,
      wcrcFrcrDvsnCd: '02',
      inqrDvsnCd: '00',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBalanceBySettlementResponseSchema);
    assertResponseShape(
      res.body,
      getBalanceBySettlementResponseSchema,
      'output1',
      getBalanceBySettlementOutput1ItemSchema,
    );
    assertResponseShape(
      res.body,
      getBalanceBySettlementResponseSchema,
      'output2',
      getBalanceBySettlementOutput2ItemSchema,
    );
  });

  it('getDailyTransactionHistory', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getDailyTransactionHistory({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      erlmStrtDt: ONE_MONTH_AGO,
      erlmEndDt: TODAY,
      ovrsExcgCd: 'NASD',
      pdno: '%',
      sllBuyDvsnCd: '0',
      loanDvsnCd: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getDailyTransactionHistoryResponseSchema,
      'output',
      getDailyTransactionHistoryItemSchema,
    );
  });

  it('getPeriodProfitLoss', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getPeriodProfitLoss({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      natnCd: '840',
      crcyCd: 'USD',
      pdno: '%',
      inqrStrtDt: ONE_MONTH_AGO,
      inqrEndDt: TODAY,
      wcrcFrcrDvsnCd: '02',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getPeriodProfitLossResponseSchema);
    assertResponseShape(res.body, getPeriodProfitLossResponseSchema, 'output', getPeriodProfitLossOutputItemSchema);
  });

  it('getMarginAggregate', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getMarginAggregate({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getMarginAggregateResponseSchema, 'output', getMarginAggregateItemSchema);
  });

  it('getLimitOrderNumber', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getLimitOrderNumber({
      tradDt: TODAY,
      cano: KIS_CANO,
      acnoPrdtCd: KIS_ACNT_PRDT_CD,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getLimitOrderNumberResponseSchema, 'output', getLimitOrderNumberItemSchema);
  });

  it('getLimitOrderExecutionHistory', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getLimitOrderExecutionHistory({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ordDt: TODAY,
      odno: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getLimitOrderExecutionHistoryResponseSchema);
    assertResponseShape(
      res.body,
      getLimitOrderExecutionHistoryResponseSchema,
      'output1',
      getLimitOrderExecutionHistoryOutput1ItemSchema,
    );
    assertResponseShape(
      res.body,
      getLimitOrderExecutionHistoryResponseSchema,
      'output3',
      getLimitOrderExecutionHistoryOutput3ItemSchema,
    );
  });
});
