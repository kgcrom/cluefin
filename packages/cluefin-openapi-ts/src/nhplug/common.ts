import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type CommonMethodName, commonEndpoints } from './metadata/common';
import type { CommonResponseMap } from './schemas/common';

export type NhplugCommon = NhplugDomainBase & DomainMethods<CommonMethodName, CommonResponseMap>;
export const NhplugCommon = class NhplugCommon extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, commonEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugCommon;
};
