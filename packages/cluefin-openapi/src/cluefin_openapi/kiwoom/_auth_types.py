from datetime import datetime

from pydantic import BaseModel, field_validator


class TokenResponse(BaseModel):
    expires_dt: datetime
    token_type: str
    token: str

    @field_validator("expires_dt", mode="before")
    def parse_expires_dt(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y%m%d%H%M%S")
            except ValueError:
                pass  # 다른 형식도 추가 가능
        return v
