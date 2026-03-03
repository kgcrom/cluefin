import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticStockInfoEndpoints, type DomesticStockInfoMethodName } from './metadata/domestic-stock-info';

export interface DomesticStockInfo extends DomainMethods<DomesticStockInfoMethodName> {}
export class DomesticStockInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticStockInfoEndpoints);
  }
}
