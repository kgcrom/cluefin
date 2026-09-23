export interface FetchCall {
  input: string;
  init: RequestInit;
}

/**
 * `fetch` 시그니처와 호환되는 최소 목(mock).
 * 호출마다 기록만 남기고 항상 같은 `response`를 반환한다.
 */
export const createFetchMock = (response: Response): { calls: FetchCall[]; fetchMock: typeof fetch } => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input, init) => {
    calls.push({ input: String(input), init: init ?? {} });
    return response;
  };
  return { calls, fetchMock };
};

export const jsonResponse = (body: unknown, status = 200, headers?: HeadersInit): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', ...headers },
  });
