from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline_keyboard(options):
    keyboard = InlineKeyboardBuilder()
    for option in options:
        button = InlineKeyboardButton(text=option["text"], callback_data=f"option_{option['id']}")
        keyboard.add(button)
    return keyboard.as_markup()