from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.resourses.strings import sres
from src.bot.resourses.strings.utils import add_counter

CONTACT_REQUEST_RM = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=sres.AUTH.BTN.SEND_CONTACT, request_contact=True)]],
    resize_keyboard=True, is_persistent=True,
)


def main_ikb(total_phrases: int, total_words: int) -> ReplyKeyboardMarkup:
    my_phrases_text = sres.GENERAL.BTN.MY_PHRASES
    if total_phrases:
        my_phrases_text = add_counter(sres.GENERAL.BTN.MY_PHRASES, total_phrases)

    my_words_text = sres.GENERAL.BTN.MY_WORDS
    if total_words:
        my_words_text = add_counter(sres.GENERAL.BTN.MY_WORDS, total_words)

    keyboard = [
        [KeyboardButton(text=sres.GENERAL.BTN.ADD_PHRASE_MODE), KeyboardButton(text=sres.GENERAL.BTN.ADD_WORD_MODE)],
        [KeyboardButton(text=my_phrases_text), KeyboardButton(text=my_words_text)],
        [KeyboardButton(text=sres.GENERAL.BTN.PHRASE_FLOW), KeyboardButton(text=sres.GENERAL.BTN.WORD_FLOW)],
        [KeyboardButton(text=sres.GENERAL.BTN.PROFILE)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, is_persistent=True)
