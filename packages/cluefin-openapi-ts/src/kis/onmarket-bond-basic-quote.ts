import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { onmarketBondBasicQuoteEndpoints } from './metadata/onmarket-bond-basic-quote';

export class OnmarketBondBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, onmarketBondBasicQuoteEndpoints);
  }
}
