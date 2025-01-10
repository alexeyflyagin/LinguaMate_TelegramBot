from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer("Hello! I'm <b>LinguaMate</b>.", parse_mode=ParseMode.HTML)
