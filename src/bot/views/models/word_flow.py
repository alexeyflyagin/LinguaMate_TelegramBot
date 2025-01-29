from pydantic import BaseModel

from src.linguamate.models.word import WordEntity


class WordFlowViewData(BaseModel):
    id: int
    word: str


class WordFlowAboutViewData(BaseModel):
    word: WordEntity
