from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Поделиться расположением', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).row(b2, b3).row(b4, b5)
