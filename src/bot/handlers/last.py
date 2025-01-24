from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.utils import set_send_contact_state, restore_state
from src.bot.states import MainStates
from src.linguamate.services.account import AccountService

router = Router(name=__name__)
account_service: AccountService


@router.message(StateFilter(None))
async def none_state__handler(msg: Message, state: FSMContext):
    await msg.answer('👋')
    await set_send_contact_state(msg, state)


@router.message(MainStates())
async def main_state__handler(msg: Message, state: FSMContext):
    await restore_state(msg, state)
