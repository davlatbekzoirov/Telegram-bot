from aiogram import types, F
from aiogram.filters import CommandStart
from loader import dp, db
from aiogram.fsm.context import FSMContext
from states.reklama import Users
from keyboards.default.phonenum import phone
from keyboards.default.role import role
from aiogram.types import ReplyKeyboardRemove
from handlers.errors.error_handler import errors_handler
import asyncpg

@dp.message(CommandStart())
async def start_command(message: types.Message, state:FSMContext):
    await message.answer(text="Assalomu alaykum, Ismingizni kiriting")
    await state.set_state(Users.first_name)

@dp.message(Users.first_name)
async def get_first_name(message:types.Message,state:FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)

    await state.set_state(Users.phone_number)
    text = f"Raqamingizni kiriting"
    await message.answer(text=text, reply_markup=phone)

@dp.message(Users.phone_number, F.contact)
async def get_phone_number(message:types.Message,state:FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)

    await state.set_state(Users.age)
    text = f"Yoshingizni kiriting!"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

@dp.message(Users.phone_number)
async def get_phone_number(message:types.Message,state:FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)

    await state.set_state(Users.phone_number)
    text = f"Raqamingizni kiriting"
    await message.answer(text=text, reply_markup=phone)

@dp.message(Users.age)
async def age(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)

    await state.set_state(Users.role)
    await message.answer("Siz abiturientmisiz yoki student, meyudan birini tanlang", reply_markup=role)
        
@dp.message(Users.role)
async def role_func(message: types.Message, state: FSMContext):
    role = message.text
    id = message.from_user.id

    data = await state.get_data()
    first_name = data.get('first_name')
    phone_number = data.get('phone_number')
    age = data.get('age')
    try:
        user = await db.add_user(
            name=first_name,
            age=age,
            phone_number=phone_number,
            role=role
        )
    except asyncpg.exceptions.UniqueViolationError:
        pass    

    text = f"Siz muvaffaqiyatli tarzda ro'yhatdan o'tdingiz🎉"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.clear()