import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type OverseasStockQuoteMethodName, overseasStockQuoteEndpoints } from './metadata/overseas-stock-quote';
import type { OverseasStockQuoteResponseMap } from './schemas/overseas-stock-quote';

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
