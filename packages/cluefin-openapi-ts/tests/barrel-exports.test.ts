import { expect, test } from 'vitest';

import * as Root from '../src';
import { BaseWebSocketClient } from '../src/core/websocket';
import * as Kis from '../src/kis';
import { KisAuth } from '../src/kis/auth';
import { KisHttpClient } from '../src/kis/http-client';
import { FileTokenCacheStore, MemoryTokenCacheStore } from '../src/kis/token-cache';
import * as Kiwoom from '../src/kiwoom';
import { KiwoomAuth } from '../src/kiwoom/auth';
import { KiwoomClient } from '../src/kiwoom/client';
import * as Nhplug from '../src/nhplug';
import { NhplugAuth } from '../src/nhplug/auth';
import { NhplugClient } from '../src/nhplug/client';
import { NhplugDomainBase } from '../src/nhplug/domain-base';
import { FileTokenCacheStore as NhplugFileTokenCacheStore } from '../src/nhplug/token-cache';

test('root barrel exposes runtime exports from core, KIS, Kiwoom, and NH PLUG modules', () => {
  expect(Root.BaseWebSocketClient).toBe(BaseWebSocketClient);

  expect(Root.KisAuth).toBe(KisAuth);
  expect(Root.KisAuth).toBe(Kis.KisAuth);
  expect(Root.KisHttpClient).toBe(KisHttpClient);
  expect(Root.KisHttpClient).toBe(Kis.KisHttpClient);
  expect(Root.MemoryTokenCacheStore).toBe(MemoryTokenCacheStore);
  expect(Root.MemoryTokenCacheStore).toBe(Kis.MemoryTokenCacheStore);
  expect(Root.FileTokenCacheStore).toBe(FileTokenCacheStore);
  expect(Root.FileTokenCacheStore).toBe(Kis.FileTokenCacheStore);

  expect(Root.KiwoomAuth).toBe(KiwoomAuth);
  expect(Root.KiwoomAuth).toBe(Kiwoom.KiwoomAuth);
  expect(Root.KiwoomClient).toBe(KiwoomClient);
  expect(Root.KiwoomClient).toBe(Kiwoom.KiwoomClient);

  expect(Root.NhplugAuth).toBe(NhplugAuth);
  expect(Root.NhplugAuth).toBe(Nhplug.NhplugAuth);
  expect(Root.NhplugClient).toBe(NhplugClient);
  expect(Root.NhplugClient).toBe(Nhplug.NhplugClient);
  expect(Root.NhplugDomainBase).toBe(NhplugDomainBase);
  // NH PLUG 토큰 캐시는 KIS 와 이름이 겹쳐 Nhplug 접두사로 재수출한다.
  expect(Root.NhplugFileTokenCacheStore).toBe(NhplugFileTokenCacheStore);
  expect(Root.NhplugFileTokenCacheStore).not.toBe(FileTokenCacheStore);
  expect(Root.NHPLUG_SUCCESS_RSP_CODES).toEqual(['00000', 'XA102']);
});
