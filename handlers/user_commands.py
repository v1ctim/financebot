from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3

DATABASE_PATH = 'finance_bot.db'

# Initialize the router
user_private_router = Router()

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Functions for database interactions
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


#FSM
class UserRegister(StatesGroup):
    user_id = State()
    first_name = State()
    plan_budget = State()
    currency = State()

@user_private_router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.reply("Welcome to the Finance Bot! Let's registrate you. Write down your name")



## надо написать регистрацию пользователя
@user_private_router.message(F.text)
async def name_registration(message: types.Message):
    user_id = message.from_user.id
    name = message.text
    conn = get_db_connection()
    c = conn.cursor()


#Это надо переписать самому
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
