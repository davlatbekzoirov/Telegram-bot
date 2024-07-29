from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤Foydalanuvchi")],
        [KeyboardButton(text="➕add admin")],
        [KeyboardButton(text="➖del admin")],
        [KeyboardButton(text="/add_button")],
        [KeyboardButton(text="/del_button")],
        [KeyboardButton(text="/add_button_in")],
        [KeyboardButton(text="/del_button_in")],
        [KeyboardButton(text="/add_video")],
        [KeyboardButton(text="/del_video")],
        [KeyboardButton(text="/add_questions")],
        [KeyboardButton(text="/del_questions")]
    ],
    resize_keyboard=True
)