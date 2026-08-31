import type { DomainMethods } from '../core/types.js';
import type { NhplugClient } from './client.js';
import { NhplugDomainBase } from './domain-base.js';
import { type KrstockQuoteMethodName, krstockQuoteEndpoints } from './metadata/krstock-quote.js';
import type { KrstockQuoteResponseMap } from './schemas/krstock-quote.js';

export type NhplugKrstockQuote = NhplugDomainBase & DomainMethods<KrstockQuoteMethodName, KrstockQuoteResponseMap>;
export const NhplugKrstockQuote = class NhplugKrstockQuote extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, krstockQuoteEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugKrstockQuote;
};
