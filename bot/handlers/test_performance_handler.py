from aiogram import types

from bot.buttons.reply_buttons import tests_button
from bot.buttons.text import performance, performance_ru, performance_en
from bot.dispatcher import dp
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals=[performance, performance_ru, performance_en]))
async def test_performance_function(msg: types.Message):
    if performance == msg.text:
        await msg.answer(text="", reply_markup=await tests_button())
    elif performance_en == msg.text:
        await msg.answer(text="In which field do you test?", reply_markup=await tests_button())
    else:
        await msg.answer(text="В какой области вы будете проходить тестирование?", reply_markup=await tests_button())
