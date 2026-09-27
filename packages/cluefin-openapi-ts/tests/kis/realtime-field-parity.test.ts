import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import * as domestic from '../../src/kis/metadata/domestic-realtime-quote';
import * as bond from '../../src/kis/metadata/onmarket-bond-realtime-quote';
import * as overseas from '../../src/kis/metadata/overseas-realtime-quote';

// 실시간 응답은 '^' 로 이어진 값 목록이라 필드 이름은 순서로만 매겨진다. TS 목록은 손으로 옮긴 것이어서
// 순서가 어긋나도 개수만 맞으면 조용히 엉뚱한 필드에 값이 들어간다 (2026-09-27 H0BJASP0 채권호가).
// Python 목록을 기준으로 순서까지 대조한다.
const pythonSources = {
  domestic: fs.readFileSync(
    path.resolve(__dirname, '../../../cluefin-openapi/src/cluefin_openapi/kis/_domestic_realtime_quote_types.py'),
    'utf8',
  ),
  overseas: fs.readFileSync(
    path.resolve(__dirname, '../../../cluefin-openapi/src/cluefin_openapi/kis/_overseas_realtime_quote_types.py'),
    'utf8',
  ),
  bond: fs.readFileSync(
    path.resolve(__dirname, '../../../cluefin-openapi/src/cluefin_openapi/kis/_onmarket_bond_realtime_quote_types.py'),
    'utf8',
  ),
};

/** `NAME: list[str] = [ ... ]` 또는 `NAME = [ ... ]` 블록의 문자열 항목 */
function pythonFieldNames(source: string, name: string): string[] {
  const lines = source.split('\n');
  const start = lines.findIndex((line) => line.startsWith(`${name}:`) || line.startsWith(`${name} =`));
  if (start < 0) throw new Error(`${name} not found`);
  const end = lines.findIndex((line, i) => i > start && line.startsWith(']'));
  const block = lines.slice(start + 1, end).join('\n');
  return [...block.matchAll(/"([^"]+)"/g)].map((m) => m[1] as string);
}

const toCamel = (name: string) => name.replace(/_([a-z0-9])/g, (_, c: string) => c.toUpperCase());

const cases: [string, readonly string[], keyof typeof pythonSources][] = [
  ['EXECUTION_FIELD_NAMES', domestic.EXECUTION_FIELD_NAMES, 'domestic'],
  ['ORDERBOOK_FIELD_NAMES', domestic.ORDERBOOK_FIELD_NAMES, 'domestic'],
  ['EXECUTION_NOTIFICATION_FIELD_NAMES', domestic.EXECUTION_NOTIFICATION_FIELD_NAMES, 'domestic'],
  ['OVERSEAS_ORDERBOOK_FIELD_NAMES', overseas.OVERSEAS_ORDERBOOK_FIELD_NAMES, 'overseas'],
  ['OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES', overseas.OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES, 'overseas'],
  ['OVERSEAS_EXECUTION_FIELD_NAMES', overseas.OVERSEAS_EXECUTION_FIELD_NAMES, 'overseas'],
  ['OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES', overseas.OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES, 'overseas'],
  ['BOND_EXECUTION_FIELD_NAMES', bond.BOND_EXECUTION_FIELD_NAMES, 'bond'],
  ['BOND_ORDERBOOK_FIELD_NAMES', bond.BOND_ORDERBOOK_FIELD_NAMES, 'bond'],
  ['BOND_INDEX_EXECUTION_FIELD_NAMES', bond.BOND_INDEX_EXECUTION_FIELD_NAMES, 'bond'],
];

describe('KIS realtime field order matches Python', () => {
  it.each(cases)('%s', (name, tsFields, source) => {
    expect([...tsFields]).toEqual(pythonFieldNames(pythonSources[source], name).map(toCamel));
  });
});
