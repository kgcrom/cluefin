import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, runIntegration } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS OverseasMarketAnalysis', () => {
  // TODO: KIS API 이슈로 비활성화 — Python 참조 코드에서도 동일하게 주석 처리됨 (404 반환)
  test.skip('getStockPriceFluctuation', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockPriceFluctuation({
      excd: 'NAS',
      gubn: '1',
      mixn: '0',
      volRang: '0',
    });
    assertKisResponse(res);
  });

  it('getStockMarketCapRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockMarketCapRank({
      excd: 'NAS',
      volRang: '0',
    });
    assertKisResponse(res);
  });

  it('getStockTradingVolumeRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingVolumeRank({
      excd: 'NAS',
      nday: '0',
      prc1: '0',
      prc2: '9999999',
      volRang: '0',
    });
    assertKisResponse(res);
  });
});
