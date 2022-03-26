from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import BotConfig
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(BotConfig.TOKEN)
dp = Dispatcher(bot, storage=storage)