import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticForeignEndpoints } from './metadata/domestic-foreign';

export class DomesticForeign extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticForeignEndpoints);
  }
}
