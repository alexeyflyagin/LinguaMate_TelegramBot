from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot import sres

CONTACT_REQUEST_RM = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=sres.AUTH.BTN.SEND_CONTACT, request_contact=True)]],
    resize_keyboard=True, is_persistent=True,
)
