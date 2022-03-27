from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/working_hours')
b2 = KeyboardButton('/geolocation')
b3 = KeyboardButton('/menu')
b4 = KeyboardButton('/moderator_mode')
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Поделиться расположением', request_location=True)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).row(b2, b3).row(b4)
