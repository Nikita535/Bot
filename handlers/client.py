"""
client.py
====================================
The module for client panel in bot.
"""
import os
from aiogram import types, Dispatcher
from create_bot import dp, bot
from KeyBoards import kb_client
from aiogram.types import ReplyKeyboardRemove
from DataBase import sqlite_db
import json


async def commands_help(message: types.Message):
    """
    Shows help commands
        :param message:
    """
    message_text1 = 'Вот, что умеет этот бот:\n' \
                    + '/start - начало работы бота\n' \
                    + '/moderators - список модераторов бота\n' \
                    + '/moderator_mode - войти в режим модерации бота'
    message_text2 = 'Небольшая инструкция:\n' \
                    + 'После команды /start наш бот напишет вам в личные сообщения, но предварительно ему нужно написать любое сообщение!!!\n\n' \
                    + 'В диалоге с ботом появится клавиатура, со следующими командами: working_hours, geolocation, menu.\n\n' \
                    + 'Удачи!'
    await bot.send_message(message.chat.id, message_text1)
    await bot.send_message(message.chat.id, message_text2)


# @dp.message_handler(commands=['start','help'])
async def commands_start(message: types.Message):
    """
    Starts bot work and add keyboard
        :param message:
    """
    try:
        await bot.send_message(message.from_user.id, 'Открывайте клавиатуру и командуйте\U0001F972',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\n@TRPP_123_bot')


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    """
    Shows working hours
        :param message:
    """

    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 До 23:00')


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    """
    Shows geolocation
        :param message:
    """
    await bot.send_message(message.from_user.id, 'пр. Вернадского 78')


async def share_phone_number(message: types.Message):
    """
    Get phone number
        :param message:
    """
    await bot.send_message(message.from_user.id,
                           'Мы запомнили ваш мобильный телефон, если что-то произойдёт с вашим заказом, мы обязательно вам перезвоним!')


# @dp.register_message_handler(commands=['Меню'])
async def pizza_menu_command(message: types.Message):
    """
    Shows menu
        :param message:
    """
    await sqlite_db.sql_read(message)


async def show_moderator(message: types.Message):
    """
    Shows moderator accounts
        :param message:
    """
    cur = await sqlite_db.sql_show_admins()
    message_text = "Аккаунты модераторов:\n"
    for ret in cur:
        message_text += f'@{ret[0]}\n'
    await message.answer(message_text)


# async def show_menu(message: types.Message):
#     with open('./ParserMenu/cake_dict.json', encoding="windows-1251") as file:
#         cake_dict = json.load(file)
#
#         menu = ''
#         for k, v in cake_dict.items():
#             menu += f"{v['name']}\n{v['desc']}\n{v['price']}\n\n"
#         await bot.send_message(message.from_user.id, menu)


async def show_menu(message: types.Message):
    """
    Loads menu from json
        :param message:
    """
    with open('./ParserMenu/menu_dict.json', encoding="utf-8") as file:
        menu_dict = json.load(file)

        for k, v in menu_dict.items():
            photo = v['photo_name']
            photopath = open("./ParserMenu/pics/" + photo, 'rb')
            menu = f"{v['name']}\n{v['price']}\n\n"
            await bot.send_photo(message.from_user.id, photopath, menu)


def register_handlers_client(dp: Dispatcher):
    """
    Register all handlers to dispatcher
        :param dp:
    """
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_help, commands=['help'])
    dp.register_message_handler(pizza_open_command, commands=['working_hours'])
    dp.register_message_handler(pizza_place_command, commands=['geolocation'])
    dp.register_message_handler(pizza_menu_command, commands=['menu'])
    dp.register_message_handler(share_phone_number, commands=['Поделиться_номером'])
    dp.register_message_handler(show_moderator, commands=['moderators'])
    dp.register_message_handler(show_menu, commands=['show_menu'])
