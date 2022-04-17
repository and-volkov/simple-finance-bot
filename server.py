import os
import logging
from typing import AnyStr

from aiogram import Bot, Dispatcher, executor, types

from middelwares import AccessMiddleware
from keyboards import MainMenu


BOT_API_TOKEN: AnyStr = os.getenv('BOT_API_TOKEN')
ACCESS_ID: AnyStr = os.getenv('MY_TELEGRAM_ID')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    x = MainMenu()
    await message.reply('Ok', reply_markup=x.keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

