import { DartApiError } from '../core/errors.js';
import type { ApiResponse, DomainMethods } from '../core/types.js';
import { readZip, ZipError } from '../core/zip.js';
import type { DartBinaryResponse, DartClient } from './client.js';
import { DartDomainBase } from './domain-base.js';
import { publicDisclosureEndpoints } from './metadata/public-disclosure.js';
import type { PublicDisclosureResponseMap, PublicDisclosureSearchResponse } from './schemas/public-disclosure.js';
import { parseFlatXmlList } from './xml.js';

export interface CorpCodeItem {
  corpCode: string;
  corpName: string;
  corpEngName?: string;
  corpCls?: string;
  stockCode?: string;
  modifyDate: string;
}

/** 고유번호 목록. XML 응답을 파싱한 결과라 JSON 엔드포인트와 같이 `status`/`message`/`list` 모양을 맞췄다. */
export interface CorpCodeResponse {
  status: string;
  message: string;
  list: CorpCodeItem[];
}

// DART 는 corp_code 없이 3개월을 넘는 기간 검색을 거절한다. 기간을 안 주면 이 안쪽의 윈도우를 쓴다.
const DEFAULT_SEARCH_WINDOW_DAYS = 89;

const formatDate = (date: Date): string =>
  `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;

const firstXmlEntry = (zip: Uint8Array, label: string): Uint8Array => {
  let files: Map<string, Uint8Array>;
  try {
    files = readZip(zip);
  } catch (error) {
    if (error instanceof ZipError) {
      throw new DartApiError(`${label} ZIP 파일을 읽을 수 없습니다: ${error.message}`);
    }
    throw error;
  }
  for (const [name, data] of files) {
    if (name.toLowerCase().endsWith('.xml')) {
      return data;
    }
  }
  throw new DartApiError(`${label} ZIP 파일에 XML 데이터가 포함되어있지 않습니다.`);
};

const isZipBytes = (bytes: Uint8Array): boolean =>
  bytes.length >= 4 && bytes[0] === 0x50 && bytes[1] === 0x4b && bytes[2] === 0x03 && bytes[3] === 0x04;

export interface PublicDisclosure extends DomainMethods<'companyOverview', PublicDisclosureResponseMap> {}

/** 공시정보 */
export class PublicDisclosure extends DartDomainBase {
  public constructor(client: DartClient) {
    super(client, publicDisclosureEndpoints, {
      custom: ['publicDisclosureSearch', 'disclosureDocumentFile', 'corpCode'],
    });
  }

  /**
   * 공시검색. `bgnDe`·`endDe` 를 모두 생략하면 오늘까지 89일을 조회한다
   * (DART 는 기간을 안 주면 빈 결과를 돌려준다).
   */
  public async publicDisclosureSearch(
    input: Record<string, unknown> = {},
  ): Promise<ApiResponse<PublicDisclosureSearchResponse>> {
    const withDates = { ...input };
    if (withDates.bgnDe === undefined && withDates.endDe === undefined) {
      const today = new Date();
      const begin = new Date(today.getFullYear(), today.getMonth(), today.getDate() - DEFAULT_SEARCH_WINDOW_DAYS);
      withDates.bgnDe = formatDate(begin);
      withDates.endDe = formatDate(today);
    }
    return (await this.invokeJson('publicDisclosureSearch', withDates)) as ApiResponse<PublicDisclosureSearchResponse>;
  }

  /** 공시서류원본파일 — ZIP 안의 첫 XML 을 풀어 바이트로 돌려준다 (ZIP 이 아니면 받은 그대로). */
  public async disclosureDocumentFile(input: Record<string, unknown>): Promise<DartBinaryResponse> {
    const response = await this.invokeBinary('disclosureDocumentFile', input);
    if (!isZipBytes(response.body)) {
      return response;
    }
    return { headers: response.headers, body: firstXmlEntry(response.body, '공시서류') };
  }

  /** 고유번호 — 공시대상회사 전체 목록 (수 MB 의 ZIP/XML 을 내려받아 파싱한다). */
  public async corpCode(): Promise<ApiResponse<CorpCodeResponse>> {
    const response = await this.invokeBinary('corpCode', {});
    const xml = new TextDecoder('utf-8').decode(firstXmlEntry(response.body, '고유번호'));

    const list: CorpCodeItem[] = [];
    for (const element of parseFlatXmlList(xml)) {
      const corpCode = element.corp_code;
      const corpName = element.corp_name;
      if (!corpCode || !corpName) {
        continue;
      }
      const item: CorpCodeItem = { corpCode, corpName, modifyDate: element.modify_date || '' };
      const corpEngName = element.corp_eng_name || element.corp_name_eng;
      if (corpEngName) item.corpEngName = corpEngName;
      if (element.corp_cls) item.corpCls = element.corp_cls;
      if (element.stock_code) item.stockCode = element.stock_code;
      list.push(item);
    }

    return { headers: response.headers, body: { status: '000', message: '정상', list } };
  }
}
