from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.video import DelButtonInState
from keyboards.default.video import all_buttons, detail_buttons_in
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions
from filters.admin import IsBotAdminFilter
from data.config import ADMINS

@dp.message(Command("del_button_in"), IsBotAdminFilter(ADMINS))
async def del_button_in(message: types.Message, state: FSMContext):
	await message.answer("Ichki tugma o'chirish🛑", reply_markup=cancel_markup)
	await message.answer("Tugmani tanlang: ", reply_markup=all_buttons())
	await state.set_state(DelButtonInState.name_in)


@dp.message(DelButtonInState.name_in)
async def button_get_id(message: types.Message, state: FSMContext):

	filter_button = functions.filter_button(message.text)
	if filter_button:
		detail_buttons = detail_buttons_in(filter_button[0][0])
		if detail_buttons_in:
			await state.set_state(DelButtonInState.name)
			await message.answer(
				"Ichki tugmani tanglang: ",
				reply_markup=detail_buttons
			)
		else:
			await message.answer("Ichki tugmalar hali mavjud emas❌")
			await state.clear()

	else:
		await message.answer("Bunday tugma mavjud emas❌")

@dp.message(DelButtonInState.name)
async def get_video(message: types.Message, state: FSMContext):
    functions.delete_button_in(message.text)

    await message.answer("Ichki tugma o'chirildi✅")
    await state.clear()
