import { describe, expect, it } from 'vitest';
import { z } from 'zod';
import { assertKisResponseShapeDeep, kisResponseShapeDiff } from '../_helpers/kis-response-shape';

const s = () => z.string().default('');

const schema = z
  .object({
    rt_cd: z.string().optional(),
    output1: z.array(z.object({ stck_prpr: s(), iscd1: s() })).default([]),
    output2: z.object({ total_cnt: s() }).optional(),
  })
  .passthrough();

const body = (overrides: Record<string, unknown> = {}) => ({
  rtCd: '0',
  output1: [{ stckPrpr: '100', iscd1: '005930' }],
  output2: { totalCnt: '1' },
  ...overrides,
});

const diff = (b: Record<string, unknown>) => kisResponseShapeDiff(b, schema.shape as never);

describe('kisResponseShapeDiff', () => {
  it('passes an exact match', () => {
    expect(diff(body())).toEqual([]);
  });

  it('reports a misnamed block as missing plus extra', () => {
    const { output1, ...rest } = body();
    expect(diff({ ...rest, output: output1 })).toEqual([
      'missing: output1 (schema declares it, server did not send it)',
      'extra: output (server sent it, schema does not declare it)',
    ]);
  });

  it('reports array/object mismatch', () => {
    expect(diff(body({ output2: [{ totalCnt: '1' }] }))).toEqual([
      'kind: output2 is array on the server, schema expects object',
    ]);
  });

  it('compares item keys over all rows', () => {
    const rows = [
      { stckPrpr: '1', iscd1: 'a' },
      { stckPrpr: '2', iscd1: 'b', iscd6: 'c' },
    ];
    expect(diff(body({ output1: rows }))).toEqual([
      'extra: output1.iscd6 (server sent it, schema does not declare it)',
    ]);
  });

  it('reports a nested key the server did not send', () => {
    expect(diff(body({ output2: {}, output1: [{ stckPrpr: '1' }] }))).toEqual([
      'missing: output1.iscd1 (schema declares it, server did not send it)',
    ]);
  });

  it('skips item keys of an empty array', () => {
    expect(diff(body({ output1: [] }))).toEqual([]);
  });
});

describe('assertKisResponseShapeDeep', () => {
  it('honours ignore paths', () => {
    const rows = [{ stckPrpr: '1', iscd1: 'a', iscd6: 'c' }];
    expect(() => assertKisResponseShapeDeep(body({ output1: rows }), schema)).toThrow();
    assertKisResponseShapeDeep(body({ output1: rows }), schema, ['output1.iscd6']);
  });
});
