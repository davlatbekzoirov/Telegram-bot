from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from states.questions import DelQuestions
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions



@dp.message(Command("del_questions"), IsBotAdminFilter(ADMINS))
async def add_questions(message: types.Message, state: FSMContext):
	await message.answer("Savolni ID sini kiriting: ", reply_markup=cancel_markup)
	await state.set_state(DelQuestions.id)

@dp.message(DelQuestions.id)
async def add_questions(message: types.Message, state: FSMContext):
	functions.del_question(id=message.text)
	
	await message.answer("Savol muvafaqiyatli o'chirildi")
	await state.clear()
