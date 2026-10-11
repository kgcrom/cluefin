// 실시간 시세 통합 테스트는 장중에만 데이터가 와서, 장외에 돌리면 수신 대기에서 실패한다.
// Python 쪽 `_is_kst_market_hours` 와 같은 기준으로 테스트를 건너뛴다.

interface WallClock {
  weekday: string;
  minutes: number;
}

const wallClock = (now: Date, timeZone: string): WallClock => {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
  }).formatToParts(now);
  const part = (type: Intl.DateTimeFormatPartTypes): string => parts.find((p) => p.type === type)?.value ?? '';
  return {
    weekday: part('weekday'),
    minutes: Number(part('hour')) * 60 + Number(part('minute')),
  };
};

const isWeekdayBetween = (now: Date, timeZone: string, open: number, close: number): boolean => {
  const { weekday, minutes } = wallClock(now, timeZone);
  if (weekday === 'Sat' || weekday === 'Sun') {
    return false;
  }
  return open <= minutes && minutes <= close;
};

/** 국내 정규장: 평일 09:00–15:30 KST. 공휴일은 따지지 않는다. */
export const isKrxMarketHours = (now: Date = new Date()): boolean =>
  isWeekdayBetween(now, 'Asia/Seoul', 9 * 60, 15 * 60 + 30);

/** 미국 정규장: 평일 09:30–16:00 America/New_York(서머타임 자동 반영). 공휴일은 따지지 않는다. */
export const isUsMarketHours = (now: Date = new Date()): boolean =>
  isWeekdayBetween(now, 'America/New_York', 9 * 60 + 30, 16 * 60);
