import { inflateRawSync } from 'node:zlib';

export class ZipError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = 'ZipError';
  }
}

const EOCD_SIGNATURE = 0x06054b50;
const CENTRAL_SIGNATURE = 0x02014b50;
const LOCAL_SIGNATURE = 0x04034b50;
const EOCD_MIN_SIZE = 22;
const MAX_COMMENT_SIZE = 0xffff;

/** ZIP 로컬 파일 헤더 시그니처(`PK\x03\x04`)로 시작하는지. */
export const isZip = (bytes: Uint8Array): boolean =>
  bytes.length >= 4 && bytes[0] === 0x50 && bytes[1] === 0x4b && bytes[2] === 0x03 && bytes[3] === 0x04;

/**
 * 의존성 없는 최소 ZIP 리더 — 중앙 디렉터리를 읽어 항목 이름 → 압축 해제된 바이트 맵을 돌려준다.
 * stored(0)·deflate(8)만 지원하고 ZIP64·암호화는 `ZipError` 로 거절한다.
 * 디렉터리 항목(이름이 `/` 로 끝남)은 건너뛴다.
 */
export const readZip = (bytes: Uint8Array): Map<string, Uint8Array> => {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);

  let eocd = -1;
  const lowest = Math.max(0, bytes.length - EOCD_MIN_SIZE - MAX_COMMENT_SIZE);
  for (let i = bytes.length - EOCD_MIN_SIZE; i >= lowest; i -= 1) {
    if (view.getUint32(i, true) === EOCD_SIGNATURE) {
      eocd = i;
      break;
    }
  }
  if (eocd < 0) {
    throw new ZipError('ZIP 끝 디렉터리(EOCD)를 찾을 수 없습니다. 손상되었거나 ZIP 파일이 아닙니다.');
  }

  const entryCount = view.getUint16(eocd + 10, true);
  let offset = view.getUint32(eocd + 16, true);
  if (entryCount === 0xffff || offset === 0xffffffff) {
    throw new ZipError('ZIP64 는 지원하지 않습니다.');
  }

  const decoder = new TextDecoder('utf-8');
  const files = new Map<string, Uint8Array>();

  for (let index = 0; index < entryCount; index += 1) {
    if (offset + 46 > bytes.length || view.getUint32(offset, true) !== CENTRAL_SIGNATURE) {
      throw new ZipError('ZIP 중앙 디렉터리가 손상되었습니다.');
    }
    const flags = view.getUint16(offset + 8, true);
    const method = view.getUint16(offset + 10, true);
    const compressedSize = view.getUint32(offset + 20, true);
    const nameLength = view.getUint16(offset + 28, true);
    const extraLength = view.getUint16(offset + 30, true);
    const commentLength = view.getUint16(offset + 32, true);
    const localOffset = view.getUint32(offset + 42, true);
    const nameBytes = bytes.subarray(offset + 46, offset + 46 + nameLength);
    // UTF-8 플래그가 없으면 CP437 이지만 DART 파일명은 ASCII 라 UTF-8 디코드로 충분하다.
    const name = decoder.decode(nameBytes);
    offset += 46 + nameLength + extraLength + commentLength;

    if ((flags & 0x1) !== 0) {
      throw new ZipError(`암호화된 ZIP 항목은 지원하지 않습니다: ${name}`);
    }
    if (name.endsWith('/')) {
      continue;
    }
    if (localOffset + 30 > bytes.length || view.getUint32(localOffset, true) !== LOCAL_SIGNATURE) {
      throw new ZipError(`ZIP 로컬 헤더가 손상되었습니다: ${name}`);
    }
    const dataStart =
      localOffset + 30 + view.getUint16(localOffset + 26, true) + view.getUint16(localOffset + 28, true);
    const compressed = bytes.subarray(dataStart, dataStart + compressedSize);
    if (compressed.length !== compressedSize) {
      throw new ZipError(`ZIP 데이터가 잘렸습니다: ${name}`);
    }

    if (method === 0) {
      files.set(name, compressed);
    } else if (method === 8) {
      try {
        files.set(name, new Uint8Array(inflateRawSync(compressed)));
      } catch {
        throw new ZipError(`ZIP 항목 압축 해제에 실패했습니다: ${name}`);
      }
    } else {
      throw new ZipError(`지원하지 않는 압축 방식(${method}): ${name}`);
    }
  }

  return files;
};
