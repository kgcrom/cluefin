import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { overseasBasicQuoteEndpoints } from './metadata/overseas-basic-quote';

export class OverseasBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasBasicQuoteEndpoints);
  }
}
