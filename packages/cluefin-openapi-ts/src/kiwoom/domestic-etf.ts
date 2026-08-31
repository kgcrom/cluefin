import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticEtfMethodName, domesticEtfEndpoints } from './metadata/domestic-etf.js';

export type DomesticETF = KiwoomDomainBase & DomainMethods<DomesticEtfMethodName>;
export const DomesticETF = class DomesticETF extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticEtfEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticETF;
};
