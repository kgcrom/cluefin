import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  type OnmarketBondBasicQuoteMethodName,
  onmarketBondBasicQuoteEndpoints,
} from './metadata/onmarket-bond-basic-quote';

export interface OnmarketBondBasicQuote extends DomainMethods<OnmarketBondBasicQuoteMethodName> {}
export class OnmarketBondBasicQuote extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, onmarketBondBasicQuoteEndpoints);
  }
}
