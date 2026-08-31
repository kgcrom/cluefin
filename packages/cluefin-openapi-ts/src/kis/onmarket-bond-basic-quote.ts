import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import {
  type OnmarketBondBasicQuoteMethodName,
  onmarketBondBasicQuoteEndpoints,
} from './metadata/onmarket-bond-basic-quote.js';

export type OnmarketBondBasicQuote = KisDomainBase & DomainMethods<OnmarketBondBasicQuoteMethodName>;
export const OnmarketBondBasicQuote = class OnmarketBondBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, onmarketBondBasicQuoteEndpoints);
  }
} as {
  new (client: KisHttpClient): OnmarketBondBasicQuote;
};
