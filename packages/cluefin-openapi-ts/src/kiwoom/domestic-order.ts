import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticOrderMethodName, domesticOrderEndpoints } from './metadata/domestic-order';

export type DomesticOrder = KiwoomDomainBase & DomainMethods<DomesticOrderMethodName>;
export const DomesticOrder = class DomesticOrder extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticOrderEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticOrder;
};
