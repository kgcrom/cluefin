from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    access_token_token_expired: str

    def get_token(self) -> str:
        return self.access_token


class ApprovalResponse(BaseModel):
    approval_key: str
