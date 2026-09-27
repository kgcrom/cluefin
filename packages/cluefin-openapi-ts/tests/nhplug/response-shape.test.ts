import { describe, expect, it } from 'vitest';
import { z } from 'zod';
import {
  assertNhplugMatchesSpec,
  nhplugLengthViolations,
  nhplugResponseShapeDiff,
  valueLength,
} from '../_helpers/nhplug-response-shape';

const num = () => z.preprocess((v) => (v === '' ? null : v), z.coerce.number().nullish()).nullish();
const summary = z.object({ total: num() }).passthrough();

const schema = z
  .object({
    rsp_cd: z.string().nullish(),
    rsp_msg: z.string().nullish(),
    message: z.object({ msg_code: z.string().nullish() }).nullish(),
    Output_0: summary.nullish(),
    Output_1: z.array(z.object({ iem_cd: z.string(), iem_nm: z.string().nullish() }).passthrough()).nullish(),
  })
  .passthrough();

const eitherSchema = z.object({
  rsp_cd: z.string().nullish(),
  rsp_msg: z.string().nullish(),
  Output_0: z.union([summary, z.array(summary)]).nullish(),
});

const body = (overrides: Record<string, unknown> = {}) => ({
  rspCd: '00000',
  rspMsg: 'ok',
  output0: { total: 1 },
  output1: [{ iemCd: '005930', iemNm: '삼성전자' }],
  ...overrides,
});

const diff = (b: Record<string, unknown>, s: z.ZodObject<z.ZodRawShape> = schema) =>
  nhplugResponseShapeDiff(b, s.shape as never);

describe('nhplugResponseShapeDiff', () => {
  it('passes an exact match', () => {
    expect(diff(body())).toEqual([]);
  });

  it('allows omitted top-level Output blocks and message', () => {
    const { output1: _, ...rest } = body();
    expect(diff(rest)).toEqual([]);
  });

  it('reports an omitted envelope key', () => {
    const { rspMsg: _, ...rest } = body();
    expect(diff(rest)).toEqual(['missing: rsp_msg (schema declares it, server did not send it)']);
  });

  it('reports a misnamed block as extra', () => {
    const { output1, ...rest } = body();
    expect(diff({ ...rest, output2: output1 })).toEqual([
      'extra: output2 (server sent it, schema does not declare it)',
    ]);
  });

  it('reports a row field that passthrough would keep silently', () => {
    expect(diff(body({ output1: [{ iemCd: '005930', iemNm: 'x', stckPrpr: 1 }] }))).toEqual([
      'extra: Output_1.stckPrpr (server sent it, schema does not declare it)',
    ]);
  });

  it('compares array rows over the key union', () => {
    expect(diff(body({ output1: [{ iemCd: '1' }, { iemCd: '2', iemNm: 'x' }] }))).toEqual([]);
  });

  it('reports array/object mismatch', () => {
    expect(diff(body({ output1: { iemCd: '1', iemNm: 'x' } }))).toEqual([
      'kind: Output_1 is object on the server, schema expects array',
    ]);
  });

  it.each([{ total: 1 }, [{ total: 1 }]])('matches an object|array union by what the server sent', (block) => {
    expect(diff({ rspCd: '00000', rspMsg: 'ok', output0: block }, eitherSchema)).toEqual([]);
  });

  it('skips key checks for an empty array', () => {
    expect(diff(body({ output1: [] }))).toEqual([]);
  });
});

describe('valueLength', () => {
  it.each([
    ['005930', '6', null],
    ['0059301', '6', '7'],
    ['삼성전자', '8', null],
    ['삼성전자우', '8', '10'],
    [-1234, '4', null],
    [12345, '4', '5'],
    [-29.99, '5.2', null],
    [123.45, '5.2', null],
    [1234.5, '5.2', '4.1'],
    [1.234, '5.2', '1.3'],
    ['', '1', null],
    [null, '1', null],
  ])('%s against %s → %s', (value, spec, expected) => {
    expect(valueLength(value, spec)).toBe(expected);
  });
});

describe('nhplugLengthViolations', () => {
  const spec = {
    known_exceed: {},
    lengths: {
      '/x': { req: {}, res: { 'Output_1.iem_nm': '4', 'Output_0.total': '2' } },
    },
  };

  it('reports the longest row, compared numerically', () => {
    const b = body({
      output1: [{ iemCd: '1', iemNm: 'ABCDEFGHI' }, { iemCd: '2', iemNm: 'ABCDEFGHIJ' }, { iemCd: '3' }],
    });
    expect(nhplugLengthViolations('/x', b, spec)).toEqual(['length: Output_1.iem_nm is up to 10, spec says 4']);
  });

  it('skips known_exceed', () => {
    const b = body({ output1: [{ iemCd: '1', iemNm: 'ABCDEFGHIJ' }] });
    expect(
      nhplugLengthViolations('/x', b, {
        ...spec,
        known_exceed: { '/x': { 'Output_1.iem_nm': 'errata' } },
      }),
    ).toEqual([]);
  });

  it('reads the shared snapshot', () => {
    expect(
      nhplugLengthViolations('/krstock/quote/v1/currentPrice', {
        output0: { iemCd: '0059301' },
      }),
    ).toEqual(['length: Output_0.iem_cd is up to 7, spec says 6']);
  });
});

describe('assertNhplugMatchesSpec', () => {
  it('honours ignore for measured divergences', () => {
    const b = body({
      output1: [{ iemCd: '005930', iemNm: 'x', korName: 'x' }],
    });
    expect(() => assertNhplugMatchesSpec('/nowhere', b, schema)).toThrow();
    expect(() => assertNhplugMatchesSpec('/nowhere', b, schema, ['Output_1.korName'])).not.toThrow();
  });
});
