import { describe, expect, test } from 'vitest';
import { isKrxMarketHours, isUsMarketHours } from '../_helpers/market-hours';

describe('isKrxMarketHours', () => {
  test.each([
    ['2026-10-12T09:00:00+09:00', true], // 월 개장
    ['2026-10-12T15:30:00+09:00', true], // 월 마감
    ['2026-10-12T08:59:00+09:00', false],
    ['2026-10-12T15:31:00+09:00', false],
    ['2026-10-11T10:00:00+09:00', false], // 일
    ['2026-10-10T10:00:00+09:00', false], // 토
  ])('%s → %s', (iso, expected) => {
    expect(isKrxMarketHours(new Date(iso))).toBe(expected);
  });
});

describe('isUsMarketHours', () => {
  test.each([
    ['2026-10-12T09:30:00-04:00', true], // 월 개장(서머타임, EDT)
    ['2026-10-12T16:00:00-04:00', true],
    ['2026-10-12T09:29:00-04:00', false],
    ['2026-12-14T09:30:00-05:00', true], // 월 개장(표준시, EST)
    ['2026-12-14T09:29:00-05:00', false],
    ['2026-10-10T10:00:00-04:00', false], // 토
  ])('%s → %s', (iso, expected) => {
    expect(isUsMarketHours(new Date(iso))).toBe(expected);
  });
});
