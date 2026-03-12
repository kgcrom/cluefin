import { describe, test } from 'vitest';
import { getKiwoomClient, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Capture DomesticSector responses', () => {
  it('capture all sector responses', async () => {
    const client = await getKiwoomClient();

    const calls = [
      ['getIndustryProgram', { stkCode: '001' }],
      ['getIndustryInvestorNetBuy', { mrktTp: '0', amtQtyTp: '1', baseDt: TODAY, stexTp: '1' }],
      ['getIndustryCurrentPrice', { mrktTp: '0', indsCd: '001' }],
      ['getIndustryPriceBySector', { mrktTp: '0', indsCd: '001', stexTp: '1' }],
      ['getAllIndustryIndex', { indsCd: '001' }],
      ['getDailyIndustryCurrentPrice', { mrktTp: '0', indsCd: '001' }],
    ] as const;

    for (const [method, params] of calls) {
      const fn = (client.domesticSector as Record<string, Function>)[method];
      const res = await fn.call(client.domesticSector, params);
      console.log(`\n=== ${method} ===`);
      console.log(JSON.stringify(res.body, null, 2));
    }
  }, 120000);
});
