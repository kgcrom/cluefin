import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import { type DomesticAccountMethodName, domesticAccountEndpoints } from './metadata/domestic-account.js';

export type DomesticAccount = KisDomainBase & DomainMethods<DomesticAccountMethodName>;
export const DomesticAccount = class DomesticAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticAccountEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticAccount;
};
