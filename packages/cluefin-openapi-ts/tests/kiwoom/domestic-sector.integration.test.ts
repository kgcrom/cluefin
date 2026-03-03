import { describe, test } from 'vitest';

import { assertKiwoomResponse, getKiwoomClient, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticSector', () => {
  it('getIndustryProgram', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryProgram({ stkCode: '001' });
    assertKiwoomResponse(res);
  });

  it('getIndustryInvestorNetBuy', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryInvestorNetBuy({
      mrktTp: '0',
      amtQtyTp: '1',
      baseDt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
  });

  it('getIndustryPriceBySector', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryPriceBySector({
      mrktTp: '0',
      indsCd: '001',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getAllIndustryIndex', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getAllIndustryIndex({ indsCd: '001' });
    assertKiwoomResponse(res);
  });

  it('getDailyIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getDailyIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
  });
});
