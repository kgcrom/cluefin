# 한국투자증권 WebSocket API 메시지 구조 및 데이터 흐름

## 1. 전체 데이터 플로우 (Sequence Diagram)

```mermaid
sequenceDiagram
    participant Client as 클라이언트
    participant REST as KIS REST API
    participant WS as KIS WebSocket

    %% 인증 단계
    Note over Client,REST: 1️⃣ 인증 단계
    Client->>REST: POST /oauth2/Approval
    Note right of Client: grant_type, appkey, appsecret
    REST-->>Client: approval_key, encryption (iv, key)

    %% WebSocket 연결
    Note over Client,WS: 2️⃣ WebSocket 연결
    Client->>WS: WebSocket Connect
    Note right of Client: ws://ops.koreainvestment.com:21000
    WS-->>Client: Connection Established

    %% 구독 요청
    Note over Client,WS: 3️⃣ 실시간 데이터 구독
    Client->>WS: Subscribe Request (JSON)
    Note right of Client: {"header": {approval_key, tr_type: "1"},<br/>"body": {"tr_id": "H0UNCNT0", "tr_key": "005930"}}
    WS-->>Client: Subscribe Success (JSON)
    Note left of WS: {"rt_cd": "0", "msg1": "SUBSCRIBE SUCCESS",<br/>"output": {"iv": "...", "key": "..."}}

    %% 실시간 데이터 수신
    Note over Client,WS: 4️⃣ 실시간 데이터 수신
    loop 장중 실시간 데이터
        WS->>Client: Data Message (Pipe-delimited)
        Note left of WS: 0|H0UNCNT0|012|005930^103422^123700^2^...
        Client->>Client: Parse & Decrypt (if encrypted)
        Client->>Client: Split by "^" → DataFrame
    end

    %% PINGPONG
    Note over Client,WS: 5️⃣ 연결 유지
    WS->>Client: PINGPONG
    Client->>WS: PONG (echo back)

    %% 구독 해제
    Note over Client,WS: 6️⃣ 구독 해제
    Client->>WS: Unsubscribe Request
    Note right of Client: {"header": {approval_key, tr_type: "0"},<br/>"body": {"tr_id": "H0UNCNT0", "tr_key": "005930"}}
    WS-->>Client: Unsubscribe Success
```

## 2. WebSocket 메시지 구조

### 2.1 메시지 타입별 포맷

```mermaid
graph TD
    A[WebSocket 수신 메시지] --> B{첫 글자 체크}

    B -->|'0' or '1'| C[데이터 메시지]
    B -->|JSON 형태| D[시스템 응답]
    B -->|'PINGPONG'| E[PINGPONG 메시지]

    C --> C1["파싱: split('|')"]
    C1 --> C2[Index 0: encrypted<br/>0=plain, 1=AES]
    C1 --> C3[Index 1: tr_id<br/>ex: H0UNCNT0]
    C1 --> C4[Index 2: count<br/>ex: 012 = 12개 레코드]
    C1 --> C5[Index 3: data<br/>^로 구분된 CSV]

    C5 --> C6{암호화 여부}
    C6 -->|encrypted=1| C7[AES-CBC Base64 복호화]
    C6 -->|encrypted=0| C8[Plain Text]
    C7 --> C9["CSV 파싱: split('^')"]
    C8 --> C9
    C9 --> C10[DataFrame 생성]

    D --> D1[JSON 파싱]
    D1 --> D2[tr_id, encrypt, iv, key 추출]
    D2 --> D3[data_map에 암호화 정보 저장]

    E --> E1[echo back으로 PONG 응답]
```

### 2.2 데이터 메시지 상세 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WebSocket Data Message Format                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  encrypted | tr_id    | count | data                                │
│  ─────────┬──────────┬───────┬─────────────────────────────────     │
│     0     │ H0UNCNT0 │  012  │ 005930^103422^123700^2^3800^...      │
│     ▲     │    ▲     │   ▲   │           ▲                          │
│     │     │    │     │   │   │           │                          │
│     │     │    │     │   │   │           └─ CSV data (^ delimited)  │
│     │     │    │     │   │   │                                      │
│     │     │    │     │   └───┴─ 12 records batched                  │
│     │     │    │     │                                              │
│     │     │    └─────────────── Transaction ID                      │
│     │     │                                                         │
│     └─────┴─────────────────── 0: Plain, 1: AES Encrypted           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 3. H0UNCNT0 (실시간 체결가) 상세

