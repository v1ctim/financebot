import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from handlers.user_commands import user_private_router

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from aiogram import Bot, Dispatcher

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(user_private_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
