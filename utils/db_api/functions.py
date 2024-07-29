from .database import DataBase 
from data.config import ADMINS


db  = DataBase()


class Functions:
	def payment(self, chat_id):
		sql = """
			UPDATE users
			SET payment = 1
			WHERE chat_id = ?
		"""
		db.commit(sql, (chat_id,))

	def is_payment(self, chat_id):
		sql = """
			SELECT * FROM users
			WHERE chat_id = ? AND payment = 1;
		"""
		return db.commit(sql, (chat_id,), fetchall=True)

	def user_create(self, chat_id, name, phone):
		sql = f"""
			INSERT INTO users(chat_id, name, phone)
			VALUES (?, ?, ?)
		"""
		db.commit(sql, (chat_id, name, phone,))

	def user_data(self, chat_id):
		sql = """
			SELECT * FROM users
			WHERE chat_id = ?;
		"""
		return db.commit(sql, (chat_id,) ,fetchall=True)

	def admins(self):
		admins_list = ADMINS.copy()
		sql = """
			SELECT chat_id FROM users
			WHERE is_admin = 1;
		"""
		admins = db.commit(sql, fetchall=True)
		for admin in admins:
			admins_list.append(int(admin[0]))

		return admins_list

	def create_admin(self, chat_id):
		sql = """
			UPDATE users
			SET is_admin = 1, payment = 1
			WHERE chat_id = ?
		"""
		db.commit(sql, (chat_id,))

	def delete_admin(self, chat_id):
		sql = """
			UPDATE users
			SET is_admin = 0, payment = 0
			WHERE chat_id = ?
		"""
		db.commit(sql, (chat_id,))

	def videos_create(self, file_id, caption, button_in_id):
		sql = f"""
			INSERT INTO videos(file_id, caption, button_in_id)
			VALUES (?, ?, ?)
		"""
		db.commit(sql, (file_id, caption, button_in_id,))

	def del_video(self, id):
		sql = """
			DELETE FROM videos
			WHERE id = ?
		"""
		db.commit(sql, (id,))

	def video_filter(self, button_in_id):
		sql = f"""
			SELECT * FROM  videos
			WHERE button_in_id = ?;
		"""
		return db.commit(sql, (button_in_id,), fetchall=True)


	def button_create(self, name):
		sql = f"""
			INSERT INTO buttons(name)
			VALUES (?)
		"""
		db.commit(sql, (name,))

	def button_delete(self, name):
		sql = f"""
			DELETE FROM buttons
			WHERE name = ?;
		"""
		db.commit(sql, (name,))


	def filter_button(self, name):
		sql = f"""
			SELECT * FROM buttons
			WHERE name = ?;
		"""

		return db.commit(sql, (name,), fetchall=True)

	def all_buttons(self):
		sql = """
			SELECT * FROM buttons;
		"""

		return db.commit(sql, fetchall=True)

	def button_in_create(self, name, button_id):
		sql = f"""
			INSERT INTO buttons_in(name, button_id)
			VALUES (?, ?)
		"""

		db.commit(sql, (name, button_id,))

	def filter_button_in(self, name, button_id):
		sql = f"""
			SELECT * FROM buttons_in
			WHERE name = ? AND button_id = ?;
		"""

		return db.commit(sql, (name, button_id,), fetchall=True)

	def detail_button_id(self, button_id):
		sql = f"""
			SELECT * FROM buttons_in
			WHERE button_id = ?;
		"""

		return db.commit(sql, (button_id,), fetchall=True)

	def button_id_filter_by_name(self, name):
		sql = f"""
			SELECT * FROM buttons_in
			WHERE name = ?;
		"""

		return db.commit(sql, (name,), fetchall=True)


	def delete_button_in(self, name):
		sql = f"""
			DELETE FROM buttons_in
			WHERE name = ?;
		"""
		db.commit(sql, (name,))

	def filter_questions(self, video_id):
		sql = """
			SELECT * FROM questions
			WHERE video_id = ?;
		"""
		return db.commit(sql, (video_id,), fetchall=True)

	def create_question(self, text, a, b, c, right, video_id):
		sql = """
			INSERT INTO questions(text, a, b, c, right, video_id)
			VALUES (?, ?, ?, ?, ?, ?)
		"""
		db.commit(sql, (text, a, b, c, right, video_id))

	def del_question(self, id):
		sql = """
			DELETE FROM questions
			WHERE id = ?
		"""
		db.commit(sql, (id,))

	def create_result(self, result, chat_id, video_id):
		sql = """
			INSERT INTO results(result, chat_id, video_id)
			VALUES (?, ?, ?)
		"""
		db.commit(sql, (result, chat_id, video_id,))

	def filter_result(self, chat_id, video_id):
		sql = """
			SELECT * FROM results
			WHERE chat_id = ? AND video_id = ?;
		"""
		return db.commit(sql, (chat_id, video_id,), fetchall=True)