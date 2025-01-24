from aiogram.enums import ContentType
from aiogram.filters import CommandObject
from aiogram.types import Message

from src.bot.resourses.strings import sres


class MsgCheckError(Exception):
    def __init__(self, e_msg: str):
        self.e_msg = e_msg
        super().__init__(e_msg)


def check_content_type(msg: Message, *allowed: ContentType, e_msg: str | None = None):
    if msg.content_type in allowed:
        return
    raise MsgCheckError(e_msg=e_msg or sres.CHECK.ERROR.CONTENT_TYPE)


def check_has_command_args(command: CommandObject, e_msg: str | None = None):
    if command.args:
        return
    raise MsgCheckError(e_msg=e_msg or sres.CHECK.ERROR.EMPTY_COMMAND_ARGS)
