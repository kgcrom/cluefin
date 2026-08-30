import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type KrstockQuoteMethodName, krstockQuoteEndpoints } from './metadata/krstock-quote';
import type { KrstockQuoteResponseMap } from './schemas/krstock-quote';

export type NhplugKrstockQuote = NhplugDomainBase & DomainMethods<KrstockQuoteMethodName, KrstockQuoteResponseMap>;
export const NhplugKrstockQuote = class NhplugKrstockQuote extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, krstockQuoteEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugKrstockQuote;
};
