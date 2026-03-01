import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticOrderEndpoints } from './metadata/domestic-order';

export class DomesticOrder extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticOrderEndpoints);
  }
}
