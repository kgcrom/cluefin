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
| 배당률 상위 `ranking/dividend-rate` (HHKDB13470100) | 블록 `output1` | `output` | 2026-08-21 | `output` |
| ETF/ETN 현재가 `etfetn/inquire-price` (FHPST02400000) | 표: output 에 `nmix_ctrt` | 안 보냄 | 2026-09-27 | 모델에 없음 |
| ETF 구성종목시세 `inquire-component-stock-price` (FHKST121600C0) | 표: `etf_cu_unit_scrt_cnt` 는 output1 에만 | output2 행에도 보냄 | 2026-09-27 | 모델에 있음 |
| 변동성완화장치(VI) 현황 `inquire-vi-status` (FHPST01390000), 국내휴장일조회 `chk-holiday` (CTCA0903R), 해외결제일자 `countries-holiday` (CTOS5011R) | 표: output 이 object | array | 2026-09-27 | array |
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
| 채권 실시간호가 `H0BJASP0` | 5호가 잔량 필드명 `askp_rsqn52`·`bidp_rsqn53` | 위치상 `askp_rsqn5`·`bidp_rsqn5` (오타) | 2026-09-27 정적 | `askp_rsqn5`·`bidp_rsqn5` |

### 요청 파라미터

| API (TR) | 문서 | 실서버 | 실측 | 코드 |
|---|---|---|---|---|
| 종목별일별매수매도체결량 `inquire-daily-trade-volume` (FHKST03010800) | `FID_COND_MRKT_DIV_CODE_1`·`FID_INPUT_ISCD_1` 없음 | 빠지면 `OPSQ2001`(INPUT FIELD NOT FOUND) 로 거절 | 2026-08 | 함께 보냄 |
| 금리 종합 `comp-interest` | TR `(구) FHPST07020000 (신) HHPST070200C0`, 신규 TR 은 필수 `DATA_GB` | 구 TR 로 동작 중 | 2026-09-27 문서 확인 | 구 TR 유지 — 신 TR 전환은 별도 실측 후 |

### 서버 동작 (문서에 없는 것)

- **금리 종합(`comp-interest`, FHPST07020000)은 `FID_DIV_CLS_CODE` 에 따라 배열의 의미가 바뀐다** (2026-09-20 실측).
  문서는 `1:해외금리지표` 만 적었지만 `0`/공백 → output1·output2 모두 국내 19종, `1` → output1 해외 7종 + output2 국내
  (뒤 8종만, **앞 10행은 필드가 한두 칸씩 밀리고 한글도 깨진다**), `2` → output1 에 국내 19 + 해외 7 이 온전히 온다.
  전체를 주는 것은 문서에 없는 `2` 뿐이라 CLI 기본값으로 쓴다. 배열 이름은 믿을 수 없으니 국내/해외는
  `bcdt_code` 접두어(`Y01`/`Y02`)로 가른다.
- **재무비율(FHKST66430300)·손익계산서(FHKST66430200)의 `fid_div_cls_code="0"`(년)은 진행 중 회계연도의 누적 행을
  최신으로 얹어 준다** (2026-08-22, 202512 위에 202606). 최신 행을 연간으로 읽으면 ROE·증가율이 부풀려진다 —
  결산월과 `stac_yymm` 뒷 2자리가 일치하는 행이 완결 연도다.
- **국내주식기간별시세(FHKST03010100)는 요청 구간과 무관하게 최신 100봉에서 잘린다** (2026-08-22, 1년 반 요청 → 100건).
  장기 일봉은 키움 ka10081 연속조회를 쓴다.
- 실서버는 값이 없는 조건부 필드(시장경고·관리종목·락 구분명 등)의 **키를 아예 생략한다** — 위 "응답 필드" 의
  현재가·시간외현재가 항목. 통합테스트는 이런 필드를 `ignore` 로 명시한다.

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
| 장내채권 평균단가조회 `domestic-bond/avg-unit` | 응답 `output1.prdt_name` / `kis_unpr` / `avg_evlu_rf_unpr` | 1 / 8 / 3 | 13 / 14 / 4 | 2026-09-27 |
| 해외주식 순위 8종 (`industry-theme`·`market-cap`·`new-highlow`·`trade-growth`·`trade-pbmn`·`trade-turnover`·`trade-vol`·`updown-rate`) | 응답 `output2.symb` | 1 | 최대 7 (티커) | 2026-09-27 |

