from aiogram.filters.callback_data import CallbackData

from src.bot.views.prefixes import WORD_FLOW_CD


class WordFlowCD(CallbackData, prefix=WORD_FLOW_CD):
    word_id: int
    action: int

    class Action:
        FORGOT = 0
        REMEMBER = 1
        OKAY = 2
