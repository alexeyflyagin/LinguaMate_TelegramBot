from pydantic import BaseModel

from src.bot.resourses.strings import sres


class ParseError(Exception):
    def __init__(self, e_msg: str):
        self.e_msg = e_msg
        super().__init__(e_msg)


class ParsedPhraseData(BaseModel):
    phrase: str
    translations: list[str]

    @staticmethod
    def from_str(text: str) -> "ParsedPhraseData":
        items = [i.strip() for i in text.strip().split("::")]
        if len(items) == 1:
            raise ParseError(sres.PHRASE.ADD_FAST.ERROR.NO_TRANSLATION)
        elif len(items) < 1:
            raise ParseError(sres.PHRASE.ADD_FAST.ERROR.INCORRECT_ARGS)
        phrase = items.pop(0)
        return ParsedPhraseData(phrase=phrase, translations=items)

    @staticmethod
    def list_from_str(text: str) -> list["ParsedPhraseData"]:
        phrase_items = [i.strip() for i in text.strip().split("\n")]
        if len(phrase_items) == 0:
            raise ParseError(sres.PHRASE.ADD_MODE.ERROR.INCORRECT_CONTENT)
        parsed_phrase_list: list[ParsedPhraseData] = []
        for phrase_item in phrase_items:
            items = [i.strip() for i in phrase_item.strip().split("::")]
            if len(items) == 1:
                raise ParseError(sres.PHRASE.ADD_MODE.ERROR.NO_TRANSLATION)
            elif len(items) < 1:
                raise ParseError(sres.PHRASE.ADD_MODE.ERROR.INCORRECT_CONTENT)
            phrase = items.pop(0)
            parsed_phrase_list.append(ParsedPhraseData(phrase=phrase, translations=items))
        return parsed_phrase_list
