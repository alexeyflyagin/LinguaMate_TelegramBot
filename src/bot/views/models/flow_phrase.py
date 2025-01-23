from pydantic import BaseModel

from src.linguamate.models.phrase import PhraseEntity


class FlowPhraseViewData(BaseModel):
    id: int
    phrase: str


class FlowPhraseAboutViewData(BaseModel):
    phrase: PhraseEntity
