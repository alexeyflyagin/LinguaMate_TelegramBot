from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message

from src.bot.views.models.general import View, ViewType
from src.loggers import bot_logger


async def answer_view(
        msg: Message,
        view: View,
        raise_if_error: bool = False
) -> Message:
    return await show_view(msg.bot, msg.chat.id, view, raise_if_error=raise_if_error)


async def update_view(
        msg: Message,
        view: View,
        raise_if_error: bool = False
) -> Message:
    return await show_view(msg.bot, msg.chat.id, view, update_msg_id=msg.message_id, raise_if_error=raise_if_error)


async def show_view(
        bot: Bot,
        chat_id: int,
        view: View,
        update_msg_id: int | None = None,
        raise_if_error: bool = False
) -> Message:
    try:
        if view.view_type == ViewType.TEXT and update_msg_id:
            new_msg = await bot.edit_message_text(chat_id=chat_id, text=view.text, parse_mode=view.parse_mode,
                                                  reply_markup=view.reply_markup, message_id=update_msg_id)

        elif view.view_type == ViewType.TEXT:
            new_msg = await bot.send_message(chat_id=chat_id, text=view.text, parse_mode=view.parse_mode,
                                             reply_markup=view.reply_markup)

        else:
            raise ValueError(f"The view cannot be displayed. Incorrect view type ({view.view_type}).")

        return new_msg
    except TelegramAPIError as e:
        bot_logger.debug(e)
        if raise_if_error:
            raise
