/**
 * Helpers for token cache files shared with the Python `cluefin_openapi` TokenManagers.
 *
 * 세 브로커 모두 파이썬·TS 가 같은 캐시 파일을 읽고 쓰므로, 여기 규칙은
 * `cluefin_openapi._atomic_file` 및 각 `_token_manager` 와 손으로 맞춰야 한다.
 */

const pad = (value: number, width = 2): string => String(value).padStart(width, '0');

/**
 * Python `datetime.now().isoformat()` 과 같은 naive 로컬 시각 (`2026-09-23T22:43:34.544`).
 *
 * `toISOString()` 의 `Z` 접미사는 Python 3.10 `datetime.fromisoformat` 이 거부한다. 그러면
 * 파이썬 TokenManager 가 토큰은 읽고 `cached_at` 만 버려 6시간 최대 수명 검사가 꺼진다.
 * 오프셋 없는 문자열은 JS `Date` 도 로컬 시각으로 해석하므로 양쪽에서 같은 순간이 된다.
 */
export const localIsoNow = (date: Date = new Date()): string =>
  `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}` +
  `T${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}` +
  `.${pad(date.getMilliseconds(), 3)}`;

/**
 * Write JSON the way Python `write_json_atomic` does: owner-only (0600) temp file in the same
 * directory, then rename over the target so readers never see a partial file.
 *
 * 파이썬 쪽의 `flock` 잠금은 Node 표준 라이브러리에 없어 생략한다 — rename 이 원자적이라
 * 읽는 쪽이 반쯤 쓰인 파일을 보지는 않는다.
 */
export const writeJsonAtomic = async (filePath: string, data: unknown): Promise<void> => {
  const fs = await import('node:fs/promises');
  const path = await import('node:path');
  const { randomBytes } = await import('node:crypto');

  const dir = path.dirname(filePath);
  const tmpPath = path.join(dir, `.${path.basename(filePath)}.${randomBytes(6).toString('hex')}.tmp`);
  await fs.mkdir(dir, { recursive: true });
  const handle = await fs.open(tmpPath, 'wx', 0o600);
  try {
    await handle.writeFile(JSON.stringify(data, null, 2), 'utf-8');
    await handle.sync();
  } finally {
    await handle.close();
  }
  try {
    await fs.rename(tmpPath, filePath);
  } catch (error) {
    await fs.rm(tmpPath, { force: true });
    throw error;
  }
};
