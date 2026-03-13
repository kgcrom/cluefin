import { EventEmitter } from 'node:events';
import WebSocket from 'ws';
import { TokenBucket } from './rate-limiter';

export type SubscriptionType = '1' | '2';
export type MessageType = 'PINGPONG' | 'DATA' | 'SYSTEM';
export type WebSocketEventType = 'data' | 'connected' | 'disconnected' | 'error' | 'subscribed' | 'unsubscribed';

export interface WebSocketMessage {
  messageType: MessageType;
  trId?: string | undefined;
  data?: string[] | undefined;
  raw: string;
  encrypted: boolean;
}

export interface WebSocketEvent {
  eventType: WebSocketEventType;
  trId?: string;
  trKey?: string;
  data?: { values: string[]; encrypted: boolean };
  error?: Error;
  raw?: string;
}

export interface BaseWebSocketClientOptions {
  url: string;
  rateLimitBurst: number;
  rateLimitRequestsPerSecond: number;
}

export interface BaseWebSocketClientEvents {
  data: [event: WebSocketEvent];
  connected: [event: WebSocketEvent];
  disconnected: [event: WebSocketEvent];
  error: [event: WebSocketEvent];
  subscribed: [event: WebSocketEvent];
  unsubscribed: [event: WebSocketEvent];
}

export class BaseWebSocketClient extends EventEmitter {
  private ws: WebSocket | null = null;
  private _connected = false;
  private readonly _subscriptions = new Map<string, string>();
  private readonly rateLimiter: TokenBucket;
  protected readonly url: string;

  constructor(options: BaseWebSocketClientOptions) {
    super();
    this.url = options.url;
    this.rateLimiter = new TokenBucket(options.rateLimitBurst, options.rateLimitRequestsPerSecond);
  }

  public get connected(): boolean {
    return this._connected;
  }

  public get subscriptions(): Map<string, string> {
    return new Map(this._subscriptions);
  }

  public connect(): void {
    this.ws = new WebSocket(this.url);

    this.ws.on('open', () => {
      this._connected = true;
      this.emitEvent({ eventType: 'connected' });
    });

    this.ws.on('message', (data: WebSocket.Data) => {
      const raw = data.toString();
      this.handleMessage(raw);
    });

    this.ws.on('close', () => {
      this._connected = false;
      this.emitEvent({ eventType: 'disconnected' });
    });

    this.ws.on('error', (err: Error) => {
      this.emitEvent({ eventType: 'error', error: err });
    });
  }

  public close(): void {
    this._connected = false;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  public async subscribe(trId: string, trKey: string): Promise<void> {
    if (!this._connected || !this.ws) {
      throw new Error('WebSocket not connected');
    }

    const ok = await this.rateLimiter.waitForToken(5000);
    if (!ok) {
      throw new Error('Subscription rate limit exceeded');
    }

    const subscriptionKey = `${trId}:${trKey}`;
    if (this._subscriptions.has(subscriptionKey)) {
      return;
    }

    const message = this.buildSubscriptionMessage(trId, trKey, '1');
    this.ws.send(message);
    this._subscriptions.set(subscriptionKey, trKey);
    this.emitEvent({ eventType: 'subscribed', trId, trKey });
  }

  public async unsubscribe(trId: string, trKey: string): Promise<void> {
    if (!this._connected || !this.ws) {
      throw new Error('WebSocket not connected');
    }

    const subscriptionKey = `${trId}:${trKey}`;
    if (!this._subscriptions.has(subscriptionKey)) {
      return;
    }

    const message = this.buildSubscriptionMessage(trId, trKey, '2');
    this.ws.send(message);
    this._subscriptions.delete(subscriptionKey);
    this.emitEvent({ eventType: 'unsubscribed', trId, trKey });
  }

  protected buildSubscriptionMessage(_trId: string, _trKey: string, _trType: SubscriptionType): string {
    throw new Error('buildSubscriptionMessage must be implemented by subclass');
  }

  private handleMessage(raw: string): void {
    const message = this.parseMessage(raw);

    if (message.messageType === 'PINGPONG') {
      this.ws?.send(raw);
      return;
    }

    if (message.messageType === 'DATA' && message.trId && message.data) {
      this.emitEvent({
        eventType: 'data',
        trId: message.trId,
        data: { values: message.data, encrypted: message.encrypted },
        raw,
      });
    }
  }

  public parseMessage(raw: string): WebSocketMessage {
    if (raw.startsWith('PINGPONG')) {
      return { messageType: 'PINGPONG', raw, encrypted: false };
    }

    if (raw.length > 0 && (raw[0] === '0' || raw[0] === '1')) {
      const parts = raw.split('|');
      if (parts.length >= 4) {
        const encrypted = parts[0] === '1';
        const trId = parts[1];
        const dataStr = parts[3] ?? '';
        const data = dataStr.length > 0 ? dataStr.split('^') : [];

        return { messageType: 'DATA', trId, data, raw, encrypted };
      }
    }

    return { messageType: 'SYSTEM', raw, encrypted: false };
  }

  private emitEvent(event: WebSocketEvent): void {
    this.emit(event.eventType, event);
  }
}
