from pydantic import BaseModel


class AddPhraseData(BaseModel):
    phrase: str
    translations: list[str]


class AddPhrasesData(BaseModel):
    phrases: list[AddPhraseData]


class AddPhraseResponse(BaseModel):
    id: int


class AddPhrasesResponse(BaseModel):
    added_ids: dict[str, int]
    already_exists: list[str]


class PhraseEntity(BaseModel):
    id: int
    account_id: int
    phrase: str
    phrase_lower: str
    translations: list[str]


class GetFlowPhraseResponse(BaseModel):
    phrase: PhraseEntity
