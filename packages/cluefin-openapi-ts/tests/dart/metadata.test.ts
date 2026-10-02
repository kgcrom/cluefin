import { describe, expect, it } from 'vitest';
import { silentLogger } from '../../src/core/logger';
import type { DartEndpointDefinition } from '../../src/core/types';
import { DartClient } from '../../src/dart/client';
import { publicDisclosureEndpoints } from '../../src/dart/metadata/public-disclosure';
import { shareDisclosureComprehensiveEndpoints } from '../../src/dart/metadata/share-disclosure-comprehensive';

// 파이썬 sibling(`cluefin_openapi/dart/_*.py`) 에서 생성되는 메타데이터라,
// 개수가 바뀌면 파이썬 쪽 엔드포인트가 늘거나 파서가 깨진 것이다. phase 마다 카테고리를 추가한다.
const categories: Array<[string, readonly DartEndpointDefinition[], number]> = [
  ['publicDisclosure', publicDisclosureEndpoints, 4],
  ['shareDisclosureComprehensive', shareDisclosureComprehensiveEndpoints, 2],
];
const allEndpoints = categories.flatMap(([, endpoints]) => endpoints);

describe('dart metadata', () => {
  it.each(categories)('%s has %i endpoints', (_name, endpoints, expected) => {
    expect(endpoints).toHaveLength(expected);
  });

  it('has 6 endpoints in total', () => {
    expect(allEndpoints).toHaveLength(6);
  });

  it('gives every endpoint a unique name and an /api/ path', () => {
    expect(new Set(allEndpoints.map((endpoint) => endpoint.methodName)).size).toBe(allEndpoints.length);
    for (const endpoint of allEndpoints) {
      expect(endpoint.path, endpoint.methodName).toMatch(/^\/api\/\w+\.(json|xml)$/);
      expect(endpoint.responseKind, endpoint.methodName).toBe(endpoint.path.endsWith('.xml') ? 'binary' : 'json');
    }
  });

  it('maps every queryMap value to a declared param', () => {
    for (const endpoint of allEndpoints) {
      const names = new Set(endpoint.params.map((param) => param.name));
      for (const inputKey of Object.values(endpoint.queryMap)) {
        expect(names.has(inputKey), `${endpoint.methodName}.${inputKey}`).toBe(true);
      }
      expect(Object.keys(endpoint.queryMap), endpoint.methodName).toHaveLength(endpoint.params.length);
      expect(Object.keys(endpoint.queryMap), endpoint.methodName).not.toContain('crtfc_key');
    }
  });

  it('sends exactly the queryMap keys plus crtfc_key on the wire', async () => {
    for (const endpoint of allEndpoints) {
      const urls: URL[] = [];
      const fetchMock: typeof fetch = async (input) => {
        urls.push(new URL(String(input)));
        return new Response(endpoint.responseKind === 'json' ? '{"status":"000","message":"정상"}' : 'x');
      };
      const client = new DartClient({ authKey: 'key', fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0 });
      const input = Object.fromEntries(endpoint.params.map((param) => [param.name, `v_${param.name}`]));

      if (endpoint.responseKind === 'json') {
        await client.invokeEndpoint(endpoint, input);
      } else {
        await client.invokeBinaryEndpoint(endpoint, input);
      }

      const sent = [...(urls[0]?.searchParams.keys() ?? [])].sort();
      expect(sent, endpoint.methodName).toEqual([...Object.keys(endpoint.queryMap), 'crtfc_key'].sort());
      expect(urls[0]?.pathname, endpoint.methodName).toBe(endpoint.path);
    }
  });
});
