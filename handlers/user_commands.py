from aiogram import types, Router, F, html
from aiogram.filters import Command, CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import User, Message
import sqlite3

DATABASE_PATH = 'finance_bot.db'


user_private_router = Router()


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_transaction(user_id, amount, description, category, transaction_type):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO UserTransaction (user_id, amount, description, category, transaction_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, amount, description, category, transaction_type, datetime.now()))
    conn.commit()
    conn.close()

def get_user_transactions(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM UserTransaction WHERE user_id = ?', (user_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions


class UserRegister(StatesGroup):
    user_id = State()
    first_name = State()
    plan_budget = State()
    currency = State()

@user_private_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await state.set_state(UserRegister.first_name)
    await message.reply("Welcome to the Finance Bot! Let's register you. Please enter your name:")


@user_private_router.message(UserRegister.first_name)
async def registration_1(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text, user_id=message.from_user.id)
    await state.set_state(UserRegister.plan_budget)
    await message.answer(f"Nice to meet you, {html.quote(message.text)}!\nHow much money would you like to spend monthly?")


@user_private_router.message(UserRegister.plan_budget)
async def registration_2(message: Message, state: FSMContext) -> None:
    try:
        plan_budget = int(message.text)
        await state.update_data(plan_budget=plan_budget)
    except ValueError:
        await message.reply("Please enter a valid number for the budget.")
        return
    
    await state.set_state(UserRegister.currency)
    
    popular_currencies = [
        "$ - US Dollar",
        "€ - Euro",
        "£ - British Pound",
        "¥ - Japanese Yen",
        "₽ - Russian Ruble",
        "₹ - Indian Rupee",
        "₣ - Swiss Franc",
        "₩ - South Korean Won",
        "₱ - Philippine Peso",
        "₪ - Israeli New Shekel"
    ]
    currency_list = "\n".join(popular_currencies)
    
    await message.reply(
        f"Type your currency. It could be a one-letter symbol. Here is the list of popular currencies:\n{currency_list}"
    )
## end fsm and send data to db

@user_private_router.message(UserRegister.currency)
async def registration_3(message: Message, state: FSMContext) -> None:
    await state.update_data(currency=message.text)
    current_state = await state.get_data()
    await state.clear()
    await message.reply("Registration complete! Your information has been saved.")
    await message.answer(f"{current_state}")


@user_private_router.message(Command('add_transaction'))
async def add_transaction_command(message: types.Message):
    try:
        args = message.text.split()[1:]
        if len(args) < 4:
            await message.reply("Usage: /add_transaction <amount> <description> <category> <type>")
            return
        
        user_id = message.from_user.id
        amount = float(args[0])
        description = args[1]
        category = args[2]
        transaction_type = args[3]
        
        add_transaction(user_id, amount, description, category, transaction_type)
        await message.reply("Transaction added successfully!")
    
    except ValueError:
        await message.reply("Invalid input. Make sure the amount is a number.")

@user_private_router.message(Command('transactions'))
async def get_transactions_command(message: types.Message):
    user_id = message.from_user.id
    transactions = get_user_transactions(user_id)
    
    if not transactions:
        await message.reply("You have no transactions yet.")
    else:
        response = "\n".join([f"{dict(t)}" for t in transactions])
        await message.reply(response)
