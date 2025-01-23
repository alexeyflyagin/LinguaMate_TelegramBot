from aiogram.types import BotCommand

ADD_PHRASE = BotCommand(command='add_phrase', description="Add new phrase")
ADD_PHRASE_MODE = BotCommand(command='add_phrase_mode', description="Turn on the phrase-adding mode")

FLOW_PHRASE = BotCommand(command='flow_phrase', description="Learn phrases from an endless stream of phrases")

EXIT = BotCommand(command='exit', description="Leave something")
