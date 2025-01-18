from uuid import UUID

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import sres, keyboards
from src.bot.states import AuthStates, MainStates

TOKEN__DATA_KEY = 'auth_token'


async def set_token(state: FSMContext, token: UUID | None):
    data = await state.get_data()
    data[TOKEN__DATA_KEY] = str(token) if token else None
    await state.set_data(data)


async def get_token(state: FSMContext) -> UUID | None:
    data = await state.get_data()
    token = data.get(TOKEN__DATA_KEY, None)
    return UUID(token) if token else None


async def cancel_action(msg: Message, state: FSMContext):
    # TODO Check the token and choose the appropriate state
    await msg.answer(text=sres.ERROR.UNEXPECTED)


async def unknown_error_handling(msg: Message, state: FSMContext, cancel: bool = False):
    await msg.answer(text=sres.ERROR.UNEXPECTED)
    if cancel:
        await cancel_action(msg, state)


async def send_contact_request(msg: Message, state: FSMContext):
    await state.set_state(AuthStates.SendContact)
    await msg.answer(text=sres.AUTH.SEND_CONTACT_REQUEST, reply_markup=keyboards.CONTACT_REQUEST_RM,
                     parse_mode=ParseMode.MARKDOWN)
