from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dependency_injector.wiring import inject

from src.linguamate.models.auth import AuthData
from src.linguamate.services.auth import AuthService

router = Router(name=__name__)
auth_service: AuthService


@router.message(CommandStart())
@inject
async def start_handler(
        msg: Message,
        state: FSMContext,
):
    res = await auth_service.auth(AuthData(phone_number="+79527971960"))
    await msg.answer(f"Hello! I'm <b>LinguaMate</b>. {res}", parse_mode=ParseMode.HTML)