### 3.1 구독 요청 메시지

```json
{
  "header": {
    "approval_key": "08b3c13e-1a7e-4f1c-b20d-417582e3b3a0",
    "custtype": "P",
    "tr_type": "1",
    "content-type": "utf-8"
  },
  "body": {
    "input": {
      "tr_id": "H0UNCNT0",
      "tr_key": "005930"
    }
  }
}
```

### 3.2 데이터 메시지 필드 (46개)

```mermaid
graph LR
    A[H0UNCNT0 Data] --> B[기본 정보<br/>5 fields]
    A --> C[가격 정보<br/>8 fields]
    A --> D[거래량 정보<br/>10 fields]
    A --> E[시고저 정보<br/>9 fields]
    A --> F[기타 정보<br/>14 fields]

    B --> B1[종목코드<br/>체결시간<br/>현재가<br/>전일대비부호<br/>전일대비]

    C --> C1[전일대비율<br/>가중평균가<br/>시가/고가/저가<br/>매도호가1<br/>매수호가1]

    D --> D1[체결거래량<br/>누적거래량<br/>누적거래대금<br/>매도/매수 체결건수<br/>체결강도 등]

    E --> E1[시가시간/대비<br/>고가시간/대비<br/>저가시간/대비]

    F --> F1[영업일자<br/>장운영구분<br/>거래정지여부<br/>호가잔량<br/>거래량회전율 등]
```

### 3.3 실제 데이터 예시

```
Raw Message:
0|H0UNCNT0|012|005930^103422^123700^2^3800^3.17^122292.62^120200^...

Parsed (첫 번째 레코드):
┌──────────────────────┬────────────┐
│ Field                │ Value      │
├──────────────────────┼────────────┤
│ MKSC_SHRN_ISCD       │ 005930     │  ← 삼성전자
│ STCK_CNTG_HOUR       │ 103422     │  ← 10:34:22
│ STCK_PRPR            │ 123700     │  ← 현재가
│ PRDY_VRSS_SIGN       │ 2          │  ← 상승
│ PRDY_VRSS            │ 3800       │  ← +3,800원
│ PRDY_CTRT            │ 3.17       │  ← +3.17%
│ ...                  │ ...        │
└──────────────────────┴────────────┘

Note: count=012 → 12개 레코드가 concatenated
      → 12 × 46 = 552 fields total
```

## 4. H0STASP0 (실시간 호가) 상세

### 4.1 구독 요청 메시지

```json
{
  "header": {
    "approval_key": "6124d873-6248-4bca-952e-76eb0c352a51",
    "custtype": "P",
    "tr_type": "1",
    "content-type": "utf-8"
  },
  "body": {
    "input": {
      "tr_id": "H0STASP0",
      "tr_key": "005930"
    }
  }
}
```

### 4.2 데이터 메시지 필드 (59개, 실제 62개 반환)

```mermaid
graph LR
    A[H0STASP0 Data] --> B[기본 정보<br/>3 fields]
    A --> C[매도호가<br/>10 fields]
    A --> D[매수호가<br/>10 fields]
    A --> E[매도잔량<br/>10 fields]
    A --> F[매수잔량<br/>10 fields]
    A --> G[호가 통계<br/>13 fields]
    A --> H[추가 필드<br/>3 fields]

    B --> B1[종목코드<br/>영업시간<br/>시간구분코드]

    C --> C1[ASKP1~10<br/>매도호가 1~10단계]

    D --> D1[BIDP1~10<br/>매수호가 1~10단계]

    E --> E1[ASKP_RSQN1~10<br/>매도호가잔량 1~10]

    F --> F1[BIDP_RSQN1~10<br/>매수호가잔량 1~10]

    G --> G1[총매도/매수잔량<br/>예상체결가/량<br/>누적거래량 등]

    H --> H1[미문서화<br/>API 스키마 변경<br/>3개 추가 필드]

    style H fill:#ff9999
    style H1 fill:#ff9999
```

### 4.3 실제 데이터 예시

