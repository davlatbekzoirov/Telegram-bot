from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from states.video import DelVideoState
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions



@dp.message(Command("del_video"), IsBotAdminFilter(ADMINS))
async def add_video(message: types.Message, state: FSMContext):
	await message.answer("Videoni ID sini kiriting: ", reply_markup=cancel_markup)
	await state.set_state(DelVideoState.id)

@dp.message(DelVideoState.id)
async def add_video(message: types.Message, state: FSMContext):
	functions.del_video(id=message.text)
	
	await message.answer("Video o'chirildi")
	await state.clear()

