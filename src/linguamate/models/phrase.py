from pydantic import BaseModel


class AddPhraseData(BaseModel):
    phrase: str
    translations: list[str]


class AddPhraseResponse(BaseModel):
    id: int
