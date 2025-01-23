from aiogram.filters.callback_data import CallbackData

from src.bot.views.prefixes import FLOW_PHRASE_CD


class FlowPhraseCD(CallbackData, prefix=FLOW_PHRASE_CD):
    phrase_id: int
    action: int

    class Action:
        FORGOT = 0
        REMEMBER = 1
        OKAY = 2
