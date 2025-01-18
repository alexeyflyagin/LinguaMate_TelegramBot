from pydantic import BaseModel

from src.bot import sres


class ParseError(Exception):
    def __init__(self, e_msg: str):
        self.e_msg = e_msg
        super().__init__(e_msg)


class FastPhraseData(BaseModel):
    phrase: str
    translations: list[str]

    @staticmethod
    def from_str(text: str):
        items = [i.strip() for i in text.strip().split("::")]
        if len(items) == 1:
            raise ParseError(sres.PHRASE.ADD_FAST.ERROR.NO_TRANSLATION)
        elif len(items) < 1:
            raise ParseError(sres.PHRASE.ADD_FAST.ERROR.INCORRECT_ARGS)
        phrase = items.pop(0)
        return FastPhraseData(phrase=phrase, translations=items)
