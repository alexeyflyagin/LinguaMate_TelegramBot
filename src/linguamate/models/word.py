from pydantic import BaseModel


class AddWordData(BaseModel):
    word: str
    translations: list[str]
    transcription: str | None = None


class AddWordsData(BaseModel):
    words: list[AddWordData]


class AddWordResponse(BaseModel):
    id: int


class AddWordsResponse(BaseModel):
    added_ids: dict[str, int]
    already_exists: list[str]


class WordEntity(BaseModel):
    id: int
    account_id: int
    word: str
    translations: list[str]
    transcription: str | None


class GetWordFlowResponse(BaseModel):
    word: WordEntity
