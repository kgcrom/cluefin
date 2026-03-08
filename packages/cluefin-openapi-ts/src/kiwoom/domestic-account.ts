import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticAccountMethodName, domesticAccountEndpoints } from './metadata/domestic-account';

export interface DomesticAccount extends DomainMethods<DomesticAccountMethodName> {}
export class DomesticAccount extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticAccountEndpoints);
  }
}
