import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticAccountEndpoints } from './metadata/domestic-account';

export class DomesticAccount extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticAccountEndpoints);
  }
}
