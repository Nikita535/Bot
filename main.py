"""
main.py
====================================
The core module of my example project
"""
from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from DataBase import sqlite_db
from ParserMenu import parser

async def on_startup(_):
    """
    Function for bot startup
    """
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()
    parser.main()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)




executor.start_polling(dp, skip_updates=True,on_startup=on_startup)