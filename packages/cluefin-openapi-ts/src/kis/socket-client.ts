import { BaseWebSocketClient, type SubscriptionType } from '../core/websocket';
import type { ApiEnv } from '../core/types';

const WS_URL_PROD = 'ws://ops.koreainvestment.com:21000/tryitout';
const WS_URL_DEV = 'ws://ops.koreainvestment.com:31000/tryitout';

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
}
