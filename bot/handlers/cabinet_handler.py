import json

import requests
from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.text import cabinet, cabinet_ru
from bot.dispatcher import dp


@dp.message_handler(Text(equals=[cabinet, cabinet_ru]))
async def get_science_function(msg: types.Message):
    user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    if msg.text == cabinet:
        await msg.answer(text=f"""
🧾 Ism-Familiangiz: {user['full_name']}
📱 Telefon-Raqamingiz: {user['phone_number']}""")
    else:
        await msg.answer(text=f"""
🧾 Ваше имя и фамилия: {user['full_name']}
📱 Ваш номер телефона: {user['phone_number']}""")
