from aiogram import Bot, Dispatcher

from app.core.settings import settings

bot = Bot(settings.token)
dp = Dispatcher()
