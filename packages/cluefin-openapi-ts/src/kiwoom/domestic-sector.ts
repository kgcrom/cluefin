import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticSectorEndpoints } from './metadata/domestic-sector';

export class DomesticSector extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticSectorEndpoints);
  }
}
