import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import test_performance_menu_button
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import performance, end_test, grammar_test
from bot.dispatcher import dp


def get_test(chat_id: str):
    test = json.loads(requests.get(url=f'http://127.0.0.1:8000/api/tests/get-test/{chat_id}/').content)
    try:
        if test['question_number']:
            return True, test
    except KeyError:
        return False, test


@dp.message_handler(Text(equals=[grammar_test]))
async def test_performance_function(msg: types.Message, state: FSMContext):
    ftest, test = get_test(str(msg.from_user.id))
    if not ftest:
            await msg.answer(text=f"""
You have completed all the test

Number of tests: {test['number_of_questions']}
Number of correct answers: {test['correct_questions']}
Number of wrong answers: {test['wrong_questions']}""")
    else:
        await state.set_state('test_performance')
        await msg.answer(text=f"""
{test['question_number']} - question

{test['question']}""", reply_markup=await test_performance_menu_button(test))


@dp.message_handler(Text(end_test), state="test_performance")
async def back_main_menu_function_3(msg: types.Message, state: FSMContext):
    await state.finish()
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    test = json.loads(requests.get(url=f'http://127.0.0.1:8000/api/tests/end-test/{msg.from_user.id}/').content)
    if tg_user['language'] == 'uz':
        await msg.answer(text=f"""
Siz testni yakunladingiz

Testlar soni: {test['number_of_questions']}
To'g'ri javoblar soni: {test['correct_questions']}
Noto'g'ri javoblar soni: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
    elif tg_user['language'] == 'en':
        await msg.answer(text=f"""
You have completed all the test

Number of tests: {test['number_of_questions']}
Number of correct answers: {test['correct_questions']}
Number of wrong answers: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
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
        elif tg_user['language'] == 'en':
            await msg.answer(text=f"""
You have completed all the test

Number of tests: {test['number_of_questions']}
Number of correct answers: {test['correct_questions']}
Number of wrong answers: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"""
Вы прошли все испытания

Количество тестов: {test['number_of_questions']}
Количество правильных ответов: {test['correct_questions']}
Количество неправильных ответов: {test['wrong_questions']}""", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await state.set_state('test_performance')
        await msg.answer(text=f"""
{answer['message']}

{test['question_number']} - question

{test['question']}
""", reply_markup=await test_performance_menu_button(test))
