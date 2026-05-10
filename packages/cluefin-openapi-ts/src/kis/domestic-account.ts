import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type DomesticAccountMethodName, domesticAccountEndpoints } from './metadata/domestic-account';

export type DomesticAccount = KisDomainBase & DomainMethods<DomesticAccountMethodName>;
export const DomesticAccount = class DomesticAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticAccountEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticAccount;
};
