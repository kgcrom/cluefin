import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type OverseasBasicQuoteMethodName, overseasBasicQuoteEndpoints } from './metadata/overseas-basic-quote';

export interface OverseasBasicQuote extends DomainMethods<OverseasBasicQuoteMethodName> {}
export class OverseasBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasBasicQuoteEndpoints);
  }
}
