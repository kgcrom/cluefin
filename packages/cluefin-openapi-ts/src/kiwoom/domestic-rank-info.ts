import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticRankInfoMethodName, domesticRankInfoEndpoints } from './metadata/domestic-rank-info';
import type { DomesticRankInfoResponseMap } from './schemas/domestic-rank-info';

export type DomesticRankInfo = KiwoomDomainBase &
  DomainMethods<DomesticRankInfoMethodName, DomesticRankInfoResponseMap>;
export const DomesticRankInfo = class DomesticRankInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticRankInfoEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticRankInfo;
};
