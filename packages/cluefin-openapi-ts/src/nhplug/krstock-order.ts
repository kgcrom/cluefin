import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type KrstockOrderMethodName, krstockOrderEndpoints } from './metadata/krstock-order';
import type { KrstockOrderResponseMap } from './schemas/krstock-order';

export type NhplugKrstockOrder = NhplugDomainBase & DomainMethods<KrstockOrderMethodName, KrstockOrderResponseMap>;
export const NhplugKrstockOrder = class NhplugKrstockOrder extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, krstockOrderEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugKrstockOrder;
};
