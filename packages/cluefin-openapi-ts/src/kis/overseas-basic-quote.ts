import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type OverseasBasicQuoteMethodName, overseasBasicQuoteEndpoints } from './metadata/overseas-basic-quote';

export type OverseasBasicQuote = KisDomainBase & DomainMethods<OverseasBasicQuoteMethodName>;
export const OverseasBasicQuote = class OverseasBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasBasicQuoteEndpoints);
  }
} as {
  new (client: KisHttpClient): OverseasBasicQuote;
};