```
Raw Message:
0|H0STASP0|001|005930^104025^0^123900^124000^124100^124200^...

Parsed:
┌──────────────────────┬────────────┐
│ Field                │ Value      │
├──────────────────────┼────────────┤
│ MKSC_SHRN_ISCD       │ 005930     │  ← 삼성전자
│ BSOP_HOUR            │ 104025     │  ← 10:40:25
│ HOUR_CLS_CODE        │ 0          │  ← 장중
│ ASKP1                │ 123900     │  ← 매도1호가
│ ASKP2                │ 124000     │  ← 매도2호가
│ ...                  │ ...        │
│ BIDP1                │ 123800     │  ← 매수1호가
│ BIDP2                │ 123700     │  ← 매수2호가
│ ...                  │ ...        │
│ ASKP_RSQN1           │ 27292      │  ← 매도1잔량
│ ...                  │ ...        │
│ Unknown Field 60     │ ???        │  ⚠️ API 변경
│ Unknown Field 61     │ ???        │  ⚠️ 미문서화
│ Unknown Field 62     │ ???        │  ⚠️ 추가 필드
└──────────────────────┴────────────┘

Note: 문서상 59개이나 실제 62개 반환
      → 처음 59개만 사용, 나머지 3개는 무시
```

## 5. 데이터 파싱 플로우

```mermaid
flowchart TD
    Start([WebSocket 메시지 수신]) --> CheckType{메시지 타입}

    CheckType -->|"raw[0] in ['0','1']"| DataMsg[데이터 메시지]
    CheckType -->|JSON| SysMsg[시스템 응답]
    CheckType -->|PINGPONG| Ping[PINGPONG]

    %% 데이터 메시지 처리
    DataMsg --> Split["split('|')"]
    Split --> Extract[d1d1#91;1#93;: encrypted<br/>d1d1#91;1#93;: tr_id<br/>d1d1#91;2#93;: count<br/>d1#91;3#93;: data]

    Extract --> GetMap["data_map[tr_id]로<br/>암호화 정보 조회"]
    GetMap --> CheckEnc{암호화?}

    CheckEnc -->|encrypt='Y'| Decrypt["AES-CBC Base64 복호화<br/>aes_cbc_base64_dec(key, iv, data)"]
    CheckEnc -->|encrypt='N'| Plain[평문 데이터]

    Decrypt --> ParseCSV
    Plain --> ParseCSV["pd.read_csv(StringIO(d),<br/>sep='^',<br/>names=columns,<br/>dtype=object)"]

    ParseCSV --> CheckBatch{count > 1?}
    CheckBatch -->|Yes| Batch["DataFrame with<br/>multiple rows"]
    CheckBatch -->|No| Single["DataFrame with<br/>single row"]

    Batch --> Callback
    Single --> Callback["on_result(ws, tr_id, df, data_map)"]
    Callback --> End([처리 완료])

    %% 시스템 응답 처리
    SysMsg --> ParseJSON[JSON 파싱]
    ParseJSON --> ExtractKeys["tr_id, encrypt,<br/>iv, key 추출"]
    ExtractKeys --> SaveMap["data_map에 저장"]
    SaveMap --> End

    %% PINGPONG 처리
    Ping --> Pong["await ws.pong(raw)"]
    Pong --> End

    style DataMsg fill:#b3d9ff
    style ParseCSV fill:#ffeb99
    style Callback fill:#c2f0c2
```

## 6. 배치 데이터 처리 로직

### 6.1 배치 처리 시나리오

```
장중 고빈도 거래 시:
┌─────────────────────────────────────────────────────┐
│ WebSocket이 여러 체결을 batch로 전송                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  count = 012 (12개 레코드)                            │
│                                                     │
│  Record 1: 005930^103422^123700^...  (46 fields)    │
│  Record 2: 005930^103423^123750^...  (46 fields)    │
│  Record 3: 005930^103424^123800^...  (46 fields)    │
│  ...                                                │
│  Record 12: 005930^103433^124200^... (46 fields)    │
│                                                     │
│  Total: 12 × 46 = 552 fields                        │
│                                                     │
└─────────────────────────────────────────────────────┘

pandas.read_csv()는 자동으로 '\n' 구분자 인식
→ DataFrame with 12 rows × 46 columns
```

### 6.2 현재 cluefin-openapi 구현

```mermaid
graph TD
    A[552 fields 수신] --> B{len%46==0?}
    B -->|Yes| C[Batched Data 감지]
    B -->|No| D[Invalid Field Count]

    C --> E["첫 46개 필드만 추출<br/>data[:46]"]
    E --> F[Single Record 파싱]
    F --> G[DomesticRealtimeExecutionItem]

    D --> H[ValueError 발생]

    style C fill:#ffeb99
    style E fill:#ffcccc
    style F fill:#c2f0c2
```

