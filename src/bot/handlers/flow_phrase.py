from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.handlers.utils import get_checked_token, invalid_token_error_handling, unknown_error_handling, \
    unknown_error_callback_handling, invalid_token_error_callback_handling
from src.bot.resourses.strings import sres
from src.bot.states import MainStates
from src.bot.views.callbacks.flow_phrase import FlowPhraseCD
from src.bot.views.flow_phrase import flow_phrase__view, flow_phrase_about__view
from src.bot.views.models.flow_phrase import FlowPhraseViewData, FlowPhraseAboutViewData
from src.bot.views.utils import answer_view, update_view
from src.linguamate.exceptions import LinguaMateInvalidTokenError, LinguaMateAPIError, LinguaMateNotFoundError
from src.linguamate.services.auth import AuthService
from src.linguamate.services.phrase import PhraseService
from src.loggers import bot_logger

router = Router(name=__name__)
auth_service: AuthService
phrase_service: PhraseService


@router.message(MainStates.Main, F.text == sres.GENERAL.BTN.PHRASE_FLOW)
async def flow_phrase_command__handler(msg: Message, state: FSMContext):
    try:
        token = await get_checked_token(state)
        flow_phrase = await phrase_service.get_flow_phrase(token)
        view = flow_phrase__view(data=FlowPhraseViewData(id=flow_phrase.phrase.id, phrase=flow_phrase.phrase.phrase))
        await answer_view(msg, view)
    except LinguaMateNotFoundError as e:
        bot_logger.debug(e)
        await msg.answer(text=sres.PHRASE.PHRASE_FLOW.ERROR.PHRASEBOOK_IS_EMPTY)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)


@router.callback_query(FlowPhraseCD.filter())
async def flow_phrase__callback(callback: CallbackQuery, state: FSMContext):
    try:
        token = await get_checked_token(state)
        data = FlowPhraseCD.unpack(callback.data)

        if data.action == data.Action.REMEMBER:
            flow_phrase = await phrase_service.get_flow_phrase(token)
            view = flow_phrase__view(
                data=FlowPhraseViewData(id=flow_phrase.phrase.id, phrase=flow_phrase.phrase.phrase))
            await update_view(callback.message, view)
            await callback.answer()

        elif data.action == data.Action.FORGOT:
            try:
                phrase = await phrase_service.get_phrase_by_id(token, data.phrase_id)
                view_data = FlowPhraseAboutViewData(phrase=phrase)
                view = flow_phrase_about__view(data=view_data)
                await callback.answer()
            except LinguaMateNotFoundError as e:
                bot_logger.debug(e)
                await callback.answer(text=sres.PHRASE.PHRASE_FLOW.ERROR.PHRASEBOOK_IS_EMPTY)
                flow_phrase = await phrase_service.get_flow_phrase(token)
                view_data = FlowPhraseViewData(id=flow_phrase.phrase.id, phrase=flow_phrase.phrase.phrase)
                view = flow_phrase__view(data=view_data)
            await update_view(callback.message, view)

        elif data.action == data.Action.OKAY:
            flow_phrase = await phrase_service.get_flow_phrase(token)
            view = flow_phrase__view(
                data=FlowPhraseViewData(id=flow_phrase.phrase.id, phrase=flow_phrase.phrase.phrase))
            await update_view(callback.message, view)
            await callback.answer()

    except LinguaMateNotFoundError as e:
        bot_logger.debug(e)
        await callback.answer(text=sres.PHRASE.PHRASE_FLOW.ERROR.PHRASEBOOK_IS_EMPTY)
    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_callback_handling(callback, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_callback_handling(callback, state)
