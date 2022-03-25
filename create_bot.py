from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import BotConfig

bot = Bot(BotConfig.TOKEN)
dp = Dispatcher(bot)