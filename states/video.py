from aiogram.fsm.state import State, StatesGroup



class AddVideoState(StatesGroup):
	button_id = State()
	button_in_id = State()
	video = State()
	caption = State()


class DelVideoState(StatesGroup):
	id = State()


class AddButtonState(StatesGroup):
    name = State()



class DelButtonState(StatesGroup):
    name = State()


class AddButtonInState(StatesGroup):
    name_in = State()
    name = State()


class DelButtonInState(StatesGroup):
    name_in = State()
    name = State()


class AddAdminState(StatesGroup):
	chat_id = State()


class DelAdminState(StatesGroup):
	chat_id = State()