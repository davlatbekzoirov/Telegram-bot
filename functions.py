from random import shuffle
from loader import bot, functions

def result_test(test_result):
	msg = ""
	num = 1
	for result in test_result:
		if result:
			msg += f"{num}) To'g'ri✅\n"
		else:
			msg += f"{num}) Xato🛑\n"

		num += 1
	return msg


async def send_admins_result(user_id, result, file_id):
	admins = functions.admins()
	user_data = functions.user_data(user_id)

	message = f"Foydalanuvchi: <a href='tg://user?id={user_id}'>{user_data[0][2]}</a>\n"
	message += f"Raqami: {user_data[0][3]}\n\n"
	message += result
	for admin_chat_id in admins:
		await bot.send_video(
			chat_id=admin_chat_id,
			video=file_id,
			caption=message,
			parse_mode="HTML",
			protect_content=True,
		)


def create_test(current_question, filter_questions):
	fq = filter_questions[current_question]
	index = [fq[2], fq[3], fq[4], fq[5]]
	index_copy  = index.copy()
	shuffle(index)

	msg = f"ID: {fq[0]}\n"
	msg += f"Savollar soni: {len(filter_questions)}\n\n"
	msg += f"{fq[1]}\n\n\n"
	msg += f"a)  {index[0]}\n"
	msg += f"b)  {index[1]}\n"
	msg += f"c)  {index[2]}\n"
	msg += f"d)  {index[3]}\n"

	return {'right':index.index(index_copy[-1]), 'message':msg}

# data = [(1, 'Hello', 'salom','test','xato','Salom')]
# print(create_test(0, data))

