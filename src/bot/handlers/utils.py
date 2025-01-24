from uuid import UUID

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from src.bot.resourses import keyboards
from src.bot.resourses.keyboards import main_ikb
from src.bot.resourses.strings import sres
from src.bot.states import AuthStates, MainStates
from src.linguamate.exceptions import LinguaMateInvalidTokenError, LinguaMateAPIError
from src.linguamate.services.account import AccountService
from src.linguamate.services.auth import AuthService
from src.loggers import bot_logger

TOKEN__DATA_KEY = 'auth_token'

auth_service: AuthService
account_service: AccountService


async def set_token(state: FSMContext, token: UUID | None):
    data = await state.get_data()
    data[TOKEN__DATA_KEY] = str(token) if token else None
    await state.set_data(data)


async def get_token(state: FSMContext) -> UUID | None:
    data = await state.get_data()
    token = data.get(TOKEN__DATA_KEY, None)
    return UUID(token) if token else None


async def get_checked_token(state: FSMContext) -> UUID:
    """
    :return The token

    :raises LinguaMateInvalidTokenError: if token is not valid
    :raises LinguaMateAPIError: Unexpected error
    """
    token = await get_token(state)
    await auth_service.check_token(token, raise_if_none=True)
    return token


async def restore_state(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        account_info = await account_service.get_info(token)
        current_state = await state.get_state()

        if current_state == MainStates.Main.state:
            markup = main_ikb(total_phrases=account_info.total_phrases)
            await msg.answer(text=sres.GENERAL.SELECT_ACTION, reply_markup=markup)

    except LinguaMateInvalidTokenError as e:
        bot_logger.debug(e)
        await invalid_token_error_handling(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)


async def cancel_action(
        msg: Message,
        state: FSMContext,
        cancel_text: str | None = None,
        new_state: State | None = None,
):
    await state.set_state(new_state or MainStates.Main)
    await msg.answer(text=cancel_text or sres.GENERAL.ACTION_CANCELED)
    await restore_state(msg, state)


async def unknown_error_handling(
        msg: Message,
        state: FSMContext,
        auth_service_for_cancel: AuthService | None = None
):
    await msg.answer(text=sres.ERROR.UNEXPECTED)
    if auth_service_for_cancel:
        await cancel_action(msg, state)


async def unknown_error_callback_handling(
        callback: CallbackQuery,
        state: FSMContext,
        auth_service_for_cancel: AuthService | None = None
):
    await unknown_error_handling(callback.message, state, auth_service_for_cancel=auth_service_for_cancel)
    await callback.answer()


async def invalid_token_error_handling(
        msg: Message,
        state: FSMContext,
):
    await set_send_contact_state(msg, state)


async def invalid_token_error_callback_handling(
        callback: CallbackQuery,
        state: FSMContext,
):
    await invalid_token_error_handling(callback.message, state)
    await callback.answer()


async def set_send_contact_state(msg: Message, state: FSMContext):
    await state.set_state(AuthStates.SendContact)
    await msg.answer(text=sres.AUTH.SEND_CONTACT_REQUEST, reply_markup=keyboards.CONTACT_REQUEST_RM,
                     parse_mode=ParseMode.MARKDOWN)
