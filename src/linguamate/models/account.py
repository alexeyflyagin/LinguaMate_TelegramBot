from pydantic import BaseModel


class AccountInfoResponse(BaseModel):
    account_id: int
    nickname: str
    phone_number: str
    total_phrases: int
    total_words: int
