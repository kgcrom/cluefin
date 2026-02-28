import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticStockInfoEndpoints } from './metadata/domestic-stock-info';

export class DomesticStockInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticStockInfoEndpoints);
  }
}