**⚠️ 현재 구현의 한계:**
- Batch된 데이터 중 첫 번째 레코드만 파싱
- 나머지 11개 레코드는 버려짐
- 고빈도 거래 시 데이터 손실 가능

**✅ 개선 방안:**
```python
# Option 1: 모든 레코드 반환
@staticmethod
def parse_execution_data_all(data: List[str]) -> List[DomesticRealtimeExecutionItem]:
    """Parse all batched records."""
    field_count = len(EXECUTION_FIELD_NAMES)
    record_count = len(data) // field_count

    results = []
    for i in range(record_count):
        start = i * field_count
        end = start + field_count
        record = data[start:end]

        field_dict = dict(zip(EXECUTION_FIELD_NAMES, record))
        results.append(DomesticRealtimeExecutionItem.model_validate(field_dict))

    return results
```

## 7. 에러 처리 및 예외 상황

```mermaid
graph TD
    A[메시지 수신] --> B{Valid Format?}
    B -->|No| E1[ValueError:<br/>data not found]
    B -->|Yes| C{tr_id in data_map?}

    C -->|No| E2[KeyError:<br/>Unknown tr_id]
    C -->|Yes| D{Field Count OK?}

    D -->|No| E3[ValueError:<br/>Field count mismatch]
    D -->|Yes| F{Decryption OK?}

    F -->|No| E4[DecryptionError:<br/>Invalid key/iv]
    F -->|Yes| G{CSV Parse OK?}

    G -->|No| E5[ParserError:<br/>Invalid CSV]
    G -->|Yes| H[Success]

    style E1 fill:#ff9999
    style E2 fill:#ff9999
    style E3 fill:#ff9999
    style E4 fill:#ff9999
    style E5 fill:#ff9999
    style H fill:#99ff99
```

## 8. 실전 사용 예시

### 8.1 기본 구독 패턴

```python
from cluefin_openapi.kis import Auth, SocketClient, DomesticRealtimeQuote
import asyncio

async def main():
    # 1. 인증
    auth = Auth(app_key="...", secret_key="...", env="dev")
    approval = auth.approve()

    # 2. WebSocket 연결
    async with SocketClient(
        approval_key=approval.approval_key,
        app_key="...",
        secret_key="...",
        env="dev"
    ) as client:
        realtime = DomesticRealtimeQuote(client)

        # 3. 구독
        await realtime.subscribe_execution("005930")  # 삼성전자
        await realtime.subscribe_orderbook("005930")

        # 4. 실시간 데이터 수신
        async for event in client.events():
            if event.event_type == "data":
                if event.tr_id == "H0UNCNT0":
                    # 체결가 데이터
                    execution = realtime.parse_execution_data(event.data["values"])
                    print(f"체결: {execution.stck_prpr}원")

                elif event.tr_id == "H0STASP0":
                    # 호가 데이터
                    orderbook = realtime.parse_orderbook_data(event.data["values"])
                    print(f"매도1: {orderbook.askp1}, 매수1: {orderbook.bidp1}")

asyncio.run(main())
```

### 8.2 장중 시간대별 데이터 특성

```
09:00 - 09:05  장 시작 │ 초당 10~50개 체결 (고빈도 batching)
09:05 - 11:30  오전장  │ 초당 1~10개 체결 (중간 빈도)
11:30 - 12:30  점심    │ 데이터 없음 (timeout/skip)
12:30 - 15:20  오후장  │ 초당 1~10개 체결
15:20 - 15:30  장 마감 │ 초당 10~100개 체결 (최고빈도 batching)
15:30 - 09:00  장외    │ 데이터 없음 (subscription은 유지)
```



## 10. 참고 자료

- **공식 문서:** https://apiportal.koreainvestment.com/
- **예제 코드:** https://github.com/koreainvestment/open-trading-api
- **cluefin-openapi:** `packages/cluefin-openapi/src/cluefin_openapi/kis/`
  - `_socket_client.py`: WebSocket 클라이언트 구현
  - `_domestic_realtime_quote.py`: H0UNCNT0/H0STASP0 파서
  - `_domestic_realtime_quote_types.py`: Pydantic 모델 정의
