from uuid import UUID

from pydantic import BaseModel


class AuthData(BaseModel):
    phone_number: str


class AuthResponse(BaseModel):
    account_id: int
    nickname: str
    token: UUID


class SignupData(BaseModel):
    nickname: str
    phone_number: str


class CheckTokenResponse(BaseModel):
    is_valid: bool
