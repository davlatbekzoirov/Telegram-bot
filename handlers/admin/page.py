from aiogram import types, F
from keyboards.default.user import user_buttons
from loader import dp, functions



@dp.message(F.text == "👤Foydalanuvchi")
async def bot_user_page(message: types.Message):
	await message.answer("👤Foydalanuvchi", reply_markup=user_buttons)