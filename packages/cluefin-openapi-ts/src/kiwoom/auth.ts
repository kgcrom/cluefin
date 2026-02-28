import { camelizeKeys } from '../core/case-convert';
import { KiwoomApiError, KiwoomAuthenticationError, KiwoomServerError, KiwoomValidationError } from '../core/errors';
import type { ApiEnv } from '../core/types';

export interface KiwoomAuthOptions {
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  fetchImpl?: typeof fetch;
}

export interface KiwoomTokenResponse {
  tokenType: string;
  token: string;
  expiresDt: string;
}

const getBaseUrl = (env: ApiEnv): string => (env === 'prod' ? 'https://api.kiwoom.com' : 'https://mockapi.kiwoom.com');

export class KiwoomAuth {
  private readonly baseUrl: string;
  private readonly fetchImpl: typeof fetch;

  public constructor(private readonly options: KiwoomAuthOptions) {
    const env = options.env ?? 'dev';
    this.baseUrl = getBaseUrl(env);
    this.fetchImpl = options.fetchImpl ?? globalThis.fetch;
  }

  public async generateToken(): Promise<KiwoomTokenResponse> {
    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify({
        grant_type: 'client_credentials',
        appkey: this.options.appKey,
        secretkey: this.options.secretKey,
      }),
    });

    if (response.status === 400) {
      throw new KiwoomValidationError('Invalid token request');
    }
    if (response.status === 401) {
      throw new KiwoomAuthenticationError('Kiwoom authentication failed');
    }
    if (response.status >= 500) {
      throw new KiwoomServerError('Kiwoom token server error');
    }
    if (!response.ok) {
      throw new KiwoomApiError(`Unexpected token response status ${response.status}`);
    }

    return camelizeKeys(await response.json()) as KiwoomTokenResponse;
  }

  public async revokeToken(token: string): Promise<boolean> {
    const response = await this.fetchImpl(`${this.baseUrl}/oauth2/revoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify({
        appkey: this.options.appKey,
        secretkey: this.options.secretKey,
        token,
      }),
    });

    if (!response.ok) {
      throw new KiwoomApiError(`Failed to revoke token (status ${response.status})`);
    }

    return true;
  }
}
