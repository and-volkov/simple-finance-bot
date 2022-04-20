import os
import logging
from typing import AnyStr

from aiogram import Bot, Dispatcher, executor, types

import db_queries
from middelwares import AccessMiddleware

import income, transactions
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
async def espense_menu(message: types.Message):
    """Open Category menu"""
    keyboard = Categories().create_keyboard()
    await message.reply('Choose Category', reply_markup=keyboard)


@dp.message_handler(
    commands=[
        'Clothes', 'Groceries', 'Home',
        'Restaurants', 'Sport', 'Travel'
    ]
)
async def choose_category(message: types.Message):
    """Open Subcategory menu, after add new transaction"""
    sub_cat_dict = {
        '/Home': HomeSubcategories(),
        '/Groceries': GroceriesSubcategories(),
        '/Restaurants': RestaurantsSubcategories(),
        '/Sport': SportSubcategories(),
        '/Clothes': ClothesSubcategories(),
        '/Travel': TravelSubcategories()
    }
    category = message.get_command()
    keyboard = sub_cat_dict[category].create_keyboard()
    await message.reply('Choose Subcategory.', reply_markup=keyboard)


@dp.message_handler(commands=db_queries.select_all_subcategories())
async def choose_subcategory(sub_name: types.Message):
    """Create new db transaction"""
    subcategory_name = sub_name.get_command().split('/')[1]
    category_name = db_queries.get_categorie_by_subcategorie(
        subcategory_name
    )
    await sub_name.answer('Enter value, description')

    @dp.message_handler()
    async def add_new_expense(amount_description: types.Message):
        amount, description = transactions.parse_message(
            amount_description.text
        )
        transaction = transactions.add_transaction(
            category=category_name,
            subcategory=subcategory_name,
            amount=int(amount),
            description=description
        )
        await sub_name.answer(str(transaction))


@dp.message_handler(commands=['Income'])
async def choose_income_category(message: types.Message):
    """Open Income Category menu"""
    keyboard = IncomeCategories().create_keyboard()
    await message.reply('Choose Income Category', reply_markup=keyboard)


@dp.message_handler(commands=["Salary", "Bonus", "Freelance", "Other"])
async def income_categories(message: types.Message):
    income_categorie = message.get_command().split('/')[1]
    await message.answer('Enter income value')

    @dp.message_handler()
    async def add_new_income(income_value: types.Message):
        amount = int(income_value.text)
        transaction = income.add_income(
            amount=amount,
            income_categorie=income_categorie,
        )
        await income_value.answer(str(transaction))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
