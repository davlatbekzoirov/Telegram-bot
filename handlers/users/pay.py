from aiogram import types, F
from aiogram.types.successful_payment import SuccessfulPayment
from loader import dp, bot, functions
from data import config
from aiogram.filters.base import Filter
# ContentTypesFilter
@dp.message(F.text == "💰To'lov")
async def bot_pay(message: types.Message):
	# Click up
    await bot.send_invoice(
    	message.chat.id, 
    	title='Click orqali to\'lov',
		description='Videolarni sotib olish uchun clickdagi hisobingizni kiriting',
		provider_token=config.CLICK_PAYMENT_TOKEN,
		currency='uzs',
		photo_url='https://play-lh.googleusercontent.com/ooPDKqNFLUMqM497zPREAkjfRdkgA209cfRdYNVmjLC6a8KwC6oZDQ_7YqLyWEa9wWg',
		photo_height=512,  # !=0/None or picture won't be shown
		photo_width=512,
		photo_size=512,
		# is_flexible=True,  # True If you need to set up Shipping Fee
		prices=[types.LabeledPrice(label='Narxi', amount=config.VIDEO_PRICES)],
		start_parameter='time-machine-example',
		payload='live-invonce-payload')

    # Payme
    await bot.send_invoice(
    	message.chat.id, 
    	title='Payme orqali to\'lov',
		description='Videolarni sotib olish uchun paymedagi hisobingizni kiriting',
		provider_token=config.PAYME_PAYMENT_TOKEN,
		currency='uzs',
		photo_url='https://synthesis.uz/wp-content/uploads/2022/01/payme-1920x1080-1.jpg',
		photo_height=512,  # !=0/None or picture won't be shown
		photo_width=512,
		photo_size=512,
		# is_flexible=True,  # True If you need to set up Shipping Fee
		prices=[types.LabeledPrice(label='Narxi', amount=config.VIDEO_PRICES)],
		start_parameter='time-machine-example',
		payload='live-invonce-payload')

# /to'lov_buyrug'iga javob berish
@dp.pre_checkout_query()
async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)

# Payment confirmation
# @dp.message(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    await message.answer("To'lov muvaffaqiyatli amalga oshirildi!")

    # Open videos
    functions.payment(message.chat.id)
