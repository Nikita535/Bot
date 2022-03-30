"""
admin.py
====================================
The module for admin panel in bot.
"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from DataBase import sqlite_db
from KeyBoards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time


# ID = None

class FSMAdmin(StatesGroup):
    """Class for state Machine"""

    name = State()
    photo = State()
    # description = State()
    price = State()


# Получим id текущего модератора
# @dp.register_message_handler(commands=['moderator'],is_chat_admin=True)
async def make_changes_command(message: types.Message):
    """
    Checks user for admin role
        :param message:
    """
    try:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if not member.is_chat_admin():
            raise Exception
        # global ID
        try:
            await sqlite_db.sql_add_admin(message)
        except Exception:
            await message.reply("Вы уже являетесь Модератором")

        await bot.send_message(message.from_user.id, "Что надо, Хозяин??",
                               reply_markup=admin_kb.button_case_admin)
    except Exception:
        await message.reply("Вы не являетесь Модератором")


# Начало диалога
# @dp.message_handler(commands='Загрузить',state=None)
async def cm_start(message: types.Message):
    """
    Starts uploading of item
        :param message:

    """
    admin = await sqlite_db.sql_show_admin_by_id(message)
    if message.from_user.id == admin[0]:
        await FSMAdmin.name.set()
        await bot.send_message(message.from_user.id, 'Введи название')


# Ловим первый ответ
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_name(message: types.Message, state: FSMContext):
    """
    Loads name to state machine
        :param message:
        :param state:

    """
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Теперь загрузи фото')


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_photo(message: types.Message, state: FSMContext):
    """
    Loads photo to state machine
        :param message:
        :param state:

    """
    async with state.proxy() as data:
        data['data'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Теперь укажи цену')


# #Ловим третий ответ
# # @dp.message_handler(state=FSMAdmin.description)
# async def load_description(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['description'] = message.text
#     await FSMAdmin.next()
#     await bot.send_message(message.from_user.id, 'Теперь укажи цену')


# Ловим четвертый ответ
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    """
    Loads price to state machine
        :param message:
        :param state:

    """
    async with state.proxy() as data:
        data['price'] = message.text + " руб."

    await sqlite_db.sql_add_command(state)
    await state.finish()


# @dp.message_handler(state="*", commands=["Отмена"])
# @dp.message_handler(Text(equals='отмена',ignore_case=True),state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Finish uploading item
        :param message:
        :param state:

    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, "OK")


# async def empty(message: types.Message):
#     if message.from_user.id == ID:
#         await message.answer("Нет такой команды")
#         await message.delete()


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    """
    Deletes the item with inline button
        :param callback_query:

    """
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


# @dp.message_handler(commands="Удалить")
async def delete_item(message: types.Message):
    """
    Prepares items to delete
        :param message:

    """
    read = await sqlite_db.sql_read2()
    t = 0
    for ret in read:
        t += 1
        if t == 10:
            time.sleep(4)
            t = 0
        if str(ret[1]).find('.') != -1:
            photopath = open("./ParserMenu/pics/" + ret[1], 'rb')
        else:
            photopath = ret[1]
        await bot.send_photo(message.from_user.id, photopath, f'{ret[0]}\nЦена {ret[-1]}')
        await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))
    # test = await sqlite_db.sql_test()
    # await bot.send_photo(message.from_user.id, test[1], f'{test[0]}\nЦена {test[-1]}')
    # await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
    #     InlineKeyboardButton(f'Удалить {test[0]}', callback_data=f'{test[1]}')))


def register_handlers_admin(dp: Dispatcher):
    """
        Register all handlers to dispatcher
            :param dp:
    """
    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=["Отмена"])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    # dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator_mode'])
    dp.register_callback_query_handler(del_callback_run)
    dp.register_message_handler(delete_item, commands='Удалить')

    # dp.register_message_handler(empty,is_chat_admin=True)
