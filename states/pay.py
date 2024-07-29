from aiogram.fsm.state import State, StatesGroup


class PayState(StatesGroup):
	card_number = State()
	date = State()
	allow = State()