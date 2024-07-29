from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.video import AddVideoState
from keyboards.default.video import all_buttons, detail_buttons_in
from keyboards.inline.cancel import cancel_markup
from loader import dp, functions
from filters.admin import IsBotAdminFilter
from data.config import ADMINS


@dp.message(Command("add_video"), IsBotAdminFilter(ADMINS))
async def add_video(message: types.Message, state: FSMContext):
    await message.answer("Video qo'shish➕", reply_markup=cancel_markup)
    await message.answer("Tugmani tanlang: ", reply_markup=all_buttons())
    await state.set_state(AddVideoState.button_id)


@dp.message(AddVideoState.button_id)
async def get_button_id(message: types.Message, state: FSMContext):
    filter_button = functions.filter_button(message.text)
    if filter_button:
        detail_button_in = detail_buttons_in(filter_button[0][0])
        if detail_button_in:
            await state.update_data(
                {"button_id": filter_button[0][0]}
            )
            await AddVideoState.button_in_id.set()
            await message.answer("Ichki tugmani tanglang: ", reply_markup=detail_button_in)
        else:
            await message.answer("Ichki tugmalar mavjud emas❌")
            await state.clear()

    else:
        await message.answer("Bunday tugma mavjud emas❌")


@dp.message(AddVideoState.button_in_id)
async def get_button_in_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    button_id = data.get("button_id")

    filter_button_in = functions.filter_button_in(message.text, button_id)
    if filter_button_in:
        await state.update_data(
            {"button_in_id": filter_button_in[0][0]}
        )
        await state.set_state(AddVideoState.video)
        await message.answer("Videoni yuboring: ")
    else:
        await message.answer("Bunday ichki tugma mavjud emas❌")


@dp.message(AddVideoState.video, F.video)
async def get_video(message: types.Message, state: FSMContext):
    await state.update_data(
        {"video": message.video.file_id}
    )
    await message.answer("Matn jo'nating: ")
    await state.set_state(AddVideoState.caption)


@dp.message(AddVideoState.caption)
async def get_caption_and_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    video = data.get("video")
    button_in_id = data.get("button_in_id")

    video_create = functions.videos_create(
        file_id=video,
        caption=message.text,
        button_in_id=button_in_id
    )

    await message.answer("Video muvafaqiyatli qo'shildi✅")
    await state.clear()
