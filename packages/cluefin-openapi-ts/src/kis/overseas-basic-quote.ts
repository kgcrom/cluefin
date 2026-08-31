import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import { type OverseasBasicQuoteMethodName, overseasBasicQuoteEndpoints } from './metadata/overseas-basic-quote.js';

export type OverseasBasicQuote = KisDomainBase & DomainMethods<OverseasBasicQuoteMethodName>;
export const OverseasBasicQuote = class OverseasBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasBasicQuoteEndpoints);
  }
} as {
  new (client: KisHttpClient): OverseasBasicQuote;
};
