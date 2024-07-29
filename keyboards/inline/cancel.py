from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from loader import dp

# cancel = InlineKeyboardButton(text="To'xtatish🛑", callback_data="cancel")
# cancel_markup = InlineKeyboardMarkup()
# cancel_markup.add(cancel)

cancel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="To'xtatish🛑", callback_data="cancel")
        ]
    ]
)
@dp.callback_query(F.callback_data == 'cancel')
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await call.message.answer("To'xtatildi🛑")
