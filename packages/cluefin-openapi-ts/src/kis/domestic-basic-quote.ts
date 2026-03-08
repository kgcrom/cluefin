import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type DomesticBasicQuoteMethodName, domesticBasicQuoteEndpoints } from './metadata/domestic-basic-quote';

export interface DomesticBasicQuote extends DomainMethods<DomesticBasicQuoteMethodName> {}
export class DomesticBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticBasicQuoteEndpoints);
  }
}
