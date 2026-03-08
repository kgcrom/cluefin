import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { overseasAccountEndpoints, type OverseasAccountMethodName } from './metadata/overseas-account';

export interface OverseasAccount extends DomainMethods<OverseasAccountMethodName> {}
export class OverseasAccount extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasAccountEndpoints);
  }
}
