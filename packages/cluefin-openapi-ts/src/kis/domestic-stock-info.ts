import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type DomesticStockInfoMethodName, domesticStockInfoEndpoints } from './metadata/domestic-stock-info';

export interface DomesticStockInfo extends DomainMethods<DomesticStockInfoMethodName> {}
export class DomesticStockInfo extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticStockInfoEndpoints);
  }
}
