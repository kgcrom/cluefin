import { expect, test } from 'bun:test';

import { camelizeKeys, toCamelCase, toSnakeCase } from '../../src/core/case-convert';

test('toCamelCase converts snake and kebab names', () => {
  expect(toCamelCase('fid_input_iscd')).toBe('fidInputIscd');
  expect(toCamelCase('next-key')).toBe('nextKey');
});

test('toSnakeCase converts camel case names', () => {
  expect(toSnakeCase('fidInputIscd')).toBe('fid_input_iscd');
});

test('camelizeKeys recursively converts object keys', () => {
  const source = {
    rt_cd: '0',
    output_data: [
      {
        stock_code: '005930',
      },
    ],
  };

  const transformed = camelizeKeys(source);
  expect(transformed).toEqual({
    rtCd: '0',
    outputData: [
      {
        stockCode: '005930',
      },
    ],
  });
});
