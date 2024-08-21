import json
import random

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from bot.buttons.inline_buttons import category_button, test_button, channel_button
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import end_test, vocabulary_test
from bot.dispatcher import dp

CHANNEL_ID = '-1002232778333'


async def is_subscribed(user_id: int) -> bool:
    chat_member = await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    return chat_member.status in ['member', 'administrator', 'creator']


async def get_test(category_id: str, words: list):
    category = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/categories/detail/{category_id}").content)
    used_words = set(words)
    while True:
        num = random.randint(0, category['words_count'] - 1)
        word_id = category['words'][num]['id']
        if word_id not in used_words:
            break
    word = category['words'][num]
    word = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/words/detail/{word['id']}").content)
    return word, category


@dp.message_handler(Text(equals=[vocabulary_test]))
async def test_performance_function(msg: types.Message, state: FSMContext):
    await state.set_state('choice_category')
    await msg.answer(text="Select a category 👇", reply_markup=await category_button(lang='en'))
    message = await msg.answer(text="Lets go!", reply_markup=ReplyKeyboardRemove())
    await message.delete()


@dp.callback_query_handler(state='choice_category')
async def test_performance_function_2(call: types.CallbackQuery, state: FSMContext):
    word, category = await get_test(call.data, words=[])
    async with state.proxy() as data:
        data['words_count'] = category['words_count']
        data['word_number'] = 1
        data['words'] = [word['word']['id']]
        data['correct_answers'] = 0
        data['correct_answer'] = word['word']['name']
        data['category_id'] = category['id']
    await call.message.delete()
    await call.message.answer_photo(photo=open(word['word']['image'][22:], 'rb'),
                                    caption=f"Test 1\n\nFind the name of this {str.lower(category['name'])} 👆",
                                    reply_markup=await test_button(words=word))
    await state.set_state('test_performance')


@dp.callback_query_handler(Text(end_test), state="test_performance")
async def test_performance_function_3(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.delete()
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
        if await is_subscribed(call.from_user.id):
            if tg_user['language'] == 'uz':
                await call.message.answer(
                    text=f"Siz testni yakunladingiz 🎉\n\nSiz to'plagan ball: {int(data['correct_answers'] / (data['word_number'] - 1) * 100)}",
                    reply_markup=await main_menu_buttons(call.from_user.id))
            elif tg_user['language'] == 'ru':
                await call.message.answer(
                    text=f"Вы прошли тест 🎉\n\nВаша оценка: {int(data['correct_answers'] / (data['word_number'] - 1) * 100)}",
                    reply_markup=await main_menu_buttons(call.from_user.id)
                )
            else:
                await call.message.answer(
                    text=f"You have completed the test 🎉\n\nYour score is: {int(data['correct_answers'] / (data['word_number'] - 1) * 100)}",
                    reply_markup=await main_menu_buttons(call.from_user.id)
                )
            await state.finish()
        else:
            if tg_user['language'] == 'uz':
                await call.message.answer(text="Natijangizni bilish uchun bizni kanalga obuna bo'ling 😊",
                                          reply_markup=await channel_button())
            elif tg_user['language'] == 'ru':
                await call.message.answer(text="Подпишитесь на наш канал, чтобы узнать свой результат 😊",
                                          reply_markup=await channel_button())
            else:
                await call.message.answer(text="Subscribe to our channel to know your result 😊",
                                          reply_markup=await channel_button())


@dp.callback_query_handler(state="test_performance")
async def test_performance_function_4(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == data['correct_answer']:
            data['correct_answers'] = data['correct_answers'] + 1
        if data['word_number'] == data['words_count']:
            tg_user = json.loads(
                requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
            if await is_subscribed(call.from_user.id):
                if tg_user['language'] == 'uz':
                    await call.message.answer(
                        text=f"Siz barcha testni tugatdingiz 🎉\n\nSiz to'plagan ball: {int(data['correct_answers'] / data['words_count'] * 100)}",
                        reply_markup=await main_menu_buttons(call.from_user.id))
                elif tg_user['language'] == 'ru':
                    await call.message.answer(
                        text=f"Вы прошли весь тест 🎉\n\nВаша оценка: {int(data['correct_answers'] / data['words_count'] * 100)}",
                        reply_markup=await main_menu_buttons(call.from_user.id)
                    )
                else:
                    await call.message.answer(
                        text=f"You have completed all tests 🎉\n\nYour score is: {int(data['correct_answers'] / data['words_count'] * 100)}",
                        reply_markup=await main_menu_buttons(call.from_user.id)
                    )
                await state.finish()
            else:
                if tg_user['language'] == 'uz':
                    await call.message.answer(text="Natijangizni bilish uchun bizni kanalga obuna bo'ling 😊",
                                              reply_markup=await channel_button())
                elif tg_user['language'] == 'ru':
                    await call.message.answer(text="Подпишитесь на наш канал, чтобы узнать свой результат 😊",
                                              reply_markup=await channel_button())
                else:
                    await call.message.answer(text="Subscribe to our channel to know your result 😊",
                                              reply_markup=await channel_button())
        else:
            word, category = await get_test(category_id=data['category_id'], words=data['words'])
            data['word_number'] = data['word_number'] + 1
            data['words'].append(word['word']['id'])
            data['correct_answer'] = word['word']['name']
            await call.message.answer_photo(photo=open(word['word']['image'][22:], 'rb'),
                                            caption=f"Test {data['word_number']}\n\nFind the name of this {str.lower(category['name'])} 👆",
                                            reply_markup=await test_button(words=word))
        await call.message.delete()
