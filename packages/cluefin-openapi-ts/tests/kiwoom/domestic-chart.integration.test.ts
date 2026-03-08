import { describe, test } from 'vitest';
import { assertKiwoomResponse, getKiwoomClient, runIntegration, SAMSUNG, TODAY } from '../_helpers/integration-setup';

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
  });

  it('getStockTick', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockTick({ stkCd: SAMSUNG, ticScope: '1' });
    assertKiwoomResponse(res);
  });

  it('getStockMinute', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockMinute({ stkCd: SAMSUNG, ticScope: '1' });
    assertKiwoomResponse(res);
  });

  it('getStockDaily', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockDaily({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
  });

  it('getStockWeekly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockWeekly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
  });

  it('getStockMonthly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockMonthly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
  });

  it('getStockYearly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getStockYearly({ stkCd: SAMSUNG, baseDt: TODAY, updStkpcTp: '1' });
    assertKiwoomResponse(res);
  });

  it('getIndustryTick', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryTick({ indsCd: '001', ticScope: '1' });
    assertKiwoomResponse(res);
  });

  it('getIndustryMinute', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryMinute({ indsCd: '001', ticScope: '1' });
    assertKiwoomResponse(res);
  });

  it('getIndustryDaily', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryDaily({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
  });

  it('getIndustryWeekly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryWeekly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
  });

  it('getIndustryMonthly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryMonthly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
  });

  it('getIndustryYearly', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticChart.getIndustryYearly({ indsCd: '001', baseDt: TODAY });
    assertKiwoomResponse(res);
  });
});
