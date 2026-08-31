import type { DomainMethods } from '../core/types.js';
import type { NhplugClient } from './client.js';
import { NhplugDomainBase } from './domain-base.js';
import { type KrstockInquiryMethodName, krstockInquiryEndpoints } from './metadata/krstock-inquiry.js';
import type { KrstockInquiryResponseMap } from './schemas/krstock-inquiry.js';

export type NhplugKrstockInquiry = NhplugDomainBase &
  DomainMethods<KrstockInquiryMethodName, KrstockInquiryResponseMap>;
export const NhplugKrstockInquiry = class NhplugKrstockInquiry extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, krstockInquiryEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugKrstockInquiry;
};
