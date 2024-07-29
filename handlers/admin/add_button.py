from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.video import AddButtonState
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions
from filters.admin import IsBotAdminFilter
from data.config import ADMINS


@dp.message(Command("add_button"), IsBotAdminFilter(ADMINS))
async def enter_test(message: types.Message, state: FSMContext):
    await message.answer("Tugma yaratish➕\n\nTugmaga nom bering: ", reply_markup=cancel_markup)
    await state.set_state(AddButtonState.name)


@dp.message(AddButtonState.name)
async def answer_phone(message: types.Message, state: FSMContext):
    functions.button_create(message.text)
    await message.answer("Tugma muvafaqiyatli yaratildi✅")
    await state.clear()
