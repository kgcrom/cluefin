import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const FIXTURES = join(__dirname, 'fixtures');

export const SAMPLE_LIMIT_MESSAGE =
  '조회건수 값의 타입이 유효하지 않습니다. 조회건수 값을 확인하십시오!\n' +
  ' 조회건수 값의 타입이 유효하지 않으면 오류를 발생합니다. \n sample은 최대 10건 이내에서 호출이 가능합니다.';

/** /api/{서비스}/{키}/json/{언어}/{시작}/{끝}/... */
const PATH = /^\/api\/(?<service>\w+)\/(?<key>[^/]+)\/json\/(?<lang>\w+)\/(?<start>\d+)\/(?<end>\d+)/;

export interface FetchCall {
  url: string;
}

export const loadFixture = (name: string): Record<string, unknown> =>
  JSON.parse(readFileSync(join(FIXTURES, name), 'utf-8')) as Record<string, unknown>;

/** 픽스처 `{"<서비스>": {"row": [...]}}` 의 행 목록. */
export const fixtureRows = (name: string, service: string): Record<string, unknown>[] => {
  const page = new Map(Object.entries(loadFixture(name))).get(service) as { row: Record<string, unknown>[] };
  return page.row;
};

export const result = (code: string, message = ''): Record<string, unknown> => ({
  RESULT: { CODE: code, MESSAGE: message },
});

export const jsonResponse = (body: unknown, status = 200): Response =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });

/** 응답을 직접 정하는 fetch 목. 호출 URL 을 기록한다. */
export const createFetchMock = (responder: (url: string, index: number) => Response) => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input) => {
    const url = String(input);
    calls.push({ url });
    return responder(url, calls.length - 1);
  };
  return { calls, fetchMock };
};

/**
 * URL 의 행 범위대로 잘라 주는 가짜 ECOS. sample 키로 sampleLimit 를 넘기면 ERROR-301.
 * `extra` 는 쪽 블록에 덧붙일 필드(예: `row_count`).
 */
export const serveRows = (
  service: string,
  rows: readonly Record<string, unknown>[],
  options: { sampleLimit?: number; extra?: Record<string, unknown> } = {},
) => {
  const sampleLimit = options.sampleLimit ?? 10;
  return createFetchMock((url) => {
    const groups = PATH.exec(new URL(url).pathname)?.groups;
    if (!groups?.start || !groups.end) {
      return jsonResponse({ message: 'bad path' }, 404);
    }
    const start = Number(groups.start);
    const end = Number(groups.end);
    if (groups.key === 'sample' && end - start + 1 > sampleLimit) {
      return jsonResponse(result('ERROR-301', SAMPLE_LIMIT_MESSAGE));
    }
    const page = rows.slice(start - 1, end);
    if (page.length === 0) {
      return jsonResponse(result('INFO-200', '해당하는 데이터가 없습니다.'));
    }
    return jsonResponse(
      Object.fromEntries([[service, { list_total_count: rows.length, row: page, ...options.extra }]]),
    );
  });
};
