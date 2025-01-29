from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.resourses.strings import sres
from src.bot.views.callbacks.word_flow import WordFlowCD


def word_flow_im(word_id: int) -> InlineKeyboardMarkup:
    remember_data = WordFlowCD(word_id=word_id, action=WordFlowCD.Action.REMEMBER).pack()
    forgot_data = WordFlowCD(word_id=word_id, action=WordFlowCD.Action.FORGOT).pack()
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=sres.DICTIONARY.WORD_FLOW.BTN.FORGOT, callback_data=forgot_data))
    ikb.add(InlineKeyboardButton(text=sres.DICTIONARY.WORD_FLOW.BTN.REMEMBER, callback_data=remember_data))
    ikb.adjust(2)
    return ikb.as_markup()


def word_flow_about_im(word_id: int) -> InlineKeyboardMarkup:
    okay_data = WordFlowCD(word_id=word_id, action=WordFlowCD.Action.OKAY).pack()
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=sres.DICTIONARY.WORD_FLOW.BTN.OKAY, callback_data=okay_data))
    ikb.adjust(1)
    return ikb.as_markup()
