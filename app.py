from loader import *
import asyncio, handlers, middlewares, utils
from utils.notify_admins import *
from utils.set_bot_commands import set_default_commands

async def main():
    dp.startup.register(on_startup_notify)
    dp.shutdown.register(on_shutdown_notify)

    await db.create()
    await db.create_table_users()
    await db.create_table_applicants()
    await db.create_table_applicant_questions()
    await db.create_table_applicant_options()
    await db.create_table_students()
    await db.create_table_student_questions()
    await db.create_table_student_options()

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
