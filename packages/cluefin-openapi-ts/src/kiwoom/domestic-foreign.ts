import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticForeignMethodName, domesticForeignEndpoints } from './metadata/domestic-foreign.js';
import type { DomesticForeignResponseMap } from './schemas/domestic-foreign.js';

export type DomesticForeign = KiwoomDomainBase & DomainMethods<DomesticForeignMethodName, DomesticForeignResponseMap>;
export const DomesticForeign = class DomesticForeign extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticForeignEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticForeign;
};
