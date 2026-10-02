import { z } from 'zod';

/** DART 공통 응답 봉투 (`status`/`message` + 페이지네이션). `list` 는 엔드포인트별로 붙인다. */
export const dartEnvelope = {
  /** 에러 및 정보 코드 (000: 정상, 013: 조회된 데이터 없음 …) */
  status: z.string(),
  /** 에러 및 정보 메시지 */
  message: z.string(),
  page_no: z.union([z.number(), z.string()]).nullish(),
  page_count: z.union([z.number(), z.string()]).nullish(),
  total_count: z.union([z.number(), z.string()]).nullish(),
  total_page: z.union([z.number(), z.string()]).nullish(),
};

/** pydantic 은 숫자 문자열도 int/float 로 강제변환해서, 와이어 값이 숫자일 수도 문자열일 수도 있다. */
export const dartNumeric = z.union([z.number(), z.string()]);
