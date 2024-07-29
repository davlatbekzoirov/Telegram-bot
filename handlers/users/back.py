from aiogram import types, F
from aiogram.fsm.context import FSMContext
from keyboards.default.user import user_buttons
from keyboards.default.video import all_buttons
from loader import dp, functions


@dp.message(F.text=="🔝Asosiy sahifa")
async def bot_main_page(message: types.Message, state: FSMContext):
	await message.answer(message.text, reply_markup=user_buttons)

	await state.clear()


@dp.message(F.text=="🔙Orqaga" )
async def bot_button_in_page(message: types.Message, state: FSMContext):
	await message.answer(message.text, reply_markup=all_buttons())

	await state.clear()