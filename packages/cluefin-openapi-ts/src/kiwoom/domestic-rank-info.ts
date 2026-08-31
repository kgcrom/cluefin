import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticRankInfoMethodName, domesticRankInfoEndpoints } from './metadata/domestic-rank-info.js';
import type { DomesticRankInfoResponseMap } from './schemas/domestic-rank-info.js';

export type DomesticRankInfo = KiwoomDomainBase &
  DomainMethods<DomesticRankInfoMethodName, DomesticRankInfoResponseMap>;
export const DomesticRankInfo = class DomesticRankInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticRankInfoEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticRankInfo;
};
