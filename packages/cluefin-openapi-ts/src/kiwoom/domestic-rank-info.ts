import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticRankInfoEndpoints } from './metadata/domestic-rank-info';

export class DomesticRankInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticRankInfoEndpoints);
  }
}
