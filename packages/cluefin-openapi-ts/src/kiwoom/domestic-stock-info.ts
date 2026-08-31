import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticStockInfoMethodName, domesticStockInfoEndpoints } from './metadata/domestic-stock-info.js';
import type { DomesticStockInfoResponseMap } from './schemas/domestic-stock-info.js';

export type DomesticStockInfo = KiwoomDomainBase &
  DomainMethods<DomesticStockInfoMethodName, DomesticStockInfoResponseMap>;
export const DomesticStockInfo = class DomesticStockInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticStockInfoEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticStockInfo;
};
