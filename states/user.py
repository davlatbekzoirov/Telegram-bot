from aiogram.fsm.state import State, StatesGroup



class UserCreateState(StatesGroup):
	selection = State()
	phone = State()