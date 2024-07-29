from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📹Video darslar")
        ],
        [
            KeyboardButton(text="💰To'lov")
        ]
    ],
    resize_keyboard=True
)

back = KeyboardButton(text="🔙Orqaga")

test_markup = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Testlar❓")
        ],
        [
            back
        ]
    ],
    resize_keyboard=True
)


phone_markup = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="📱Telefon raqam", request_contact=True)]
    ],
    resize_keyboard=True
)

selection = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text="Ha✅")]
    ],
    resize_keyboard=True
)


retry_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Qayta urinish🔄")],
        [back]
    ],
    resize_keyboard=True
)


next_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Keyingi video➡️")],
        [back]
    ],
    resize_keyboard=True
)