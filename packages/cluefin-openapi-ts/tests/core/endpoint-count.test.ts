import { expect, test } from 'bun:test';

import { domesticBasicQuoteEndpoints } from '../../src/kis/metadata/domestic-basic-quote';
import { domesticStockInfoEndpoints as kisDomesticStockInfoEndpoints } from '../../src/kis/metadata/domestic-stock-info';
import { domesticChartEndpoints } from '../../src/kiwoom/metadata/domestic-chart';
import { domesticRankInfoEndpoints } from '../../src/kiwoom/metadata/domestic-rank-info';
import { domesticStockInfoEndpoints as kiwoomDomesticStockInfoEndpoints } from '../../src/kiwoom/metadata/domestic-stock-info';

test('v1 endpoint total should be 112', () => {
  const total =
    domesticBasicQuoteEndpoints.length +
    kisDomesticStockInfoEndpoints.length +
    domesticChartEndpoints.length +
    kiwoomDomesticStockInfoEndpoints.length +
    domesticRankInfoEndpoints.length;

  expect(total).toBe(112);
});