## Kiwoom

아직 대조 전이다. 그동안의 실측 기록은 `AGENTS.md` 의 Kiwoom 항목에 있다 — 대조할 때 이 절로 옮긴다.

## NH PLUG

문서 출처: `https://www.nhplug.com/openapi-docs/<slug>/openapi.json` (krstock 기준 "API명세서 260911").
길이 기준은 그 스냅샷 `tests/nhplug/spec_lengths.json` — 확인된 초과는 그 파일의 `known_exceed` 와 아래 "길이" 에 함께 적는다.
모의(moapi)만 확인한 항목은 "모의" 로 표시한다. 테스트는 모의에서만 `mock_omits`/`nhplugMockOmits` 로 건너뛰고
운영(`NHPLUG_ENV=prod`)에서는 그대로 검사한다 — 운영에서 확인되면 이 표를 고친다.

### 요청 파라미터

| API | 문서 | 실서버 | 실측 | 코드 |
|---|---|---|---|---|
| 주식잔고조회 `balance`·잔고조회_실현손익 `realizedPnl`·투자계좌자산현황 `assetStatus` | `aly_qut_cd`(적용시세코드) **필수** (260911 추가) | 생략해도 `00000`, 1·2 와 같은 형태 (보유 0 계좌라 값 차이는 미확인) | 2026-09-27 모의 | 선택 인자, 값이 있을 때만 전송 |

### 응답 필드 (모의 서버가 보내지 않는 스펙 필드)

모의 서버는 아래 필드를 키째 생략한다. 모델에서 지우지 않는다(운영 미확인).

| API | 생략 필드 | 실측 |
|---|---|---|
| 계좌 목록 `/n2/acctinfo` | `cust_no` | 2026-09-27 모의 |
| `assetStatus` | Output_0 `cus_fnm`·`rnm_cfm_no`·`ctc_tp_cd_nm`·`act_amn_tab_cd`·`act_pdt_llf_cd`·`amn_emp_fnm`·`ima_wtm` | 2026-09-27 모의 |
| `balance` | Output_0 `fc_dca`·`fc_mgg_amt`·`fc_orr_pbl_amt`·`fnn_amt`·`rit_eal_amt`·`orr_pbl_amt`·`act_no` | 2026-09-27 모의 |
| 매수가능수량 `buyableQuantity` | Output_0 `sll_ctc_amt(1)`·`byn_ctc_amt1`·`sdr_xps(1)`·`ost_byn_ctc_amt`·`byn_ny_cns_orr_amt`·`int_rt`·`orr_pr`·`rp_eal_amt`·`ny_stl_qty` | 2026-09-27 모의 |
| 매도가능수량 `sellableQuantity` | Output_0 `cus_fnm`·`ost_dit_cd`·`cfd_lon_cd(_nm)`·`ttn_tp_cd(_nm)`·`sll_ny_stl_qty`·`byn_ny_stl_qty`·`phs_uit_pr` | 2026-09-27 모의 |
| `realizedPnl` | Output_0 `cus_fnm`·`rnm_cfm_no`·`act_atv_tp_dtl_cd`·`act_amn_tab_cd`·`act_pdt_llf_cd` | 2026-09-27 모의 |
| 실현손익일별합산 `dailyPnl` | Output_0 `act_fnm` | 2026-09-27 모의 |
| 종목별실현손익 `tradingPnl` | Output_0 `iem_cd`·`byn_uit_pr`·`sll_uit_pr`·`fee_sum`·`tax_sum` | 2026-09-27 모의 |

### 서버 동작 (문서에 없는 것)

- 응답 최상위에 스펙의 `message` 블록이 **키째 없다** (null 도 아님). 결과는 `rsp_cd`/`rsp_msg` 로 온다 (2026-09-27 모의).
- 모의 조회 성공 코드에 `XA102`("모의투자 조회가 완료되었습니다")가 섞인다 (2026-08-22). 문서의 성공은 `00000` 뿐.
- 모의 서버는 연속 호출에 `IGW42903`(HTTP 429, "API 호출 거래건수를 초과")을 준다. 1.5초 간격이면 통과 (2026-09-27).

### 길이

2026-09-27 모의 조회 12종·계좌 목록에서 스펙 길이를 넘는 값은 없었다.
