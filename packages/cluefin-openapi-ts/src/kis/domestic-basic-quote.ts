import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticBasicQuoteEndpoints } from './metadata/domestic-basic-quote';

export class DomesticBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticBasicQuoteEndpoints);
  }
}
