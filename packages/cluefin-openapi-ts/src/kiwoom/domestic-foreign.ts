import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticForeignEndpoints, type DomesticForeignMethodName } from './metadata/domestic-foreign';

export interface DomesticForeign extends DomainMethods<DomesticForeignMethodName> {}
export class DomesticForeign extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticForeignEndpoints);
  }
}
