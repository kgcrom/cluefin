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

test('root barrel exposes runtime exports from core, KIS, and Kiwoom modules', () => {
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
});
