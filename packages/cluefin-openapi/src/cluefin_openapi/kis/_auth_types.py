from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    access_token_token_expired: str

class ApprovalResponse(BaseModel):
    approval_key: str
