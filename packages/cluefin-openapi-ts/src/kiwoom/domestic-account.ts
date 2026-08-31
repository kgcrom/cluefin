import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticAccountMethodName, domesticAccountEndpoints } from './metadata/domestic-account.js';
import type { DomesticAccountResponseMap } from './schemas/domestic-account.js';

export type DomesticAccount = KiwoomDomainBase & DomainMethods<DomesticAccountMethodName, DomesticAccountResponseMap>;
export const DomesticAccount = class DomesticAccount extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticAccountEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticAccount;
};
