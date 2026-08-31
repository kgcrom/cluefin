import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import { type OverseasAccountMethodName, overseasAccountEndpoints } from './metadata/overseas-account.js';

export type OverseasAccount = KisDomainBase & DomainMethods<OverseasAccountMethodName>;
export const OverseasAccount = class OverseasAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasAccountEndpoints);
  }
} as {
  new (client: KisHttpClient): OverseasAccount;
};
