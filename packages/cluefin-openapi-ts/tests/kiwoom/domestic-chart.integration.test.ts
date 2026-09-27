import { describe, test } from 'vitest';

import {
  individualStockInstitutionalChartResponseSchema,
  industryDailyResponseSchema,
  industryMinuteResponseSchema,
  industryMonthlyResponseSchema,
  industryTickResponseSchema,
  industryWeeklyResponseSchema,
  industryYearlyResponseSchema,
  intradayInvestorTradingResponseSchema,
  stockDailyResponseSchema,
  stockMinuteResponseSchema,
  stockMonthlyResponseSchema,
  stockTickResponseSchema,
  stockWeeklyResponseSchema,
  stockYearlyResponseSchema,
} from '../../src/kiwoom/schemas/domestic-chart';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  runIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticChart', () => {
  setupKiwoomRateLimit();
  it('getIndividualStockInstitutionalChart', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndividualStockInstitutionalChart({
      dt: TODAY,
      stkCd: SAMSUNG,
      amtQtyTp: '1',
      trdeTp: '0',
      unitTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(individualStockInstitutionalChartResponseSchema);
  });

  it('getIntradayInvestorTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIntradayInvestorTrading({
      mrktTp: '000',
      amtQtyTp: '1',
      trdeTp: '0',
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(intradayInvestorTradingResponseSchema);
  });

  it('getStockTick', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockTick({ stkCd: SAMSUNG, ticScope: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockTickResponseSchema);
  });

  it('getStockMinute', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockMinute({ stkCd: SAMSUNG, ticScope: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockMinuteResponseSchema);
  });

  it('getStockDaily', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockDaily({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockDailyResponseSchema);
  });

  it('getStockWeekly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockWeekly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockWeeklyResponseSchema);
  });

  it('getStockMonthly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockMonthly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockMonthlyResponseSchema);
  });

  it('getStockYearly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockYearly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockYearlyResponseSchema);
  });

  it('getIndustryTick', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryTick({ indsCd: '001', ticScope: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryTickResponseSchema);
  });

  it('getIndustryMinute', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryMinute({ indsCd: '001', ticScope: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryMinuteResponseSchema);
  });

  it('getIndustryDaily', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryDaily({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryDailyResponseSchema);
  });

  it('getIndustryWeekly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryWeekly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    // 실측: base_dt 는 YYYYMMDD 인데 문서 Length 가 3 — VENDOR_DOC_ERRATA.md
    assertKiwoomSpecConformance(industryWeeklyResponseSchema, { ignoreLength: ['base_dt'] });
  });

  it('getIndustryMonthly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryMonthly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryMonthlyResponseSchema);
  });

  it('getIndustryYearly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryYearly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryYearlyResponseSchema);
  });
});
