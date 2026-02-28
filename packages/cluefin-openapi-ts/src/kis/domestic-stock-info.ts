import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticStockInfoEndpoints } from './metadata/domestic-stock-info';

export class DomesticStockInfo extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticStockInfoEndpoints);
  }
}
