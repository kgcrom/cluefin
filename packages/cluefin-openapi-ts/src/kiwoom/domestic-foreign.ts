import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticForeignMethodName, domesticForeignEndpoints } from './metadata/domestic-foreign';
import type { DomesticForeignResponseMap } from './schemas/domestic-foreign';

export interface DomesticForeign extends DomainMethods<DomesticForeignMethodName, DomesticForeignResponseMap> {}
export class DomesticForeign extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticForeignEndpoints);
  }
}
