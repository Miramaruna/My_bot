
# sqlite3

import sqlite3

# aiogram

import asyncio, logging, random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# config

from config import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()
admin_id = 5626265763

# Version = 2.1.5
# home Replit
# UptimeRobot

# @dp.message()
async def echo(message: Message):
    await message.answer("pon")

# start

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")