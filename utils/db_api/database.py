import sqlite3




class DataBase:
	connect = sqlite3.connect("database.db")
	cursor = connect.cursor()

	
	def commit(self, cls, params=(), fetchall=False):
		execute = self.cursor.execute(cls, params)
		
		self.connect.commit()
		if fetchall:
			return execute.fetchall()

		# self.connect.close()
