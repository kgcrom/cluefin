import type { ApiEnv } from '../core/types.js';
import { BaseWebSocketClient, type SubscriptionType, type WebSocketMessage } from '../core/websocket.js';

/**
 * WebSocket URLs (정본은 각 자산군 openapi.json 의 `x-environments`).
 *
 * 운영은 국내(7070)/해외(7080) 주소가 갈리고, 모의투자는 단일 주소(17070)다.
 */
const WS_URL_PROD_KR = 'wss://api.nhplug.com:7070';
const WS_URL_PROD_GB = 'wss://api.nhplug.com:7080';
const WS_URL_DEV = 'wss://moapi.nhplug.com:17070';

/** 접속 대상 시장. `kr` = 국내, `gb` = 해외(운영 전용 주소). */
export type NhplugMarket = 'kr' | 'gb';

export interface NhplugSocketClientOptions {
  /** REST 와 동일한 access token (`NhplugAuth.generate()`). */
  token: string;
  /** prod = 운영, dev = 모의투자(moapi). 기본값은 `NhplugClient` 와 같은 `dev`. */
  env?: ApiEnv;
  /** 운영에서만 의미가 있다. 모의투자는 국내/해외가 같은 주소를 쓴다. */
  market?: NhplugMarket;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
}

export const getNhplugSocketUrl = (env: ApiEnv, market: NhplugMarket): string => {
  if (env !== 'prod') {
    return WS_URL_DEV;
  }
  return market === 'gb' ? WS_URL_PROD_GB : WS_URL_PROD_KR;
};

/**
 * NH PLUG 실시간 시세 WebSocket 클라이언트.
 *
 * 인증은 REST 와 달리 구독 메시지 `header.token` 에 access token 만 실어 보낸다
 * (approval key 없음). 서버 푸시는 평문 JSON
 * `{"header": {"tr_cd", "tr_key"}, "body": {…}}` 이며 heartbeat 응답이 필요 없다.
 *
 * `subscribe`/`unsubscribe` 의 첫 인자는 REST 경로가 아니라 웹소켓 전용 채널 코드
 * (`tr_cd`) 다 — 국내 통합시세 체결가는 `mc`, 해외는 실시간 `RC` / 지연 `rc` 처럼
 * 대소문자로 갈린다. 정본은 각 자산군 openapi.json 의 `x-realtime-channels[].tr_cd`.
 */
export class NhplugSocketClient extends BaseWebSocketClient {
  public readonly env: ApiEnv;
  public readonly market: NhplugMarket;
  private readonly token: string;

  public constructor(options: NhplugSocketClientOptions) {
    const env = options.env ?? 'dev';
    const market = options.market ?? 'kr';
    super({
      url: getNhplugSocketUrl(env, market),
      rateLimitBurst: options.rateLimitBurst ?? 3,
      rateLimitRequestsPerSecond: options.rateLimitRequestsPerSecond ?? 5,
    });
    this.env = env;
    this.market = market;
    this.token = options.token;
  }

  protected override buildSubscriptionMessage(trCd: string, trKey: string, trType: SubscriptionType): string {
    return JSON.stringify({
      header: {
        token: this.token,
        tr_type: trType,
      },
      body: {
        tr_cd: trCd,
        tr_key: trKey,
      },
    });
  }

  /**
   * 평문 JSON 푸시를 파싱한다. KIS 의 `0|TR|001|a^b` 파이프 포맷과 다르므로 전면 대체한다.
   * `tr_cd` 가 없는 메시지(구독 응답 등)는 SYSTEM 으로 본다.
   */
  public override parseMessage(raw: string): WebSocketMessage {
    let parsed: unknown;
    try {
      parsed = JSON.parse(raw);
    } catch {
      return { messageType: 'SYSTEM', raw, encrypted: false };
    }

    if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
      return { messageType: 'SYSTEM', raw, encrypted: false };
    }

    const envelope = parsed as { header?: unknown; body?: unknown };
    const header =
      typeof envelope.header === 'object' && envelope.header !== null
        ? (envelope.header as Record<string, unknown>)
        : {};
    const trCd = typeof header.tr_cd === 'string' ? header.tr_cd : undefined;
    const trKey = typeof header.tr_key === 'string' ? header.tr_key : undefined;
    const body =
      typeof envelope.body === 'object' && envelope.body !== null && !Array.isArray(envelope.body)
        ? (envelope.body as Record<string, unknown>)
        : undefined;

    if (trCd === undefined) {
      return { messageType: 'SYSTEM', raw, encrypted: false };
    }

    return { messageType: 'DATA', trId: trCd, trKey, body, raw, encrypted: false };
  }

  protected override handleMessage(raw: string): void {
    const message = this.parseMessage(raw);

    if (message.messageType === 'DATA' && message.trId !== undefined) {
      this.emitEvent({
        eventType: 'data',
        trId: message.trId,
        ...(message.trKey !== undefined ? { trKey: message.trKey } : {}),
        ...(message.body !== undefined ? { body: message.body } : {}),
        raw,
      });
      return;
    }

    // 구독 응답 등 tr_cd 없는 시스템성 메시지
    this.emitEvent({ eventType: 'system', raw });
  }
}
