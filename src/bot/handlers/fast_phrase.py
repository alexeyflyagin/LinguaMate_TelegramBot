from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import commands, sres
from src.bot.handlers.utils import get_token, get_checked_token, invalid_token_error_handling, unknown_error_handling
from src.bot.models.parsers import ParsedPhraseData, ParseError
from src.bot.msg_checks.checks import check_has_command_args, MsgCheckError
from src.bot.states import MainStates
from src.linguamate.exceptions import LinguaMateInvalidTokenError, LinguaMateAPIError, LinguaMateConflictError
from src.linguamate.models.phrase import AddPhraseData
from src.linguamate.services.auth import AuthService
from src.linguamate.services.phrase import PhraseService
from src.loggers import bot_logger

router = Router(name=__name__)
auth_service: AuthService
phrase_service: PhraseService


@router.message(MainStates.Main, Command(commands.ADD_PHRASE))
async def fast_add_phrase_command__handler(msg: Message, state: FSMContext, command: CommandObject):
    try:
        token = await get_checked_token(auth_service, state)
        check_has_command_args(command, e_msg=sres.PHRASE.ADD_FAST.ERROR.NO_ARGS)
        phrase = ParsedPhraseData.from_str(command.args)
        add_phrase_data = AddPhraseData(phrase=phrase.phrase, translations=phrase.translations)
        await phrase_service.add_phrase(token, add_phrase_data)
        await msg.answer(text=sres.PHRASE.ADD_FAST.SUCCESS, parse_mode=ParseMode.MARKDOWN)
    except (MsgCheckError, ParseError) as e:
        await msg.answer(e.e_msg, parse_mode=ParseMode.MARKDOWN)
    except LinguaMateConflictError as e:
        bot_logger.debug(e)
        await msg.answer(text=sres.PHRASE.ADD_FAST.ERROR.ALREADY_EXISTS, parse_mode=ParseMode.MARKDOWN)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)
