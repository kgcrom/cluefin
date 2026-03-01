import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticAccountEndpoints } from './metadata/domestic-account';

export class DomesticAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticAccountEndpoints);
  }
}
