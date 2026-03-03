import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { overseasBasicQuoteEndpoints, type OverseasBasicQuoteMethodName } from './metadata/overseas-basic-quote';

export interface OverseasBasicQuote extends DomainMethods<OverseasBasicQuoteMethodName> {}
export class OverseasBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasBasicQuoteEndpoints);
  }
}
