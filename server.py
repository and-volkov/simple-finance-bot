import os
import re
import logging
from time import sleep
from typing import AnyStr

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db_queries import StatsQueries
from middelwares import AccessMiddleware

from income import add_income
from tables import GraphStatistic
from expenses import add_expense, parse_stats_query
from db_queries import DeleteQueries
from keyboards import (MainMenu, ExpensesCategories,
                       IncomeCategories, expenses_keyboards_dict,
                       TextStats, TextGraph, GraphStats, DeleteChoices)

BOT_API_TOKEN: AnyStr = os.getenv('BOT_API_TOKEN')
ACCESS_ID: AnyStr = os.getenv('MY_TELEGRAM_ID')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


MAIN_MENU = MainMenu().create_keyboard()


class IncomeForm(StatesGroup):
    categorie = State()
    amount = State()


class ExpenseForm(StatesGroup):
    categorie = State()
    subcategorie = State()
    amount = State()


class DeleteForm(StatesGroup):
    table_name = State()
    operation = State()


@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    """Open Main Menu"""
    await message.reply('Choose option', reply_markup=MAIN_MENU)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """Show Help message"""
    await message.reply(
        'Bot for finance monitoring\n\n'
        'You can add expenses by categories\n'
        'Add income, delete expense/income\n'
        'Look at your stats for day, week, month, all time',
        reply_markup=MAIN_MENU
    )


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=MAIN_MENU)


#  Set state for Income Command
@dp.message_handler(commands='Income')
async def income(message: types.Message):
    """Showing income categories menu"""
    await IncomeForm.categorie.set()
    await message.reply(
        'Choose subcategory',
        reply_markup=IncomeCategories().create_keyboard()
    )


#  Getting income categorie
@dp.message_handler(state=IncomeForm.categorie)
async def process_income_categorie(message: types.Message, state: FSMContext):
    """Process income categorie"""
    async with state.proxy() as data:
        data['categorie'] = message.text.split('/')[1]

    await IncomeForm.next()
    await message.reply('Enter income amount')


#  Check amount not digit
@dp.message_handler(
    lambda message: not message.text.isdigit(),
    state=IncomeForm.amount
)
async def invalid_income_amount(message: types.Message):
    await message.reply('Amount gotta be a number\nEnter Income amount')


#  Check amount is digit
@dp.message_handler(
    lambda message: message.text.isdigit(),
    state=IncomeForm.amount
)
async def process_income_amount(message: types.Message, state: FSMContext):
    """Getting amount of income if message is correct (digit)"""
    async with state.proxy() as data:
        data['amount'] = int(message.text)

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Category: ', md.bold(data['categorie'])),
                md.text('Amount: ', md.bold(data['amount'])),
                sep='\n'
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    add_income(
        amount=data['amount'],
        categorie=data['categorie']
    )

    await state.finish()
    await message.reply(
        'Add more, or write "cancel"',
        reply_markup=MAIN_MENU
    )


#  Set state for Expense Command
@dp.message_handler(commands='Expense')
async def income(message: types.Message):
    """Showing expenses categories menu"""
    await ExpenseForm.categorie.set()
    await message.reply(
        'Category subcategory',
        reply_markup=ExpensesCategories().create_keyboard()
    )


@dp.message_handler(state=ExpenseForm.categorie)
async def process_expense_categorie(message: types.Message, state: FSMContext):
    """Process expenses categorie"""
    categorie = message.text.split('/')[1]
    async with state.proxy() as data:
        data['categorie'] = categorie

    await ExpenseForm.next()
    await message.reply(
        'Choose subcategory',
        reply_markup=expenses_keyboards_dict[categorie]
    )


@dp.message_handler(state=ExpenseForm.subcategorie)
async def process_expense_subcategorie(
        message: types.Message, state: FSMContext
):
    subcategorie = message.text.split('/')[1]
    async with state.proxy() as data:
        data['subcategorie'] = subcategorie

    await ExpenseForm.next()
    await message.reply('Enter amount of expense')


