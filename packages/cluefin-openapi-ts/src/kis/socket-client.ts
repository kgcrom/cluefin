import { KisApiError } from '../core/errors.js';
import type { ApiEnv } from '../core/types.js';
import { BaseWebSocketClient, type SubscriptionType } from '../core/websocket.js';

const WS_URL_PROD = 'ws://ops.koreainvestment.com:21000/tryitout';
const WS_URL_DEV = 'ws://ops.koreainvestment.com:31000/tryitout';

/**
 * rt_cd 가 "0" 이 아닌 JSON 시스템 응답을 오류로 바꾼다. 거절이 아니면 undefined.
 *
 * KIS 는 세션 단위로 거절하고 연결을 끊는다 — 다른 세션이 같은 app key 를 쓰면 OPSP8996
 * "ALREADY IN USE appkey", 더 새 approve() 가 key 를 대체했으면 OPSP0011 "invalid approval"
 * (2026-10-12 실측). msg1 이 approval key 를 그대로 돌려주므로 가린다.
 */
export interface KisRejection {
  trId: string | undefined;
  error: KisApiError;
}

export const parseKisRejection = (raw: string, approvalKey: string): KisRejection | undefined => {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return undefined;
  }
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    return undefined;
  }

  const envelope = parsed as { header?: unknown; body?: unknown };
  if (typeof envelope.body !== 'object' || envelope.body === null) {
    return undefined;
  }
  const body = envelope.body as { rt_cd?: unknown; msg_cd?: unknown; msg1?: unknown };
  if (typeof body.rt_cd !== 'string' || body.rt_cd === '0') {
    return undefined;
  }

  const header = typeof envelope.header === 'object' && envelope.header !== null ? envelope.header : {};
  const trId = 'tr_id' in header && typeof header.tr_id === 'string' ? header.tr_id : undefined;
  const msgCd = typeof body.msg_cd === 'string' ? body.msg_cd : '';
  const rawMsg1 = typeof body.msg1 === 'string' ? body.msg1 : '';
  const msg1 = (approvalKey ? rawMsg1.split(approvalKey).join('***') : rawMsg1).trim();

  const error = new KisApiError(`KIS WebSocket rejected ${trId}: [${msgCd}] ${msg1}`, {
    errorCode: msgCd,
    responseData: { tr_id: trId, rt_cd: body.rt_cd, msg_cd: msgCd, msg1 },
  });
  return { trId, error };
};

export interface KisSocketClientOptions {
  approvalKey: string;
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
}

export class KisSocketClient extends BaseWebSocketClient {
  public readonly env: ApiEnv;
  private readonly approvalKey: string;
  private lastRejection: KisApiError | undefined;

  constructor(options: KisSocketClientOptions) {
    const env = options.env ?? 'dev';
    super({
      url: env === 'prod' ? WS_URL_PROD : WS_URL_DEV,
      rateLimitBurst: options.rateLimitBurst ?? 3,
      rateLimitRequestsPerSecond: options.rateLimitRequestsPerSecond ?? 5,
    });
    this.env = env;
    this.approvalKey = options.approvalKey;
  }

  protected override buildSubscriptionMessage(trId: string, trKey: string, trType: SubscriptionType): string {
    return JSON.stringify({
      header: {
        approval_key: this.approvalKey,
        custtype: 'P',
        tr_type: trType,
        'content-type': 'utf-8',
      },
      body: {
        input: {
          tr_id: trId,
          tr_key: trKey,
        },
      },
    });
  }

  public override connect(): void {
    this.lastRejection = undefined;
    super.connect();
  }

  protected override handleMessage(raw: string): void {
    super.handleMessage(raw);

    const rejection = parseKisRejection(raw, this.approvalKey);
    if (rejection === undefined) {
      return;
    }
    this.lastRejection = rejection.error;
    // EventEmitter 는 리스너 없는 'error' 를 throw 한다 — 서버 메시지 하나로 프로세스가 죽지 않게,
    // 듣는 쪽이 없으면 기록만 해 두고 다음 subscribe 의 "not connected" 오류로 알린다.
    if (this.listenerCount('error') > 0) {
      this.emitEvent({
        eventType: 'error',
        ...(rejection.trId ? { trId: rejection.trId } : {}),
        error: rejection.error,
      });
    }
  }

  protected override notConnectedError(): Error {
    if (this.lastRejection === undefined) {
      return super.notConnectedError();
    }
    return new KisApiError(`WebSocket not connected (server closed it after: ${this.lastRejection.message})`, {
      errorCode: this.lastRejection.errorCode,
      responseData: this.lastRejection.responseData,
    });
  }
}
