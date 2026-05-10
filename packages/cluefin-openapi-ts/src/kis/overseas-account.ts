import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type OverseasAccountMethodName, overseasAccountEndpoints } from './metadata/overseas-account';

export type OverseasAccount = KisDomainBase & DomainMethods<OverseasAccountMethodName>;
export const OverseasAccount = class OverseasAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasAccountEndpoints);
  }
} as {
  new (client: KisHttpClient): OverseasAccount;
};
