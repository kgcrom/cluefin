import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticEtfEndpoints, type DomesticEtfMethodName } from './metadata/domestic-etf';

export interface DomesticETF extends DomainMethods<DomesticEtfMethodName> {}
export class DomesticETF extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticEtfEndpoints);
  }
}
