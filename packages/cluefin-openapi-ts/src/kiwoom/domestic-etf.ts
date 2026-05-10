import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticEtfMethodName, domesticEtfEndpoints } from './metadata/domestic-etf';

export type DomesticETF = KiwoomDomainBase & DomainMethods<DomesticEtfMethodName>;
export const DomesticETF = class DomesticETF extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticEtfEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticETF;
};
