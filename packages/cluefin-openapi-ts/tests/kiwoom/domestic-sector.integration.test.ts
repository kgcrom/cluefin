import { describe, test } from 'vitest';

import { assertKiwoomResponse, getKiwoomClient, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticSector', () => {
  it('getIndustryProgram', async () => {
    const client = await getKiwoomClient();
    const res = await (client.domesticSector as any).getIndustryProgram({ stkCode: '001' });
    assertKiwoomResponse(res);
  });

  it('getIndustryInvestorNetBuy', async () => {
    const client = await getKiwoomClient();
    const res = await (client.domesticSector as any).getIndustryInvestorNetBuy({
      mrktTp: '0',
      amtQtyTp: '1',
      baseDt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await (client.domesticSector as any).getIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
  });

  it('getIndustryPriceBySector', async () => {
    const client = await getKiwoomClient();
    const res = await (client.domesticSector as any).getIndustryPriceBySector({
      mrktTp: '0',
      indsCd: '001',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getAllIndustryIndex', async () => {
    const client = await getKiwoomClient();
    const res = await (client.domesticSector as any).getAllIndustryIndex({ indsCd: '001' });
    assertKiwoomResponse(res);
  });

  it('getDailyIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await (client.domesticSector as any).getDailyIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
  });
});
