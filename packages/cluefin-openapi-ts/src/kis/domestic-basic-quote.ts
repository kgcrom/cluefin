import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import { type DomesticBasicQuoteMethodName, domesticBasicQuoteEndpoints } from './metadata/domestic-basic-quote.js';

export type DomesticBasicQuote = KisDomainBase & DomainMethods<DomesticBasicQuoteMethodName>;
export const DomesticBasicQuote = class DomesticBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticBasicQuoteEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticBasicQuote;
};
