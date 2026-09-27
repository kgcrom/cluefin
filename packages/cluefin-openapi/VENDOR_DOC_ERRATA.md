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
| 프로그램매매 종합현황(일별) `comp-program-trade-daily` (FHPPG04600001) | 표: `whol_*` 순매수 계열 9개 없음 (`whol_smtn_ntby_qty` 등) / 예시: 있음 | 보냄 | 2026-09-27, K | 모델에 추가 |
| 관심종목(멀티종목) 시세조회 `intstock-multprice` (FHKST11300006) | 표: output 이 object | array | 2026-09-27 | array |
| 해외주식 현재가 10호가 `overseas-price/inquire-asking-price` (HHDFS76200100) | 표: output2 가 array | object 하나에 1~10호가 | 2026-09-27, NAS AAPL | object, 2~10호가 모델에 추가 |
| 해외주식 체결추이 `overseas-price/inquire-ccnl` (HHDFS76200300) | 표: output1 `NREC`·`ZDIV` 대문자 | 소문자 `nrec`·`zdiv` | 2026-09-27 | 소문자 |
| 해외지수·환율 기간별 시세 `overseas-price/inquire-daily-chartprice` (FHKST03030100) | 표: output1 에 `prdy_vol` | 안 보냄 | 2026-09-27 | 모델에 남기고 테스트 `ignore` |
| 해외주식 상품기본정보 `search-info` (CTPF1702R) | 표: `etp_bast_lcls_cd`·`etp_bast_mcls_cd`·`etp_bast_scls_cd`·`sgle_item_lvrg_etp_yn` / 예시: 없음 | 보냄 | 2026-09-27 | 모델에 추가 |
| 해외주식 시가총액순위 `ranking/market-cap` (HHDFS76350100) | output1 에 `curr`·`t_rate` 없음, output2 에 `*_org`(`last_org`·`diff_org`·`tomv_org`) 없음 | 보냄 | 2026-09-27 | 모델에 추가·있음 |
| 해외주식 매수체결강도상위 `ranking/volume-power` (HHDFS76280000) | output2 `knam`·`enam` | `name`·`ename` | 2026-08 | 두 이름 모두 수용 |
| 해외주식 거래회전율순위 `ranking/trade-turnover` (HHDFS76340000) | 표: output2 에 `n_tvol` | 안 보냄 | 2026-09-27 | 모델에 없음 |
| 해외주식 분봉조회 `inquire-time-itemchartprice` (HHDFS76950200) | 표: output1 array·output2 object / 예시: 반대 | 예시대로 (output1 object, output2 array) | 2026-09-27 | 예시대로 |
| 해외결제일자조회 `countries-holiday` (CTOS5011R), 기간별권리조회 `period-rights` (CTRGT011R), 담보대출가능종목 `colable-by-company` (CTLN4050R) | 표: 최상위 연속조회 키 `ctx_area_*` 없음 / 예시: 있음 | 보냄 | 2026-09-27 | 모델에 있음 |

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
| 주식예상체결가 추이 `exp-price-trend` | 요청 `FID_INPUT_ISCD` | 5 | 6 (종목코드) | 2026-09-27 |
| 종목별 프로그램매매추이(체결) `program-trade-by-stock` | 응답 `output.whol_ntby_tr_pbmn_icdc` | 10 | 11 | 2026-09-27 |
| HTS조회상위20종목 `hts-top-view` | 응답 `output1.mksc_shrn_iscd` | 2 | 6 | 2026-09-27 |
| 우선주 괴리율 상위 `prefer-disparate-ratio` | 응답 `output.hts_kor_isnm` / `prst_kor_isnm` / `prdy_ctrt` | 10 / 10 / 1 | 13 / 16 / 5 | 2026-09-27 |
| 해외주식 업종별시세 `industry-theme` | 요청 `ICOD` | 1 | 3 (업종코드) | 2026-09-27 |
| 해외주식 순위 8종 (`industry-theme`·`market-cap`·`new-highlow`·`trade-growth`·`trade-pbmn`·`trade-turnover`·`trade-vol`·`updown-rate`) | 응답 `output2.symb` | 1 | 최대 7 (티커) | 2026-09-27 |
