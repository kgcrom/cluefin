import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, runIntegration } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

const BOND_CODE = 'KR2033022D33';

describe('KIS OnmarketBondBasicQuote', () => {
  it('getBondPrice', async () => {
    const client = await getKisClient();
    const res = await (client.onmarketBondBasicQuote as any).getBondPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondInfo', async () => {
    const client = await getKisClient();
    const res = await (client.onmarketBondBasicQuote as any).getBondInfo({
      pdno: BOND_CODE,
    });
    assertKisResponse(res);
  });
});
