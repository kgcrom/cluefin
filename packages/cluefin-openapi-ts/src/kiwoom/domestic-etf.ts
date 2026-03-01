import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticEtfEndpoints } from './metadata/domestic-etf';

export class DomesticETF extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticEtfEndpoints);
  }
}
