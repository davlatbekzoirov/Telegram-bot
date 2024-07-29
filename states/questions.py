from aiogram.fsm.state import State, StatesGroup


class AddQuestions(StatesGroup):
	title = State()
	a = State()
	b = State()
	c = State()
	right = State()
	video_id = State()


class DelQuestions(StatesGroup):
	id = State()