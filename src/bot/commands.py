from aiogram.types import BotCommand

ADD_PHRASE = BotCommand(command='addphrase', description="Add new phrase")
ADD_PHRASE_MODE = BotCommand(command='addphrasemode', description="Turn on the phrase-adding mode")

FLOW_PHRASE = BotCommand(command='flowphrase', description="Learn phrases from an endless stream of phrases")

EXIT = BotCommand(command='exit', description="Leave something")
