from aiogram import Bot, Dispatcher
from bot_filters import IsConfigChat, CallbackCmd
from dispatcher import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(config.tg_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.bind_filter(IsConfigChat)
dp.bind_filter(CallbackCmd)
