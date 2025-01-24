from aiogram import Router, F
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.resourses import commands
from src.bot.resourses.strings import sres
from src.bot.handlers.utils import get_checked_token, invalid_token_error_handling, unknown_error_handling, \
    cancel_action
from src.bot.models.parsers import ParsedPhraseData, ParseError
from src.bot.msg_checks.checks import MsgCheckError, check_content_type
from src.bot.states import MainStates, AddPhraseModeStates
from src.linguamate.exceptions import LinguaMateInvalidTokenError, LinguaMateAPIError
from src.linguamate.models.phrase import AddPhraseData, AddPhrasesData
from src.linguamate.services.phrase import PhraseService
from src.loggers import bot_logger

router = Router(name=__name__)
phrase_service: PhraseService


@router.message(MainStates.Main, F.text == sres.GENERAL.BTN.ADD_PHRASE_MODE)
async def add_phrase_mode_command__handler(msg: Message, state: FSMContext):
    try:
        await get_checked_token(state)
        await state.set_state(AddPhraseModeStates.EnterPhrase)
        await msg.answer(text=sres.PHRASE.ADD_MODE.ENTER_PHRASE, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)


@router.message(AddPhraseModeStates.EnterPhrase, Command(commands.EXIT))
async def exit__handler(msg: Message, state: FSMContext):
    await cancel_action(msg, state, cancel_text=sres.PHRASE.ADD_MODE.EXIT)


@router.message(AddPhraseModeStates.EnterPhrase)
async def enter_phrase__handler(msg: Message, state: FSMContext):
    try:
        token = await get_checked_token(state)
        check_content_type(msg, ContentType.TEXT, e_msg=sres.PHRASE.ADD_MODE.ERROR.INCORRECT_CONTENT)
        parsed_phrases = ParsedPhraseData.list_from_str(msg.text)
        add_phrase_datas = [AddPhraseData(phrase=i.phrase, translations=i.translations) for i in parsed_phrases]
        add_phrases_data = AddPhrasesData(phrases=add_phrase_datas)
        response = await phrase_service.add_phrases(token, add_phrases_data)
        if response.added_ids:
            await msg.answer(text=sres.PHRASE.ADD_MODE.SUCCESS.format(added_count=len(response.added_ids)),
                             parse_mode=ParseMode.MARKDOWN)
        else:
            await msg.answer(text=sres.PHRASE.ADD_MODE.ERROR.ALREADY_EXIST, parse_mode=ParseMode.MARKDOWN)
    except (MsgCheckError, ParseError) as e:
        await msg.answer(e.e_msg, parse_mode=ParseMode.MARKDOWN)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)
