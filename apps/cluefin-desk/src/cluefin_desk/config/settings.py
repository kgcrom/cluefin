"""desk 설정. 브로커 키는 cluefin-openapi 의 `BrokerClientConfig` 가 읽는다 — cwd 의 `.env` 위에 실제 환경변수."""

from __future__ import annotations

from dataclasses import dataclass

from cluefin_openapi import BrokerClientConfig, load_env


@dataclass(frozen=True, slots=True)
class Settings:
    brokers: BrokerClientConfig
    # KIS HTS 로그인 ID — HTS 관심종목 조회에만 쓴다. 없으면 관심종목 화면이 안내 문구만 띄운다.
    kis_hts_user_id: str | None = None

    @classmethod
    def from_env(cls) -> Settings:
        env = load_env()
        return cls(brokers=BrokerClientConfig.from_env(env), kis_hts_user_id=env.get("KIS_HTS_USER_ID") or None)


settings = Settings.from_env()
