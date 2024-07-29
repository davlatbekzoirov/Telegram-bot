from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.video import AddAdminState, DelAdminState
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions
from filters.admin import IsBotAdminFilter
from data.config import ADMINS

@dp.message(F.text == "➕add admin", IsBotAdminFilter(ADMINS))
async def add_video(message: types.Message, state: FSMContext):
    await message.answer("Admin `chat_id` sini kiritng: ", reply_markup=cancel_markup)
    await state.set_state(AddAdminState.chat_id)


@dp.message(AddAdminState.chat_id)
async def add_video(message: types.Message, state: FSMContext):
	functions.create_admin(message.text)

	await message.answer("Admin muvafaqiyatli qo'shildi✅")
	await state.clear()



# ------------------ DELETE ADMIN ---------------------
@dp.message(F.text == "➖del admin", IsBotAdminFilter(ADMINS))
async def add_video(message: types.Message, state: FSMContext):
    await message.answer("Admin `chat_id` sini kiritng: ", reply_markup=cancel_markup)
    await state.set_state(DelAdminState.chat_id)


@dp.message(DelAdminState.chat_id)
async def add_video(message: types.Message, state: FSMContext):
	functions.delete_admin(message.text)

	await message.answer("Admin o'chirildi🛑")
	await state.clear()
