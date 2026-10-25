# cluefin-openapi

> ⚠️ **웹소켓(실시간 시세·조건검색) 코드 주의사항**
>
> 웹소켓 연결 관련 integration 테스트는 **장중(09:00–15:30 KST)에만** 실제 검증이 가능합니다.
> 메인테이너가 본업으로 인해 장중 테스트가 어려워, 웹소켓 관련 변경사항은 실서버 검증이
> 지연되거나 충분히 이루어지지 않았을 수 있습니다. 웹소켓 기능을 사용하거나 수정할 때는
> 이 점을 감안하고, 가능하면 장중에 직접 동작을 확인해 주세요.

> **cluefin-openapi**: 주식 투자 OpenAPI를 위한 Python 클라이언트

![Python](https://img.shields.io/badge/Python-3.11%2B-green)
![Pydantic](https://img.shields.io/badge/Pydantic-Type%20Safe-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 주요 기능

- **계좌 정보 조회**: 잔고, 보유종목, 수익률 등 계좌 관련 정보
- **국내/해외 주식 정보**: 실시간 시세, 종목 정보, 기업 정보
- **키움 미국주식 API**: 계좌, 주문, 시세, 차트, 순위정보 등 미국주식 전용 카테고리 (`client.overseas_*`)
- **NH투자증권 PLUG API**: 국내주식(krstock) 31종 · 해외주식(gbstock) 18종 REST — 주문/조회/시세 카테고리
- **웹소켓 조건검색·실시간 시세**: 국내/미국 조건검색식 조회·요청·실시간 등록, 실시간 시세 구독
- **차트 데이터 및 분석**: 일/주/월 차트, 기술적 지표, 시계열 데이터
- **ETF, 섹터, 테마**: ETF 정보, 업종별 정보, 테마별 종목 분류
- **시장 상황 모니터링**: 시장 지수, 거래량, 시장 동향
- **기업 공시 분석 (DART)**: 공시 원문, 재무제표, 대량보유상황 등 공시 데이터
- **미국 공시 (SEC EDGAR)**: 티커→CIK, 제출 이력, XBRL 값(companyfacts·companyconcept·frames), 공시 원문·XBRL·13F 파일 다운로드, CUSIP→티커(Fails-to-Deliver)

## ⚡ 빠른 시작

### 설치

```bash
# 워크스페이스 설치 (권장)
git clone https://github.com/kgcrom/cluefin
cd cluefin
uv venv --python 3.11
uv sync --all-packages

# 패키지만 단독 설치
pip install cluefin-openapi
```

## 🎯 왜 cluefin-openapi인가요?

### 통합된 인터페이스
키움증권, 한국투자증권(KIS), NH투자증권(PLUG), DART 등 여러 금융 OpenAPI를 하나의 Python 인터페이스로 통합하여 제공합니다.

### 개발 시간 단축
복잡한 금융 API 통합 작업을 대신 처리하여, 투자 도구 개발에 집중할 수 있습니다.

### 타입 안전성
Pydantic을 활용한 강력한 타입 검증으로 런타임 에러를 방지합니다.

### 풍부한 기능
- 실시간 데이터 스트리밍
- 자동 토큰 갱신
- 요청 제한 관리
- 포괄적인 에러 처리

## 📖 시작하기

### 1. 키움증권 API 신청

1. [키움증권 OpenAPI 사이트](https://apiportal.kiwoom.com/)에서 계정 생성
2. API 사용 신청 및 승인 대기
3. APP_KEY 및 SECRET_KEY 발급 받기

### 2. 한국투자증권 API 신청

1. [한국투자증권 OpenAPI 사이트](https://apiportal.koreainvestment.com/)에서 계정 생성
2. API 사용 신청 및 승인 대기
3. APP_KEY 및 SECRET_KEY 발급 받기

### 3. NH투자증권 PLUG API 신청

1. [NH투자증권 PLUG 사이트](https://www.nhplug.com/)에서 계정 생성 (나무증권 사용자는 [N2 PLUG](https://www.n2plug.com/))
2. API 사용 신청 및 승인 대기
3. APP_KEY 및 SECRET_KEY 발급 받기

> 토큰 발급(`/oauth2/token`)은 **운영 도메인 전용**입니다(모의투자 엔드포인트 없음).
> 발급받은 토큰 하나로 운영·모의투자 호출을 모두 처리하므로, `Auth.generate()`의
> 파일 캐시 경로를 반드시 사용하세요. 불필요한 재발급은 계좌 보안 알림을 유발합니다.

### 4. 환경 변수 설정

```bash
# 워크스페이스 루트 디렉토리에서
cp packages/cluefin-openapi/.env.sample .env

# .env 파일 수정 (워크스페이스 루트에 생성)

# 키움증권 API 키 설정 (OAuth2-style 인증)
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here
KIWOOM_ENV=dev # options: prod | dev(default)

# 한국투자증권 API 키 설정 (토큰 기반 인증)
KIS_APP_KEY=your_kis_app_key_here
KIS_SECRET_KEY=your_kis_secret_key_here
KIS_ENV=dev # options: prod | dev(default)

# NH투자증권 PLUG API 키 설정 (토큰 기반 인증)
NHPLUG_APP_KEY=your_nhplug_app_key_here
NHPLUG_SECRET_KEY=your_nhplug_secret_key_here
# NHPLUG_ENV는 조회·주문 도메인만 선택합니다 (prod: api.nhplug.com, dev: moapi.nhplug.com 모의투자).
# 토큰 발급은 env와 무관하게 항상 운영 도메인을 씁니다.
NHPLUG_ENV=dev # options: prod | dev(default)

# 금융감독원 DART API 키 설정
DART_AUTH_KEY=your_dart_auth_key_here

# SEC EDGAR — API 키 대신 User-Agent에 "이름 이메일"을 밝혀야 합니다 (없으면 SEC가 403)
SEC_USER_AGENT="Your Name your.email@example.com"

# 한국은행 ECOS — 비우면 공개 시험 키 sample (한 번에 10행, 쪽 넘김으로 이어 받음)
ECOS_AUTH_KEY=your_ecos_auth_key_here
```

### 기본 사용법

```python
from loguru import logger
from pydantic import SecretStr
import os
from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
import dotenv

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")
auth = Auth(
    app_key=os.getenv("KIWOOM_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIWOOM_SECRET_KEY")),
    env="dev",  # 개발환경: "dev", 운영환경: "prod"
)

# 토큰 생성 및 클라이언트 초기화
token = auth.generate_token()
client = Client(token=token.get_token(), env="dev")

# 삼성전자(005930) 일별 실현손익 조회
response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")
logger.info(f"응답 헤더: ${response.headers}")
logger.info(f"응답 데이터: ${response.body}")
```

## 📚 API 문서

### 인증

```python
# 키움증권
from loguru import logger
import os
from pydantic import SecretStr
import dotenv
from cluefin_openapi.kiwoom._auth import Auth

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")

auth = Auth(
    app_key=os.getenv("KIWOOM_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIWOOM_SECRET_KEY")),
    env="dev",  # 개발환경: "dev", 운영환경: "prod"
)

# 토큰 생성
token = auth.generate_token()
logger.info(f"token => ${token}")
```

### 클라이언트 초기화

```python
# 키움증권
from cluefin_openapi.kiwoom._client import Client

client = Client(
    token=token.get_token(),
    env="dev",
)
```

```python
# 한국투자증권
from loguru import logger
import os
from pydantic import SecretStr
import dotenv
from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._client import Client as KISClient

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")

# 토큰 생성
auth = Auth(
    app_key=os.getenv("KIS_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIS_SECRET_KEY")),
    env="dev",
)
token = auth.generate()

# 클라이언트 초기화
kis_client = KISClient(
    app_key=os.getenv("KIS_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIS_SECRET_KEY")),
    token=token,
    env="dev",
)
logger.info(f"kis_client => ${kis_client}")
```

```python
# NH투자증권 PLUG
from loguru import logger
import os
from pydantic import SecretStr
import dotenv
from cluefin_openapi.nhplug import Auth as NHPlugAuth, HttpClient as NHPlugClient

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")

# 토큰 생성 (파일 캐시 우선 — 만료 전까지 실제 발급은 1회)
auth = NHPlugAuth(
    app_key=os.getenv("NHPLUG_APP_KEY"),
    secret_key=SecretStr(os.getenv("NHPLUG_SECRET_KEY")),
)
token = auth.generate()

# 클라이언트 초기화 (env는 조회·주문 도메인만 결정)
nhplug_client = NHPlugClient(
    token=token.access_token,
    app_key=os.getenv("NHPLUG_APP_KEY"),
    secret_key=SecretStr(os.getenv("NHPLUG_SECRET_KEY")),
    env="dev",  # 모의투자: "dev", 운영: "prod"
)
logger.info(f"nhplug_client => ${nhplug_client}")
```

## 📊 KIS API 사용 예제

### 국내 주식 시세 조회

```python
from loguru import logger
from cluefin_openapi.kis._client import Client as KISClient

# 주식 현재가 시세 조회
current_price = kis_client.domestic_basic_quote.get_inquire_price(
    fid_cond_mrkt_div_code="J",  # 시장 분류 코드 (J: 주식)
    fid_input_iscd="005930"      # 종목 코드 (삼성전자)
)
logger.info(f"현재가: {current_price}")

# 주식 일별 시세 조회
daily_price = kis_client.domestic_basic_quote.get_inquire_daily_itemchartprice(
    fid_cond_mrkt_div_code="J",
    fid_input_iscd="005930",
    fid_input_date_1="20250101",  # 조회 시작일
    fid_input_date_2="20250131",  # 조회 종료일
    fid_period_div_code="D"        # 기간 분류 코드 (D: 일)
)
logger.info(f"일별 시세: {daily_price}")
```

### 국내 계좌 조회

```python
# 주식 잔고 조회
balance = kis_client.domestic_account.get_inquire_balance(
    cano="12345678",      # 종합계좌번호
    acnt_prdt_cd="01",    # 계좌상품코드
    afhr_flpr_yn="N",     # 시간외단일가여부
    ofl_yn="N",           # 오프라인여부
    inqr_dvsn="01",       # 조회구분
    unpr_dvsn="01",       # 단가구분
    fund_sttl_icld_yn="N", # 펀드결제분포함여부
    fncg_amt_auto_rdpt_yn="N", # 융자금액자동상환여부
    prcs_dvsn="00",       # 처리구분
    ctx_area_fk100="",    # 연속조회검색조건100
    ctx_area_nk100=""     # 연속조회키100
)
logger.info(f"잔고: {balance}")
```

### 해외 주식 시세 조회

```python
# 해외 주식 현재가 조회 (미국 주식)
overseas_price = kis_client.overseas_basic_quote.get_inquire_price(
    exch="NAS",           # 거래소 코드 (NAS: 나스닥)
    symb="AAPL"           # 종목 코드 (애플)
)
logger.info(f"해외 주식 현재가: {overseas_price}")
```

## 🏦 NH PLUG API 사용 예제

모든 호출은 `POST` + JSON 바디이며, 요청 파라미터는 `Input_0` 봉투로 감싸 전송됩니다.
응답은 `rsp_cd`/`rsp_msg` + `Output_N` 봉투이고, 연속조회는 `cts` 인자로 처리합니다.

카테고리는 `common`(계좌·실시간 세션), 국내주식 `krstock_order`/`krstock_inquiry`/`krstock_quote`,
해외주식 `overseas_stock_order`/`overseas_stock_inquiry`/`overseas_stock_quote` 입니다.

### 계좌 목록 조회

```python
from loguru import logger

# 계좌번호는 모든 조회·주문 API의 act_no 로 사용합니다.
# 운영은 acct_type=01·02, 모의투자는 03 계좌만 유효합니다.
accounts = nhplug_client.common.get_account_list()
for account in accounts.body.output_0 or []:
    logger.info(f"{account.acct_no} (acct_type={account.acct_type})")
```

### 국내주식 시세·잔고 조회

```python
# 주식현재가 시세 — 시세 API는 계좌번호가 필요 없습니다.
current = nhplug_client.krstock_quote.current_price(market_cd="KRX", iem_cd="005930")
logger.info(f"현재가: {current.body.output_0.stck_prpr}")

# 주식 잔고 조회
balance = nhplug_client.krstock_inquiry.balance(
    act_no="12345678901",
    bnc_bse_cd="1",      # 잔고기준코드: 주식관련 총 평가(체결기준)
    ltg_aot_dit_cd="1",  # 상장폐지구분코드: 상장종목
    aet_bse="1",         # 자산기준: 순자산
    qut_dit_cd="UNT",    # 시세구분코드: 통합시세
)
logger.info(f"잔고: {balance.body}")
```

### 해외주식 조회·시세

```python
# 해외주식 잔고 (요약 Output_0 + 종목별 Output_1)
balance = nhplug_client.overseas_stock_inquiry.balance(
    act_no="12345678901",
    qut_iqr_dit_cd="9",       # 전체
    fc_sec_trd_nat_cd="200",  # 미국
    cur_cd="KRW",             # 전체
)
logger.info(f"평가금액합계: {balance.body.output_0.eal_amt_sum}")

# 해외주식 매수가능금액 조회
buyable = nhplug_client.overseas_stock_inquiry.buyable_amount(
    act_no="12345678901",
    pcs_dit="1",              # 매수가능금액조회
    fc_sec_trd_nat_cd="200",  # 미국
    iem_cd="AAPL",
    wtm_cur_knd_cd="2",       # 원화
    oss_orr_knd_cd="1",       # GTS(미국시장주문)
    ahi_nmn_pr_tp_cd="03",    # 시장가
)
logger.info(f"매수가능: {buyable.body.output_0}")

# 해외주식 현재가상세 — 종목명은 iem_nm 을 읽습니다(스펙의 kor_name 은 실서버 미사용)
price = nhplug_client.overseas_stock_quote.current(iem_cd="AAPL")
logger.info(f"{price.body.output_0.iem_nm}: {price.body.output_0.trdprc}")
```

> ⚠️ 해외주식 시세 4종(`/gbstock/quote/v1/*`)은 **모의투자에서 제공되지 않습니다**.
> `NHPLUG_ENV=dev`로 호출하면 `IGW40019`가 반환되며, `current`의 경우
> "종목코드(iem_cd)를 확인해주세요"라는 (실제 원인과 무관한) 메시지로 거부됩니다.

### 해외주식 주문

```python
# ⚠️ env="prod"는 실제 주문이 접수됩니다. 검증은 모의투자(env="dev")로 하세요.
order = nhplug_client.overseas_stock_order.buy(
    act_no="12345678901",
    fc_sec_trd_nat_cd="200",  # 미국
    iem_cd="AAPL",
    orr_qty=1,
    ahi_nmn_pr_tp_cd="00",    # 지정가
    wtm_cur_knd_cd="2",       # 원화
    fc_orr_uit_pr=300.00,     # 지정가 유형이면 필수
)
logger.info(f"주문번호: {order.body.output_0.orr_no}")
```

### NH PLUG 실시간 시세 (웹소켓)

`SocketClient`는 비동기(`asyncio`)로 동작하며, `tr_cd`/`tr_key` 기반으로 구독합니다.
`market`으로 국내(`"kr"`, `:7070`)/해외(`"gb"`, `:7080`) 엔드포인트를 선택합니다
(`env="dev"`는 `market`과 무관하게 모의투자 단일 주소 `:17070`을 씁니다).

`tr_cd`는 REST 엔드포인트가 아니라 **웹소켓 전용 실시간 채널 코드**입니다.
정본은 각 자산군 `openapi.json`의 `x-realtime-channels[].tr_cd` 입니다.

| 자산군 | tr_cd | 채널 | tr_key |
|---|---|---|---|
| 국내 | `mc` / `mb` / `ma` | 체결가 · 호가 · 예상체결 (통합시세) | 종목코드 |
| 국내 | `oc` / `ob` / `oa` | 체결가 · 호가 · 예상체결 (KRX) | 종목코드 |
| 국내 | `nc` / `nb` / `na` | 체결가 · 호가 · 예상체결 (NXT) | 종목코드 |
| 국내 | `d2` / `d3` | 체결통보 · 주문내역통보 | 사용자ID |
| 해외 | `RC` / `RH` | 실시간 체결가 · 호가 (유료시세 약정 필요) | 종목코드 |
| 해외 | `rc` / `rh` | 지연 체결가 · 호가 (미국·중국만) | 종목코드 |
| 해외 | `d0` / `d1` | 체결통보 · 주문내역통보 | 사용자ID |

> ⚠️ 해외 채널 코드는 **대소문자로 실시간/지연이 갈립니다**(`RC`=실시간 유료, `rc`=지연).
> 전체 목록(회원사·프로그램매매·시간외 등)은 위 `x-realtime-channels`를 참고하세요.

```python
import asyncio
from cluefin_openapi.nhplug import SocketClient

async def main():
    # 국내 실시간 체결가(통합시세) — 해외는 market="gb" + env="prod" + tr_cd="rc" 등
    async with SocketClient(token=token.access_token, env="dev", market="kr") as ws:
        await ws.subscribe(tr_cd="mc", tr_key="005930")
        async for event in ws.events():
            if event.event_type == "data":
                print(event.tr_cd, event.data)

asyncio.run(main())
```

체결·주문내역 통보(`d2`/`d3`, `d0`/`d1`)는 종목코드가 아니라 **사용자ID**를 `tr_key`로 넘깁니다.

세션이 남아 끊기지 않을 때는 `nhplug_client.common.close_websocket_session()`으로 정리합니다.

## 🇺🇸 SEC EDGAR 사용 예제

SEC는 API 키가 없고, 모든 요청의 User-Agent에 이름과 이메일을 요구합니다. 클라이언트는 초당 8회(SEC 한도 10회)로
요청을 제한하고, 429·5xx는 재시도합니다. 403은 User-Agent가 없거나 한도를 넘겨 차단된 것이라 재시도하지 않습니다.

```python
import os

from cluefin_openapi.sec import Client

client = Client(user_agent=os.environ["SEC_USER_AGENT"])

# 티커 → CIK
cik = client.reference.ticker_to_cik("AAPL")  # 320193

# 제출 이력 (최신순). include_older=True 면 오래된 페이지까지 받는다
tenks = client.submissions.filings(cik, forms=["10-K"])
latest = tenks[0]  # accession_number, filing_date, report_date, primary_document, is_inline_xbrl ...

# XBRL 값: 회사 전체 / 개념 하나 / 기간 하나의 모든 회사
facts = client.xbrl.company_facts(cik)
revenue = facts.concept("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax")
concept = client.xbrl.company_concept(cik, "us-gaap", "NetIncomeLoss")
frame = client.xbrl.frames("us-gaap", "Assets", "USD", "CY2023Q4I")

# 시점 기준 값: 같은 기간 값이 원공시·비교 표시·정정마다 한 행씩 있고 재작성으로 바뀌기도 한다.
# as_of 전날까지 제출된(filed < as_of) 행 중 기간마다 가장 늦은 행을 고른다. frame 으로 고르면 미래 값이 섞인다
from datetime import date
from cluefin_openapi.sec import values_as_of

known = values_as_of(concept.units["USD"], date(2024, 1, 2))  # 기간(start, end)마다 FactValue 하나

# 공시 원문과 XBRL 파일 (cluefin-xbrl 의 parse_xbrl_directory 로 파싱)
client.archives.download_filing_document(cik, latest.accession_number, latest.primary_document, destination="aapl")
client.archives.download_xbrl_files(cik, latest.accession_number, destination="aapl-xbrl")

# 공시 상세: 문서마다 종류(EX-99.1 등)와 제출 당사자 CIK. 폴더는 다른 회사 CIK 경로로도 열리니 ciks로 확인한다
detail = client.archives.filing_detail(cik, latest.accession_number)
press = next(d for d in detail.documents if d.type == "EX-99.1")  # 8-K 실적 보도자료 (파일명은 공시마다 다름)
assert cik in detail.ciks

# 13F 기관 보유 보고: 표지와 정보표 (cluefin-sec-notes 의 load_13f 로 파싱)
thirteen_f = client.submissions.filings(1067983, forms=["13F-HR"])[0]
files = client.archives.download_13f_files(1067983, thirteen_f.accession_number, destination="brk-13f")
files.cover, files.information_table  # 통지(13F-NT)는 information_table 이 None

# CUSIP → 티커: 13F 정보표엔 티커가 없다. Fails-to-Deliver(반월마다, 2009-07~)에 CUSIP·티커가 함께 있다
from cluefin_openapi.sec import cusip_symbols

recent = client.fails_to_deliver.files()[:12]  # 최신순. 6개월치
symbols = cusip_symbols(r for f in recent for r in client.fails_to_deliver.records(f))
symbols.get("037833100")  # "AAPL". 티커가 바뀐 CUSIP은 결제일이 가장 늦은 티커
```

Fails-to-Deliver에는 결제 불이행이 한 번이라도 있었던 종목만 실립니다. 6개월치로 2026년 13F 12건의 금액
99.7–99.9%가 매핑됐고(행 기준 93–99%), 과거 보고를 매핑할 때는 그 시기 파일을 쓰는 편이 맞습니다(티커는 바뀝니다).

`BrokerClientFactory().create("sec")` 도 `.env` 의 `SEC_USER_AGENT` 로 같은 클라이언트를 만듭니다.

## 🏦 한국은행 ECOS 사용 예제

ECOS(경제통계시스템) Open API 6개 서비스를 지원합니다. 키가 없으면 공개 시험 키 `sample`로 동작하고(한 번에 10행,
클라이언트가 쪽 넘김으로 이어 받음), [ECOS](https://ecos.bok.or.kr/api/)에서 받은 키를 주면 1000행씩 받습니다.

```python
import os

from cluefin_openapi.ecos import CORP_BOND_3Y_AA_MINUS, CPI_TOTAL, KTB_10Y, USD_KRW, Client

client = Client(auth_key=os.getenv("ECOS_AUTH_KEY"))  # None 이면 sample

# 통계 조회: 통계표·주기·기간·항목코드. 휴일은 행이 없으니 "최근 값"은 2주쯤 받아 마지막 행을 쓴다
page = client.statistic_search.search_series(KTB_10Y, "20261005", "20261017")
latest = page.rows[-1]
print(latest.time, latest.data_value, latest.unit_name)  # 20261016 4.182 연%  (원문 문자열, latest.value 는 Decimal)

# 항목코드 없이 통계표 전체 (시장금리 817Y002 는 27개 항목)
rates = client.statistic_search.search("817Y002", "D", "20261005", "20261017")

# 항목코드 찾기
tables = client.statistic_catalog.table_list()              # 통계표 목록 (분류 행 포함)
items = client.statistic_catalog.item_list("817Y002")       # 통계표의 항목
key100 = client.statistic_catalog.key_statistic_list()      # 100대 통계지표 최근 값

# 용어사전·메타
client.statistic_glossary.word("소비자동향지수")
client.statistic_glossary.meta("경제심리지수")
```

- 상수: 국고채 1·3·5·10·20·30년, 통안증권·CD 91일, 회사채 3년 AA-·BBB-(`MARKET_RATES`), 원/달러 매매기준율 `USD_KRW`,
  소비자물가 총지수 `CPI_TOTAL`. 값은 원문 그대로(연 % 등) 두고 비율 변환은 쓰는 쪽에서 합니다.
- 오류도 HTTP 200 본문 `RESULT.CODE`로 옵니다. 데이터 없음(`INFO-200`)은 빈 `rows`, 나머지는
  `EcosAuthenticationError`·`EcosRequestError`(`EcosSampleLimitError`)·`EcosServerError`(`EcosQueryTimeoutError`)·
  `EcosRateLimitError`입니다. 예외의 `hint` 에 코드별 조치가 실리고, 일시 오류(`ERROR-600`·`602`)는 자동 재시도합니다.
- `BrokerClientFactory().create("ecos")` 는 `.env` 의 `ECOS_AUTH_KEY`(없으면 sample)로 같은 클라이언트를 만듭니다.

### 조회할 수 있는 데이터 — 금리·신용·증시

ECOS에서 조회할 수 있는 표는 617개(통화/금융·국민계정·환율·물가·기업경영분석·심리지수·지급결제·산업·해외 9개 분류)입니다.
그중 시장을 볼 때 자주 쓰는 금리·신용·증시 계열을 정리했습니다. 2026-10-20 실조회 기준이고, 호출은 모두
`client.statistic_search.search(통계표, 주기, 시작, 끝, [항목코드…])` 형식입니다.

| 보고 싶은 것 | 통계표 | 주기 | 항목코드 | 단위 |
|---|---|---|---|---|
| 한국은행 기준금리 | `722Y001` | D·M·Q·A | `0101000` | 연% |
| CD 91일 · CP 91일 · KOFR(무위험 익일물) | `817Y002` | D | `010502000` · `010503000` · `010901000` | 연% |
| 국고채 1·3·5·10·20·30년 | `817Y002` | D | 상수 `KTB_1Y`~`KTB_30Y` (2·50년도 같은 표) | 연% |
| 회사채 3년 AA- · BBB- | `817Y002` | D | `010300000` · `010320000` | 연% |
| 예금은행 대출금리(신규취급액): 평균 · 주택담보 · 기업 | `121Y006` | M | `BECBLA01` · `BECBLA0302` · `BECBLA02` | 연% |
| M2(평잔, 원계열) | `161Y006` | M | `BBHA00` | 십억원 |
| 가계신용 | `151Y001` | Q | `1000000` | 십억원 |
| 예금은행 가계대출 | `151Y002` | M | `1111000` | 십억원 |
| 은행 연체율(1일 이상): 가계 · 기업 | `901Y054` | M | `["MO3AB", "AB"]` · `["MO3AA", "AB"]` | % |
| 대출태도지수(국내은행 종합) | `514Y001` | Q | `AA` | 지수 |
| KOSPI · KOSDAQ 지수 | `802Y001` | D | `0001000` · `0089000` | 지수 |
| 유가증권시장 외국인 순매수 · 시가총액 | `802Y001` | D | `0030000` · `0183000` | 억원 |
| KOSPI PER · 배당수익률 | `901Y014` | M | `1110000` · `1100000` | 배 · % |
| 투자자 예탁금 · 신용융자 잔고 | `901Y056` | M | `S23A` · `S23E` | 원 |
| 투자자별 순매수 대금: 외국인 · 개인 | `901Y055` | M | `["S22CC", "VA"]` · `["S22CB", "VA"]` | 백만원 |

```python
# 기준금리 월말 값
client.statistic_search.search("722Y001", "M", "201601", "202609", ["0101000"])

# 가계대출 연체율 — 항목 그룹이 둘인 표는 그룹 순서대로 두 코드를 넣는다
client.statistic_search.search("901Y054", "M", "201601", "202609", ["MO3AB", "AB"])
```

- **장단기 금리차·신용 스프레드는 따로 있는 계열이 아닙니다.** 국고채 10년−3년, 회사채 AA−−국고채 3년처럼 두 계열을 받아 날짜를 맞춰 뺍니다.
- **단위가 표마다 다릅니다**(원·억원·십억원·백만원, 연%·%). 행의 `unit_name`을 보고 환산하세요.
- **월·분기 통계는 늦게 나옵니다.** 2026-10-20 기준 대출금리·M2는 2026-08, 연체율은 2026-07, 가계신용은
  2026Q2가 마지막이었습니다. "최근 값"을 받을 때는 기간을 넉넉히 잡고 마지막 행을 씁니다.
- 주식 계열은 한국거래소 자료를 ECOS가 다시 싣는 것입니다. 종목 시세는 증권사 API가 낫고, ECOS는 금리·환율과
  같은 날짜 축으로 맞춰 볼 때 씁니다.
- 위 표에 없는 계열은 `statistic_catalog.table_list()`에서 표를 찾고 `item_list(통계표)`로 항목코드·주기·수록 기간을 확인합니다.

## 🔌 키움 웹소켓 사용 예제 (조건검색·실시간 시세)

키움 웹소켓 기능은 HTTP `Client`와 별개로 비동기(`asyncio`)로 동작합니다.
`KiwoomWebSocketClient`가 LOGIN/PING을 처리하며, `market` 파라미터로 국내(`"domestic"`)/미국(`"overseas"`) 엔드포인트를 선택합니다.

```python
import asyncio
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketClient
from cluefin_openapi.kiwoom._domestic_condition_search import DomesticConditionSearch

async def main():
    # 국내주식 조건검색 (미국주식은 market="overseas" + OverseasConditionSearch)
    async with KiwoomWebSocketClient(token=token.get_token(), env="dev", market="domestic") as ws:
        condition = DomesticConditionSearch(ws)

        # 조건검색식 목록 조회
        condition_list = await condition.get_condition_search_list()

        # 첫 번째 조건검색식으로 검색 요청
        seq = condition_list.data[0].seq
        result = await condition.request_condition_search(seq=seq)
        print(result)

asyncio.run(main())
```

실시간 시세는 같은 방식으로 `DomesticRealtime`(국내) / `OverseasRealtime`(미국) 클래스를 사용해 `register`/`remove`로 구독을 관리합니다.

## 🔧 구성 옵션

### 로깅 설정

```python
import logging
from loguru import logger

# 로그 레벨 설정
logger.add("kiwoom_api.log", level="INFO", rotation="10 MB")
```

### 요청 제한 관리

라이브러리는 자동으로 API 요청 제한을 관리합니다:

- 초당 요청 수 제한
- 일일 요청 수 제한
- 자동 재시도 메커니즘

## ⚠️ 에러 처리

### 키움증권 API 에러 처리

```python
from loguru import logger
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError, KiwoomRateLimitError

try:
    response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")
except KiwoomRateLimitError as e:
    logger.info(f"요청 제한 초과, 재시도 대기: {e.retry_after}")
except KiwoomAPIError as e:
    logger.info(f"API 에러: {e.message}")
    logger.info(f"HTTP 상태 코드: {e.status_code}")
    logger.info(f"응답 데이터: {e.response_data}")
except Exception as e:
    logger.info(f"일반 에러: {str(e)}")
```

키움 API 서버가 응답 본문에 `return_code`를 내려주면, 라이브러리가 `_error_codes.py`의
`KIWOOM_ERROR_CODES` 매핑으로 에러 메시지를 해석하고 코드 성격에 맞는 예외 클래스
(`KiwoomValidationError`, `KiwoomAuthenticationError`, `KiwoomRateLimitError`,
`KiwoomServerError` 등 `KiwoomAPIError` 하위 클래스)를 발생시킵니다.

### 한국투자증권 API 에러 처리

```python
from loguru import logger
from cluefin_openapi.kis._exceptions import KISAPIError

try:
    response = kis_client.domestic_basic_quote.get_inquire_price(
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="005930"
    )
except KISAPIError as e:
    logger.error(f"KIS API 에러: {e.message}")
    logger.error(f"HTTP 상태 코드: {e.status_code}")
except Exception as e:
    logger.error(f"일반 에러: {str(e)}")
```

### NH투자증권 PLUG API 에러 처리

NH PLUG는 **HTTP 200이어도 응답 본문 `rsp_cd`가 실패**일 수 있습니다. 각 카테고리가
본문 코드를 먼저 검사해 실패면 `NHPlugAPIError`를 던지므로, 200을 성공으로 가정하면 안 됩니다.

뜻이 확인된 본문 코드는 전용 예외로 나뉘고(모두 `NHPlugAPIError` 하위), 어떤 예외든 `e.rsp_cd` 로
코드를 바로 볼 수 있습니다.

| 예외 | `rsp_cd` | 뜻 |
|---|---|---|
| `NHPlugNoDataError` | `13578`·`11512`·`16935` | 조회 결과 0건 (잔고·내역이 없는 계좌) |
| `NHPlugMockUnsupportedError` | `19999` | 모의투자 미제공 업무 — 운영에서만 호출 가능 |
| `NHPlugNotBusinessDayError` | `14100` | 영업일이 아님 |
| `NHPlugAPIError` | 그 외 | 분류되지 않은 실패 |

```python
from loguru import logger
from cluefin_openapi.nhplug import (
    NHPlugAPIError,
    NHPlugNoDataError,
    NHPlugRateLimitError,
    NHPlugValidationError,
)

try:
    response = nhplug_client.krstock_inquiry.sellable_quantity(act_no="12345678901", iem_cd="005930", cfd_lon_cd="00")
except NHPlugNoDataError:
    logger.info("매도 가능한 잔고 없음")
except NHPlugValidationError as e:
    # 입력 오류는 HTTP 400 + rsp_cd(IGW…) 형태로 옵니다
    logger.error(f"입력 오류 [{e.rsp_cd}]: {e.message}")
except NHPlugRateLimitError as e:
    logger.error(f"요청 제한 초과: {e.message}")
except NHPlugAPIError as e:
    logger.error(f"API 에러 [{e.rsp_cd}]: {e.message}")
```

성공으로 취급하는 본문 코드는 `nhplug._model.SUCCESS_RSP_CODES`로 관리합니다.
문서상 성공은 `00000` 뿐이지만, 실서버는 API 마다 다른 성공 코드를 주므로 함께 포함되어 있습니다 —
모의 조회의 `XA102`("모의투자 조회가 완료되었습니다"), 운영 조회의 `00166`("조회가 완료되었습니다"),
운영 매수가능수량의 `00221`("계좌/종목별 주문가능수량/금액 조회가 완료되었습니다").

### 일반적인 에러 시나리오

**키움증권 API 서버 오류코드 (`return_code`):**
- `1501`: API ID가 Null이거나 값이 없습니다
- `1700`: 허용된 API 요청 개수를 초과하였습니다
- `8005`: Token이 유효하지 않습니다

전체 목록은 `cluefin_openapi.kiwoom._error_codes`의 `KIWOOM_ERROR_CODES`를 참고하세요.

**한국투자증권 API 에러 코드:**
- `EGW00001`: 잘못된 요청 형식
- `EGW00123`: API 키 오류
- `EGW00201`: 토큰 만료 - 토큰 재생성 필요 (1분 간격 제한)
- `40000000`: 서버 내부 오류

**NH투자증권 PLUG API 에러 코드 (`rsp_cd`):**
- `00000`: 성공 / `XA102`: 성공(모의투자 조회) / `00166`·`00221`: 성공(운영 조회)
- `IGW40018`, `IGW40019`: 입력값 오류 — 단, `IGW40019`는 "모의투자 미지원"을 뜻할 때도 있습니다
- `14100`: 모의투자 영업일이 아닙니다 (`NHPlugNotBusinessDayError`)
- `19999`: 모의투자에서는 해당업무가 제공되지 않습니다 (`NHPlugMockUnsupportedError`)
- `13578`·`11512`·`16935`: 조회 결과 없음 (`NHPlugNoDataError`)
- `IGW50025`: 일시적인 오류 (열린 실시간 세션이 없을 때의 세션해제 응답)

## 📓 예제 노트북

`examples/` 디렉토리에 클라이언트를 실제로 호출해 보는 Jupyter 노트북이 있습니다.

```bash
# 워크스페이스 루트에서 실행 — .env.test 의 자격증명을 사용합니다
uv run --with jupyter jupyter lab packages/cluefin-openapi/examples/nhplug_quickstart.ipynb
```

- `nhplug_quickstart.ipynb` — NH PLUG 인증 → 계좌 조회 → 국내/해외 시세·잔고 조회. `NHPLUG_ENV=dev`(모의투자) 기준이며, **`prod` 는 실계좌**이므로 주문 셀은 주석 처리되어 있습니다.

## 🧪 테스트

```bash
# 워크스페이스 루트에서 실행

# 단위 테스트만 실행 (통합 테스트 제외)
uv run pytest -m "not integration"

# 통합 테스트만 실행 (API 키 필요)
uv run pytest -m "integration"

# KIS integration 테스트 실패 시 마지막 raw 응답 출력
# 기본값은 조용함. 필요할 때만 켜서 사용
KIS_DEBUG_ON_FAILURE=1 uv run pytest packages/cluefin-openapi/tests/kis/ -m "integration"

# Kiwoom 통합 테스트는 .env.test의 KIWOOM_ENV(dev|prod)를 사용
# - KIWOOM_ENV=dev  -> mockapi 키 사용
# - KIWOOM_ENV=prod -> 실서버 키 사용

# NH PLUG 통합 테스트도 .env.test의 NHPLUG_ENV(dev|prod)를 사용
# 모의투자 미지원 API는 real_account_only 로 자동 skip 됩니다
uv run pytest packages/cluefin-openapi/tests/nhplug/ -m "integration"

# 권한/샌드박스 환경에서 uv 캐시 접근 오류가 나면
# (예: ".../.cache/uv/... Operation not permitted")
# 워크스페이스 내부 캐시 경로를 지정해서 실행
mkdir -p .uv-cache
UV_CACHE_DIR=.uv-cache uv run pytest packages/cluefin-openapi/tests/kiwoom/test_domestic_chart_integration.py -q

# cluefin-openapi 패키지 테스트만 실행
uv run pytest packages/cluefin-openapi/tests/ -v

# 특정 모듈 테스트 실행
uv run pytest packages/cluefin-openapi/tests/kiwoom/test_auth_unit.py -v

# 코드 커버리지 확인
uv run pytest --cov=cluefin_openapi --cov-report=html
```

### Kiwoom 실계좌 전용(`real_account_only`) 테스트 실행

모의투자에서 제공되지 않는 API 테스트는 `real_account_only` 데코레이터로 skip 처리되어 있습니다.
`KIWOOM_ENV=prod`(+ 실계좌 키)를 셸 환경변수로 주면 코드 수정 없이 skip이 자동으로 풀리고 실제 검증이 실행됩니다.

> ⚠️ `KIWOOM_ENV=prod`로 전체 통합 테스트를 돌리면 안 됩니다. 주문 테스트(`test_*_order_integration.py`)는
> 실제 주문이 접수되고, `test_request_exchange`(ust31302)는 실제 환전이 실행됩니다. 조회성 계좌 테스트만 골라서 실행하세요.

```bash
# 국내 계좌의 real_account_only 대상만
KIWOOM_ENV=prod KIWOOM_APP_KEY=<실계좌키> KIWOOM_SECRET_KEY=<실계좌시크릿> \
  uv run pytest packages/cluefin-openapi/tests/kiwoom/test_domestic_account_integration.py \
  -m integration -k "estimated_deposit or execution_balance or withdrawal_amount or margin_loan_stock or consignment or profit_rate_details or current_day_status" -v

# 해외 계좌 조회 계열
KIWOOM_ENV=prod KIWOOM_APP_KEY=<실계좌키> KIWOOM_SECRET_KEY=<실계좌시크릿> \
  uv run pytest packages/cluefin-openapi/tests/kiwoom/test_overseas_account_integration.py -m integration -v
```

### KIS 통합 테스트 디버깅

- 기본적으로 KIS integration 테스트 실패 시 raw 응답을 출력하지 않습니다.
- 필요할 때만 `KIS_DEBUG_ON_FAILURE=1` 를 주면 실패한 테스트의 마지막 KIS 응답이 같이 출력됩니다.
- 출력에는 `status_code`, `tr_id`, `path`, 요청 파라미터 요약, `response_preview`, `artifact_path` 가 포함됩니다.
- 전체 payload는 `artifact_path` 로 표시된 `/tmp/cluefin-kis-debug/*.json` 파일에서 확인할 수 있습니다.

```bash
# KIS integration 실패 시 마지막 raw 응답 보기
KIS_DEBUG_ON_FAILURE=1 uv run pytest packages/cluefin-openapi/tests/kis/test_domestic_market_analysis_integration.py -m "integration"
```

### 통합 테스트 실행 이슈 (uv 캐시 권한)

- 증상: `uv run pytest ...` 실행 시 `.../.cache/uv/... Operation not permitted`
- 원인: 실행 환경(샌드박스/권한 정책)에서 기본 uv 캐시 경로 접근이 제한됨
- 해결:
  1. 워크스페이스 내부 캐시 디렉터리 생성: `mkdir -p .uv-cache`
  2. 실행 시 캐시 경로 지정: `UV_CACHE_DIR=.uv-cache uv run pytest <file_or_args>`
  3. 필요하면 동일 세션에서 `export UV_CACHE_DIR=.uv-cache` 후 반복 실행

## 🏗️ 프로젝트 구조

```
packages/cluefin-openapi/
├── src/cluefin_openapi/
│   ├── dart/                      # 금융감독원 DART 공시 클라이언트
│   ├── ecos/                      # 한국은행 ECOS 경제통계 클라이언트
│   ├── kiwoom/                    # 키움증권 API 클라이언트
│   ├── kis/                       # 한국투자증권 API 클라이언트
│   ├── nhplug/                    # NH투자증권 PLUG API 클라이언트
│   │   ├── _krstock_*.py         # 국내주식 주문/조회/시세
│   │   └── _overseas_stock_*.py  # 해외주식 주문/조회/시세
│   ├── sec/                       # SEC EDGAR 클라이언트 (미국 공시)
│   └── __init__.py
├── tests/                        # 테스트 스위트
│   ├── kiwoom/                   # 키움증권 API 테스트
│   │   ├── test_*_unit.py        # 단위 테스트 (requests_mock 사용)
│   │   └── test_*_integration.py # 통합 테스트 (@pytest.mark.integration)
│   ├── kis/                       # 한국투자증권 API 테스트
│   │   ├── test_*_unit.py        # 단위 테스트 (Mock 사용, JSON 테스트 케이스)
│   │   └── test_*_integration.py # 통합 테스트 (@pytest.mark.integration)
│   ├── nhplug/                    # NH투자증권 PLUG API 테스트
│   │   ├── test_*_unit.py        # 단위 테스트 (requests_mock 사용)
│   │   └── test_*_integration.py # 통합 테스트 (@pytest.mark.integration)
│   ├── dart/                      # Dart API 테스트
│   │   ├── test_*_unit.py        # 단위 테스트
│   │   └── test_*_integration.py # 통합 테스트
│   ├── ecos/                      # ECOS 테스트 (통합 테스트는 sample 키로 늘, 실키는 .env.test 의 ECOS_AUTH_KEY 가 있을 때)
│   └── sec/                       # SEC EDGAR 테스트 (통합 테스트는 .env.test 의 SEC_USER_AGENT 사용)
├── pyproject.toml               # 패키지 의존성 및 설정
└── README.md                    # 이 문서
```

### 핵심 설계 패턴

**응답 래퍼 패턴**: 모든 API 응답을 구조화된 형태로 반환
```python
@dataclass
class KiwoomHttpResponse(Generic[T]):
    headers: KiwoomHttpHeader  # 헤더 정보 (연속조회키 등)
    body: T                    # 응답 데이터 (Pydantic 모델)
```

**한국 금융 API 특화 기능**:
- 한국 시장 시간대(KST) 처리
- 한국 주식 코드 형식 (6자리, 예: "005930")
- 한국어 필드명에 대한 영어 별칭: `cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")`

## 🛠️ 개발 가이드

프로젝트는 다음 도구들을 사용합니다:

- **Uv**: Rust로 만들어진 Python 패키지 메니저
- **Ruff**: 코드 포맷팅 및 린팅
- **pytest**: 테스트 프레임워크
- **Pydantic**: 데이터 검증 및 타입 안전성
- **requests**: HTTP 클라이언트
- **loguru**: 구조화된 로깅

```bash
# 워크스페이스 루트에서 실행

# 코드 포맷팅 (전체 프로젝트)
uv run ruff format .

# 린팅 확인 및 자동 수정
uv run ruff check . --fix

# cluefin-openapi만 포맷팅
uv run ruff format packages/cluefin-openapi/

# cluefin-openapi만 린팅
uv run ruff check packages/cluefin-openapi/
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

## 🔗 관련 링크

- [키움증권 OpenAPI 포털](https://openapi.kiwoom.com/)
- [한국투자증권 OpenAPI 포털](https://apiportal.koreainvestment.com/)
- [NH투자증권 PLUG 포털](https://www.nhplug.com/) ([N2 PLUG](https://www.n2plug.com/))
- [금융감독원 OpenAPI 포털](https://opendart.fss.or.kr/)
- [한국은행 ECOS Open API](https://ecos.bok.or.kr/api/) · [개발 명세서](https://ecos.bok.or.kr/api/#/DevGuide/DevSpeciflcation)
- [SEC EDGAR API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) · [접근 정책(User-Agent·요청 한도)](https://www.sec.gov/os/accessing-edgar-data)

---

> ⚠️ **투자 주의사항**: 이 프로젝트는 키움증권, 한국투자증권, NH투자증권과 공식적으로 연관되지 않습니다.
> 투자는 신중하게 하시고, 모든 투자 손실에 대한 책임은 투자자 본인에게 있습니다.
