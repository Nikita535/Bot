"""
other.py
====================================
The module for extra functions in bot.
"""
from aiogram import types
from create_bot import dp, Dispatcher
import json, string

# @dp.message_handler()
async def echo_send(message: types.Message):
    """
    Swear words control
        :param message:
    """
    if {
        i.lower().translate(str.maketrans('', '', string.punctuation))
        for i in message.text.split(' ')
    }.intersection(set(json.load(open('./SwearGen/Swear.json')))) != set():
        await message.answer('Маты запрещены')
        await message.delete()


def register_handlers_other(dp : Dispatcher):
    """
    Registers hadlers to dispatcher
        :param dp:
    """
    dp.register_message_handler(echo_send)

