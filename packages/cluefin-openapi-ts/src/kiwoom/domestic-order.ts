import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticOrderMethodName, domesticOrderEndpoints } from './metadata/domestic-order';

export interface DomesticOrder extends DomainMethods<DomesticOrderMethodName> {}
export class DomesticOrder extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticOrderEndpoints);
  }
}
