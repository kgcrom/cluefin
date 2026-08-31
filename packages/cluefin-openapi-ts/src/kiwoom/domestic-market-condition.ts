import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import {
  type DomesticMarketConditionMethodName,
  domesticMarketConditionEndpoints,
} from './metadata/domestic-market-condition.js';
import type { DomesticMarketConditionResponseMap } from './schemas/domestic-market-condition.js';

export type DomesticMarketCondition = KiwoomDomainBase &
  DomainMethods<DomesticMarketConditionMethodName, DomesticMarketConditionResponseMap>;
export const DomesticMarketCondition = class DomesticMarketCondition extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticMarketConditionEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticMarketCondition;
};
