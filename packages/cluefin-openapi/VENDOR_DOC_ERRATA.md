# 브로커 공식 문서 오류·누락 (실측 기준)

공식 문서와 실서버 응답이 다른 경우를 모은다. 코드는 **실측을 따르고**, 테스트의 `ignore`·주석은 이 파일을 가리킨다.
항목마다 실측일과 조건을 적는다 — 브로커가 서버를 바꾸면 다시 확인해야 하기 때문이다.

- 응답 모델에 길이 제약(`max_length`)을 넣지 않는다. 아래 "길이" 항목처럼 문서의 길이 값은 믿을 수 없다 (`AGENTS.md`).
- 문서 출처: KIS `apiportal.koreainvestment.com` 상세 명세(`api/apis/public/detail`)의 필드 표와 응답 예시(`resAuth`).
  **필드 표와 예시가 서로 다른 경우가 많다** — 아래 "표/예시" 열이 그 구분이다.

## KIS

### 응답 필드

| API (TR) | 문서 | 실서버 | 실측 | 코드 |
|---|---|---|---|---|
| 업종기간별시세 `inquire-daily-indexchartprice` (FHKUP03500100) | 표: output1 에 `bstp_nmix_prdy_vrss` 없음 / 예시: 있음 | 보냄 | 2026-09-27, 0001 | 모델에 추가 |
| 시황·공시 제목 `news-title` (FHKST01011800) | 표: `iscd1~5` 만 / 예시: `iscd1~10`, `kor_isnm1~10` | 예시대로 보냄 | 2026-09-27, 전체 | 모델에 추가 |
| 주식현재가 시세 `inquire-price` (FHKST01010100) | 표: output 에 `apprch_rate`, `new_hgpr_lwpr_cls_code` | 둘 다 안 보냄 | 2026-09-27, 005930 | `apprch_rate` 는 모델에 없음. `new_hgpr_lwpr_cls_code` 는 조건부로 보고 `ignore` (평일 재확인) |
| 주식현재가 시세2 `inquire-price-2` (FHPST01010000) | 표: `new_hgpr_lwpr_cls_code`, `mxpr_llam_cls_code`, `flng_cls_name`, `revl_issu_reas_name`, `mrkt_warn_cls_name`, `fcam_mod_cls_name` | 안 보냄 — 값이 없는 조건부 필드는 키를 생략하는 것으로 보인다 | 2026-09-27, 035720 | 선택 필드로 유지, 테스트 `ignore` |
| 시간외현재가 `inquire-overtime-price` (FHPST02300000) | 표: `mang_issu_cls_name`, `mrkt_warn_cls_name`, `revl_issu_reas_name`, `flng_cls_name` | 안 보냄 (위와 같은 조건부 생략) | 2026-09-27 | 선택 필드로 유지, 테스트 `ignore` |
| 시간외호가 `inquire-overtime-asking-price` (FHPST02300400) | 표: 블록 `output1`, 증감 `ovtm_untp_askp/bidp_icdc1~10` / 예시: 블록 `output`, 증감 1~3 | 블록 `output`, 증감 **1~3 만** | 2026-09-27 | 모델은 `output`, 4~10 은 테스트 `ignore` |
| 국내주식기간별시세 `inquire-daily-itemchartprice` (FHKST03010100) | `itewhol_loan_rmnd_ratem` | 키가 **`itewhol_loan_rmnd_ratem name`** (공백 포함) | 2026-08 | 두 키 모두 수용 |
| 주식현재가 회원사 `inquire-member` (FHKST01010600) | 표: output 에 `acml_vol` 없음 | 보냄 | 2026-09-27 | 모델에 있음 |
| 예상체결가 `exp-closing-price` (FHKST117300C0) | 표: 블록 `output1` / 예시: `output` | `output` | 2026-09-27 | 모델은 `output` |
| 주식현재가 시간대별체결 `inquire-time-itemconclusion` (FHPST01060000) | 표: output2 가 object, `stck_pbpr` / 예시: array | array, `stck_prpr` | 2026-09-27 | 모델은 array, `stck_prpr` |
| 업종 분봉조회 `inquire-time-indexchartprice` (FHKUP03500200) | 표: `Output1`·`Output2` (대문자) | 소문자 `output1`·`output2` | 2026-09-27 | 소문자 |
| 예탁원 유상증자일정 `ksdinfo/paidin-capin` (HHKDB669100C0) | 블록 `output` | `output1` | 2026-08-21 | `output1` |
| ETF/ETN 현재가 `etfetn/inquire-price` (FHPST02400000) | 표: output 에 `nmix_ctrt` | 안 보냄 | 2026-09-27 | 모델에 없음 |
| ETF 구성종목시세 `inquire-component-stock-price` (FHKST121600C0) | 표: `etf_cu_unit_scrt_cnt` 는 output1 에만 | output2 행에도 보냄 | 2026-09-27 | 모델에 있음 |
| 국내휴장일조회 `chk-holiday` (CTCA0903R), 당사 대주가능 종목 `lendable-by-company` (CTSC2702R) | 표: 최상위 연속조회 키 `ctx_area_*` 없음 / 예시: 있음 | 보냄 | 2026-09-27 | 모델에 있음 |
| 금리 종합 `comp-interest` (FHPST07020000) | 표: output1 에 `bond_cntg_ert`·`bond_stnd_iscd`·`date_time`·`indicator_nm`·`prdy_vrss` | 안 보냄. `FID_DIV_CLS_CODE` 도 문서에 없는 `2` 만 온전한 값을 준다 (`AGENTS.md`) | 2026-09-20·27 | 모델에 없음 |

### 길이

문서의 `propertyLength` 보다 실제 값이 길다. 요청 쪽은 문서 길이를 지키면 호출이 안 되는 경우다.

| API | 필드 | 문서 길이 | 실제 | 실측 |
|---|---|---|---|---|
| 주식현재가 체결 `inquire-ccnl` | 요청 `FID_INPUT_ISCD` | 2 | 6 (종목코드) | 2026-09-27 |
| 업종기간별시세 `inquire-daily-indexchartprice` | 요청 `FID_INPUT_ISCD` | 2 | 4 (업종코드) | 2026-09-27 |
| 주식일별분봉 `inquire-time-dailychartprice` | 요청 `FID_INPUT_DATE_1` | 2 | 8 (YYYYMMDD) | 2026-09-27 |
| 국내주식 종목추정실적 `estimate-perform` | 요청 `SHT_CD` | 2 | 6 (종목코드) | 2026-09-27 |
| 국내주식 종목추정실적 `estimate-perform` | 응답 `output1.estdate` | 1 | 8 | 2026-09-27 |
| 주식현재가 시세2 `inquire-price-2` | 응답 `output.bstp_cls_code` | 4 | 6 | 2026-09-27 |
