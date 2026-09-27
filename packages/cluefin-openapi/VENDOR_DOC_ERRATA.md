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

- 문서 출처: `openapi.kiwoom.com/guide/apiGuideContents/{jobTpCode}/{apiId}` 의 요청/응답 Body 표와 요청·응답 예시.
  Length 기준은 `tests/kiwoom/spec_lengths.json` (같은 표에서 덤프, 2026-09-27).
- **실측 환경**: 따로 적지 않으면 `KIWOOM_ENV=dev`(모의투자, `mockapi.kiwoom.com`). 모의서버는 주말에도 시세 데이터를 준다.
- 미국주식 문서는 필드의 약 70% 가 Length 칸이 비어 있다 — 그 필드는 길이를 대조하지 못한다.
- Python 응답 모델은 문서 표와 키가 사실상 같다 (2026-09-27 정적 대조, 254 TR 중 차이 2건). 아래 차이는 모두 실서버에서 나온 것이다.

### 응답 필드

| TR | 문서 | 실서버 | 실측 | 코드 |
|---|---|---|---|---|
| ka10044 일별기관매매종목 `daly_orgn_trde_stk[]` | 표: `prsm_avg_pric`·`cur_prc`·`avg_pric_pre`·`pre_rt` 없음 | 보냄 | 2026-08, 2026-09-27 | 모델에 추가 (TS 는 2026-08 에 이미 추가) |
| ka10099 종목정보리스트 `list[]`, ka10100 종목정보조회 | 표: `kind` 없음 | 보냄 | 2026-08, 2026-09-27 | 모델에 추가 (TS 는 이미 있음) |
| ka10080 주식분봉차트 `stk_min_pole_chart_qry[]` | 표: `acc_trde_qty` 없음 | 보냄 | 2026-08, 2026-09-27 | 모델에 추가 (TS 는 이미 있음) |
| ka90009 외국인기관매매상위 `frgnr_orgn_trde_upper[]` | 표: `pipe1`·`pipe2`·`pipe3` 없음 | 보냄 (의미 미확인). 예전 기록엔 ka10131 로 적혀 있었으나 ka10131 은 문서대로 온다 | 2026-08, 2026-09-27 | 모델에 추가 (TS 는 이미 있음) |

### 요청 파라미터

| TR | 문서 | 실서버 | 실측 | 코드 |
|---|---|---|---|---|
| ka90001 테마그룹별 | `qry_tp` 는 `0:전체검색, 2:종목검색` 만, `thema_nm` 은 "삭제 예정". 예전 문서엔 `1:테마검색` 이 있었다 | `qry_tp="1"`+`thema_nm="test"` → 빈 목록, 문서 예시값(`"0"`, `date_tp="10"`, `thema_nm=""`) → 데이터 | 2026-09-27 | Literal 은 `"1"` 을 남겨 둠 (CLI 호환), 테스트는 예시값 |
| ka90005·ka90010 프로그램매매추이 | `date` 는 "다른 날짜를 넣어도 당일치만 제공, 삭제 예정" (ka90005) | — | 2026-09-27 문서 확인 | 변경 없음 |

### 길이

요청 쪽은 **문서가 허용값으로 적은 코드가 문서 자신의 Length 보다 길다** (문서 내부 모순). 서버는 문서 허용값을 받는다.

| TR | 필드 | 문서 Length | 실제 | 실측 |
|---|---|---|---|---|
| ka10019 가격급등락 | 요청 `trde_qty_tp` | 4 | 5 (`00000` — 문서 허용값) | 2026-09-27 |
| ka10025 매물대집중 | 요청 `cycle_tp` | 2 | 3 (`100` — 문서 허용값) | 2026-09-27 |
| ka10099 종목정보리스트 | 응답 `list.state` | 20 | 21 | 2026-09-27, `mrkt_tp=0` |
| ka20007 업종주봉 | 요청 `base_dt` | 3 | 8 (Description 은 `YYYYMMDD`) | 2026-09-27 |
| ka90009 외국인기관매매상위 | 응답 `frgnr_orgn_trde_upper.orgn_netslmt_stk_nm` (종목명 칸 4개 모두 같은 Length) | 20 | 25 | 2026-09-27 |

정적 대조로만 확인한 같은 종류의 문서 모순 (Phase 3 이후 실측): ka10020 `trde_qty_tp`(4, 허용값 `00100`), ka10022·23 `trde_qty_tp`(1, `1000`),
ka10023 `stk_cnd`(1, `11`~`20`), ka10030 `mang_stk_incls`·`trde_qty_tp`·`trde_prica_tp`(1), ka10033 `trde_qty_tp`(3), ka10038 `dt`(2, `119`), ka10062 `unit_tp`(1, `1000`).

### 문서 표기 함정

- 종목코드 Description 의 `거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)` 는 거래소별 **형식 예시**다.
  `KRX:` 는 접두어가 아니다 — `KRX:069500` 을 보내면 에러 없이 빈 결과가 온다 (2026-09-27 ETF 8 TR, TS 테스트가 그렇게 통과하고 있었다).
- 기간 필드(`dt`: `5:5일, 10:10일…`)에 날짜를 넣으면 에러 없이 빈 결과가 오거나 요청 Length 를 넘는다.
- 계좌 TR 의 `dmst_stex_tp` 는 문서 허용값(`KRX`·`NXT`·`%` 등, TR 마다 다름)이 아니면 `501307:거래소구분을 확인해주십시오`
  로 거절된다. kt00004·kt00018 TS 테스트는 `'0'` 을 보내 이 에러를 받고 "모의 미지원" 으로 오해해 skip 돼 있었다 —
  문서 값이면 모의에서도 동작한다 (2026-09-27).
- ka10088 미체결분할주문상세는 없는 주문번호에 에러 없이 빈 목록을 준다 (2026-09-27 dev).

### 서버 동작 (문서에 없는 것)

그동안 `AGENTS.md`·메모리에 흩어져 있던 기록 (대조 전 실측):

- ka10009 는 문서 목록에서 빠졌지만 API 는 동작한다. ka10087·ka10098 은 2026-09-23 문서·서버 모두에서 제거됐다 (`1504`).
- 음수를 부호 겹침(`--123`)으로 내려준다 — `float()` 전에 정규화해야 한다.
- ka10051 업종별투자자순매수는 `cur_prc`·`pred_pre`·`flu_rt` 를 소수점 없는 100배 정수로 준다 (`-210` = -2.10%).
  같은 업종 TR 인 ka20001·ka20002 는 소수 문자열이라 TR 마다 다르다. ka10051·ka20002 의 `mrkt_tp` 는 한 자리
  (`"0"` 코스피 / `"1"` 코스닥)만 맞고, `"0001"` 을 주면 에러 없이 **코스닥** 데이터가 온다 (2026-09-02 prod).
- ka10061 종목별투자자기관별합계 `amt_qty_tp="1"`(금액)의 단위는 백만원이다.
- ka90001 테마명은 문서 Length(20)를 넘는다 (2026-09-02, 응답 모델 `max_length` 제거의 계기).

## NH PLUG

아직 대조 전이다. 그동안의 실측 기록은 `AGENTS.md` 의 NH PLUG 절에 있다 — 대조할 때 이 절로 옮긴다.
