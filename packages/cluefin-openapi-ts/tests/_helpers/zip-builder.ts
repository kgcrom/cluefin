import { deflateRawSync } from 'node:zlib';

export interface ZipEntry {
  name: string;
  data: Uint8Array | string;
  /** 기본 deflate(8), `store` 면 무압축(0). */
  method?: 'deflate' | 'store';
}

const u16 = (value: number): number[] => [value & 0xff, (value >>> 8) & 0xff];
const u32 = (value: number): number[] => [
  value & 0xff,
  (value >>> 8) & 0xff,
  (value >>> 16) & 0xff,
  (value >>> 24) & 0xff,
];

/** 테스트용 최소 ZIP 생성기 (CRC 는 리더가 검증하지 않아 0 으로 둔다). */
export const buildZip = (entries: readonly ZipEntry[]): Uint8Array<ArrayBuffer> => {
  const encoder = new TextEncoder();
  const chunks: number[] = [];
  const central: number[] = [];

  for (const entry of entries) {
    const raw = typeof entry.data === 'string' ? encoder.encode(entry.data) : entry.data;
    const stored = entry.method === 'store';
    const payload = stored ? raw : new Uint8Array(deflateRawSync(raw));
    const name = encoder.encode(entry.name);
    const method = stored ? 0 : 8;
    const localOffset = chunks.length;

    chunks.push(...u32(0x04034b50), ...u16(20), ...u16(0), ...u16(method), ...u16(0), ...u16(0), ...u32(0));
    chunks.push(...u32(payload.length), ...u32(raw.length), ...u16(name.length), ...u16(0), ...name, ...payload);

    central.push(
      ...u32(0x02014b50),
      ...u16(20),
      ...u16(20),
      ...u16(0),
      ...u16(method),
      ...u16(0),
      ...u16(0),
      ...u32(0),
    );
    central.push(...u32(payload.length), ...u32(raw.length), ...u16(name.length), ...u16(0), ...u16(0));
    central.push(...u16(0), ...u16(0), ...u32(0), ...u32(localOffset), ...name);
  }

  const eocd = [
    ...u32(0x06054b50),
    ...u16(0),
    ...u16(0),
    ...u16(entries.length),
    ...u16(entries.length),
    ...u32(central.length),
    ...u32(chunks.length),
    ...u16(0),
  ];
  return Uint8Array.from([...chunks, ...central, ...eocd]);
};
