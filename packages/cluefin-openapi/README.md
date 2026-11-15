# cluefin-openapi

> 키움증권·한국투자증권(KIS)·NH투자증권 PLUG·DART·SEC EDGAR·한국은행 ECOS OpenAPI 를 한 패키지로 묶은 Python 클라이언트

![Python](https://img.shields.io/badge/Python-3.11%2B-green)
![Pydantic](https://img.shields.io/badge/Pydantic-Type%20Safe-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

```bash
pip install cluefin-openapi
```

- Python 3.11 이상, **macOS·Linux 전용**입니다(토큰 캐시가 `fcntl` 파일 잠금을 씁니다).
- 응답은 Pydantic 모델입니다. 메서드와 필드는 타입 힌트와 docstring 에 있고, 이 문서는 **공식 문서만 봐서는 알 수 없는 것**
  (실서버가 문서와 다르게 동작하는 곳, 모의투자에서 안 되는 것)을 적습니다. 항목별 실측 기록은 저장소의
  [VENDOR_DOC_ERRATA.md](https://github.com/kgcrom/cluefin/blob/main/packages/cluefin-openapi/VENDOR_DOC_ERRATA.md) 에 있습니다.
- 키움증권·한국투자증권·NH투자증권과 무관한 비공식 프로젝트입니다.

## 키 신청과 환경 변수

| 대상 | 신청 | 환경 변수 |
|---|---|---|
| 키움증권 | [openapi.kiwoom.com](https://openapi.kiwoom.com/) 에서 API 사용 신청 | `KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`, `KIWOOM_ENV` |
| 한국투자증권 | [apiportal.koreainvestment.com](https://apiportal.koreainvestment.com/) | `KIS_APP_KEY`, `KIS_SECRET_KEY`, `KIS_ENV` |
| NH투자증권 PLUG | [nhplug.com](https://www.nhplug.com/) (나무증권은 [n2plug.com](https://www.n2plug.com/)) | `NHPLUG_APP_KEY`, `NHPLUG_SECRET_KEY`, `NHPLUG_ENV` |
| 금융감독원 DART | [opendart.fss.or.kr](https://opendart.fss.or.kr/) | `DART_AUTH_KEY` |
| SEC EDGAR | 키 없음. User-Agent 에 이름과 이메일을 밝힌다 ([접근 정책](https://www.sec.gov/os/accessing-edgar-data)) | `SEC_USER_AGENT` |
| 한국은행 ECOS | [ecos.bok.or.kr/api](https://ecos.bok.or.kr/api/) (없으면 공개 시험 키 `sample`) | `ECOS_AUTH_KEY` |

`*_ENV` 는 `dev`(모의투자, 기본값) 또는 `prod`(실계좌)입니다. `NHPLUG_ENV` 는 조회·주문 도메인만 고르고 토큰 발급은 늘 운영
도메인입니다. `SEC_USER_AGENT` 는 `"Your Name your.email@example.com"` 형식이고, 선택 값으로 `CLUEFIN_OPENAPI_CACHE_DIR`
(토큰 캐시 폴더, 기본은 시스템 임시 폴더)과 `CLUEFIN_OPENAPI_DEBUG=1`(요청·응답 DEBUG 로그)이 있습니다.

`Auth`·`Client` 같은 클래스는 환경 변수를 읽지 않습니다. 값을 직접 넘기거나, 위 이름을 읽는 팩토리를 씁니다.
팩토리는 **실행 위치의 `.env`** 위에 실제 환경 변수를 덮어 읽고(`python-dotenv` 불필요) 토큰 발급·캐시까지 처리합니다.

```python
from cluefin_openapi import BrokerClientFactory

factory = BrokerClientFactory()           # 현재 폴더의 .env + os.environ
kiwoom = factory.create("kiwoom")         # "kis" | "kiwoom" | "nhplug" | "dart" | "sec" | "ecos"
```

`KIS_HTS_USER_ID` 는 라이브러리가 읽는 값이 아니라 KIS 관심종목 API 에 넘기는 HTS ID 입니다.

### 먼저 알아 둘 것

- **`env` 기본값이 클래스마다 다릅니다.** KIS·키움 `Auth` 는 `dev`, KIS·NH PLUG 의 `HttpClient` 와 세 브로커의 WebSocket 클라이언트는
  `prod` 입니다(키움 WebSocket 은 `market="overseas"` 도 기본). `env` 를 한쪽에만 주면 모의 토큰으로 실서버를 부릅니다.
  모의·실전 토큰을 섞으면 서버가 거절합니다(키움 `8031`, KIS `EGW00123` "기간이 만료된 token").
- **토큰은 파일에 캐시됩니다** — `<임시 폴더>/cluefin-openapi/` 아래, 환경·앱키별 파일. 발급 횟수 제한(KIS 1분 1회, NH 1초 1회)
  때문에 프로세스마다 새로 발급하면 안 됩니다. 폴더는 `Auth(..., cache_dir=...)` 로 바꿉니다.
- **HTTP 200 이 성공이 아닙니다.** 세 증권사 모두 실패를 200 본문 코드(`rt_cd`·`return_code`·`rsp_cd`)로 주고, DART·ECOS 도
  그렇습니다. 클라이언트가 본문 코드를 먼저 보고 `KISAPIError`·`KiwoomAPIError`·`NHPlugAPIError`·`DartAPIError`·
  `EcosAPIError` 의 하위 예외를 던집니다. 429·5xx·타임아웃은 `max_retries` 만큼 다시 보냅니다.
- 응답 래퍼의 헤더 속성은 키움이 `response.headers`, KIS·NH PLUG 는 `response.header` 입니다.

## 키움증권

```python
import os

from pydantic import SecretStr

from cluefin_openapi.kiwoom import Auth, Client

auth = Auth(app_key=os.environ["KIWOOM_APP_KEY"], secret_key=SecretStr(os.environ["KIWOOM_SECRET_KEY"]), env="dev")
client = Client(token=auth.generate_token().get_token(), env="dev")

info = client.stock_info.get_stock_info("005930")     # ka10001 주식기본정보
print(info.body.stk_nm, info.body.cur_prc)            # 숫자도 원문 문자열 그대로
print(info.headers.cont_yn, info.headers.next_key)    # 연속조회는 cont_yn="Y", next_key=... 로 다시 호출
```

- 미국주식은 `client.overseas_*` 입니다.
- **잘못된 입력에 오류 대신 빈 결과가 옵니다.** 문서의 `KRX:039490` 은 형식 예시이지 접두어가 아닙니다 —
  `KRX:069500` 을 보내면 빈 목록입니다. 기간 필드에 날짜를 넣어도 같습니다.
- 가격에는 등락 부호가 붙고(`-270406`), 음수는 `--123` 처럼 부호가 겹쳐 오기도 합니다. `float()` 전에 정리하세요.
- 모의투자: 키가 만료되면 **토큰 발급부터** 실패합니다(200 본문 `return_code: 3`, `8005` → `TokenResponse` 검증 오류).
  국내·미국 모의투자는 따로 신청하고 따로 만료됩니다(`RC4091`). `RC9000`·`8104` 는 모의가 제공하지 않는 TR 입니다.
- 오류 코드 표는 `cluefin_openapi.kiwoom.KIWOOM_ERROR_CODES` 에 있습니다.

실시간 시세와 조건검색은 `asyncio` 기반 `KiwoomWebSocketClient(token=..., env=..., market="domestic" | "overseas")` 에
`DomesticRealtime`·`OverseasRealtime`(`register`/`remove`), `DomesticConditionSearch`·`OverseasConditionSearch` 를 얹어 씁니다.
한 프레임에 여러 type 이 섞여 오므로 `DomesticRealtime.parse(message)` 는 모델 **리스트**를 줍니다. 모의 국내 소켓은 KRX 만 됩니다.

## 한국투자증권 (KIS)

```python
import os

from pydantic import SecretStr

from cluefin_openapi.kis import Auth, HttpClient

app_key, secret_key = os.environ["KIS_APP_KEY"], SecretStr(os.environ["KIS_SECRET_KEY"])
auth = Auth(app_key=app_key, secret_key=secret_key, env="dev")
client = HttpClient(token=auth.generate().get_token(), app_key=app_key, secret_key=secret_key, env="dev")

price = client.domestic_basic_quote.get_stock_current_price(fid_cond_mrkt_div_code="J", fid_input_iscd="005930")
print(price.body.output.stck_prpr)
```

- 토큰은 표시된 24시간보다 일찍 무효가 되기도 해, 캐시가 6시간을 넘으면 다시 발급합니다. 발급 제한에 걸리면
  `KISRateLimitError`(`EGW00133`), 키가 틀리면 `KISAuthenticationError`(`EGW00103`·`EGW00105`)입니다.
- 본문 `rt_cd` 실패는 `KISResponseError`, 응답이 모델과 안 맞으면 `KISValidationError` 이고 원문은 `e.response_data` 에 있습니다.
- **`HttpClient` 는 받은 응답 원문을 매번 `<임시 폴더>/cluefin-kis-debug/` 에 JSON 파일로 남깁니다**(계좌 조회 응답 포함,
  자동 삭제 없음). 공용 장비에서는 그 폴더를 관리하세요.
- 국내주식 기간별시세는 요청 구간과 무관하게 최신 100봉에서 잘립니다.
- 국내주식 종목분석 7종(재무비율 등)은 KIS 가 2026-11-11 에 호출을 막아 1.1.0 에서 뺐습니다. 재무 수치는 DART 로 받습니다.
- WebSocket(`SocketClient`)은 접근토큰이 아니라 `Auth.approve()` 의 `approval_key` 를 씁니다. **앱키 하나에 세션 하나**만
  열 수 있고, `approve()` 를 다시 부르면 앞서 받은 키는 무효가 됩니다(`OPSP8996`·`OPSP0011`).

## NH투자증권 PLUG

모든 호출은 `POST` + JSON 이고 요청은 `Input_0`, 응답은 `rsp_cd`/`rsp_msg` + `Output_N` 봉투입니다. 연속조회는 `cts` 인자입니다.

```python
import os

from pydantic import SecretStr

from cluefin_openapi.nhplug import Auth, HttpClient

app_key, secret_key = os.environ["NHPLUG_APP_KEY"], SecretStr(os.environ["NHPLUG_SECRET_KEY"])
token = Auth(app_key=app_key, secret_key=secret_key).generate().access_token   # 운영·모의 공용 토큰

# 계좌·조회·주문은 모의투자(dev)로 — 계좌번호는 이후 모든 API 의 act_no
mock = HttpClient(token=token, app_key=app_key, secret_key=secret_key, env="dev")
for account in mock.common.get_account_list().body.output_0 or []:
    print(account.acct_no, account.acct_type)     # 운영은 01·02, 모의투자는 03 계좌만 유효

# 시세는 운영(prod) 전용 — 읽기만 하므로 계좌에 영향이 없다
live = HttpClient(token=token, app_key=app_key, secret_key=secret_key, env="prod")
current = live.krstock_quote.current_price(market_cd="KRX", iem_cd="005930")
print(current.body.output_0.stck_prpr)
```

- **토큰 발급(`/oauth2/token`)은 운영 도메인에만 있고**, 토큰 하나로 운영·모의를 모두 부릅니다. 불필요한 재발급은 계좌에
  보안 알림을 쌓으니 `Auth.generate()`(파일 캐시)만 쓰세요.
- **시세 API 전부(`/krstock/quote/*`, `/gbstock/quote/*`)와 WebSocket 시세 채널은 모의투자에서 거부됩니다** — 문서 머리말은
  "모의·운영 모두 제공"이라고 적습니다. REST 는 `IGW40023` 또는 `IGW40019`("종목코드(iem_cd)를 확인해주세요" — 원인과 무관한
  문구), 소켓은 `WSS10006` 입니다.
- 해외 현재가의 종목명은 `iem_nm` 입니다(스펙의 `kor_name` 은 오지 않습니다). 국내 시세의 등락부호는 `"1E"` 같은 2자리로도 옵니다.
- 스펙이 숫자인 요청 필드를 문자열로 보내면 `IGW40011`(HTTP 400)입니다. `env="prod"` 의 주문 메서드는 실제 주문입니다.

### 본문 코드 (`rsp_cd`)

문서의 성공 코드는 `00000` 뿐이지만 실서버는 API 마다 다른 성공 코드를 주고, **빈 결과를 실패 코드로** 줍니다.
어떤 예외든 `e.rsp_cd` 로 코드를 볼 수 있습니다.

| `rsp_cd` | 뜻 | 클라이언트 |
|---|---|---|
| `00000` · `XA102`(모의 조회) · `00166`(운영 계좌 조회) · `00221`(운영 매수가능수량) | 성공 | 정상 반환 |
| `13578` · `11512` · `16935` | 조회 결과 0건 (잔고·내역 없는 계좌) | `NHPlugNoDataError` |
| `19999` | 모의투자 미제공 업무 | `NHPlugMockUnsupportedError` |
| `14100` | 영업일이 아님 | `NHPlugNotBusinessDayError` |
| `IGW40018` · `IGW40019` (HTTP 400) | 입력값 오류. `IGW40019` 는 "모의 미지원"일 때도 있다 | `NHPlugValidationError` |
| `IGW42903` (HTTP 429) | 호출 건수 초과. 모의는 1.5초 간격이면 통과 | 재시도 뒤 `NHPlugRateLimitError` |
| 그 외 | 분류되지 않은 실패 | `NHPlugAPIError` |

### 실시간 (WebSocket)

`SocketClient` 는 `tr_cd`/`tr_key` 로 구독합니다. `tr_cd` 는 REST 경로가 아니라 **웹소켓 전용 채널 코드**이고, 정본은 각 자산군
`openapi.json` 의 `x-realtime-channels[].tr_cd` 입니다(회원사·프로그램매매·시간외 등 전체 목록도 거기 있습니다).

| 자산군 | tr_cd | 채널 | tr_key |
|---|---|---|---|
| 국내 | `mc` / `mb` / `ma` | 체결가 · 호가 · 예상체결 (통합시세) | 종목코드 |
| 국내 | `oc` / `ob` / `oa` | 체결가 · 호가 · 예상체결 (KRX) | 종목코드 |
| 국내 | `nc` / `nb` / `na` | 체결가 · 호가 · 예상체결 (NXT) | 종목코드 |
| 국내 | `d2` / `d3` | 체결통보 · 주문내역통보 | 사용자ID |
| 해외 | `RC` / `RH` | 실시간 체결가 · 호가 (유료시세 약정 필요) | 종목코드 |
| 해외 | `rc` / `rh` | 지연 체결가 · 호가 (미국·중국만) | 종목코드 |
| 해외 | `d0` / `d1` | 체결통보 · 주문내역통보 | 사용자ID |

- **해외 채널은 대소문자로 실시간/지연이 갈립니다**(`RC` = 실시간 유료, `rc` = 무료 지연).
- `market="kr"` 은 운영 `:7070`, `market="gb"` 는 `:7080` 입니다. **`:7080` 은 해외 시세만** 받으므로 해외 체결·주문
  통보(`d0`/`d1`)도 `market="kr"` 로 붙습니다. `env="dev"` 는 `market` 과 무관하게 모의 주소 하나이고 시세 채널을 거부합니다.
- 없는 종목을 구독해도 서버는 성공(`00000`)을 답합니다. 구독 응답이 아니라 데이터 수신으로 확인하세요.

```python
import asyncio

from cluefin_openapi.nhplug import SocketClient


async def main() -> None:
    async with SocketClient(token=token, env="prod", market="kr") as ws:   # 시세 채널은 운영 전용
        await ws.subscribe(tr_cd="oc", tr_key="005930")
        async for event in ws.events():
            if event.event_type == "data":
                print(event.tr_cd, event.tr_key, event.data)


asyncio.run(main())
```

세션이 남아 끊기지 않으면 `live.common.close_websocket_session()` 으로 정리합니다. 열린 세션이 없으면 이 호출은 예외입니다
(`rsp_cd="10000"`, 때로 HTTP 500 `IGW50025`).

## DART

```python
import os

from cluefin_openapi.dart import Client

client = Client(auth_key=os.environ["DART_AUTH_KEY"])

# corp_code 는 종목코드가 아니라 DART 고유번호(8자리). 전체 목록에서 종목코드로 찾는다
codes = client.public_disclosure.corp_code().result.list or []
corp_code = next(item.corp_code for item in codes if item.stock_code == "005930")

found = client.public_disclosure.public_disclosure_search(
    corp_code=corp_code, bgn_de="20260101", end_de="20260331", pblntf_ty="A"   # A: 정기공시
)
for item in found.result.list or []:
    print(item.rcept_dt, item.report_nm, item.rcept_no)
```

- 행은 늘 `result.list` 에 있습니다. **데이터 없음(`013`)은 예외가 아니라** `result.status == "013"`, `result.list is None` 입니다.
- 키가 틀리면 HTTP 200 본문 `status` 010·011·012·901 로 오고, ZIP 을 주는 API 는 ZIP 자리에 오류 XML 을 줍니다.
  클라이언트는 `DartAuthenticationError` 로 올립니다.
- 주요사항보고서는 `client.major_matters_report` 입니다. 예전 이름 `major_shareholder_disclosure` 와 옛 메서드 이름은
  `DeprecationWarning` 별칭으로만 남아 있습니다. 5% 대량보유는 `share_disclosure_comprehensive.large_holding_report` 입니다.
- 다중회사 주요계정(`get_multi_company_major_accounts`)은 한 번에 100개사까지입니다. 101개째부터는 호출 전체가 `021` 로 실패합니다.
- 주요계정·주요지표의 연결 순이익·자본은 지배·비지배 합계입니다. 지배주주 몫은 전체 재무제표에서 계정을 찾아 나눠야 합니다.
- 주요사항보고서의 금액·주식수는 콤마 문자열(`"12,345,678,900"`), 빈 값은 `"-"` 로 옵니다.
- `disclosure_document_file` 은 ZIP 의 첫 XML 만 꺼냅니다. 첨부 감사보고서까지 받으려면 `disclosure_document_files` 를 씁니다.

## SEC EDGAR

SEC 는 API 키가 없고 모든 요청의 User-Agent 에 이름과 이메일을 요구합니다. 클라이언트는 초당 8회(SEC 한도 10회)로 제한하고
429·5xx 는 재시도합니다. **403 은 User-Agent 가 없거나 한도를 넘겨 차단된 것**이라 재시도하지 않습니다 — 차단 페이지 제목이
"Request Rate Threshold Exceeded" 여도 User-Agent 부터 확인하세요.

```python
import os
from datetime import date

from cluefin_openapi.sec import Client, cusip_symbols, values_as_of

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
known = values_as_of(concept.units["USD"], date(2024, 1, 2))  # 기간(start, end)마다 FactValue 하나

# 공시 원문과 XBRL 파일
client.archives.download_filing_document(cik, latest.accession_number, latest.primary_document, destination="aapl")
client.archives.download_xbrl_files(cik, latest.accession_number, destination="aapl-xbrl")

# 공시 상세: 문서마다 종류(EX-99.1 등)와 제출 당사자 CIK. 폴더는 다른 회사 CIK 경로로도 열리니 ciks 로 확인한다
detail = client.archives.filing_detail(cik, latest.accession_number)
assert cik in detail.ciks

# 13F 기관 보유 보고: 표지와 정보표. 통지(13F-NT)는 information_table 이 None
thirteen_f = client.submissions.filings(1067983, forms=["13F-HR"])[0]
files = client.archives.download_13f_files(1067983, thirteen_f.accession_number, destination="brk-13f")

# CUSIP → 티커: 13F 정보표엔 티커가 없다. Fails-to-Deliver(반월마다, 2009-07~)에 CUSIP·티커가 함께 있다
recent = client.fails_to_deliver.files()[:12]  # 최신순. 6개월치
symbols = cusip_symbols(r for f in recent for r in client.fails_to_deliver.records(f))
symbols.get("037833100")  # "AAPL". 티커가 바뀐 CUSIP 은 결제일이 가장 늦은 티커
```

- companyfacts 의 `fy`/`fp` 는 값의 기간이 아니라 **그 값을 실은 공시**의 것입니다. 행은 `start`/`end`/`accn` 으로 고르세요.
- `acceptance_date_time` 은 `Z` 로 끝나지만 UTC 가 아닌 것이 섞여 있습니다. 시점 판단에는 `filed` 를 씁니다.
- Fails-to-Deliver 에는 결제 불이행이 한 번이라도 있었던 종목만 실립니다. 6개월치로 2026년 13F 12건의 금액 99.7–99.9% 가
  매핑됐고(행 기준 93–99%), 과거 보고를 매핑할 때는 그 시기 파일을 쓰는 편이 맞습니다(티커는 바뀝니다).

## 한국은행 ECOS

키가 없으면 공개 시험 키 `sample` 로 동작합니다(한 번에 10행, 클라이언트가 쪽 넘김으로 이어 받음). 받은 키를 주면 1000행씩 받습니다.

```python
import os

from cluefin_openapi.ecos import KTB_10Y, Client

client = Client(auth_key=os.getenv("ECOS_AUTH_KEY"))  # None 이면 sample

# 통계 조회: 휴일은 행이 없으니 "최근 값"은 2주쯤 받아 마지막 행을 쓴다
page = client.statistic_search.search_series(KTB_10Y, "20261005", "20261017")
latest = page.rows[-1]
print(latest.time, latest.data_value, latest.unit_name)  # 20261016 4.182 연%  (원문 문자열, latest.value 는 Decimal)

# 상수가 없는 계열: 통계표·주기·기간·항목코드. 항목 그룹이 둘인 표는 그룹 순서대로 두 코드를 넣는다
client.statistic_search.search("722Y001", "M", "201601", "202609", ["0101000"])       # 기준금리
client.statistic_search.search("901Y054", "M", "201601", "202609", ["MO3AB", "AB"])   # 가계대출 연체율

# 항목코드 찾기
tables = client.statistic_catalog.table_list()          # 통계표 목록 (분류 행 포함)
items = client.statistic_catalog.item_list("817Y002")   # 통계표의 항목·주기·수록 기간
```

- 상수: 국고채 1·3·5·10·20·30년(`KTB_1Y`~`KTB_30Y`), 통안증권·CD 91일, 회사채 3년 AA-·BBB-(`MARKET_RATES`), 원/달러 매매기준율
  `USD_KRW`, 소비자물가 총지수 `CPI_TOTAL`. 값은 원문 그대로(연 % 등) 두고 비율 변환은 쓰는 쪽에서 합니다.
- 오류도 HTTP 200 본문 `RESULT.CODE` 로 옵니다. 데이터 없음(`INFO-200`)은 빈 `rows`, 나머지는 `EcosAuthenticationError`·
  `EcosRequestError`(`EcosSampleLimitError`)·`EcosServerError`(`EcosQueryTimeoutError`)·`EcosRateLimitError` 입니다.
  예외의 `hint` 에 코드별 조치가 실리고, 일시 오류(`ERROR-600`·`602`)는 자동 재시도합니다.
- 주기는 그 항목이 가진 주기여야 합니다. 없는 주기는 오류가 아니라 빈 결과입니다.

### 자주 쓰는 계열 — 금리·신용·증시

2026-10-20 실조회 기준입니다. 호출은 모두 `client.statistic_search.search(통계표, 주기, 시작, 끝, [항목코드…])` 형식입니다.

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

- **장단기 금리차·신용 스프레드는 따로 있는 계열이 아닙니다.** 국고채 10년−3년처럼 두 계열을 받아 날짜를 맞춰 뺍니다.
- **단위가 표마다 다릅니다**(원·억원·십억원·백만원, 연%·%). 행의 `unit_name` 을 보고 환산하세요.
- **월·분기 통계는 늦게 나옵니다.** 2026-10-20 기준 대출금리·M2 는 2026-08, 연체율은 2026-07, 가계신용은 2026Q2 가
  마지막이었습니다. "최근 값"을 받을 때는 기간을 넉넉히 잡고 마지막 행을 씁니다.
- 주식 계열은 한국거래소 자료를 ECOS 가 다시 싣는 것입니다. 종목 시세는 증권사 API 가 낫습니다.

## 실시간(WebSocket) 검증 범위

실시간 통합 테스트는 장중에만 돌 수 있어 자동 검사(CI)에 들어 있지 않습니다. 시세 채널(체결·호가)은 KIS·키움·NH PLUG 모두
장중에 데이터 수신까지 확인했습니다(2026-10~11). **체결·주문 통보 채널과 키움 조건검색의 검색 요청·실시간 편입/이탈은 실서버
검증 없이 단위 테스트만** 있습니다. 이 부분을 쓸 때는 장중에 직접 확인해 주세요.

## 로깅

stdlib `logging` 으로 `cluefin_openapi.<브로커>.<모듈>` 로거에 남기고 핸들러는 붙이지 않습니다. 출력 위치와 레벨은 쓰는 쪽에서
정합니다. 요청·응답 단위의 DEBUG 로그는 클라이언트를 `debug=True` 로 만들어야 나옵니다.

```python
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("cluefin_openapi").setLevel(logging.INFO)  # 토큰 발급 등 INFO 까지
```

## 링크

- 저장소: [github.com/kgcrom/cluefin](https://github.com/kgcrom/cluefin) — 실측 기록(`VENDOR_DOC_ERRATA.md`), NH PLUG 예제 노트북(`examples/`)
- [키움 REST API](https://openapi.kiwoom.com/) · [KIS Developers](https://apiportal.koreainvestment.com/) · [NH PLUG](https://www.nhplug.com/) · [OpenDART](https://opendart.fss.or.kr/)
- [ECOS 개발 명세서](https://ecos.bok.or.kr/api/#/DevGuide/DevSpeciflcation) · [SEC EDGAR API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

## 라이선스

MIT — [LICENSE](https://github.com/kgcrom/cluefin/blob/main/LICENSE)

> ⚠️ **투자 주의사항**: 이 프로젝트는 키움증권, 한국투자증권, NH투자증권과 공식적으로 연관되지 않습니다.
> 투자는 신중하게 하시고, 모든 투자 손실에 대한 책임은 투자자 본인에게 있습니다.
