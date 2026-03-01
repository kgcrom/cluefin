import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticMarketConditionEndpoints } from './metadata/domestic-market-condition';

export class DomesticMarketCondition extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticMarketConditionEndpoints);
  }
}
