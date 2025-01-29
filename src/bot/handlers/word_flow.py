from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.handlers.utils import get_checked_token, invalid_token_error_handling, unknown_error_handling, \
    unknown_error_callback_handling, invalid_token_error_callback_handling
from src.bot.resourses.strings import sres
from src.bot.states import MainStates
from src.bot.views.callbacks.word_flow import WordFlowCD
from src.bot.views.models.word_flow import WordFlowViewData, WordFlowAboutViewData
from src.bot.views.utils import answer_view, update_view
from src.bot.views.word_flow import word_flow__view, word_flow_about__view
from src.linguamate.exceptions import LinguaMateInvalidTokenError, LinguaMateAPIError, LinguaMateNotFoundError
from src.linguamate.services.auth import AuthService
from src.linguamate.services.dictionary import DictionaryService
from src.loggers import bot_logger

router = Router(name=__name__)
auth_service: AuthService
dict_service: DictionaryService


@router.message(MainStates.Main, F.text == sres.GENERAL.BTN.WORD_FLOW)
async def word_flow_command__handler(msg: Message, state: FSMContext):
    try:
        token = await get_checked_token(state)
        res = await dict_service.get_word_flow(token)
        view = word_flow__view(data=WordFlowViewData(id=res.word.id, word=res.word.word))
        await answer_view(msg, view)
    except LinguaMateNotFoundError as e:
        bot_logger.debug(e)
        await msg.answer(text=sres.DICTIONARY.WORD_FLOW.ERROR.DICTIONARY_IS_EMPTY)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)


@router.callback_query(WordFlowCD.filter())
async def word_flow__callback(callback: CallbackQuery, state: FSMContext):
    try:
        token = await get_checked_token(state)
        data = WordFlowCD.unpack(callback.data)

        if data.action == data.Action.REMEMBER:
            res = await dict_service.get_word_flow(token)
            view = word_flow__view(
                data=WordFlowViewData(id=res.word.id, word=res.word.word))
            await update_view(callback.message, view)
            await callback.answer()

        elif data.action == data.Action.FORGOT:
            try:
                word = await dict_service.get_word_by_id(token, data.word_id)
                view_data = WordFlowAboutViewData(word=word)
                view = word_flow_about__view(data=view_data)
                await callback.answer()
            except LinguaMateNotFoundError as e:
                bot_logger.debug(e)
                await callback.answer(text=sres.DICTIONARY.WORD_FLOW.ERROR.DICTIONARY_IS_EMPTY)
                res = await dict_service.get_word_flow(token)
                view_data = WordFlowViewData(id=res.word.id, word=res.word.word)
                view = word_flow__view(data=view_data)
            await update_view(callback.message, view)

        elif data.action == data.Action.OKAY:
            res = await dict_service.get_word_flow(token)
            view = word_flow__view(
                data=WordFlowViewData(id=res.word.id, word=res.word.word))
            await update_view(callback.message, view)
            await callback.answer()

    except LinguaMateNotFoundError as e:
        bot_logger.debug(e)
        await callback.answer(text=sres.DICTIONARY.WORD_FLOW.ERROR.DICTIONARY_IS_EMPTY)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_callback_handling(callback, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_callback_handling(callback, state)
