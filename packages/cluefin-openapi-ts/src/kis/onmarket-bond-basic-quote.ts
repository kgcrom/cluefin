import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  type OnmarketBondBasicQuoteMethodName,
  onmarketBondBasicQuoteEndpoints,
} from './metadata/onmarket-bond-basic-quote';

export type OnmarketBondBasicQuote = KisDomainBase & DomainMethods<OnmarketBondBasicQuoteMethodName>;
export const OnmarketBondBasicQuote = class OnmarketBondBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, onmarketBondBasicQuoteEndpoints);
  }
} as {
  new (client: KisHttpClient): OnmarketBondBasicQuote;
};
