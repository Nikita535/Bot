from aiogram import types
from create_bot import dp, Dispatcher
import json, string

# @dp.message_handler()
async def echo_send(message: types.Message):
    if {
        i.lower().translate(str.maketrans('', '', string.punctuation))
        for i in message.text.split(' ')
    }.intersection(set(json.load(open('Swear.json')))) != set():
        await message.answer('Маты запрещены')
        await message.delete()


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)

