from aiogram import types, Dispatcher
from create_bot import dp, bot
from KeyBoards import kb_client
from aiogram.types import ReplyKeyboardRemove

# @dp.message_handler(commands=['start','help'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита',reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\n@TRPP_123_bot')

# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 До 23:00')


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'пр. Вернадского 78')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command,commands=['Расположение'])
