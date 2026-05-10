import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticAccountMethodName, domesticAccountEndpoints } from './metadata/domestic-account';
import type { DomesticAccountResponseMap } from './schemas/domestic-account';

export type DomesticAccount = KiwoomDomainBase & DomainMethods<DomesticAccountMethodName, DomesticAccountResponseMap>;
export const DomesticAccount = class DomesticAccount extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticAccountEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticAccount;
};
