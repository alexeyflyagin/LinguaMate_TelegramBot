from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.utils import set_send_contact_state

router = Router(name=__name__)


@router.message(StateFilter(None))
async def none_state__handler(msg: Message, state: FSMContext):
    await msg.answer('👋')
    await set_send_contact_state(msg, state)
