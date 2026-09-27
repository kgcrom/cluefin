import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import * as domestic from '../../src/kis/metadata/domestic-realtime-quote';
import * as bond from '../../src/kis/metadata/onmarket-bond-realtime-quote';
import * as overseas from '../../src/kis/metadata/overseas-realtime-quote';

// 실시간 응답은 '^' 로 이어진 값 목록이라 필드 이름은 순서로만 매겨진다. TS 목록은 손으로 옮긴 것이어서
// 순서가 어긋나도 개수만 맞으면 조용히 엉뚱한 필드에 값이 들어간다 (2026-09-27 H0BJASP0 채권호가).
// Python 목록을 기준으로 순서까지 대조한다.
const pythonKisDir = path.resolve(__dirname, '../../../cluefin-openapi/src/cluefin_openapi/kis');

function pythonFieldNames(file: string, name: string): string[] {
  const source = fs.readFileSync(path.join(pythonKisDir, file), 'utf8');
  const match = source.match(new RegExp(`^${name}\\s*(?::[^=]+)?=\\s*\\[([\\s\\S]*?)\\]`, 'm'));
  if (!match?.[1]) throw new Error(`${name} not found in ${file}`);
  return [...match[1].matchAll(/"([^"]+)"/g)].map((m) => m[1] as string);
}

const toCamel = (name: string) => name.replace(/_([a-z0-9])/g, (_, c: string) => c.toUpperCase());

const cases: [string, readonly string[], string][] = [
  ['EXECUTION_FIELD_NAMES', domestic.EXECUTION_FIELD_NAMES, '_domestic_realtime_quote_types.py'],
  ['ORDERBOOK_FIELD_NAMES', domestic.ORDERBOOK_FIELD_NAMES, '_domestic_realtime_quote_types.py'],
  [
    'EXECUTION_NOTIFICATION_FIELD_NAMES',
    domestic.EXECUTION_NOTIFICATION_FIELD_NAMES,
    '_domestic_realtime_quote_types.py',
  ],
  ['OVERSEAS_ORDERBOOK_FIELD_NAMES', overseas.OVERSEAS_ORDERBOOK_FIELD_NAMES, '_overseas_realtime_quote_types.py'],
  [
    'OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES',
    overseas.OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES,
    '_overseas_realtime_quote_types.py',
  ],
  ['OVERSEAS_EXECUTION_FIELD_NAMES', overseas.OVERSEAS_EXECUTION_FIELD_NAMES, '_overseas_realtime_quote_types.py'],
  [
    'OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES',
    overseas.OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES,
    '_overseas_realtime_quote_types.py',
  ],
  ['BOND_EXECUTION_FIELD_NAMES', bond.BOND_EXECUTION_FIELD_NAMES, '_onmarket_bond_realtime_quote_types.py'],
  ['BOND_ORDERBOOK_FIELD_NAMES', bond.BOND_ORDERBOOK_FIELD_NAMES, '_onmarket_bond_realtime_quote_types.py'],
  ['BOND_INDEX_EXECUTION_FIELD_NAMES', bond.BOND_INDEX_EXECUTION_FIELD_NAMES, '_onmarket_bond_realtime_quote_types.py'],
];

describe('KIS realtime field order matches Python', () => {
  it.each(cases)('%s', (name, tsFields, file) => {
    expect([...tsFields]).toEqual(pythonFieldNames(file, name).map(toCamel));
  });
});
