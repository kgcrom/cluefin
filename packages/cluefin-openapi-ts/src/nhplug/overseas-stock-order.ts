import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type OverseasStockOrderMethodName, overseasStockOrderEndpoints } from './metadata/overseas-stock-order';
import type { OverseasStockOrderResponseMap } from './schemas/overseas-stock-order';

/** NH PLUG 해외주식(gbstock) 주문 API (`/gbstock/order/v1/*`). */
export type NhplugOverseasStockOrder = NhplugDomainBase &
  DomainMethods<OverseasStockOrderMethodName, OverseasStockOrderResponseMap>;
export const NhplugOverseasStockOrder = class NhplugOverseasStockOrder extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, overseasStockOrderEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugOverseasStockOrder;
};
