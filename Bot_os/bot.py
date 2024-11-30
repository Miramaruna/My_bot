
# sqlite3

import sqlite3

# aiogram

import asyncio, logging, random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from aiogram import types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram.types import ContentType
from aiogram.exceptions import TelegramBadRequest

# config

from config import TOKEN
from app.handlers import *
from app.keyboard import *
from app.BD import *

fm_t = False

bot = Bot(token=TOKEN)
dp = Dispatcher()
admin = 5626265763
admin2 = 45
Dispatcher(storage=MemoryStorage())

logging.basicConfig(
level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"), 
        logging.StreamHandler()          
    ]
)

class BroadcastForm(StatesGroup):
    waiting_for_message = State()

def get_all_users():
    conn = sqlite3.connect('Mana.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    conn.close()
    return [user[0] for user in users]

async def broadcast_message(message_text):
    users = get_all_users()
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message_text)
        except TelegramBadRequest as e:
            print(f"Ошибка отправки пользователю {user_id}: {e}")

@dp.message(Command("mailing"))
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id == admin or admin2:
        await message.answer("Введите сообщение для рассылки:")
        await state.set_state(BroadcastForm.waiting_for_message)
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.message(BroadcastForm.waiting_for_message, F.content_type == ContentType.TEXT)
async def get_broadcast_message(message: Message, state: FSMContext):
    broadcast_text = message.text

    await broadcast_message(broadcast_text)
    
    await message.answer("Рассылка завершена.")
    await state.clear()


class Register(StatesGroup):
    password = State()

@dp.message(Command("add_admin"))
async def add_task(message: Message, state: FSMContext):
    await message.answer("Введите код проверки🔑:")
    await state.set_state(Register.password)
    await message.delete()

@dp.message(Register.password, F.content_type == ContentType.TEXT)
async def save_admin(message: Message, state: FSMContext):
    password = message.text
    await accept_admin(password, message.from_user.id, message.from_user.first_name)
    await state.clear()

async def accept_admin(message, idi, first_name):
    if message == 'gavno':
        cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {idi}")
        pop = cursor.fetchall()
        connection.commit()
        if pop == []:
            cursor.execute(
             "INSERT INTO admin (user_id, name) VALUES (?, ?)",
            (idi, first_name)
            )
            connection.commit()
            await bot.send_message(idi, "Авторизация прошла успешно!👌")
        else:
            await bot.send_message(idi, "Аккаунт существует😉")
    else:
        await bot.send_message(idi, "Код не правильный!🧨")
    await bot.send_message(idi, "Исполнено!🫡")
    connection.commit()

async def create_farm(idi):
        cursor.execute("INSERT INTO farm(user_id, size, lvl) VALUES(?, ?, ?)", (idi, 100, 1))
        connection.commit()
        await bot.send_message(idi, "--Ферма--\nЛюдей - 100\nlvl - 1", reply_markup=arm_kb)

async def afk_farm():
    while True:
        cursor.execute(f"SELECT user_id FROM users")
        users = cursor.fetchall()
        for user in users:
            user_id = user[0]
            await balance(user_id, 10)
            print(f'Начислено 10 монет пользователю с ID {user_id}')
            await bot.send_message(user_id, "Вознагрождение по 10 мин каждые")

        await asyncio.sleep(600)

async def balance(idi, money):
    cursor.execute(F"UPDATE users SET cash = cash + ? WHERE user_id = ?", (money, idi))
    connection.commit()

@dp.callback_query(F.data == 'st')
async def start_darm(callback: CallbackQuery):
    global fm_t
    if not fm_t:
        fm_t = True
        asyncio.create_task(start_farm(callback.from_user.id))
        await callback.answer("в процесее")

async def start_farm(idi):
    global fm_t
    cursor.execute(F"SELECT size FROM farm WHERE user_id = {idi}")
    size = cursor.fetchone()
    result = size[0]
    connection.commit()
    while fm_t:
        await update_balance(idi, 10, result)
        await bot.send_message(idi, f"Вам начислено {50 + result} монет с фермы")
        print(f'Начислено {50 + result} монет пользователю с ID {idi}')
        await asyncio.sleep(60)

@dp.callback_query(F.data == 'sp')
async def sp_farm(callback: CallbackQuery):
    global fm_t
    if fm_t:
        fm_t = False
        await callback.answer()
        await callback.message.answer("Ферма остановлена")
    else:
        await callback.answer()

async def update_balance(idi, money, people):

    cursor.execute(f"UPDATE users SET cash = cash + ? WHERE user_id = ?", (money+people, idi))
    connection.commit() 

@dp.message(F.text == 'stop')
async def stop(message: Message, state: FSMContext):
    if message.from_user.id == admin:
        await message.answer("Бот остановлен!🔑")
        await dp.stop_polling()
    else:
        message.answer("Такой команды нет!")

# start

async def on_startup():
    await bot.set_my_commands([
        BotCommand(command="/start", description='Запустить бота'),
        BotCommand(command="/help", description='Помощь'),
        BotCommand(command="/info", description='Информация'),
        BotCommand(command="register", description='регистрация')
    ])

async def main():
    await on_startup()
    asyncio.create_task(afk_farm())
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except BaseException as e:
        print("Exit")