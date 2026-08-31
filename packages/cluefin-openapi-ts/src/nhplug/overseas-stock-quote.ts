import type { DomainMethods } from '../core/types.js';
import type { NhplugClient } from './client.js';
import { NhplugDomainBase } from './domain-base.js';
import { type OverseasStockQuoteMethodName, overseasStockQuoteEndpoints } from './metadata/overseas-stock-quote.js';
import type { OverseasStockQuoteResponseMap } from './schemas/overseas-stock-quote.js';

/** NH PLUG 해외주식(gbstock) 시세 API (`/gbstock/quote/v1/*`). */
export type NhplugOverseasStockQuote = NhplugDomainBase &
  DomainMethods<OverseasStockQuoteMethodName, OverseasStockQuoteResponseMap>;
export const NhplugOverseasStockQuote = class NhplugOverseasStockQuote extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, overseasStockQuoteEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugOverseasStockQuote;
};
