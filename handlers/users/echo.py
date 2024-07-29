from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.default.video import all_buttons, detail_buttons_in
from keyboards.default.user import test_markup
from states.direction import DirectionState
from keyboards.inline.test import test, variant_buttons, make_callback_data
from keyboards.default.user import retry_markup, user_buttons, next_markup
from functions import create_test, result_test, send_admins_result
from loader import dp, bot, functions


# Echo bot
@dp.message()
async def bot_echo(message: types.Message, state: FSMContext):
	button_data = functions.filter_button(message.text)
	if button_data:
		buttons_in = detail_buttons_in(button_data[0][0])
		await message.answer(message.text, reply_markup=buttons_in)
		# State
		await state.set_state(DirectionState.button_in)
		await state.update_data(
			{"button_id": button_data[0][0], "current_question":0, "buttons_in":buttons_in},
		)

@dp.message(DirectionState.button_in)
async def send_videos(message: types.Message, state: FSMContext, next_video_index: int = None):
	if functions.is_payment(chat_id=message.chat.id):
		data = await state.get_data()
		button_id = data.get("button_id")

		button_in_data = functions.filter_button_in(message.text, button_id)
		if button_in_data:
			# Video filter button_in_id
			video_filt = functions.video_filter(button_in_id=button_in_data[0][0])
			video_filter: list = [video_filt[next_video_index]] if next_video_index else video_filt[::]
			if video_filter:
				# Send videos
				index = 0
				video_id = 0
				video_file_id = ""
				for video in video_filter:
					filter_result = functions.filter_result(message.chat.id, video[0])
					video_index = video_filter.index(video)
					if filter_result or index == video_index:
						await bot.send_video(
							chat_id=message.chat.id,
							video=video[1],
							caption=f"ID: {video[0]}\n\n" + video[2],
							protect_content=True,
							reply_markup=test_markup
						)
						video_id = video[0]
						video_file_id = video[1]
						if filter_result:
							index = video_index+1

				await state.update_data({
					"video_id":video_id,
					"video":video_file_id, 
					"video_index":video_index-1,
					"last_video":True if index+1==len(video_filt) else False,
					"button_in_text":message.text
				})
				await state.set_state(DirectionState.questions)
			else:
				await message.answer("Bu bo'limda hali video mavjud emas", reply_markup=all_buttons())
		else:
			await message.answer("Bosh menu", reply_markup=all_buttons())
			await state.clear()
	else:
		await message.answer("📹Video darslar ni ko'rish uchun 💰To'lov qiling", reply_markup=user_buttons)
		await state.clear()

@dp.message(DirectionState.questions, text="Testlar❓")
async def questions_state(message: types.Message, state: FSMContext):
	data = await state.get_data()
	current_question = data.get("current_question")
	video_id = data.get("video_id")
	results = data.get("results")
	video = data.get("video")
	last_video = data.get("last_video")
	buttons_in = data.get("buttons_in")

	filter_questions = functions.filter_questions(video_id=video_id)
	if current_question+1 <= len(filter_questions):
		test = create_test(current_question, filter_questions)
		await message.answer(test['message'], protect_content=True, reply_markup=variant_buttons())
		await state.update_data({
				"current_question": current_question+1, 
				"right":test['right']
			})
		await state.set_state(DirectionState.test)
	elif len(filter_questions) == 0:
		await message.answer("Bu videoda hali testlar mavjud emas")
		await state.clear()
	else:
		percentage = round((results.count(1) / len(filter_questions)) * 100, 2)
		if percentage > 80:
			functions.create_result(percentage, message.chat.id, video_id)
			# Help text
			if not last_video:
				await message.answer("Keyingi videolarga o'tish uchun Keyingi video➡️ ni bosing", reply_markup=next_markup)
			else:
				await message.answer("Siz joriy bo'limdagi videolarni tugatdingiz🥳")
			await message.answer("Siz test o'tdingiz✅")
		else:
			await message.answer("Siz testdan o'ta olmadingiz❌", reply_markup=retry_markup)

		test = result_test(results) + f'\n\nNatija: {percentage}%'
		await message.answer(test)
		await send_admins_result(message.chat.id, test, video)


@dp.callback_query(test.filter(), DirectionState.test)	
async def test_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
	data = await state.get_data()
	results = data.get("results")
	right = data.get("right")
	variant_number = callback_data.get("number")

	if results:
		results.append(1 if int(variant_number) == int(right) else 0)
	else:
		results = [1 if int(variant_number) == int(right) else 0]
	
	await state.update_data({"results": results})
	await questions_state(call.message, state)


@dp.message(DirectionState)
async def stop_state(message: types.Message, state: FSMContext):
	data = await state.get_data()
	button_in_text = data.get("button_in_text")
	video_index = data.get("video_index")
	last_video = data.get("last_video")

	await state.update_data({"current_question": 0, "results":[]})

	if message.text == "Qayta urinish🔄":
		await questions_state(message, state)
	elif message.text == "Keyingi video➡️" and not last_video:
		message.text = button_in_text
		await send_videos(message, state, video_index)
	else: # message.text != "Testlar❓":
		await state.clear()
		await message.reply(f"Siz test yechish jarayonini to'xtatdingiz\n\n**{message.text}** ni qaytib yozing")
	