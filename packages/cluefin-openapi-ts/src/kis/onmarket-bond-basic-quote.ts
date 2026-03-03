import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  onmarketBondBasicQuoteEndpoints,
  type OnmarketBondBasicQuoteMethodName,
} from './metadata/onmarket-bond-basic-quote';

export interface OnmarketBondBasicQuote extends DomainMethods<OnmarketBondBasicQuoteMethodName> {}
export class OnmarketBondBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, onmarketBondBasicQuoteEndpoints);
  }
}
