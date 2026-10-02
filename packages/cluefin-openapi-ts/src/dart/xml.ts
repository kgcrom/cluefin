/**
 * DART 가 내려주는 XML 은 두 가지뿐이라 범용 파서 대신 소형 파서를 쓴다.
 * - `corpCode.xml`: `<result><list><corp_code>…</corp_code>…</list>…</result>` 평면 반복
 * - 바이너리 엔드포인트의 에러 본문: `<result><status>013</status><message>…</message></result>`
 */

const ENTITY = /&(?:#x(?<hex>[0-9a-fA-F]+)|#(?<dec>\d+)|(?<named>amp|lt|gt|quot|apos));/g;
const NAMED: Record<string, string> = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };
const CDATA = /^<!\[CDATA\[(?<text>[\s\S]*)\]\]>$/;

const decodeText = (raw: string): string => {
  const trimmed = raw.trim();
  const cdata = CDATA.exec(trimmed);
  if (cdata) {
    return cdata.groups?.text ?? '';
  }
  return trimmed.replace(ENTITY, (...args) => {
    const groups = args.at(-1) as { hex?: string; dec?: string; named?: string };
    if (groups.hex !== undefined) return String.fromCodePoint(Number.parseInt(groups.hex, 16));
    if (groups.dec !== undefined) return String.fromCodePoint(Number.parseInt(groups.dec, 10));
    return NAMED[groups.named ?? ''] ?? '';
  });
};

const CHILD = /<(?<name>[A-Za-z_][\w.-]*)>(?<body>[\s\S]*?)<\/\k<name>>|<(?<empty>[A-Za-z_][\w.-]*)\s*\/>/g;

/** `<tag>…</tag>` 의 첫 구간(여는 태그 끝 ~ 닫는 태그 시작)을 찾는다. 동적 RegExp 대신 indexOf 로 훑는다. */
const findElement = (xml: string, tag: string, from: number): { body: string; next: number } | undefined => {
  const open = `<${tag}>`;
  const close = `</${tag}>`;
  const start = xml.indexOf(open, from);
  if (start < 0) {
    return undefined;
  }
  const end = xml.indexOf(close, start + open.length);
  if (end < 0) {
    return undefined;
  }
  return { body: xml.slice(start + open.length, end), next: end + close.length };
};

/** `<tag>…</tag>` 반복을 `{ 자식태그: 텍스트 }` 배열로 바꾼다. 중첩 요소는 지원하지 않는다. */
export const parseFlatXmlList = (xml: string, itemTag = 'list'): Record<string, string>[] => {
  const items: Record<string, string>[] = [];
  let from = 0;
  for (let found = findElement(xml, itemTag, from); found; found = findElement(xml, itemTag, from)) {
    from = found.next;
    const item: Record<string, string> = {};
    for (const child of found.body.matchAll(CHILD)) {
      const { name, body, empty } = child.groups ?? {};
      if (name !== undefined) {
        item[name] = decodeText(body ?? '');
      } else if (empty !== undefined) {
        item[empty] = '';
      }
    }
    items.push(item);
  }
  return items;
};

const tagText = (xml: string, tag: string): string | undefined => {
  const found = findElement(xml, tag, 0);
  return found ? decodeText(found.body) : undefined;
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
