import { describe, expect, test } from 'vitest';

import * as domesticBasicQuote from '../../../src/kis/schemas/domestic-basic-quote';
import * as domesticRankingAnalysis from '../../../src/kis/schemas/domestic-ranking-analysis';
import * as domesticStockInfo from '../../../src/kis/schemas/domestic-stock-info';
import * as onmarketBondBasicQuote from '../../../src/kis/schemas/onmarket-bond-basic-quote';
import * as overseasAccount from '../../../src/kis/schemas/overseas-account';
import * as overseasBasicQuote from '../../../src/kis/schemas/overseas-basic-quote';
import * as overseasMarketAnalysis from '../../../src/kis/schemas/overseas-market-analysis';

interface ParseableSchema {
  parse(input: unknown): unknown;
}

const envelope = {
  rt_cd: '0',
  msg_cd: '0000',
  msg1: 'OK',
};

const schemaGroups: Array<{ name: string; schemas: ParseableSchema[] }> = [
  {
    name: 'domestic basic quote',
    schemas: [
      domesticBasicQuote.getStockCurrentPriceResponseSchema,
      domesticBasicQuote.getStockCurrentPriceConclusionResponseSchema,
      domesticBasicQuote.getStockCurrentPriceAskingExpectedConclusionResponseSchema,
      domesticBasicQuote.getEtfComponentStockPriceResponseSchema,
      domesticBasicQuote.getEtfNavComparisonTimeTrendResponseSchema,
    ],
  },
  {
    name: 'domestic stock info',
    schemas: [
      domesticStockInfo.getProductBasicInfoResponseSchema,
      domesticStockInfo.getBalanceSheetResponseSchema,
      domesticStockInfo.getKsdDividendDecisionResponseSchema,
      domesticStockInfo.getKsdPaidInCapitalIncreaseScheduleResponseSchema,
      domesticStockInfo.getInvestmentOpinionByBrokerageResponseSchema,
    ],
  },
  {
    name: 'domestic ranking analysis',
    schemas: [
      domesticRankingAnalysis.getTradingVolumeRankResponseSchema,
      domesticRankingAnalysis.getStockFluctuationRankResponseSchema,
      domesticRankingAnalysis.getStockAfterHoursFluctuationRankResponseSchema,
      domesticRankingAnalysis.getStockAfterHoursVolumeRankResponseSchema,
      domesticRankingAnalysis.getHtsInquiryTop20ResponseSchema,
    ],
  },
  {
    name: 'overseas account',
    schemas: [
      overseasAccount.requestStockOrderResponseSchema,
      overseasAccount.getBuyTradableAmountResponseSchema,
      overseasAccount.getStockBalanceResponseSchema,
      overseasAccount.getDailyTransactionHistoryResponseSchema,
      overseasAccount.getLimitOrderExecutionHistoryResponseSchema,
    ],
  },
  {
    name: 'overseas market analysis',
    schemas: [
      overseasMarketAnalysis.getStockPriceFluctuationResponseSchema,
      overseasMarketAnalysis.getStockVolumeSurgeResponseSchema,
      overseasMarketAnalysis.getStockMarketCapRankResponseSchema,
      overseasMarketAnalysis.getStockCollateralLoanEligibleResponseSchema,
      overseasMarketAnalysis.getBreakingNewsTitleResponseSchema,
    ],
  },
  {
    name: 'overseas basic quote',
    schemas: [
      overseasBasicQuote.getStockCurrentPriceDetailResponseSchema,
      overseasBasicQuote.getStockCurrentPriceConclusionResponseSchema,
      overseasBasicQuote.getStockPeriodQuoteResponseSchema,
      overseasBasicQuote.getProductBaseInfoResponseSchema,
      overseasBasicQuote.getSectorCodesResponseSchema,
    ],
  },
  {
    name: 'onmarket bond basic quote',
    schemas: [
      onmarketBondBasicQuote.getBondAskingPriceResponseSchema,
      onmarketBondBasicQuote.getBondPriceResponseSchema,
      onmarketBondBasicQuote.getBondExecutionResponseSchema,
      onmarketBondBasicQuote.getBondAvgUnitPriceResponseSchema,
      onmarketBondBasicQuote.getBondIssueInfoResponseSchema,
    ],
  },
];

describe('KIS generated schema coverage smoke tests', () => {
  for (const group of schemaGroups) {
    test(`${group.name} response schemas accept a minimal KIS envelope`, () => {
      for (const schema of group.schemas) {
        expect(schema.parse(envelope)).toMatchObject(envelope);
      }
    });
  }
});
