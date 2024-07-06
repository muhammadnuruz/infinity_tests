import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import test_performance_menu_button
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import performance, end_test, performance_ru, end_test_ru
from bot.dispatcher import dp


def get_test(chat_id: str):
    test = json.loads(requests.get(url=f'http://127.0.0.1:8000/api/tests/get-test/{chat_id}/').content)
    try:
        if test['question_number']:
            return True, test
    except KeyError:
        return False, test


@dp.message_handler(Text(equals=[performance, performance_ru]))
async def test_performance_function(msg: types.Message, state: FSMContext):
    ftest, test = get_test(str(msg.from_user.id))
    if not ftest:
        if msg.text == performance:
            await msg.answer(text=f"""
Siz barcha testni yakunladingiz

Testlar soni: {test['number_of_questions']}
To'g'ri javoblar soni: {test['correct_questions']}
Noto'g'ri javoblar soni: {test['wrong_questions']}""")
        else:
            await msg.answer(text=f"""
Вы прошли все испытания

Количество тестов: {test['number_of_questions']}
Количество правильных ответов: {test['correct_questions']}
Количество неправильных ответов: {test['wrong_questions']}""")
    else:
        await state.set_state('test_performance')
        text = "savol"
        if msg.text == performance_ru:
            text = 'вопрос'
        await msg.answer(text=f"""
{test['question_number']} - {text}

{test['question']}""", reply_markup=await test_performance_menu_button(test, msg.from_user.id))


@dp.message_handler(Text(equals=[end_test, end_test_ru]), state="test_performance")
async def back_main_menu_function_3(msg: types.Message, state: FSMContext):
    await state.finish()
    test = json.loads(requests.get(url=f'http://127.0.0.1:8000/api/tests/end-test/{msg.from_user.id}/').content)
    if msg.text == end_test:
        await msg.answer(text=f"""
Siz testni yakunladingiz

Testlar soni: {test['number_of_questions']}
To'g'ri javoblar soni: {test['correct_questions']}
Noto'g'ri javoblar soni: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text=f"""
Вы прошли испытания

Количество тестов: {test['number_of_questions']}
Количество правильных ответов: {test['correct_questions']}
Количество неправильных ответов: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(state="test_performance")
async def test_performance_function_2(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    answer = json.loads(
        requests.post(url=f'http://127.0.0.1:8000/api/tests/submit-answer/{str(msg.from_user.id)}/',
                      data={'answer': msg.text}).content)
    ftest, test = get_test(str(msg.from_user.id))
    if not ftest:
        await state.finish()
        if tg_user['language'] == 'uz':
            await msg.answer(text=f"""
Siz barcha testni yakunladingiz

Testlar soni: {test['number_of_questions']}
To'g'ri javoblar soni: {test['correct_questions']}
Noto'g'ri javoblar soni: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"""
Вы прошли все испытания

Количество тестов: {test['number_of_questions']}
Количество правильных ответов: {test['correct_questions']}
Количество неправильных ответов: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await state.set_state('test_performance')
        text = "savol"
        if tg_user['language'] == 'ru':
            text = 'вопрос'
        await msg.answer(text=f"""
{answer['message']}

{test['question_number']} - {text}

{test['question']}
""", reply_markup=await test_performance_menu_button(test, msg.from_user.id))
