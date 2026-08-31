import type { DomainMethods } from '../core/types.js';
import type { NhplugClient } from './client.js';
import { NhplugDomainBase } from './domain-base.js';
import { type CommonMethodName, commonEndpoints } from './metadata/common.js';
import type { CommonResponseMap } from './schemas/common.js';

export type NhplugCommon = NhplugDomainBase & DomainMethods<CommonMethodName, CommonResponseMap>;
export const NhplugCommon = class NhplugCommon extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, commonEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugCommon;
};
