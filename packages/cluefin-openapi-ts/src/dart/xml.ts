/**
 * DART 가 내려주는 XML 은 두 가지뿐이라 범용 파서 대신 소형 파서를 쓴다.
 * - `corpCode.xml`: `<result><list><corp_code>…</corp_code>…</list>…</result>` 평면 반복
 * - 바이너리 엔드포인트의 에러 본문: `<result><status>013</status><message>…</message></result>`
 */

const ENTITY = /&(?:#x([0-9a-fA-F]+)|#(\d+)|(amp|lt|gt|quot|apos));/g;
const NAMED: Record<string, string> = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };
const CDATA = /^<!\[CDATA\[([\s\S]*)\]\]>$/;

const decodeText = (raw: string): string => {
  const trimmed = raw.trim();
  const cdata = CDATA.exec(trimmed);
  if (cdata) {
    return cdata[1] ?? '';
  }
  return trimmed.replace(ENTITY, (_, hex?: string, dec?: string, name?: string) => {
    if (hex !== undefined) return String.fromCodePoint(Number.parseInt(hex, 16));
    if (dec !== undefined) return String.fromCodePoint(Number.parseInt(dec, 10));
    return NAMED[name ?? ''] ?? '';
  });
};

const CHILD = /<([A-Za-z_][\w.-]*)>([\s\S]*?)<\/\1>|<([A-Za-z_][\w.-]*)\s*\/>/g;

/** `<tag>…</tag>` 반복을 `{ 자식태그: 텍스트 }` 배열로 바꾼다. 중첩 요소는 지원하지 않는다. */
export const parseFlatXmlList = (xml: string, itemTag = 'list'): Record<string, string>[] => {
  const itemPattern = new RegExp(`<${itemTag}>([\\s\\S]*?)</${itemTag}>`, 'g');
  const items: Record<string, string>[] = [];
  for (const itemMatch of xml.matchAll(itemPattern)) {
    const item: Record<string, string> = {};
    for (const child of (itemMatch[1] ?? '').matchAll(CHILD)) {
      if (child[1] !== undefined) {
        item[child[1]] = decodeText(child[2] ?? '');
      } else if (child[3] !== undefined) {
        item[child[3]] = '';
      }
    }
    items.push(item);
  }
  return items;
};

const tagText = (xml: string, tag: string): string | undefined => {
  const match = new RegExp(`<${tag}>([\\s\\S]*?)</${tag}>`).exec(xml);
  return match ? decodeText(match[1] ?? '') : undefined;
};

export interface DartXmlStatus {
  status: string;
  message: string;
}

/** 에러 본문(`<result><status>…</status><message>…</message></result>`)이면 상태를, 아니면 `undefined`. */
export const parseXmlStatus = (xml: string): DartXmlStatus | undefined => {
  const status = tagText(xml, 'status');
  if (status === undefined || status === '') {
    return undefined;
  }
  return { status, message: tagText(xml, 'message') ?? '' };
};
