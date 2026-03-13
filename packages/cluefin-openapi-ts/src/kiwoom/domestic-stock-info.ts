import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticStockInfoMethodName, domesticStockInfoEndpoints } from './metadata/domestic-stock-info';
import type { DomesticStockInfoResponseMap } from './schemas/domestic-stock-info';

export interface DomesticStockInfo extends DomainMethods<DomesticStockInfoMethodName, DomesticStockInfoResponseMap> {}
export class DomesticStockInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticStockInfoEndpoints);
  }
}
