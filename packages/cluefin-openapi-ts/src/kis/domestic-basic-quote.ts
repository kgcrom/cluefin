import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type DomesticBasicQuoteMethodName, domesticBasicQuoteEndpoints } from './metadata/domestic-basic-quote';

export type DomesticBasicQuote = KisDomainBase & DomainMethods<DomesticBasicQuoteMethodName>;
export const DomesticBasicQuote = class DomesticBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticBasicQuoteEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticBasicQuote;
};
