import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticStockInfoMethodName, domesticStockInfoEndpoints } from './metadata/domestic-stock-info';
import type { DomesticStockInfoResponseMap } from './schemas/domestic-stock-info';

export type DomesticStockInfo = KiwoomDomainBase &
  DomainMethods<DomesticStockInfoMethodName, DomesticStockInfoResponseMap>;
export const DomesticStockInfo = class DomesticStockInfo extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticStockInfoEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticStockInfo;
};
