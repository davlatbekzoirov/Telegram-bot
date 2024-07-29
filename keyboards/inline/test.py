from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

test = CallbackData("test", "number")

def make_callback_data(number):
    return test.new(number=number)

def variant_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_number = 0
    for variant in ['a', 'b', 'c', 'd']:
        markup.insert(
            InlineKeyboardButton(
                text=variant,
                callback_data=make_callback_data(number=callback_number)
            )
        )
        callback_number += 1
    return markup

test = CallbackData("test", "number")

def make_callback_data(number):
    return test.new(number=number)

def variant_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_number = 0
    for variant in ['a', 'b', 'c', 'd']:
        markup.insert(
            InlineKeyboardButton(
                text=variant,
                callback_data=make_callback_data(number=callback_number)
            )
        )
        callback_number += 1
    return markup