#  Check amount not digit
@dp.message_handler(
    lambda message: not message.text.isdigit(),
    state=ExpenseForm.amount
)
async def invalid_expense_amount(message: types.Message):
    await message.reply('Amount gotta be a number\nEnter Expense amount')


#  Check amount is digit
@dp.message_handler(
    lambda message: message.text.isdigit(),
    state=ExpenseForm.amount
)
async def process_expense_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = int(message.text)

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Category: ', md.bold(data['categorie'])),
                md.text('Subcategorie', md.bold(data['subcategorie'])),
                md.text('Amount: ', md.bold(data['amount'])),
                sep='\n'
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    add_expense(
        category=data['categorie'],
        subcategory=data['subcategorie'],
        amount=data['amount']
    )

    await state.finish()
    await message.reply(
        'Add more, or write "cancel"',
        reply_markup=MAIN_MENU
    )


@dp.message_handler(commands='Stats')
async def stats_menu(message: types.Message):
    """Open stats menu"""
    keyboard = TextGraph().create_keyboard()
    await message.reply('Choose stat type', reply_markup=keyboard)


@dp.message_handler(commands=['TextStats'])
async def text_stats(message: types.Message):
    """Choose text stats option"""
    keyboard = TextStats().create_keyboard()
    await message.reply('Choose stat option', reply_markup=keyboard)


@dp.message_handler(
    commands=['TextToday', 'TextWeek', 'TextMonth', 'TextAllTime']
)
async def show_text_stats(message: types.Message):
    """Showing stat"""
    command = message.text.split('/')[1]
    stats_dict = StatsQueries().get_stats_dict()
    try:
        query_result = stats_dict[command]
        amount, subcategorie, categorie = parse_stats_query(
            query_result
        )
        for i in range(len(amount)):
            await bot.send_message(
                message.chat.id,
                md.text(
                    f'{amount[i]} | {subcategorie[i]} | {categorie[i]}'
                )
            )
    except ValueError:
        await message.answer('No spending`s today')
    await message.reply(text='Continue', reply_markup=MAIN_MENU)


@dp.message_handler(commands=['GraphStats'])
async def graph_stats(message: types.Message):
    """Choose graph stats option"""
    keyboard = GraphStats().create_keyboard()
    await message.reply('Choose stat option', reply_markup=keyboard)


@dp.message_handler(
    commands=['GraphToday', 'GraphWeek', 'GraphMonth', 'GraphAllTime']
)
async def send_graph_stat(message: types.Message):
    """Create and send plot of chosen type"""
    stat_type = message.text.split('/')[1]
    GraphStatistic().create_plot(query_name=stat_type)
    # need some time to create plot
    await message.answer('Calculating...Wait please')
    sleep(5)
    with open('graphs/output.png', 'rb') as f:
        graph = f.read()
    await message.reply('Continue', reply_markup=MAIN_MENU)
    await bot.send_photo(chat_id=message.chat.id, photo=graph)


@dp.message_handler(commands=['DeleteExpenses', 'DeleteIncome'])
async def set_delete_state(message: types.Message, state: FSMContext):
    text = message.text.split('/')[1]
    table_name = re.findall('[A-Z][^A-Z]*', text)[1].lower()
    await DeleteForm.table_name.set()
    async with state.proxy() as data:
        data['table_name'] = table_name
    await DeleteForm.next()
    keyboard = DeleteChoices().create_keyboard()
    await message.reply('Choose', reply_markup=keyboard)


@dp.message_handler(state=DeleteForm.operation)
async def process_delete_operation(message: types.Message, state: FSMContext):
    operation = message.text.split('/')[1]
    async with state.proxy() as data:
        data['operation'] = operation
        delete_func_dict = DeleteQueries(
            data['table_name']
        ).delete_choices_dict()
        result = delete_func_dict[data['operation']]()

    await state.finish()
    await message.reply(result, reply_markup=MAIN_MENU)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
