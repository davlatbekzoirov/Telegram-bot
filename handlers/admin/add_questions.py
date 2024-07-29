from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.questions import AddQuestions
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions
from filters.admin import IsBotAdminFilter
from data.config import ADMINS


@dp.message(Command("add_questions"), IsBotAdminFilter(ADMINS))
async def add_questions(message: types.Message, state: FSMContext):
	await message.answer("Savolni kiriting: ", reply_markup=cancel_markup)
	await state.set_state(AddQuestions.title)

@dp.message(AddQuestions.title)
async def add_questions(message: types.Message, state: FSMContext):
	await state.update_data({"title":message.text},)
	await message.answer("A javobni kiriting: ")
	await state.set_state(AddQuestions.a)

@dp.message(AddQuestions.a)
async def add_questions(message: types.Message, state: FSMContext):
	await state.update_data({"a":message.text},)
	await message.answer("B javobni kiriting: ")
	await state.set_state(AddQuestions.b)


@dp.message(AddQuestions.b)
async def add_questions(message: types.Message, state: FSMContext):
	await state.update_data({"b":message.text},)
	await message.answer("C javobni kiriting: ")
	await state.set_state(AddQuestions.c)


@dp.message(AddQuestions.c)
async def add_questions(message: types.Message, state: FSMContext):
	await state.update_data({"c":message.text},)
	await message.answer("To'g'ri javobni kiriting: ")
	await state.set_state(AddQuestions.right)

@dp.message(AddQuestions.right)
async def add_questions(message: types.Message, state: FSMContext):
	await state.update_data({"right":message.text},)
	await message.answer("Videoni ID sini kiriting: ")
	await state.set_state(AddQuestions.video_id)


@dp.message(AddQuestions.video_id)
async def add_questions(message: types.Message, state: FSMContext):
	data = await state.get_data()
	title = data.get("title")
	a = data.get("a")
	b = data.get("b")
	c = data.get("c")
	right = data.get("right")
	video_id = message.text

	# Create questions
	functions.create_question(text=title, a=a, b=b, c=c, right=right, video_id=video_id)
	await message.answer("Savol muvafaqiyatli qo'shildi")
	await state.clear()
