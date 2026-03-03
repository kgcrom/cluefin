import { describe, test } from 'vitest';
import { assertKiwoomResponse, getKiwoomClient, runIntegration, SAMSUNG, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticForeign', () => {
  it('getForeignInvestorTradingTrendByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticForeign.getForeignInvestorTradingTrendByStock({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getStockInstitution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticForeign.getStockInstitution({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getConsecutiveNetBuySellStatusByInstitutionForeigner', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticForeign.getConsecutiveNetBuySellStatusByInstitutionForeigner({ dt: TODAY, mrktTp: '0', stkIndsTp: '0', amtQtyTp: '1', stexTp: '1' });
    assertKiwoomResponse(res);
  });
});
