from aiogram import Router
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot import sres
from src.bot.handlers.utils import unknown_error_handling, set_token, send_contact_request
from src.bot.msg_checks.checks import MsgCheckError, check_content_type
from src.bot.states import AuthStates, MainStates
from src.linguamate.exceptions import LinguaMateNotFoundError, LinguaMateAPIError
from src.linguamate.models.auth import AuthData, SignupData
from src.linguamate.services.auth import AuthService
from src.loggers import bot_logger

router = Router(name=__name__)
auth_service: AuthService


@router.message(AuthStates.SendContact)
async def send_contact__handler(msg: Message, state: FSMContext):
    try:
        check_content_type(msg, ContentType.CONTACT)

        auth_data = AuthData(phone_number=msg.contact.phone_number)
        try:
            response = await auth_service.auth(auth_data)
        except LinguaMateNotFoundError:
            signup_data = SignupData(nickname=msg.contact.first_name, phone_number=msg.contact.phone_number)
            await auth_service.signup(signup_data)
            bot_logger.debug(
                f"The account (phone_number='{auth_data.phone_number}') was not found. A new account has been created.")
            response = await auth_service.auth(auth_data)

        bot_logger.debug(f"Authorization was successful.")
        await set_token(state, response.token)
        await state.set_state(MainStates.Main)
        await msg.answer(text=sres.AUTH.SUCCESS, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)
    except MsgCheckError as e:
        await send_contact_request(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)
