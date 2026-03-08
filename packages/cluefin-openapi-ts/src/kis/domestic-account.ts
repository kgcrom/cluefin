import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticAccountEndpoints, type DomesticAccountMethodName } from './metadata/domestic-account';

export interface DomesticAccount extends DomainMethods<DomesticAccountMethodName> {}
export class DomesticAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticAccountEndpoints);
  }
}
