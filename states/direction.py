from aiogram.fsm.state import State, StatesGroup



class DirectionState(StatesGroup):
	button_in = State()
	questions = State()
	test = State()