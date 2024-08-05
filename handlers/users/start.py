from aiogram import types, F
from aiogram.filters import CommandStart
from loader import dp
from utils.db_api.api import create_user, fetch_questions, fetch_options, create_applicant, create_student
from aiogram.fsm.context import FSMContext
from states.reklama import Users
from keyboards.default.phonenum import phone
from keyboards.default.role import role
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.options import create_inline_keyboard

# Handler for the /start command
@dp.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(text="Assalomu alaykum, Ismingizni kiriting")
    await state.set_state(Users.first_name)

# Handler for receiving the first name
@dp.message(Users.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await state.set_state(Users.phone_number)
    text = "Raqamingizni kiriting"
    await message.answer(text=text, reply_markup=phone)

# Handler for receiving the phone number (when contact is shared)
@dp.message(Users.phone_number, F.contact)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await state.set_state(Users.age)
    text = "Yoshingizni kiriting!"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

# Handler for receiving the phone number (when text is provided instead of contact)
@dp.message(Users.phone_number)
async def handle_invalid_phone_number(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, haqiqiy telefon raqamini yuboring yoki kontaktingizni tanlang.", reply_markup=phone)

# Handler for receiving the age
@dp.message(Users.age)
async def age(message: types.Message, state: FSMContext):
    age_text = message.text
    if not age_text.isdigit():
        await message.answer("Iltimos, yoshingizni raqam sifatida kiriting.")
        await state.set_state(Users.age)
        return
    
    age = int(age_text)
    await state.update_data(age=age)
    await state.set_state(Users.role)
    await message.answer("Siz abiturientmisiz yoki student, meyudan birini tanlang", reply_markup=role)

# Handler for receiving the role
@dp.message(Users.role)
async def role_func(message: types.Message, state: FSMContext):
    role = message.text
    user_id = message.from_user.id

    data = await state.get_data()
    first_name = data.get('first_name')
    phone_number = data.get('phone_number')
    age = data.get('age')

    create_user(user_id=user_id, name=first_name, age=age, phonenumber=phone_number, role=role)

    questions = fetch_questions(role)
    options = fetch_options(role)

    # Store questions and options in state
    await state.update_data(questions=questions, options=options, current_question_index=0, score=0)

    if questions:
        first_question = questions[0]

        # Create a list of options for the current question
        filtered_options = [o for o in options if o['question'] == first_question['id']]

        keyboard = create_inline_keyboard(filtered_options)
        await message.answer(f"Savol: {first_question['text']}", reply_markup=keyboard)
    else:
        await message.answer("Savollar topilmadi.", reply_markup=ReplyKeyboardRemove())

    await state.set_state(Users.selected_option)

# Handler for handling option selection from inline keyboard
@dp.callback_query(F.data.startswith("option_"))
async def handle_option_selection(callback_query: types.CallbackQuery, state: FSMContext):
    option_id = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id

    data = await state.get_data()
    role = data.get('role')
    questions = data.get('questions')
    options = data.get('options')
    current_question_index = data.get('current_question_index', 0)
    user_responses = data.get('user_responses', {})
    score = data.get('score', 0)

    # Save the selected option
    if role == "student":
        create_student(user_id, option_id)
    else:
        create_applicant(user_id, option_id)

    # Record user response
    current_question = questions[current_question_index]
    user_responses[current_question['id']] = option_id
    await state.update_data(user_responses=user_responses)

    # Check if the selected option is correct
    correct_option_id = current_question.get('correct_option')
    if correct_option_id:
        correct_option = next((o for o in options if o['id'] == correct_option_id), None)
        if correct_option and correct_option['id'] == option_id:
            score += 1

    # Move to the next question
    current_question_index += 1
    if current_question_index >= len(questions):
        # Generate the final result message
        result_message = f"Javobingiz uchun rahmat!\nSizning natijangiz: {score} ball\n\n"
        for question_id, selected_option_id in user_responses.items():
            try:
                question = next(q for q in questions if q['id'] == question_id)
                option = next(o for o in options if o['id'] == selected_option_id)
                result_message += f"{question['text']}: {option['text']}\n"
            except StopIteration:
                pass
        await callback_query.message.edit_text(result_message)
        await state.clear()
        return

    # Handle the next question
    if current_question_index < len(questions):
        next_question = questions[current_question_index]

        # Create a list of options for the current question
        filtered_options = [o for o in options if o['question'] == next_question['id']]

        # Check if we have options to display
        if not filtered_options:
            await callback_query.message.edit_text("Bu savol uchun hech qanday variant mavjud emas.")
            await state.clear()
            return

        keyboard = create_inline_keyboard(filtered_options)
        await callback_query.message.edit_text(f"Savol: {next_question['text']}", reply_markup=keyboard)

        # Update state with the new index and score
        await state.update_data(current_question_index=current_question_index, score=score)

    await callback_query.answer()
