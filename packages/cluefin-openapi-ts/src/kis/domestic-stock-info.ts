import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import { type DomesticStockInfoMethodName, domesticStockInfoEndpoints } from './metadata/domestic-stock-info.js';

export type DomesticStockInfo = KisDomainBase & DomainMethods<DomesticStockInfoMethodName>;
export const DomesticStockInfo = class DomesticStockInfo extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticStockInfoEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticStockInfo;
};
