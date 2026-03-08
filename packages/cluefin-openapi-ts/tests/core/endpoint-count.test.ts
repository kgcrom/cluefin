import { expect, test } from 'vitest';

import { domesticBasicQuoteEndpoints } from '../../src/kis/metadata/domestic-basic-quote';
import { domesticStockInfoEndpoints as kisDomesticStockInfoEndpoints } from '../../src/kis/metadata/domestic-stock-info';
import { onmarketBondBasicQuoteEndpoints } from '../../src/kis/metadata/onmarket-bond-basic-quote';
import { overseasBasicQuoteEndpoints } from '../../src/kis/metadata/overseas-basic-quote';
import { domesticChartEndpoints } from '../../src/kiwoom/metadata/domestic-chart';
import { domesticRankInfoEndpoints } from '../../src/kiwoom/metadata/domestic-rank-info';
import { domesticStockInfoEndpoints as kiwoomDomesticStockInfoEndpoints } from '../../src/kiwoom/metadata/domestic-stock-info';

test('v1 endpoint total should be 132', () => {
  const total =
    domesticBasicQuoteEndpoints.length +
    kisDomesticStockInfoEndpoints.length +
    overseasBasicQuoteEndpoints.length +
    onmarketBondBasicQuoteEndpoints.length +
    domesticChartEndpoints.length +
    kiwoomDomesticStockInfoEndpoints.length +
    domesticRankInfoEndpoints.length;

  expect(total).toBe(132);
});
