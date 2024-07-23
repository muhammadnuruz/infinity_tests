import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu, choice_language, choice_language_ru, back_main_menu_ru, back_main_menu_en, \
    choice_language_en
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_en]), )
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    try:
        if tg_user['detail']:
            await state.set_state('language_1')
            await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык

-------------

Select a language""", reply_markup=await language_buttons())
    except KeyError:
        if tg_user.get('language') == 'uz':
            await msg.answer(text=f"Bot yangilandi ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        elif tg_user['language'] == 'en':
            await msg.answer(text="The bot has been updated ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def language_function(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['language'] = call.data.split("_")[-1]
    await call.message.delete()
    await state.set_state('register_1')
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text=f"Ism-Familiyangizni kiriting ✍️:")
    elif call.data.split("_")[-1] == 'en':
        await call.message.answer(text="Enter your name and surname ✍️:")
    else:
        await call.message.answer(text=f"Введите свое имя и фамилию ✍️:")


@dp.message_handler(state='register_1')
async def register_function(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = msg.text
    k = KeyboardButton(text="MY NUMBER📲", request_contact=True)
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_client.add(k)
    await state.set_state("register_2")
    if data['language'] == 'uz':
        await msg.answer(text="«MY NUMBER📲» - tugmasini bosish orqali telefon raqamingizni yuboring 👇",
                         reply_markup=kb_client)
    elif data['language'] == 'en':
        await msg.answer(text="Send your phone number by clicking the «MY NUMBER📲» button 👇", reply_markup=kb_client)
    else:
        await msg.answer(text="Укажите свой номер телефона, нажав кнопку «MY NUMBER📲» 👇", reply_markup=kb_client)


@dp.message_handler(state='register_2', content_types=types.ContentTypes.CONTACT)
async def register_function_4(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        for admin in admins:
            await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {data['full_name']}
Telefon raqam: {msg.contact.phone_number}""", parse_mode='HTML')
        data = {
            "chat_id": str(msg.from_user.id),
            "username": msg.from_user.username,
            "full_name": data['full_name'],
            "phone_number": msg.contact.phone_number,
            'language': data['language']
        }
        requests.post(url=f"http://127.0.0.1:8000/api/telegram-users/create/", data=data)
    if data['language'] == 'uz':
        await msg.answer(text="Ro'yhatdan o'tdingiz ✅", reply_markup=await main_menu_buttons(msg.from_user.id))
    elif data['language'] == 'en':
        await msg.answer(text="You have registered ✅", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text="Вы зарегистрированы ✅", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru, choice_language_en]))
async def change_language_function_1(msg: types.Message):
    if msg.text == choice_language:
        await msg.answer(text="Tilni tanlang", reply_markup=await language_buttons())
    elif msg.text == choice_language_en:
        await msg.answer(text="Select a language", reply_markup=await language_buttons())
    else:
        await msg.answer(text="Выберите язык", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'))
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    s = requests.put(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == 'en':
        await call.message.answer(text="The language has been changed 🇺🇿",
                                  reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))
