import { z } from 'zod';

/** 응답 이름 언어 — kr(국문) / en(영문) */
export type EcosLang = 'kr' | 'en';

/** 주기 — A(년) S(반년) Q(분기) M(월) SM(반월) D(일) */
export type EcosCycle = 'A' | 'S' | 'Q' | 'M' | 'SM' | 'D';

/** 행 범위·언어. 범위를 주면 그 쪽만, 생략하면 `listTotalCount` 를 다 채울 때까지 쪽 넘김한다. */
export interface EcosPageOptions {
  lang?: EcosLang;
  startRow?: number;
  endRow?: number;
}

/** ECOS 서비스 공통 응답 `{"<서비스명>": {"list_total_count": N, "row": [...]}}` 의 안쪽. */
export interface EcosPage<Row> {
  /** 조건에 맞는 전체 행 수 (받은 행 수가 아님) */
  listTotalCount: number;
  /** 이번 쪽 행 수. KeyStatisticList 만 준다(명세에 없음). 쪽 넘김으로 받았으면 null */
  rowCount: number | null;
  /** 행 목록. 데이터 없음(INFO-200)이면 빈 배열 */
  rows: Row[];
}

/** ECOS 는 같은 필드를 문자열("1000")로도 숫자(1000)로도 준다(WGT 실측). 문자열 필드는 숫자도 받아 문자열로 둔다. */
export const ecosText = z.union([z.string(), z.number()]).transform(String);

/** 숫자 필드(DATA_CNT 등). pydantic int 처럼 숫자 문자열도 받는다. */
export const ecosCount = z.union([z.number(), z.string()]).transform(Number);
