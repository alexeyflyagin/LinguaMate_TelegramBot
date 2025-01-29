from aiogram import Router, F
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.handlers.utils import get_checked_token, invalid_token_error_handling, unknown_error_handling, \
    cancel_action
from src.bot.models.parsers import ParsedWordData, ParseError
from src.bot.msg_checks.checks import MsgCheckError, check_content_type
from src.bot.resourses import commands
from src.bot.resourses.strings import sres
from src.bot.states import MainStates, AddWordModeStates
from src.linguamate.exceptions import LinguaMateInvalidTokenError, LinguaMateAPIError
from src.linguamate.models.word import AddWordData, AddWordsData
from src.linguamate.services.dictionary import DictionaryService
from src.loggers import bot_logger

router = Router(name=__name__)
dict_service: DictionaryService


@router.message(MainStates.Main, F.text == sres.GENERAL.BTN.ADD_WORD_MODE)
async def add_word_mode_command__handler(msg: Message, state: FSMContext):
    try:
        await get_checked_token(state)
        await state.set_state(AddWordModeStates.EnterWord)
        await msg.answer(text=sres.DICTIONARY.ADD_MODE.ENTER_WORD, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)


@router.message(AddWordModeStates.EnterWord, Command(commands.EXIT))
async def exit__handler(msg: Message, state: FSMContext):
    await cancel_action(msg, state, cancel_text=sres.DICTIONARY.ADD_MODE.EXIT)


@router.message(AddWordModeStates.EnterWord)
async def enter_word__handler(msg: Message, state: FSMContext):
    try:
        token = await get_checked_token(state)
        check_content_type(msg, ContentType.TEXT, e_msg=sres.DICTIONARY.ADD_MODE.ERROR.INCORRECT_CONTENT)
        parsed_words = ParsedWordData.list_from_str(msg.text)
        add_word_datas = [AddWordData(word=i.word, translations=i.translations) for i in parsed_words]
        add_words_data = AddWordsData(words=add_word_datas)
        response = await dict_service.add_words(token, add_words_data)
        if response.added_ids:
            await msg.answer(text=sres.DICTIONARY.ADD_MODE.SUCCESS.format(added_count=len(response.added_ids)),
                             parse_mode=ParseMode.MARKDOWN)
        else:
            await msg.answer(text=sres.DICTIONARY.ADD_MODE.ERROR.ALREADY_EXIST, parse_mode=ParseMode.MARKDOWN)
    except (MsgCheckError, ParseError) as e:
        await msg.answer(e.e_msg, parse_mode=ParseMode.MARKDOWN)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)
