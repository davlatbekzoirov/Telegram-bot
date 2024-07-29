from aiogram import types, F
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.default.admin import admin_buttons
from keyboards.default.user import user_buttons, phone_markup, selection
from states.user import UserCreateState
from loader import dp, functions


@dp.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
	# Is user
	if not functions.user_data(message.chat.id):
		msg = f"Assalomu alaykum {message.chat.first_name}!\n\n"
		msg += "Bu bot orqali sifatli video darslarni sotib olish imkoniga ega bo'lasiz✅\n\n\n"
		msg += f"Shartlarga rozi bo'lsangiz **Ha✅** tugmasini bosing"
		await message.answer(msg, reply_markup=selection)
		# set phone
		await state.set_state(UserCreateState.selection)
	else:
		if int(message.chat.id) in functions.admins():
			await message.answer(f"Salom, {message.from_user.full_name}!\n\nAdmin✅", reply_markup=admin_buttons)
		else:
			await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=user_buttons)


@dp.message(F.text == "Ha✅", UserCreateState.selection)
async def UserCreateSelection(message: types.Message, state: FSMContext):
	msg = f"Ro'yxatdan o'tish uchun telefon raqamingizni kiriting\n\n"
	msg += "Raqamni +998******* shaklida yuboring"
	await message.answer(msg, reply_markup=phone_markup)
	# set phone
	await state.set_state(UserCreateState.phone)



@dp.message(UserCreateState.phone, F.text and F.contact)
async def UserCreatePhone(message: types.Message, state: FSMContext):
	phone = message.text if message.text else message.contact.phone_number
	if str(phone[1:]).isdigit() and len(phone) < 20:
		# Create user
		functions.user_create(
			chat_id=message.chat.id, 
			name=message.from_user.full_name,
			phone=phone)

		await message.answer(f"{message.chat.first_name} siz ro'yxatdan muvafaqiyatli o'tdingiz✅", reply_markup=user_buttons)
		# state finish
		await state.clear()
	else:
		await message.answer("No'to'gri telefon raqam❌\n\nQaytib urinib ko'ring:")