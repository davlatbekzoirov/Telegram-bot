from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from states.video import DelButtonState
from keyboards.default.video import all_buttons
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions


# @dp.message(Command("del_button"), IsBotAdminFilter(ADMINS))
# async def del_button(message: types.Message, state: FSMContext):
# 	await message.answer("Tugma o'chirish🛑", reply_markup=cancel_markup)
# 	await message.answer("Tugmani nomni kiriting: ", reply_markup=all_buttons())
#     # await state.set_state(DelButtonState.name)
#     await state.set_state(DelButtonState.name)

@dp.message(Command("del_button"), IsBotAdminFilter(ADMINS))
async def del_button(message: types.Message, state: FSMContext):
    await message.answer("Tugma o'chirish🛑", reply_markup=cancel_markup)
    await message.answer("Tugmani nomni kiriting: ", reply_markup=all_buttons())
    await state.set_state(DelButtonState.name)

@dp.message(DelButtonState.name)
async def del_button_finish(message: types.Message, state: FSMContext):
    functions.button_delete(message.text)
    await message.answer("Tugma o'chirildi✅")
    await state.finish()
