import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticStockInfoEndpoints, type DomesticStockInfoMethodName } from './metadata/domestic-stock-info';

export interface DomesticStockInfo extends DomainMethods<DomesticStockInfoMethodName> {}
export class DomesticStockInfo extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticStockInfoEndpoints);
  }
}
