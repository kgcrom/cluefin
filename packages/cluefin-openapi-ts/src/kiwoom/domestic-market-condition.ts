import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import {
  domesticMarketConditionEndpoints,
  type DomesticMarketConditionMethodName,
} from './metadata/domestic-market-condition';

export interface DomesticMarketCondition extends DomainMethods<DomesticMarketConditionMethodName> {}
export class DomesticMarketCondition extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticMarketConditionEndpoints);
  }
}
