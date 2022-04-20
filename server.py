import os
import logging
from typing import AnyStr

from aiogram import Bot, Dispatcher, executor, types

from middelwares import AccessMiddleware
from keyboards import (MainMenu, Categories, HomeSubcategories,
                       GroceriesSubcategories, RestaurantsSubcategories,
                       SportSubcategories, ClothesSubcategories,
                       TravelSubcategories, IncomeCategories)

BOT_API_TOKEN: AnyStr = os.getenv('BOT_API_TOKEN')
ACCESS_ID: AnyStr = os.getenv('MY_TELEGRAM_ID')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """Show Help message"""
    keyboard = MainMenu().create_keyboard()
    await message.reply(
        'Bot for finance monitoring\n\n'
        'You can add expenses by categories\n'
        'Add income, delete expense/income\n'
        'Look at your stats for day, week, month, all time',
        reply_markup=keyboard
    )


@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    """Open Main Menu"""
    keyboard = MainMenu().create_keyboard()
    await message.reply('Choose option', reply_markup=keyboard)


@dp.message_handler(commands=['Expense'])
async def choose_category(message: types.Message):
    """Open Category menu"""
    keyboard = Categories().create_keyboard()
    await message.reply('Choose Category', reply_markup=keyboard)


@dp.message_handler(
    commands=[
        'Clothes', 'Groceries', 'Home',
        'Restaurants', 'Sport', 'Travel'
    ]
)
async def choose_subcategory(message: types.Message):
    """Open Subcategory menu"""
    sub_cat_dict = {
        '/Home': HomeSubcategories(),
        '/Groceries': GroceriesSubcategories(),
        '/Restaurants': RestaurantsSubcategories(),
        '/Sport': SportSubcategories(),
        '/Clothes': ClothesSubcategories(),
        '/Travel': TravelSubcategories()
    }
    keyboard = sub_cat_dict[message.get_command()].create_keyboard()
    await message.reply('Choose Subcategory', reply_markup=keyboard)


@dp.message_handler(commands=['income'])
async def income_categories(message: types.Message):
    keyboard = IncomeCategories().create_keyboard()
    await message.reply('Choose Category', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
