
import sqlite3
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
import random, time, asyncio
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.enums import ChatMemberStatus

fm_t = False

bot = Bot(token=TOKEN)
dp = Dispatcher()
admin = 5626265763

import sqlite3


connection = sqlite3.connect("Mana.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    name VARCHAR(30),
    wins INTEGER,
    cash INTEGER,
    phone INTEGER,
    car INTEGER,
    house INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS farm(
    user_id INTEGER,
    size INTEGER,
    lvl INTEGER
    )
""")

connection.commit()


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# buttons

button_start = [
    [KeyboardButton(text='/play'), KeyboardButton(text='/info')],
    [KeyboardButton(text='/help'), KeyboardButton(text='register')],
    [KeyboardButton(text='Профиль'), KeyboardButton(text='users')],
    [KeyboardButton(text='/help_admin'), KeyboardButton(text="Копать")],
    [KeyboardButton(text='/shop')]
]

button_play = [
    [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3')]
]

button_info = [
    [KeyboardButton(text='geeks')]
]

keyboard_play = ReplyKeyboardMarkup(keyboard=button_play, resize_keyboard=True, one_time_keyboard=True)
keyboard_start = ReplyKeyboardMarkup(keyboard=button_start,resize_keyboard=True)
keyboard_info = ReplyKeyboardMarkup(keyboard=button_info,resize_keyboard=True, one_time_keyboard=True)

army = [
    [InlineKeyboardButton(text='Увеличить кол. Людей', callback_data='add')],
    [InlineKeyboardButton(text='start', callback_data='st')],
    [InlineKeyboardButton(text='stop', callback_data='sp')]
]

arm_kb = InlineKeyboardMarkup(inline_keyboard=army)

shop = [
    [KeyboardButton(text='Телефоны')],
    [KeyboardButton(text='Машины')],
    [KeyboardButton(text='Дома')]
    # [KeyboardButton(text='Дома еще в разработке')]
]
shop_kb = ReplyKeyboardMarkup(keyboard=shop, resize_keyboard=True, one_time_keyboard=True)

car = [
    [KeyboardButton(text='Mercedes')],
    [KeyboardButton(text='BMW')]
]
car_kb = ReplyKeyboardMarkup(keyboard=car, resize_keyboard=True, one_time_keyboard=True)

ar = [
    [InlineKeyboardButton(text='Ad. Soldiers', callback_data='sol')],
    [InlineKeyboardButton(text='Ad. Cars', callback_data='car')],
    [InlineKeyboardButton(text='Ad. Tanks', callback_data='tan')]
]
armmy_kb = InlineKeyboardMarkup(inline_keyboard=ar)

admin = [
    [KeyboardButton(text='stop'), KeyboardButton(text='/передача')],
    [KeyboardButton(text="ban_admin"), KeyboardButton(text="ban_admin")],
    [KeyboardButton(text="delete"), KeyboardButton(text="/mailing")]
]
admin_kb = ReplyKeyboardMarkup(keyboard=admin, resize_keyboard=True, one_time_keyboard=True)

@dp.message(Command("start"))
async def start_bot(message: Message):
    await message.reply(f"Привет {message.from_user.first_name}!\nЭто бот мируни🧑‍💻\nТут все команды этого бота📁\nИграть🤠 - /play\nПерезапуск бота💊 - /start\nПомощь😭 - /help\nИнформация🤔 - /info,\nРегистрация😀 - registr,\nПользователи👨 - users,\nКоманды для админов - /help_admin", reply_markup=keyboard_start)
    await message.delete()

@dp.message(F.text == "register")
async def start_bot(message: Message):
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
    users = cursor.fetchall()
    if users == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",(message.from_user.id, message.from_user.first_name, 0, 500, None, None, None))
        connection.commit()
        await message.reply("Регистрация прошла успешно прошла успешно!👌")
        await message.reply(f"Вы были зарегистрированы под именем {message.from_user.first_name}")
    else:
        await message.reply("Аккаунт существует😉")
    await message.reply("Успешно выполнено!😄")

@dp.message(F.text == "профиль")
async def info_profile(message : Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    u = cursor.fetchone()
    cursor.execute(f"SELECT wins FROM users WHERE user_id = {message.from_user.id}")
    w = cursor.fetchone()
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {message.from_user.id}")
    m = cursor.fetchone()
    connection.commit()
    wins = w[0]
    money = m[0]
    if u is None:
        user_id = None
    else:
        user_id = u[0]
    await message.reply(f"Имя - {message.from_user.first_name},\nid - {message.from_user.id},\nКоличество побед - {wins},\nДеньги💵 - {money},\nНаличие админки🤗 - {user_id}") 

@dp.message(F.text == "users")
async def users(message: Message):
    cursor.execute(f"SELECT name, user_id, cash FROM users")
    useri = cursor.fetchall()
    connection.commit()
    if useri:
        response = "список всех пользователей:\n"
        for user_id, name, cash in useri:
            users = useri
            response += f"id - {user_id}, name - {name}, cash-{cash}\n"
    await message.reply(f"{response}")

@dp.message(F.text.in_({"Ферма", "athvf", "ферма"}))
async def farm(message: Message):
    cursor.execute(f"SELECT user_id FROM farm WHERE user_id = {message.from_user.id}")
    us = cursor.fetchall()
    connection.commit()
    if us == []:
        await message.reply("Ферма создана⚔️")
        await create_farm(message.from_user.id)
    else:
        cursor.execute(f"SELECT size FROM farm WHERE user_id = {message.from_user.id}")
        s = cursor.fetchone()
        cursor.execute(F"SELECT lvl FROM farm WHERE user_id = {message.from_user.id}")
        l = cursor.fetchone()
        connection.commit()
        size = s[0]
        lvl = l[0]
        await message.reply(f"--Ферма--\nЛюди - {size}\nlvl - {lvl}", reply_markup=arm_kb)

@dp.callback_query(F.data == 'add')
async def add(callback: CallbackQuery):
    await callback.answer("Выполнение")
    acc = await accept(callback.from_user.id)
    if acc == True:
        await callback.message.answer("50 Людей добавлено в ферму✅")
        await add_people_farm(callback.from_user.id)
    else:
        await callback.message.answer("Не достаточно денег📉")

async def add_people_farm(idi):
        cursor.execute("UPDATE farm SET size = size + ? WHERE user_id = ?", (50, idi))
        cursor.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", (500, idi))
        connection.commit()

async def accept(idi):
    cursor.execute(F"SELECT cash FROM users WHERE user_id = {idi}")
    cash = cursor.fetchone()
    result = cash[0]
    connection.commit()
    if result > 500:
        acc = True
    else:
        acc = False
    return acc

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

async def update_balance(idi, money, people):

    cursor.execute(f"UPDATE users SET cash = cash + ? WHERE user_id = ?", (money+people, idi))
    connection.commit() 

@dp.callback_query(F.data == 'sp')
async def sp_farm(callback: CallbackQuery):
    global fm_t
    if fm_t:
        fm_t = False
        await callback.answer()
        await callback.message.answer("Ферма остановлена")
    else:
        await callback.answer()

async def create_farm(idi):
        cursor.execute("INSERT INTO farm(user_id, size, lvl) VALUES(?, ?, ?)", (idi, 100, 1))
        connection.commit()
        await bot.send_message(idi, "--Армия--\nЛюдей - 100\nlvl - 1", reply_markup=arm_kb)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("Exit")