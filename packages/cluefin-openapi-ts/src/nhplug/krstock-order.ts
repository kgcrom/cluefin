import type { DomainMethods } from '../core/types.js';
import type { NhplugClient } from './client.js';
import { NhplugDomainBase } from './domain-base.js';
import { type KrstockOrderMethodName, krstockOrderEndpoints } from './metadata/krstock-order.js';
import type { KrstockOrderResponseMap } from './schemas/krstock-order.js';

export type NhplugKrstockOrder = NhplugDomainBase & DomainMethods<KrstockOrderMethodName, KrstockOrderResponseMap>;
export const NhplugKrstockOrder = class NhplugKrstockOrder extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, krstockOrderEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugKrstockOrder;
};
