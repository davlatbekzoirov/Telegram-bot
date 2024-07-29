from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.video import AddButtonInState
from keyboards.default.video import all_buttons
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions
from filters.admin import IsBotAdminFilter
from data.config import ADMINS


@dp.message(Command("add_button_in"), IsBotAdminFilter(ADMINS))
async def button_id_create(message: types.Message, state: FSMContext):
	await message.answer("Ichki tugma yaratish➕", reply_markup=cancel_markup)
	await message.answer("Tugmani tanlang: ", reply_markup=all_buttons())
	await state.set_state(AddButtonInState.name_in)


@dp.message(AddButtonInState.name_in)
async def button_get_id(message: types.Message, state: FSMContext):
	filter_button = functions.filter_button(message.text)
	if filter_button:
		await state.update_data(
			{"button_id": filter_button[0][0]}
		)
		await state.set_state(AddButtonInState.name)
		await message.answer("Ichki tugmaga nom bering: ")
	else:
		await message.answer("Bunday tugma mavjud emas❌")


@dp.message(AddButtonInState.name)
async def button_id_finish(message: types.Message, state: FSMContext):
	data = await state.get_data()
	button_id = data.get("button_id")

	functions.button_in_create(message.text, button_id)

	await message.answer("Muvafaqiyatli yaratildi✅")
	await state.clear()