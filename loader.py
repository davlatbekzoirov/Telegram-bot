from aiogram import Bot, Dispatcher
from data import config
from utils.db_api.database import DataBase
from utils.db_api.functions import Functions

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

db = DataBase()
functions = Functions()