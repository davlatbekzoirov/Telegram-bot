from utils.db_api.tables import (
	USERS_TABLE, 
	VIDOES, 
	BUTTONS, 
	BUTTONS_IN,
	QUESTIONS,
	RESULTS
)
from loader import db


db.commit(USERS_TABLE)
print("CREATE USERS")

db.commit(BUTTONS)
print("CREATE BUTTONS")

db.commit(BUTTONS_IN)
print("CREATE BUTTONS_IN")

db.commit(VIDOES)
print("CREATE VIDOES")

db.commit(QUESTIONS)
print("CREATE QUESTIONS")

db.commit(RESULTS)
print("CREATE RESULTS")