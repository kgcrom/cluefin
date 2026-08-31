import type { DomainMethods } from '../core/types.js';
import type { NhplugClient } from './client.js';
import { NhplugDomainBase } from './domain-base.js';
import { type OverseasStockOrderMethodName, overseasStockOrderEndpoints } from './metadata/overseas-stock-order.js';
import type { OverseasStockOrderResponseMap } from './schemas/overseas-stock-order.js';

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
