from aiogram import types, F
from keyboards.default.video import all_buttons
from loader import dp


@dp.message(F.text == '📹Video darslar')
async def video(message: types.Message):
	await message.answer("📹Video darslar", reply_markup=all_buttons())