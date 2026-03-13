import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticAccountMethodName, domesticAccountEndpoints } from './metadata/domestic-account';
import type { DomesticAccountResponseMap } from './schemas/domestic-account';

export interface DomesticAccount extends DomainMethods<DomesticAccountMethodName, DomesticAccountResponseMap> {}
export class DomesticAccount extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticAccountEndpoints);
  }
}
