import { describe, expect, it } from 'vitest';

import { isZip, readZip, ZipError } from '../../src/core/zip';
import { buildZip } from '../_helpers/zip-builder';

const text = (bytes: Uint8Array | undefined): string => new TextDecoder().decode(bytes);

describe('readZip', () => {
  it('deflate·stored 항목을 모두 풀고 디렉터리 항목은 건너뛴다', () => {
    const zip = buildZip([
      { name: 'dir/', data: '', method: 'store' },
      { name: 'a.xml', data: '<a>한글</a>'.repeat(50) },
      { name: 'b.txt', data: 'plain', method: 'store' },
    ]);

    const files = readZip(zip);

    expect([...files.keys()]).toEqual(['a.xml', 'b.txt']);
    expect(text(files.get('a.xml'))).toBe('<a>한글</a>'.repeat(50));
    expect(text(files.get('b.txt'))).toBe('plain');
  });

  it('isZip 은 로컬 헤더 시그니처로 판별한다', () => {
    expect(isZip(buildZip([{ name: 'a', data: 'x' }]))).toBe(true);
    expect(isZip(new TextEncoder().encode('<result/>'))).toBe(false);
    expect(isZip(new Uint8Array())).toBe(false);
  });

  it('ZIP 이 아니면 ZipError', () => {
    expect(() => readZip(new TextEncoder().encode('<result><status>013</status></result>'))).toThrow(ZipError);
  });

  it('데이터가 잘리면 ZipError', () => {
    const zip = buildZip([{ name: 'a.xml', data: 'hello world '.repeat(20) }]);
    expect(() => readZip(zip.subarray(0, zip.length - 30))).toThrow(ZipError);
  });

  it('손상된 deflate 데이터는 ZipError', () => {
    const zip = buildZip([{ name: 'a.xml', data: 'hello world '.repeat(20) }]);
    // 로컬 헤더(30) + 이름(5) 직후의 압축 데이터를 망가뜨린다.
    for (let i = 35; i < 45; i += 1) zip[i] = 0xff;
    expect(() => readZip(zip)).toThrow(ZipError);
  });
});
