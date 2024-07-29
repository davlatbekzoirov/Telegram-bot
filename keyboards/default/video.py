from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import functions


def all_buttons():
	markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	buttons = functions.all_buttons()
	
	for button in buttons:
		markup.insert(
			KeyboardButton(
				text=button[1]
			)
		)

	markup.row(
		KeyboardButton(
			text="🔝Asosiy sahifa"
		),
	)

	return markup


def detail_buttons_in(button_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	buttons = functions.detail_button_id(button_id=button_id)
	for button in buttons:
		markup.insert(
			KeyboardButton(
				text=button[1],
			)
		)
	if buttons:
		markup.row(
			KeyboardButton(
				text="🔙Orqaga"
			)
		)
		return markup

	return None

