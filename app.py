from aiogram import Dispatcher
from loader import *
import asyncio, handlers, middlewares, utils
from utils.notify_admins import *
from utils.set_bot_commands import set_default_commands

async def main():
    dp.startup.register(on_startup_notify)
    dp.shutdown.register(on_shutdown_notify)
    try:db.create_table_users()
    except Exception as e:print(f"User:\n {e}")
    try:db.create_table_candidates()
    except Exception as e:print(f"Candidates:\n {e}")
    try:db.create_table_ratings()
    except Exception as e:print(f"Rating:\n {e}")
    await set_default_commands(bot)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())