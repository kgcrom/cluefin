import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticOrderMethodName, domesticOrderEndpoints } from './metadata/domestic-order.js';

export type DomesticOrder = KiwoomDomainBase & DomainMethods<DomesticOrderMethodName>;
export const DomesticOrder = class DomesticOrder extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticOrderEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticOrder;
};
