from pydantic import BaseModel, ConfigDict, Field


class TokenResponse(BaseModel):
    """접근토큰발급 (`POST /oauth2/token`) 응답."""

    model_config = ConfigDict(extra="allow")

    access_token: str = Field(description="접근토큰")
    scope: str = Field(description='"oob" 고정')
    token_type: str = Field(description='토큰유형, "Bearer" 고정')
    expires_in: int = Field(description="접근토큰 유효시간(초), 86400 = 24시간")

    def get_token(self) -> str:
        return self.access_token


class TokenRevokeResponse(BaseModel):
    """접근토큰폐기 (`POST /oauth2/revoke`) 응답.

    성공 시 code/message, 실패 시 error_code/error_description 이 내려온다.
    """

    model_config = ConfigDict(extra="allow")

    code: int | None = Field(default=None, description="응답코드 (성공 시)")
    message: str | None = Field(default=None, description="응답메시지 (성공 시)")
    error_code: str | None = Field(default=None, description="응답코드 (실패 시)")
    error_description: str | None = Field(default=None, description="응답메시지 (실패 시)")
