from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.resourses.strings import sres
from src.bot.views.callbacks.flow_phrase import FlowPhraseCD


def flow_phrase_im(phrase_id: int) -> InlineKeyboardMarkup:
    remember_data = FlowPhraseCD(phrase_id=phrase_id, action=FlowPhraseCD.Action.REMEMBER).pack()
    forgot_data = FlowPhraseCD(phrase_id=phrase_id, action=FlowPhraseCD.Action.FORGOT).pack()
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=sres.PHRASE.PHRASE_FLOW.BTN.FORGOT, callback_data=forgot_data))
    ikb.add(InlineKeyboardButton(text=sres.PHRASE.PHRASE_FLOW.BTN.REMEMBER, callback_data=remember_data))
    ikb.adjust(2)
    return ikb.as_markup()


def flow_phrase_about_im(phrase_id: int) -> InlineKeyboardMarkup:
    okay_data = FlowPhraseCD(phrase_id=phrase_id, action=FlowPhraseCD.Action.OKAY).pack()
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=sres.PHRASE.PHRASE_FLOW.BTN.OKAY, callback_data=okay_data))
    ikb.adjust(1)
    return ikb.as_markup()
