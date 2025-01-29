from aiogram import Router
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.utils import unknown_error_handling, set_token, set_send_contact_state
from src.bot.msg_checks.checks import MsgCheckError, check_content_type
from src.bot.resourses.keyboards import main_ikb
from src.bot.resourses.strings import sres
from src.bot.resourses.strings.utils import esc_md
from src.bot.states import AuthStates, MainStates
from src.linguamate.exceptions import LinguaMateNotFoundError, LinguaMateAPIError, LinguaMateInvalidTokenError
from src.linguamate.models.auth import AuthData, SignupData
from src.linguamate.services.account import AccountService
from src.linguamate.services.auth import AuthService
from src.loggers import bot_logger

router = Router(name=__name__)
auth_service: AuthService
account_service: AccountService


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

        info = await account_service.get_info(response.token)
        main_markup = main_ikb(total_phrases=info.total_phrases, total_words=info.total_words)
        bot_logger.debug(f"Authorization was successful.")

        await set_token(state, response.token)
        await state.set_state(MainStates.Main)
        await msg.answer(text=sres.AUTH.SUCCESS.format(nickname=esc_md(response.nickname)),
                         reply_markup=main_markup, parse_mode=ParseMode.MARKDOWN)
    except (MsgCheckError, LinguaMateInvalidTokenError) as e:
        bot_logger.debug(e)
        await set_send_contact_state(msg, state)
    except (LinguaMateAPIError, Exception) as e:
        bot_logger.error(e)
        await unknown_error_handling(msg, state)
