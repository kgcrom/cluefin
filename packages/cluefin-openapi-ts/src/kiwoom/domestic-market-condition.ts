import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import {
  type DomesticMarketConditionMethodName,
  domesticMarketConditionEndpoints,
} from './metadata/domestic-market-condition';
import type { DomesticMarketConditionResponseMap } from './schemas/domestic-market-condition';

export type DomesticMarketCondition = KiwoomDomainBase &
  DomainMethods<DomesticMarketConditionMethodName, DomesticMarketConditionResponseMap>;
export const DomesticMarketCondition = class DomesticMarketCondition extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticMarketConditionEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticMarketCondition;
};
