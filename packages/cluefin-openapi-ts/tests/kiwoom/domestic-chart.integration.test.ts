import { describe, test } from 'vitest';

import {
  individualStockInstitutionalChartItemSchema,
  individualStockInstitutionalChartResponseSchema,
  industryDailyItemSchema,
  industryDailyResponseSchema,
  industryMinuteItemSchema,
  industryMinuteResponseSchema,
  industryMonthlyItemSchema,
  industryMonthlyResponseSchema,
  industryTickItemSchema,
  industryTickResponseSchema,
  industryWeeklyItemSchema,
  industryWeeklyResponseSchema,
  industryYearlyItemSchema,
  industryYearlyResponseSchema,
  intradayInvestorTradingItemSchema,
  intradayInvestorTradingResponseSchema,
  stockDailyItemSchema,
  stockDailyResponseSchema,
  stockMinuteItemSchema,
  stockMinuteResponseSchema,
  stockMonthlyItemSchema,
  stockMonthlyResponseSchema,
  stockTickItemSchema,
  stockTickResponseSchema,
  stockWeeklyItemSchema,
  stockWeeklyResponseSchema,
  stockYearlyItemSchema,
  stockYearlyResponseSchema,
} from '../../src/kiwoom/schemas/domestic-chart';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  runIntegration,
  SAMSUNG,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticChart', () => {
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
    assertResponseShape(
      res.body,
      individualStockInstitutionalChartResponseSchema,
      'stkInvsrOrgnChart',
      individualStockInstitutionalChartItemSchema,
    );
  });

  it('getIntradayInvestorTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIntradayInvestorTrading({
      mrktTp: '0',
      amtQtyTp: '1',
      trdeTp: '0',
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      intradayInvestorTradingResponseSchema,
      'opmrInvsrTrdeChart',
      intradayInvestorTradingItemSchema,
    );
  });

  it('getStockTick', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockTick({ stkCd: SAMSUNG, ticScope: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockTickResponseSchema, 'stkTicChartQry', stockTickItemSchema);
  });

  it('getStockMinute', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockMinute({ stkCd: SAMSUNG, ticScope: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockMinuteResponseSchema, 'stkMinPoleChartQry', stockMinuteItemSchema);
  });

  it('getStockDaily', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockDaily({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockDailyResponseSchema, 'stkDtPoleChartQry', stockDailyItemSchema);
  });

  it('getStockWeekly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockWeekly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockWeeklyResponseSchema, 'stkStkPoleChartQry', stockWeeklyItemSchema);
  });

  it('getStockMonthly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockMonthly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockMonthlyResponseSchema, 'stkMthPoleChartQry', stockMonthlyItemSchema);
  });

  it('getStockYearly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockYearly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockYearlyResponseSchema, 'stkYrPoleChartQry', stockYearlyItemSchema);
  });

  it('getIndustryTick', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryTick({ indsCd: '001', ticScope: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryTickResponseSchema, 'indsTicChartQry', industryTickItemSchema);
  });

  it('getIndustryMinute', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryMinute({ indsCd: '001', ticScope: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryMinuteResponseSchema, 'indsMinPoleQry', industryMinuteItemSchema);
  });

  it('getIndustryDaily', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryDaily({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryDailyResponseSchema, 'indsDtPoleQry', industryDailyItemSchema);
  });

  it('getIndustryWeekly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryWeekly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryWeeklyResponseSchema, 'indsStkPoleQry', industryWeeklyItemSchema);
  });

  it('getIndustryMonthly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryMonthly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryMonthlyResponseSchema, 'indsMthPoleQry', industryMonthlyItemSchema);
  });

  it('getIndustryYearly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryYearly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryYearlyResponseSchema, 'indsYrPoleQry', industryYearlyItemSchema);
  });
});
