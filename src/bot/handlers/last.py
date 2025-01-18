from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.utils import send_contact_request

router = Router(name=__name__)


@router.message(StateFilter(None))
async def none_state__handler(msg: Message, state: FSMContext):
    await msg.answer('👋')
    await send_contact_request(msg, state)
