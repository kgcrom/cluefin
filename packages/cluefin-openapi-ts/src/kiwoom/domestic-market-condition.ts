import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import {
  type DomesticMarketConditionMethodName,
  domesticMarketConditionEndpoints,
} from './metadata/domestic-market-condition';
import type { DomesticMarketConditionResponseMap } from './schemas/domestic-market-condition';

export interface DomesticMarketCondition
  extends DomainMethods<DomesticMarketConditionMethodName, DomesticMarketConditionResponseMap> {}
export class DomesticMarketCondition extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticMarketConditionEndpoints);
  }
}
