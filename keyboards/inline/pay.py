from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel import cancel

pay_allow = InlineKeyboardButton(text="Tasdiqlash", callback_data="pay_allow")

allow_markup = InlineKeyboardMarkup()
allow_markup.add(pay_allow, cancel)